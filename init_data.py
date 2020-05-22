# !/usr/bin/python
# -*- coding:utf-8 -*-

import asyncio
from commons import common_utils
from commons.common_utils import md5
from db import STATUS_USER_ACTIVE, models
from db.models import User
from enums import ALL_PERMISSION_TYPE_LIST, KEY_INCREASE_USER
from motorengine import DocumentMetaclass


async def init_indexes():
    """
    初始化索引
    :return:
    """
    model_list = []
    attributes = vars(models)
    if attributes:
        for name, attribute in attributes.items():
            if name not in ['SyncDocument', 'AsyncDocument', 'Document', 'BaseModel'] \
                    and attribute.__class__ == DocumentMetaclass:
                model_list.append((name, attribute))

    if model_list:
        for name, model in model_list:
            result = await model.create_indexes()
            if result:
                print('Model [%s] indexes create succeed!' % name)


async def init_users():
    """
    初始化用户信息
    :return:
    """

    user = await User.find_one(dict(login_name='admin'))
    if user:
        await user.delete()

    user = User()
    user.code = common_utils.get_increase_code(KEY_INCREASE_USER)
    user.name = '超级管理员'
    user.email = '943738808@qq.com'  # 邮箱
    user.mobile = '15106139173'  # 手机
    user.superuser = True  # 是否为超管
    user.login_name = 'admin'  # 用户名
    user.login_password = md5('123456')  # 密码
    user.status = STATUS_USER_ACTIVE  # 状态
    user.content = '超级管理员，无所不能'  # 备注
    user.permission_code_list = ALL_PERMISSION_TYPE_LIST

    oid = await user.save()
    if oid:
        print('Initialize user [', user.name, '] succeed!')


task_list = [
    init_indexes(),
    init_users(),
]
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(task_list))
loop.close()
