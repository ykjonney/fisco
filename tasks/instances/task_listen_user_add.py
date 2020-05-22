# !/usr/bin/python
# -*- coding:utf-8 -*-


from logger import log_utils
from tasks import app
from commons import web3_utils
from db.models import Member
import time

logger = log_utils.get_logging('tasks_listen_user_add', 'tasks_listen_user_add.log')


@app.task(bind=True, queue='listen_user_add')
def listen_user_add(self):
    logger.info("user add")
    users_contract, _ = web3_utils.load_via_artifact('Users', wss=True)
    filter = users_contract.events.newUser.createFilter(fromBlock=0)
    while True:
        try:
            for event in filter.get_new_entries():
                logger.info('event => {0}'.format(event.event))
                logger.info(event.args)

                # 同步数据到 中心化应用数据库
                init_members(event.args)
        except:
            pass
        time.sleep(2)

# @app.task(bind=True, queue='listen_user_add', soft_time_limit=20)
@app.task(bind=True, queue='listen_user_add')
def listen_user_add(self):
    logger.info("user add")
    try:
        users_contract, _ = web3_utils.load_via_artifact('Users', wss=True)
        filter = users_contract.events.newUser.createFilter(fromBlock=0)
        while True:
            for event in filter.get_new_entries():
                logger.info('event => {0}'.format(event.event))
                logger.info(event.args)

                # 同步数据到 中心化应用数据库
                init_members(event.args)
            time.sleep(2)
    except:
        pass

def init_members(member_dict):
    """
    初始化会员信息
    :return:
    """
    logger.info("init member")
    logger.info(member_dict)
    member = Member()
    member.address = member_dict._userOwner
    member.id_number = member_dict._ID_Number.decode().strip(b'\x00'.decode())
    member.id_url = member_dict._ID_url
    member.username = member_dict._username
    member.phone = member_dict._phone
    member.driver_license = member_dict._driver_license
    member.driver_license_url = member_dict._driver_license_url
    member.status=1
    member.sync_save()
    logger.info(member)
