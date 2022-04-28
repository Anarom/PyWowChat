import time
import random
import hashlib

import PyByteBuffer

from src.common.config import cfg
from src.common.packet import Packet
from src.common.message import ChatMessage
from src.common.utils import read_string


class GamePacketHandler:
    ADDON_INFO = b'V\x01\x00\x00x\x9cu\xcc\xbd\x0e\xc20\x0c\x04\xe0\xf2\x1e\xbc\x0ca@\x95\xc8B\xc3\x8cL\xe2"\x0b\xc7' \
                 b'\xa9\x8c\xcbO\x9f\x1e\x16$\x06s\xebww\x81iY@\xcbi3g\xa3&\xc7\xbe[\xd5\xc7z\xdf}\x12\xbe\x16\xc0' \
                 b'\x8cq$\xe4\x12I\xa8\xc2\xe4\x95H\n\xc9\xc5=\xd8\xb6z\x06K\xf84\x0f\x15Fsg\xbb8\xccz\xc7\x97\x8b' \
                 b'\xbd\xdc&\xcc\xfe0B\xd6\xe6\xca\x01\xa8\xb8\x90\x80Q\xfc\xb7\xa4Pp\xb8\x12\xf3?&A\xfd\xb57\x90' \
                 b'x19f\x8f'

    def __init__(self, out_queue):
        self.out_queue = out_queue
        self.received_char_enum = False
        self.in_world = False
        self.last_roster_update = None
        self.character = None
        self.roster = None
        self.guild_info = None

    def handle_packet(self, packet):
        data = packet.to_byte_buff()
        match packet.id:
            case cfg.game_packets.SMSG_AUTH_CHALLENGE:
                return self.handle_SMSG_AUTH_CHALLENGE(data)
            case cfg.game_packets.SMSG_AUTH_RESPONSE:
                return self.handle_SMSG_AUTH_RESPONSE(data)
            case cfg.game_packets.SMSG_NAME_QUERY:
                return self.handle_SMSG_NAME_QUERY(data)
            case cfg.game_packets.SMSG_CHAR_ENUM:
                return self.handle_SMSG_CHAR_ENUM(data)
            case cfg.game_packets.SMSG_LOGIN_VERIFY_WORLD:
                return self.handle_SMSG_LOGIN_VERIFY_WORLD(data)
            case cfg.game_packets.SMSG_GUILD_QUERY:
                return self.handle_SMSG_GUILD_QUERY(data)
            case cfg.game_packets.SMSG_GUILD_EVENT:
                return self.handle_SMSG_GUILD_EVENT(data)
            case cfg.game_packets.SMSG_GUILD_ROSTER:
                return self.handle_SMSG_GUILD_ROSTER(data)
            case cfg.game_packets.SMSG_MESSAGECHAT:
                return self.handle_SMSG_MESSAGECHAT(data)
            case cfg.game_packets.SMSG_CHANNEL_NOTIFY:
                return self.handle_SMSG_CHANNEL_NOTIFY(data)
            case cfg.game_packets.SMSG_NOTIFICATION:
                return self.handle_SMSG_NOTIFICATION(data)
            case cfg.game_packets.SMSG_WHO:
                return self.handle_SMSG_WHO(data)
            case cfg.game_packets.SMSG_SERVER_MESSAGE:
                return self.handle_SMSG_SERVER_MESSAGE(data)
            case cfg.game_packets.SMSG_INVALIDATE_PLAYER:
                return self.handle_SMSG_INVALIDATE_PLAYER(data)
            case cfg.game_packets.SMSG_WARDEN_DATA:
                return self.handle_SMSG_WARDEN_DATA(data)
            case cfg.game_packets.SMSG_GROUP_INVITE:
                return self.handle_SMSG_GROUP_INVITE(data)
            case _:
                cfg.logger.error(f'No handling method for this type of packet: {packet.id}')

    def handle_SMSG_AUTH_CHALLENGE(self, data):
        challenge = self.parse_auth_challenge(data)
        cfg.crypt.initialize(cfg.realm['session_key'])
        self.out_queue.put_nowait(Packet(cfg.game_packets.CMSG_AUTH_CHALLENGE, challenge))

    def parse_auth_challenge(self, data):
        account_bytes = bytes(cfg.account, 'utf-8')
        client_seed = random.randbytes(4)
        server_seed = int.to_bytes(data.get(4), 4, 'big')
        buff = PyByteBuffer.ByteBuffer.allocate(400)
        buff.put(0)
        buff.put(cfg.build, 4, 'little')
        buff.put(account_bytes)
        buff.put(0)
        buff.put(client_seed)
        md = hashlib.sha1(account_bytes)
        md.update(bytearray(4))
        md.update(client_seed)
        md.update(server_seed)
        md.update(cfg.realm['session_key'])
        buff.put(md.digest())
        buff.put(GamePacketHandler.ADDON_INFO)
        buff.strip()
        buff.rewind()
        return buff.array()

    def handle_SMSG_AUTH_RESPONSE(self, data):
        code = data.get(1)
        if code == cfg.game_packets.AUTH_OK:
            cfg.logger.info('Successfully logged into game server')
            if not self.received_char_enum:
                self.out_queue.put_nowait(Packet(cfg.game_packets.CMSG_CHAR_ENUM, b''))
        else:
            cfg.logger.error(cfg.auth_results.get_message(code))
            return

    def handle_SMSG_CHAR_ENUM(self, data):
        if self.received_char_enum:
            return
        self.received_char_enum = True
        self.character = self.parse_char_enum(data)
        if not self.character:
            cfg.logger.error(f'Character {cfg.character} not found')
            return
        cfg.logger.info(f'Logging in with character {self.character["name"]}')
        guid = int.to_bytes(self.character['guid'], 8, 'little')
        self.out_queue.put_nowait(Packet(cfg.game_packets.CMSG_PLAYER_LOGIN, guid))

    def parse_char_enum(self, data):
        n_of_chars = data.get(1)
        chars = []
        correct_char = None
        for _ in range(n_of_chars):
            char = {}
            char['guid'] = data.get(8, 'little')
            char['name'] = read_string(data)
            if char['name'].lower() == cfg.character:
                correct_char = char
            char['race'] = data.get(1)
            char['class'] = data.get(1)
            char['gender'] = data.get(1)
            char['skin'] = data.get(1)
            char['face'] = data.get(1)
            char['hair_style'] = data.get(1)
            char['hair_color'] = data.get(1)
            char['facial hair'] = data.get(1)
            char['level'] = data.get(1)
            char['zone'] = data.get(4, 'little')
            char['map'] = data.get(4, 'little')
            char['x'] = data.get(4, 'little')
            char['y'] = data.get(4, 'little')
            char['z'] = data.get(4, 'little')
            char['guild_guid'] = data.get(4, 'little')
            char['flags'] = data.get(4, 'little')
            char['first_login'] = data.get(1)
            char['pet_info'] = data.get(12, 'little')
            char['equip_info'] = self.get_equip_info(data)
            char['bag_display_info'] = self.get_bag_display_info(data)
            chars.append(char)
        string = 'Available characters:' + ''.join([f'\n\t{char["name"]}' for char in chars])
        cfg.logger.debug(string)
        return correct_char

    @staticmethod
    def get_equip_info(data):
        return data.get(19 * 5, 'little')

    @staticmethod
    def get_bag_display_info(data):
        return data.get(5, 'little')

    def handle_SMSG_LOGIN_VERIFY_WORLD(self, data):
        if self.in_world:
            return
        self.in_world = True
        cfg.logger.info('Successfully joined the world')
        if self.character['guild_guid']:
            self.update_roster()
            # query guild_name
            guid = int.to_bytes(self.character['guild_guid'], 4, 'little')
            self.out_queue.put_nowait(Packet(cfg.game_packets.CMSG_GUILD_QUERY, guid))
        return 2

    def update_roster(self):
        if not self.last_roster_update or time.time() - self.last_roster_update > 60:
            self.last_roster_update = time.time()
            self.out_queue.put_nowait(Packet(cfg.game_packets.CMSG_GUILD_ROSTER, b''))

    def handle_SMSG_NAME_QUERY(self, data):
        pass

    def handle_SMSG_GUILD_QUERY(self, data):
        data.get(4)
        name = read_string(data)
        # TODO ranks

    def handle_SMSG_GUILD_EVENT(self, data):
        pass

    def handle_SMSG_GUILD_ROSTER(self, data):
        pass

    def handle_SMSG_MESSAGECHAT(self, data):
        pass

    def handle_SMSG_CHANNEL_NOTIFY(self, data):
        pass

    def handle_SMSG_NOTIFICATION(self, data):
        pass

    def handle_SMSG_WHO(self, data):
        pass

    def handle_SMSG_SERVER_MESSAGE(self, data):
        pass

    def handle_SMSG_INVALIDATE_PLAYER(self, data):
        pass

    def handle_SMSG_WARDEN_DATA(self, data):
        pass

    def handle_SMSG_GROUP_INVITE(self, data):
        pass

    def send_chat_message(self, message):
        pass
