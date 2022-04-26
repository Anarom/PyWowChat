import hashlib
import re

import PyByteBuffer

from src.common.config import cfg
from src.common.packet import Packet
from src.common.SRP import SRPHandler


class RealmPacketHandler:
    def __init__(self, out_queue):
        self.out_queue = out_queue
        self.srp_handler = None

    def handle_packet(self, packet):
        if not isinstance(packet, Packet):
            cfg.logger.error(f'packet is instance of {type(packet)}')
            return
        match packet.id:
            case cfg.realm_packets.CMD_AUTH_LOGON_CHALLENGE:
                self.handle_CMD_AUTH_LOGON_CHALLENGE(packet)
            case cfg.realm_packets.CMD_AUTH_LOGON_PROOF:
                self.handle_CMD_AUTH_LOGON_PROOF(packet)
            case cfg.realm_packets.CMD_REALM_LIST:
                self.handle_CMD_REALM_LIST(packet)
            case _:
                cfg.logger.error(f'Received packet {packet.id:04X} in unexpected logonState')

    def handle_CMD_AUTH_LOGON_CHALLENGE(self, packet):
        byte_buff = PyByteBuffer.ByteBuffer.wrap(packet.data)
        byte_buff.get(1)  # error code
        result = byte_buff.get(1)
        if not cfg.realm_packets.AUTH.is_success(result):
            cfg.logger.error(cfg.realm_packets.get_message(result))
            raise ValueError

        B = int.from_bytes(byte_buff.array(32), 'little')
        g_length = byte_buff.get(1)
        g = int.from_bytes(byte_buff.array(g_length), 'little')
        n_length = byte_buff.get(1)
        N = int.from_bytes(byte_buff.array(n_length), 'little')
        salt = int.from_bytes(byte_buff.array(32), 'little')
        byte_buff.array(16)
        security_flag = byte_buff.get(1)

        self.srp_handler = SRPHandler(B, g, N, salt, security_flag)
        self.srp_handler.step1()

        buff = bytearray()
        buff += self.srp_handler.A
        buff += self.srp_handler.M

        md = hashlib.sha1(self.srp_handler.A)
        md.update(self.srp_handler.crc_hash)
        buff += md.digest()

        buff += int.to_bytes(0, 2, 'big')
        packet = Packet(cfg.realm_packets.CMD_AUTH_LOGON_PROOF, buff)
        self.out_queue.put_nowait(packet)

    def handle_CMD_AUTH_LOGON_PROOF(self, packet):
        byte_buff = PyByteBuffer.ByteBuffer.wrap(packet.data)
        result = byte_buff.get(1)
        if not cfg.realm_packets.AUTH.is_success(result):
            cfg.logger.error(cfg.realm_packets.get_message(result))
            return
        proof = byte_buff.array(20)
        if proof != self.srp_handler.generate_hash_logon_proof():
            cfg.logger.error(
                'Logon proof generated by client and server differ. Something is very wrong!')
            return
        else:
            byte_buff.get(4)  # account flag
            cfg.logger.info(f'Successfully logged into realm server')
            packet = Packet(cfg.realm_packets.CMD_REALM_LIST, int.to_bytes(0, 4, 'big'))
            self.out_queue.put_nowait(packet)

    def handle_CMD_REALM_LIST(self, packet):
        realm_name = cfg.realm_name
        realms = self.parse_realm_list(packet)
        target_realm = tuple(filter(lambda r: r['name'].lower() == realm_name.lower(), realms))[0]
        if not target_realm:
            cfg.logger.error(f'Realm {realm_name} not found!')
            return
        target_realm['session_key'] = int.to_bytes(self.srp_handler.K, 40, 'little')
        cfg.realm = target_realm

    def parse_realm_list(self, packet):  # different for Vanilla/TBC+
        not_vanilla = cfg.expansion != 'Vanilla'
        byte_buff = PyByteBuffer.ByteBuffer.wrap(packet.data)
        byte_buff.get(4)
        realms = []
        realm_count = byte_buff.get(2, endianness='little')
        for _ in range(realm_count):
            realm = {}
            realm['is_pvp'] = bool(byte_buff.get(1)) if not_vanilla else None
            realm['lock_flag'] = bool(byte_buff.get(1)) if not_vanilla else None
            realm['flags'] = byte_buff.get(1)  # offline/recommended/for newbies
            realm['name'] = self.read_string(byte_buff)
            address = self.read_string(byte_buff).split(':')
            realm['host'] = address[0]
            realm['port'] = int(address[1])
            realm['population'] = byte_buff.get(4)
            realm['num_chars'] = byte_buff.get(1)
            realm['timezone'] = byte_buff.get(1)
            realm['id'] = byte_buff.get(1)
            if realm['flags'] & 0x04 == 0x04:
                realm['build_info'] = byte_buff.get(5) if not_vanilla else None
                # exclude build info from realm name
                realm['name'] == realm['name'] if not_vanilla else re.sub(r'\(\d+,\d+,\d+\)', '', realm['name'])
            else:
                realm['build_info'] = None
            realms.append(realm)
        string = 'Available realms:' + ''.join(
            [f'\n\t{realm["name"]} {"PvP" if realm["is_pvp"] else "PvE"} - {realm["host"]}:{realm["port"]}'
             for realm in realms])
        cfg.logger.debug(string)
        return realms

    @staticmethod
    def read_string(buff):
        btarr = bytearray()
        while buff.remaining:
            byte = buff.get(1)
            if not byte:
                break
            btarr += int.to_bytes(byte, 1, 'big')
        return btarr.decode('utf-8')