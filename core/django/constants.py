# coding=utf-8


DEFAULT_DASHBOARD_TITLE = '首页'

MALE = 'male'
FEMALE = 'female'

SEX = (
    (MALE, '男'),
    (FEMALE, '女'),
)

TRUE_FALSE = (
    (True, '是'),
    (False, '否')
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
        (UNREAD, '未读'),
        (READ, '已读'),
        (DELETED, '删除'),
    )


class MailStatus(object):
    UNREAD = 0
    READ = 1
    DRAFT = 2
    TRASH = 3
    DELETED = 99
    STATUS = (
        (UNREAD, '未读'),
        (READ, '已读'),
        (DRAFT, '草稿'),
        (TRASH, '回收站'),
        (DELETED, '删除'),
    )


class UsableStatus(object):
    UNUSABLE = 0
    USABLE = 1
    DELETED = 99
    STATUS = (
        (UNUSABLE, '禁用'),
        (USABLE, '启用'),
        (DELETED, '删除'),
    )


class DeletableStatus(object):
    NORMAL = 1
    DELETED = 99
    STATUS = (
        (NORMAL, '启用'),
        (DELETED, '删除'),
    )


class TaskStatus(object):
    NORMAL = 0
    EXCEPT = 1
    FINISHED = 2
    DELETED = 99
    TASK_STATUS = (
        (NORMAL, '正常(进行中)'),
        (EXCEPT, '异常'),
        (FINISHED, '完成'),
        (DELETED, '删除')
    )


class Position(object):
    STAFF = 0
    MANAGE = 1
    VICE_PRESIDENT = 2
    PRESIDENT = 3

    POSITIONS = (
        (STAFF, '职工'),
        (MANAGE, '经理'),
        (VICE_PRESIDENT, '副总裁'),
        (PRESIDENT, '总裁'),
    )


COUNTRIES_CHOICES = (
    ('AU', '澳洲'),
    ('US', '北美'),
    ('EU', '澳洲'),
    ('GB', '英国'),
    ('JP', '日本'),
    ('KR', '韩国'),
    ('TW', '台湾'),
    ('SEA', '东南亚'),
)

CURRENCY_CHOICES = (
    ('AUDCNH', '澳元'),
    ('USDCNH', '美元'),
    ('NZDCNH', '纽元'),
    ('EURCNH', '欧元'),
    ('GBPCNH', '英镑'),
    ('CADCNH', '加元'),
    ('JPYCNH', '日元'),
)
