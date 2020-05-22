#!/usr/bin/env python
# -*- coding: utf-8 -*-


from client.bcosclient import BcosClient
import os
import settings
from client.datatype_parser import DatatypeParser


def fisco_add_data_demo():
    try:
        client = BcosClient()
        print(client.getinfo())

        abi_file = os.path.join(settings.SITE_ROOT, "contracts", "HelloWorld.abi")
        data_parser = DatatypeParser()
        data_parser.load_abi_file(abi_file)
        contract_abi = data_parser.contract_abi

        # 发送交易，调用一个改写数据的接口
        print("\n>>sendRawTransaction:----------------------------------------------------")
        to_address = '0x548fd1e8af9ca9131c04ab7e1031579f6498ddaf'  # use new deploy address
        args = ["xy1211ddd"]

        receipt = client.sendRawTransactionGetReceipt(to_address, contract_abi, "set", args)
        print("receipt:", receipt)

        # 解析receipt里的log
        print("\n>>parse receipt and transaction:--------------------------------------")
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

        # 调用一下call，获取数据
        print("\n>>Call:------------------------------------------------------------------------")
        res = client.call(to_address, contract_abi, "get")
        print("call get result:", res)

        # 关闭连接
        client.finish()

    except:
        pass


def fisco_add_data_demo1():
    try:
        client = BcosClient()
        print(client.getinfo())
        print(client.client_account)
        abi_file = os.path.join(settings.SITE_ROOT, "contracts", "UserTempInfo.abi")
        data_parser = DatatypeParser()
        data_parser.load_abi_file(abi_file)
        contract_abi = data_parser.contract_abi

        # 发送交易，调用一个改写数据的接口
        # print("\n>>sendRawTransaction:----------------------------------------------------")
        to_address = '0x2b042831e72894e292507629bec3ae4886f6fe06'  # use new deploy address
        args = ['99999','武汉','38.9度',20000]

        receipt = client.sendRawTransactionGetReceipt(to_address, contract_abi, "insert", args)
        print("receipt:", receipt)

        # # 调用一下call，获取数据
        # args = ['99']
        # print("\n>>Call:------------------------------------------------------------------------")
        # res = client.call(to_address, contract_abi, "select", args)
        # print("call get result:", res)


        # 解析receipt里的log
        print("\n>>parse receipt and transaction:--------------------------------------")
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

        # 调用一下call，获取数据
        args = ['99999']
        print("\n>>Call:------------------------------------------------------------------------")
        res = client.call(to_address, contract_abi, "select",args)
        print("call get result:", res)

        print("\n>>Call:------------------------------------------------------------------------")
        res = client.call(to_address, contract_abi, "selectLatest", args)
        print("call get result:", res)

        # 关闭连接
        client.finish()

    except:
        pass


if __name__ == '__main__':
    fisco_add_data_demo1()
