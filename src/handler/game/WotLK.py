import random
import hashlib

import PyByteBuffer

from src.common.config import cfg
from src.handler.game import TBC


class GamePacketHandler(TBC.GamePacketHandler):
    ADDON_INFO = b'\x9e\x02\x00\x00x\x9cu\xd2\xc1j\xc30\x0c\xc6q\xef)v\xe9\x9b\xec\xb4\xb4P\xc2\xea\xcb\xe2\x9e\x8bb' \
                 b'\x7fKDl98N\xb7\xf6=\xfa\xbee\xb7\r\x94\xf3OH\xf0G\xaf\xc6\x98&\xf2\xfdN%\\\xde\xfd\xc8\xb8"A\xea' \
                 b'\xb95/\xe9{w2\xff\xbc@H\x97\xd5W\xce\xa2ZC\xa5GY\xc6<op\xad\x11_\x8c\x18,\x0b\'\x9a\xb5!\x96\xc02' \
                 b'\xa8\x0b\xf6\x14!\x81\x8aF9\xf5TOy\xd84\x87\x9f\xaa\xe0\x01\xfd:\xb8\x9c\xe3\xa2\xe0\xd1\xeeG\xd2' \
                 b'\x0b\x1dm\xb7\x96+n:\xc6\xdb<\xea\xb2r\x0c\r\xc9\xa4j+\xcb\x0c\xaf\x1fl+R\x97\xfd\x84\xba\x95\xc7' \
                 b'\x92/Y\x95O\xe2\xa0\x82\xfb-\xaa\xdfs\x9c`Ih\x80\xd6\xdb\xe5\t\xfa\x13\xb8B\x01\xdd\xc41n1\x0b' \
                 b'\xca_{{\x1c>\x9e\xe1\x93\xc8\x8d'

    def parse_auth_challenge(self, packet):
        in_buff = packet.to_byte_buff()
        buff = PyByteBuffer.ByteBuffer.allocate(400)
        bin_account = bytes(cfg.account, 'utf-8')

        in_buff.get(4)
        server_seed = in_buff.get(4, 'big')
        client_seed = int.from_bytes(random.randbytes(4), 'big')
        buff.put(0, 2, 'little')
        buff.put(cfg.build, 4, 'little')
        buff.put(0, 4, 'little')
        buff.put(bin_account)
        buff.put(0)
        buff.put(0, 4, 'big')
        buff.put(client_seed)
        buff.put(0, 4, 'little')
        buff.put(0, 4, 'little')
        buff.put(cfg.realm['id'], 4, 'little')
        buff.put(3, 8, 'little')

        md = hashlib.sha1(bin_account)
        md.update(bytearray(4))
        md.update(int.to_bytes(client_seed, 4, 'big'))
        md.update(int.to_bytes(server_seed, 4, 'big'))
        md.update(cfg.realm['session_key'])
        buff.put(md.digest())
        buff.put(GamePacketHandler.ADDON_INFO)
        buff.strip()
        buff.rewind()
        return buff.array()

    @staticmethod
    def get_bag_display_info(buff):
        return buff.get(4 * 9, 'little')

    def parse_name_query(self, packet):
        raise NotImplementedError

    def parse_chat_message(self, packet):
        raise NotImplementedError

    def handle_achievement_event(self, guid, achievement_id):
        raise NotImplementedError

    def unpack_guid(self, buff):
        raise NotImplementedError
