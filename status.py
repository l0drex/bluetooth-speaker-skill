from enum import Enum


class Status(Enum):
    INACTIVE = 'inactive'
    POWERED = 'powered'
    DISCOVERABLE = 'discoverable'
    PAIRING = 'pairing'
    CONNECTED = 'connected'
