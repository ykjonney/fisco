# !/usr/bin/python
# -*- coding:utf-8 -*-

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 9966
SERVER_PROTOCOL = 'http'

# 缓存Redis配置
REDIS_CLUSTER = False
# REDIS_NODES = ['192.168.1.241:6378','192.168.1.241:6379','192.168.1.242:6378','192.168.1.242:6379']
REDIS_NODES = ['127.0.0.1:6379']
# 数据库配置
# DB_ADDRESS_LIST = ['192.168.1.241:27017','192.168.1.241:27018','192.168.1.242:27017','192.168.1.242:27018']
DB_ADDRESS_LIST = ['127.0.0.1:27017']
DB_NAME = 'base'  # 数据名
AUTH_USER_NAME = None  # 用户名
AUTH_USER_PASSWORD = None  # 密码

OPT_REPLICA_SET_NAME = 'XJYT'  # 副本集名称
OPT_DISTRIBUTED_CACHED_ENABLE = True  # 启用数据库分布式缓存， 开启此选项请启用缓存
# OPT_READ_PREFERENCE = 'primary'  # 副本集读写方式, primary
# 任务Redis配置
REDIS_TASK_HOST = '127.0.0.1'
REDIS_TASK_PORT = 6379
REDIS_TASK_DB = 8

NUM_PROCESSES = 1

LOG_LEVEL = 'DEBUG'  # DEBUG|INFO|WARNING|ERROR|NONE
LOG_STDERR = False  # 输出到标准错误流

# 分布式任务配置
SCHEDULE_IN = False  # 是否包含排班任务
WORKER_CONCURRENCY = 1  # 建议CPU数量整数倍
TASKS_FUNC_MODULE_CFG_LIST = [

    # ('tasks.instances.task_send_msg', 'send_msg'),


]


