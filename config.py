from enum import Enum

class DangerLv(Enum):
    LOW='低'
    MIDDLE='中'
    HIGH='高'

class DangerType(Enum):
    FUNCTION='功能问题'
    PERFORMANCE='性能问题'
    SECURITY='安全问题'
    USEREXP='用户体验'

KEYWORDS=('1','2','3')