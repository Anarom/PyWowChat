import logging
import os
import sys

import lxml.objectify
from importlib import import_module


class _Config:

    def __init__(self):
        self.logger = self.setup_log()
        with open(os.path.join(os.path.dirname(sys.argv[0]), 'config.xml'), 'r', encoding='utf-8') as file:
            xml_obj = lxml.objectify.fromstring(file.read())

        self.account = str(xml_obj.wow.account).upper()
        self.password = str(xml_obj.wow.password).upper()
        self.version = str(xml_obj.wow.version)
        self.platform = str(xml_obj.wow.platform)
        self.realmlist = str(xml_obj.wow.realmlist)
        self.locale = str(xml_obj.wow.locale)
        self.realm_name = str(xml_obj.wow.realm)
        self.host, self.port = self.parse_realm_list()
        self.build = self.get_build()
        self.expansion = self.get_expansion()

        self.realm = None
        self.game_packets = getattr(import_module(f'src.packets.game.{self.expansion}'), 'GamePackets')
        self.realm_packets = getattr(import_module('src.packets.realm'), 'RealmPackets')
        self.crypt = getattr(import_module(f'src.header_crypt.{self.expansion}'), 'GameHeaderCrypt')()

        self.logger.debug('Config values:\n\t'
                          # f'account = {self.account}\n\t'
                          # f'password = {self.password}\n\t'
                          f'platform = {self.platform}\n\t'
                          f'locale = {self.locale}\n\t'
                          f'expansion = {self.expansion}\n\t'
                          f'version = {self.version}\n\t'
                          f'build = {self.build}\n\t'
                          f'host = {self.host}\n\t'
                          f'port = {self.port}\n\t'
                          f'realm = {self.realm_name}')

    def setup_log(self):
        log = logging.getLogger('app')
        log.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
        log.addHandler(handler)
        return log

    def parse_realm_list(self):
        split_pos = self.realmlist.find(':')
        if split_pos == -1:
            host = self.realmlist
            port = 3724
        else:
            host = self.realmlist[:split_pos]
            port = self.realmlist[:split_pos + 1]
        return host, port

    def get_build(self):
        match self.version:
            case '1.11.2':
                return 5464
            case '1.12.1':
                return 5875
            case '1.12.2':
                return 6005
            case '1.12.3':
                return 6141
            case '2.4.3':
                return 8606
            case '3.2.2':
                return 10505
            case '3.3.0':
                return 11159
            case '3.3.2':
                return 11723
            case '3.3.5':
                return 12340
            case '4.3.4':
                return 15595
            case '5.4.8':
                return 18414
            case _:
                self.logger.error(f'Build version {self.version} not supported')
                raise ValueError

    def get_expansion(self):
        match self.version[0]:
            case '1':
                return 'Vanilla'
            case '2':
                return 'TBC'
            case '3':
                return 'WotLK'
            case '4':
                return 'Cataclysm'
            case '5':
                return 'MoP'
            case _:
                self.logger.error(f'Expansion {self.version} not supported!')
                raise ValueError


cfg = _Config()