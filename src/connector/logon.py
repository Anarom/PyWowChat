import asyncio
import socket

import PyByteBuffer

from src.common.config import cfg
from src.common.packet import Packet
from src.connector.base import Connector


class LogonConnector(Connector):
    def __init__(self):
        super().__init__()
        self.srp_handler = None
        self.logon_finished = False

    async def run(self):
        host, port = cfg.parse_realm_list()
        await self.out_queue.put(self.get_initial_packet())
        cfg.logger.info(f'Connecting to logon server: {host}')
        cfg.logger.debug(f'Connecting to logon server: {host}:{port}')
        try:
            self.reader, self.writer = await asyncio.open_connection(host, port)
        except socket.gaierror:
            cfg.logger.error('Can\'t establish connection')
            return
        self.main_task = asyncio.gather(self.receiver_coroutine(), self.sender_coroutine(), self.handler_coroutine())
        try:
            await self.main_task
        except asyncio.exceptions.CancelledError:
            return

    def handle_result(self, result):
        match result:
            case 1:
                self.writer.close()
                self.main_task.cancel()

    def get_initial_packet(self):
        version = [bytes(x, 'utf-8') for x in cfg.version.split('.')]
        account = bytes(cfg.account, 'utf-8')
        buffer = PyByteBuffer.ByteBuffer.allocate(100)
        buffer.put(3 if cfg.expansion == 'Vanilla' else 8)
        buffer.put(30 + len(account), endianness='little', size=2)
        buffer.put(b'WoW\x00')
        buffer.put(version[0])
        buffer.put(version[1])
        buffer.put(version[2])
        buffer.put(cfg.build, endianness='little')
        buffer.put(self.str_to_int('x86'), endianness='little', size=4)
        buffer.put(self.str_to_int(cfg.platform), endianness='little', size=4)
        buffer.put(self.str_to_int(cfg.locale), endianness='little', size=4)
        buffer.put(b'\x00\x00\x00\x00\x7f\x00\x00\x01')  # 0 + 0 + 127 (size=4) + 0 + 0 + 1
        buffer.put(len(account))
        buffer.put(account)
        buffer.strip()
        buffer.rewind()
        return Packet(cfg.codes.realm_headers.AUTH_LOGON_CHALLENGE, buffer.array())

    @staticmethod
    def str_to_int(string):
        return int.from_bytes(bytes(string, 'utf-8'), 'big')