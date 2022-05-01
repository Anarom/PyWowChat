import asyncio

import PyByteBuffer

from src.common.config import cfg


class Connector:
    RECV_SIZE = cfg.buff_size

    def __init__(self):
        self.reader = None
        self.writer = None
        self.main_task = None
        self.decoder = None
        self.encoder = None
        self.handler = None
        self.in_queue = asyncio.Queue()
        self.out_queue = asyncio.Queue()

    async def run(self):
        raise NotImplementedError

    def handle_result(self, result):
        raise NotImplementedError

    async def sender_coroutine(self):
        while not self.writer.is_closing():
            try:
                packet = await self.out_queue.get()
                self.writer.write(self.encoder.encode(packet))
                await self.writer.drain()
            except asyncio.exceptions.CancelledError:
                break
            cfg.logger.debug(f'PACKET SENT: {packet}')

    async def receiver_coroutine(self):
        while not self.writer.is_closing():
            try:
                data = await self.reader.read(Connector.RECV_SIZE)
                if not data:
                    cfg.logger.error('Received empty packet')
                    raise ValueError
                if self.decoder.remaining_data:
                    data = self.decoder.remaining_data + data
                buff = PyByteBuffer.ByteBuffer.wrap(data)  # While loop accesses same buffer each time
                while True:
                    packet = self.decoder.decode(buff)
                    if packet:
                        cfg.logger.debug(f'PACKET RECV: {packet}')
                        await self.in_queue.put(packet)
                        if not self.decoder.incomplete_packet:
                            break
                    else:
                        break
            except asyncio.exceptions.CancelledError:
                break

    async def handler_coroutine(self):
        while not self.writer.is_closing():
            try:
                packet = await self.in_queue.get()
            except asyncio.exceptions.CancelledError:
                break
            result = self.handler.handle_packet(packet)
            self.handle_result(result)
