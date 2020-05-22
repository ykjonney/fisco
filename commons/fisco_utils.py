#!/usr/bin/env python
# -*- coding: utf-8 -*-
from client.bcosclient import BcosClient
import os
import settings
from client.datatype_parser import DatatypeParser


def fisco_add_data(contract_name, contract_address, func_name, args):
    try:
        client = BcosClient()
        print(client.getinfo())
        abi_file = os.path.join(settings.SITE_ROOT, "contracts", contract_name + ".abi")
        data_parser = DatatypeParser()
        data_parser.load_abi_file(abi_file)
        contract_abi = data_parser.contract_abi
        # 发送交易
        to_address = contract_address
        receipt = client.sendRawTransactionGetReceipt(to_address, contract_abi, func_name, args)
        print("receipt:", receipt)
        # 解析receipt里的log
        print("parse receipt and transaction:--------------------------------------")
        tx_hash = receipt['transactionHash']
        print("transaction hash: ", tx_hash)
        log_result = data_parser.parse_event_logs(receipt["logs"])
        i = 0
        for log in log_result:
            if 'eventname' in log:
                i = i + 1
                print("{}): log name: {} , data: {}".format(i, log['eventname'], log['eventdata']))
        # 获取对应的交易数据，解析出调用方法名和参数
        tx_response = client.getTransactionByHash(tx_hash)
        input_result = data_parser.parse_transaction_input(tx_response['input'])
        print("transaction input parse:", tx_hash)
        print(input_result)
        # 解析该交易在receipt里输出的output,即交易调用的方法的return值
        output_result = data_parser.parse_receipt_output(input_result['name'], receipt['output'])
        print("receipt output :", output_result)
        # 关闭连接
        client.finish()
    except:
        pass


def fisco_select_data(contract_name, contract_address, func_name, args):
    try:
        client = BcosClient()
        print(client.getinfo())
        abi_file = os.path.join(settings.SITE_ROOT, "contracts", contract_name + ".abi")
        data_parser = DatatypeParser()
        data_parser.load_abi_file(abi_file)
        contract_abi = data_parser.contract_abi
        res = client.call(contract_address, contract_abi, func_name, args)
        print("call get result:", res)
        # 关闭连接
        client.finish()
        return res
    except:
        return None
