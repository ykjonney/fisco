# !/usr/bin/python
# -*- coding:utf-8 -*-


from logger import log_utils
from tasks import app
from commons import web3_utils
from db.models import Cars
import time

logger = log_utils.get_logging('tasks_listen_car_add', 'tasks_listen_car_add.log')


# @app.task(bind=True, queue='listen_car_add')
# def listen_car_add(self):
#     logger.info("car add")
#     cars_contract, _ = web3_utils.load_via_artifact('Cars', wss=True)
#     filter = cars_contract.events.newCar.createFilter(fromBlock=0)
#     while True:
#         try:
#             for event in filter.get_new_entries():
#                 logger.info('event => {0}'.format(event.event))
#                 logger.info(event.args)
#
#                 # 同步数据到 中心化应用数据库
#                 init_cars(event.args)
#         except:
#             pass
#         time.sleep(2)


# @app.task(bind=True, queue='listen_car_add', soft_time_limit=20)
@app.task(bind=True, queue='listen_car_add')
def listen_car_add(self):
    logger.info("car add")
    try:
        cars_contract, _ = web3_utils.load_via_artifact('Cars', wss=True)
        filter = cars_contract.events.newCar.createFilter(fromBlock=0)
        while True:
            for event in filter.get_new_entries():
                logger.info('event => {0}'.format(event.event))
                logger.info(event.args)

                # 同步数据到 中心化应用数据库
                init_cars(event.args)
            time.sleep(2)
    except :
        pass



def init_cars(car_dict):
    """
    初始化车辆信息
    :return:
    """
    logger.info("init car")
    car = Cars()
    # car.index = 1
    car.address = car_dict._carOwner
    car.vin = car_dict._vin.decode().strip(b'\x00'.decode())
    car.car_url = car_dict._carUrl
    car.status=1
    car.sync_save()
    logger.info(car)
