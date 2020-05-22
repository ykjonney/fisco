# !/usr/bin/python
# -*- coding:utf-8 -*-


from logger import log_utils
from tasks import app
from commons import web3_utils
from db.models import DriveInfo
import traceback
import time

logger = log_utils.get_logging('tasks_listen_driveInfo_add', 'tasks_listen_driveInfo_add.log')


# @app.task(bind=True, queue='listen_driveInfo_add')
# def listen_driveInfo_add(self):
#     logger.info("driveInfo add")
#     drives_contract, _ = web3_utils.load_via_artifact('DriveInfo', wss=True)
#     filter = drives_contract.events.newDriveInfo.createFilter(fromBlock=0)
#     while True:
#         try:
#             for event in filter.get_new_entries():
#                 logger.info('event => {0}'.format(event.event))
#                 logger.info(event.args)
#
#                 # 同步数据到 中心化应用数据库
#                 init_driveInfos(event.args)
#         except:
#             pass
#         time.sleep(2)

# @app.task(bind=True, queue='listen_driveInfo_add', soft_time_limit=20)
@app.task(bind=True, queue='listen_driveInfo_add')
def listen_driveInfo_add(self):
    logger.info("driveInfo add")
    try:
        drives_contract, _ = web3_utils.load_via_artifact('DriveInfo', wss=True)
        filter = drives_contract.events.newDriveInfo.createFilter(fromBlock=0)
        while True:
            for event in filter.get_new_entries():
                logger.info('event => {0}'.format(event.event))
                logger.info(event.args)

                # 同步数据到 中心化应用数据库
                init_driveInfos(event.args)

            time.sleep(2)
    except:
        pass



def init_driveInfos(drive_dict):
    """
    初始化行使订单信息
    :return:
    """
    logger.info("init drive info")
    logger.info(drive_dict)
    try:
        driveInfo = DriveInfo()
        driveInfo.order_id = drive_dict._orderId.decode().strip(b'\x00'.decode())
        driveInfo.id_number = drive_dict._userIDNo.decode().strip(b'\x00'.decode())
        driveInfo.vin = drive_dict._vin.decode().strip(b'\x00'.decode())
        driveInfo.start_km = drive_dict._startKm
        driveInfo.end_km = drive_dict._endKm
        driveInfo.start_time = drive_dict._startTime
        driveInfo.end_time = drive_dict._endTime
        driveInfo.total_price = drive_dict._totalPrice
        driveInfo.status=1
        driveInfo.sync_save()
    except RuntimeError:
        logger.error(traceback.format_exc())
    logger.info(driveInfo)
