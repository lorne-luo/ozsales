# coding=utf-8


DEFAULT_DASHBOARD_TITLE = u'首页'

MALE = 'male'
FEMALE = 'female'

SEX = (
    (MALE, u'男'),
    (FEMALE, u'女'),
)

TRUE_FALSE = (
    (True, u'是'),
    (False, u'否')
)

DICT_NULL_BLANK_TRUE = {
    'null': True,
    'blank': True
}

DICT_NULL_BLANK_FALSE = {
    'null': False,
    'blank': False
}


class ReadStatus(object):
    UNREAD = 0
    READ = 1
    DELETED = 99
    STATUS = (
        (UNREAD, u'未读'),
        (READ, u'已读'),
        (DELETED, u'删除'),
    )


class MailStatus(object):
    UNREAD = 0
    READ = 1
    DRAFT = 2
    TRASH = 3
    DELETED = 99
    STATUS = (
        (UNREAD, u'未读'),
        (READ, u'已读'),
        (DRAFT, u'草稿'),
        (TRASH, u'回收站'),
        (DELETED, u'删除'),
    )


class UsableStatus(object):
    UNUSABLE = 0
    USABLE = 1
    DELETED = 99
    STATUS = (
        (UNUSABLE, u'禁用'),
        (USABLE, u'启用'),
        (DELETED, u'删除'),
    )


class DeletableStatus(object):
    NORMAL = 1
    DELETED = 99
    STATUS = (
        (NORMAL, u'启用'),
        (DELETED, u'删除'),
    )


class TaskStatus(object):
    NORMAL = 0
    EXCEPT = 1
    FINISHED = 2
    DELETED = 99
    TASK_STATUS = (
        (NORMAL, u'正常(进行中)'),
        (EXCEPT, u'异常'),
        (FINISHED, u'完成'),
        (DELETED, u'删除')
    )


class Position(object):
    STAFF = 0
    MANAGE = 1
    VICE_PRESIDENT = 2
    PRESIDENT = 3

    POSITIONS = (
        (STAFF, u'职工'),
        (MANAGE, u'经理'),
        (VICE_PRESIDENT, u'副总裁'),
        (PRESIDENT, u'总裁'),
    )


COUNTRIES_CHOICES = (
    ('AU', u'澳洲'),
    ('US', u'北美'),
    ('EU', u'澳洲'),
    ('GB', u'英国'),
    ('JP', u'日本'),
    ('KR', u'韩国'),
    ('TW', u'台湾'),
    ('SEA', u'东南亚'),
)

CURRENCY_CHOICES = (
    ('AUDCNH', u'澳元'),
    ('USDCNH', u'美元'),
    ('NZDCNH', u'纽元'),
    ('EURCNH', u'欧元'),
    ('GBPCNH', u'英镑'),
    ('CADCNH', u'加元'),
    ('JPYCNH', u'日元'),
)
