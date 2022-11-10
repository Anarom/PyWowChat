class CodeCollection:

    @classmethod
    def get_str(cls, code):
        string = 'Unknown'
        for attr_name in dir(cls):
            if getattr(cls, attr_name) == code:
                string = attr_name
                break
        return string

    @classmethod
    def get_from_str(cls, string):
        attr_name = string.upper().replace(' ', '_')
        attr = getattr(cls, attr_name)
        if attr is None:
            return -1
        return attr


class GameAuthResults(CodeCollection):
    OK = 0x0C
    FAILED = 0x0D
    REJECT = 0x0E
    BAD_SERVER_PROOF = 0x0F
    UNAVAILABLE = 0x10
    SYSTEM_ERROR = 0x11
    BILLING_ERROR = 0x12
    BILLING_EXPIRED = 0x13
    VERSION_MISMATCH = 0x14
    UNKNOWN_ACCOUNT = 0x15
    INCORRECT_PASSWORD = 0x16
    SESSION_EXPIRED = 0x17
    SERVER_SHUTTING_DOWN = 0x18
    ALREADY_LOGGING_IN = 0x19
    LOGIN_SERVER_NOT_FOUND = 0x1A
    WAIT_QUEUE = 0x1B
    BANNED = 0x1C
    ALREADY_ONLINE = 0x1D
    NO_TIME = 0x1E
    DB_BUSY = 0x1F
    SUSPENDED = 0x20
    PARENTAL_CONTROL = 0x21


class LogonAuthResults(CodeCollection):
    SUCCESS = 0x00
    FAIL_BANNED = 0x03
    FAIL_UNKNOWN_ACCOUNT = 0x04
    FAIL_INCORRECT_PASSWORD = 0x05
    FAIL_ALREADY_ONLINE = 0x06
    FAIL_NO_TIME = 0x07
    FAIL_DB_BUSY = 0x08
    FAIL_VERSION_INVALID = 0x09
    FAIL_VERSION_UPDATE = 0x0A
    FAIL_INID_SERVER = 0x0B
    FAIL_SUSPENDED = 0x0C
    FAIL_FAIL_NOACCESS = 0x0D
    SUCCESS_SURVEY = 0x0E
    FAIL_PARENTCONTROL = 0x0F
    FAIL_LOCKED_ENFORCED = 0x10
    FAIL_TRIAL_ENDED = 0x11
    FAIL_USE_BATTLENET = 0x12
    FAIL_ANTI_INDULGENCE = 0x13
    FAIL_EXPIRED = 0x14
    FAIL_NO_GAME_ACCOUNT = 0x15
    FAIL_CHARGEBACK = 0x16
    FAIL_INTERNET_GAME_ROOM_WITHOUT_BNET = 0x17
    FAIL_GAME_ACCOUNT_LOCKED = 0x18
    FAIL_UNLOCKABLE_LOCK = 0x19
    FAIL_CONVERSION_REQUIRED = 0x20
    FAIL_DISCONNECTED = 0xFF

    @classmethod
    def is_success(cls, result):
        return result == cls.SUCCESS or result == cls.SUCCESS_SURVEY


class ServerMessages(CodeCollection):
    SHUTDOWN_TIME = 0x01
    RESTART_TIME = 0x02
    CUSTOM = 0x03
    SHUTDOWN_CANCELLED = 0x04
    RESTART_CANCELLED = 0x05


class CharClasses(CodeCollection):
    WARRIOR = 0x01
    PALADIN = 0x02
    HUNTER = 0x03
    ROGUE = 0x04
    PRIEST = 0x05
    DEATH_KNIGHT = 0x06
    SHAMAN = 0x07
    MAGE = 0x08
    WARLOCK = 0x09
    DRUID = 0x0B


class CharRaces(CodeCollection):
    HUMAN = 0x01
    ORC = 0x02
    DWARF = 0x03
    NIGHTELF = 0x04
    UNDEAD = 0x05
    TAUREN = 0x06
    GNOME = 0x07
    TROLL = 0x08
    GOBLIN = 0x09
    BLOODELF = 0x0A
    DRAENEI = 0x0B
    WORGEN = 0x16
    PANDAREN_NEUTRAL = 0x18
    PANDAREN_ALLIANCE = 0x19
    PANDAREN_HORDE = 0x1A

    @classmethod
    def get_language(cls, race):
        match race:
            case cls.ORC | cls.UNDEAD | cls.TAUREN | cls.TROLL | cls.BLOODELF | cls.GOBLIN | cls.PANDAREN_HORDE:
                return 0x01  # orcish
            case cls.PANDAREN_NEUTRAL:
                return 0x2A
            case _:
                return 0x07  # common


class CharGenders(CodeCollection):
    MALE = 0
    FEMALE = 1
    NONE = 2


class ChatChannels(CodeCollection):
    SYSTEM = 0x00
    SAY = 0x01
    GUILD = 0x04
    OFFICER = 0x05
    YELL = 0x06
    WHISPER = 0x07
    TEXT_EMOTE = 0x0B
    CHANNEL = 0x11
    CHANNEL_JOIN = 0x12
    CHANNEL_LEAVE = 0x13
    CHANNEL_LIST = 0x14
    CHANNEL_NOTICE = 0x15
    CHANNEL_NOTICE_USER = 0x16
    GUILD_RECRUITMENT = 0x19
    EMOTE = 0x0A
    ANNOUNCEMENT = 0xFF
    ACHIEVEMENT = 0x30
    GUILD_ACHIEVEMENT = 0x31
    GENERAL = 0x01
    TRADE = 0x02
    LOCAL_DEFENSE = 0x16
    WORLD_DEFENSE = 0x17
    LOOKING_FOR_GROUP = 0x1A


class ChatEvents(CodeCollection):
    JOINED = 0x00
    LEFT = 0x01
    YOU_JOINED = 0x02
    YOU_LEFT = 0x03
    WRONG_PASSWORD = 0x04
    NOT_MEMBER = 0x05
    NOT_MODERATOR = 0x06
    PASSWORD_CHANGED = 0x07
    OWNER_CHANGED = 0x08
    PLAYER_NOT_FOUND = 0x09
    NOT_OWNER = 0x0A
    CHANNEL_OWNER = 0x0B
    MODE_CHANGE = 0x0C
    ANNOUNCEMENTS_ON = 0x0D
    ANNOUNCEMENTS_OFF = 0x0E
    MODERATION_ON = 0x0F
    MODERATION_OFF = 0x10
    MUTED = 0x11
    PLAYER_KICKED = 0x12
    BANNED = 0x13
    PLAYER_BANNED = 0x14
    PLAYER_UNBANNED = 0x15
    PLAYER_NOT_BANNED = 0x16
    PLAYER_ALREADY_MEMBER = 0x17
    INVITE = 0x18
    INVITE_WRONG_FACTION = 0x19
    WRONG_FACTION = 0x1A
    INVALID_NAME = 0x1B
    NOT_MODERATED = 0x1C
    PLAYER_INVITED = 0x1D
    PLAYER_INVITE_BANNED = 0x1E
    THROTTLED = 0x1F
    NOT_IN_AREA = 0x20
    NOT_IN_LFG = 0x21
    VOICE_ON = 0x22
    VOICE_OFF = 0x23


class GuildEvents(CodeCollection):
    PROMOTED = 0x00
    DEMOTED = 0x01
    MOTD = 0x02
    JOINED = 0x03
    LEFT = 0x04
    REMOVED = 0x05
    SIGNED_ON = 0x0C
    SIGNED_OFF = 0x0D


class ClientHeaders(CodeCollection):
    AUTH_CHALLENGE = 0x01ED
    CHAR_ENUM = 0x37
    PLAYER_LOGIN = 0x3D
    LOGOUT_REQUEST = 0x4B
    NAME_QUERY = 0x50
    GUILD_QUERY = 0x54
    GUILD_ROSTER = 0x89
    MESSAGECHAT = 0x95
    JOIN_CHANNEL = 0x97
    PING = 0x01DC
    TIME_SYNC_RESP = 0x039
    WARDEN_DATA = 0x02E7
    WHO = 0x62
    KEEP_ALIVE = 0x0407

    GROUP_INVITE = 0x06E
    GROUP_ACCEPT = 0x072
    GROUP_DECLINE = 0x073
    GROUP_DISBAND = 0x07B
    GROUP_RAID_CONVERT = 0x28E

    CHANGEPLAYER_DIFFICULTY = 0x1FD

    CALENDAR_GET_CALENDAR = 0x429
    CALENDAR_GET_EVENT = 0x42A
    CALENDAR_GUILD_FILTER = 0x42B
    CALENDAR_ARENA_TEAM = 0x42C
    CALENDAR_ADD_EVENT = 0x42D
    CALENDAR_UPDATE_EVENT = 0x43E
    CALENDAR_REMOVE_EVENT = 0x42F
    CALENDAR_COPY_EVENT = 0x430
    CALENDAR_EVENT_INVITE = 0x431
    CALENDAR_EVENT_RSVP = 0x432
    CALENDAR_EVENT_REMOVE_INVITE = 0x433
    CALENDAR_EVENT_STATUS = 0x434
    CALENDAR_EVENT_MODERATOR_STATUS = 0x435


class ServerHeaders(CodeCollection):
    AUTH_LOGON_CHALLENGE = 0x00
    AUTH_LOGON_PROOF = 0x01
    REALM_LIST = 0x10
    AUTH_CHALLENGE = 0x01EC
    AUTH_RESPONSE = 0x01EE
    CHANNEL_NOTIFY = 0x99
    CHAR_ENUM = 0x3B
    NAME_QUERY = 0x51
    GUILD_QUERY = 0x55
    INVALIDATE_PLAYER = 0x031C
    LOGIN_VERIFY_WORLD = 0x0236
    TIME_SYNC_REQ = 0x0390
    SERVER_MESSAGE = 0x0291
    GUILD_ROSTER = 0x8A
    GUILD_EVENT = 0x92
    MESSAGECHAT = 0x96
    NOTIFICATION = 0x01CB
    WARDEN_DATA = 0x02E6
    WHO = 0x63
    CLIENTCACHE_VERSION = 0x4AB
    TUTORIAL_FLAGS = 0x0FD
    ADDON_INFO = 0x2ef
    UPDATE_WORLD_STATE = 0x2C3
    SET_PROFICIENCY = 0x127
    SET_DUNGEON_DIFFICULTY = 0x329
    ACCOUNT_DATA_TIMES = 0x209
    GUILD_BANK_LIST = 0x3e8
    CONTACT_LIST = 0x67
    FEATURE_SYSTEM_STATUS = 0x3C9
    BINDPOINTUPDATE = 0x155
    TALENT_UPDATE = 0x4C0
    INSTANCE_DIFFICULTY = 0x33B
    INITIAL_SPELLS = 0x12A
    SEND_UNLEARN_SPELLS = 0x41E
    ACTION_BUTTONS = 0x129
    INITIALIZE_FACTIONS = 0x122
    ALL_ACHIEVEMENT_DATA = 0x47d
    LOAD_EQUIPMENT_SET = 0x4bc
    LOGIN_SETTIMESPEED = 0x042
    SET_FORCED_REACTIONS = 0x2a5
    INIT_WORLD_STATES = 0x2c2
    GM_MESSAGECHAT = 0x03B3
    MOTD = 0x033D
    EMOTE = 0x103
    PONG = 0x1dd
    MONSTER_MOVE = 0x0DD
    DESTROY_OBJECT = 0x0AA
    UPDATE_OBJECT = 0x0A9
    COMPRESSED_UPDATE_OBJECT = 0x1F6
    AI_REACTION = 0x13c
    QUESTGIVER_STATUS_MULTIPLE = 0x418
    GAMEOBJECT_DESPAWN_ANIM = 0x215

    CALENDAR_SEND_CALENDAR = 0x436
    CALENDAR_SEND_EVENT = 0x437
    CALENDAR_FILTER_GUILD = 0x438
    CALENDAR_ARENA_TEAM = 0x439
    CALENDAR_EVENT_INVITE = 0x43A
    CALENDAR_EVENT_INVITE_REMOVED = 0x43B
    CALENDAR_EVENT_STATUS = 0x43C
    CALENDAR_COMMAND_RESULT = 0x43D
    CALENDAR_RAID_LOCKOUT_ADDED = 0x43E
    CALENDAR_RAID_LOCKOUT_REMOVED = 0x43F
    CALENDAR_EVENT_INVITE_ALERT = 0x440
    CALENDAR_EVENT_INVITE_REMOVED_ALERT = 0x441
    CALENDAR_EVENT_INVITE_STATUS_ALERT = 0x442
    CALENDAR_EVENT_REMOVED_ALERT = 0x443
    CALENDAR_EVENT_UPDATED_ALERT = 0x444
    CALENDAR_EVENT_MODERATOR_STATUS_ALERT = 0x445
    CALENDAR_COMPLAIN = 0x446
    CALENDAR_GET_NUM_PENDING = 0x447
    CALENDAR_SEND_NUM_PENDING = 0x448

    MOVE_SET_FACING = 0x0DA
    MOVE_SET_PITCH = 0x0DB
    MOVE_HEARTBEAT = 0x0EE
    MOVE_START_FORWARD = 0x0B5
    MOVE_START_BACKWARD = 0x0B6
    MOVE_STOP = 0x0B7
    MOVE_START_STRAFE_LEFT = 0x0B8
    MOVE_START_STRAFE_RIGHT = 0x0B9
    MOVE_STOP_STRAFE = 0x0BA
    MOVE_JUMP = 0x0BB
    MOVE_START_TURN_LEFT = 0x0BC
    MOVE_START_TURN_RIGHT = 0x0BD
    MOVE_STOP_TURN = 0x0BE
    MOVE_START_PITCH_UP = 0x0BF
    MOVE_START_PITCH_DOWN = 0x0C0
    MOVE_STOP_PITCH = 0x0C1
    MOVE_SET_RUN_MODE = 0x0C2
    MOVE_SET_WALK_MODE = 0x0C3
    MOVE_FALL_LAND = 0x0C9
    MOVE_START_SWIM = 0x0CA
    MOVE_STOP_SWIM = 0x0CB
    MOVE_SET_WALK_SPEED = 0x0D1
    MOVE_SET_RUN_SPEED = 0x0CD
    MOVE_SET_RUN_BACK_SPEED = 0x0CF
    MOVE_TIME_SKIPPED = 0x319
    MOVE_TELEPORT = 0x0C5
    MOVE_ROOT = 0x0EC
    MOVE_UNROOT = 0x0ED

    SPLINE_SET_RUN_SPEED = 0x2FE
    SPLINE_SET_RUN_BACK_SPEED = 0x2FF
    SPLINE_SET_SWIM_SPEED = 0x300
    SPLINE_SET_WALK_SPEED = 0x301
    SPLINE_SET_SWIM_BACK_SPEED = 0x302
    SPLINE_SET_TURN_RATE = 0x303
    SPLINE_MOVE_UNROOT = 0x304
    SPLINE_MOVE_FEATHER_FALL = 0x305
    SPLINE_MOVE_NORMAL_FALL = 0x306
    SPLINE_MOVE_SET_HOVER = 0x306
    SPLINE_MOVE_UNSET_HOVER = 0x308
    SPLINE_MOVE_WATER_WALK = 0x309
    SPLINE_MOVE_LAND_WALK = 0x30A
    SPLINE_MOVE_START_SWIM = 0x30B
    SPLINE_MOVE_STOP_SWIM = 0x30C
    SPLINE_MOVE_SET_RUN_MODE = 0x30D
    SPLINE_MOVE_SET_WALK_MODE = 0x30E
    SPLINE_SET_FLIGHT_SPEED = 0x385
    SPLINE_SET_FLIGHT_BACK_SPEED = 0x386

    AURA_UPDATE_ALL = 0x495
    AURA_UPDATE = 0x496
    POWER_UPDATE = 0x480
    HEALTH_UPDATE = 0x47F

    GROUP_INVITE = 0x06F
    GROUP_LIST = 0x07D
    GROUP_DESTROYED = 0x07C
    GROUP_SET_LEADER = 0x079
    PARTY_MEMBER_STATS = 0x07E
    PARTY_COMMAND_RESULT = 0x07F

    SPELL_START = 0x131
    SPELL_GO = 0x132
    SPELL_FAILURE = 0x133
    SPELL_COOLDOWN = 0x134
    SPELLLOGEXECUTE = 0x24C
    SPELL_FAILED_OTHER = 0x2A6
    PERIODICAURALOG = 0x24E

    LFG_UPDATE_PARTY = 0x368
    ACHIEVEMENT_EARNED = 0x468

    ATTACKSTART = 0x143
    ATTACKSTOP = 0x144
    ATTACKSWING_NOTINRANGE = 0x145
    ATTACKSWING_BADFACING = 0x146
    ATTACKSWING_DEADTARGET = 0x147
    ATTACKSWING_CANT_ATTACK = 0x148

    HIGHEST_THREAT_UPDATE = 0x482
    THREAT_UPDATE = 0x483
    THREAT_REMOVE = 0x484
    THREAT_CLEAR = 0x485

    PLAY_SPELL_VISUAL = 0x1F3
    PLAY_SPELL_IMPACT = 0x1f7

    WEATHER = 0x2f4
    LEARNED_DANCE_MOVES = 0x455


class DiscordHeaders(CodeCollection):
    MESSAGE = 0x00
    ACTIVITY_UPDATE = 0x01
    GUILD_EVENT = 0x02
    ADD_CALENDAR_EVENT = 0x03
    REMOVE_CALENDAR_EVENT = 0x04
    PURGE_CALENDAR = 0x05
    UPDATE_CALENDAR_EVENT = 0x06

class Codes:
    classes = CharClasses
    races = CharRaces
    genders = CharGenders
    game_auth_results = GameAuthResults
    logon_auth_results = LogonAuthResults
    client_headers = ClientHeaders
    server_headers = ServerHeaders
    guild_events = GuildEvents
    servers_messages = ServerMessages
    chat_events = ChatEvents
    chat_channels = ChatChannels
    discord_headers = DiscordHeaders
