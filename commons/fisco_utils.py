#!/usr/bin/env python
# -*- coding: utf-8 -*-
from client.bcosclient import BcosClient
import os
import settings
from client.datatype_parser import DatatypeParser

class Client:
    def __init__(self,contract_name, contract_address):

        abi_file = os.path.join(settings.SITE_ROOT, "contracts", contract_name + ".abi")
        self.data_parser = DatatypeParser()
        self.data_parser.load_abi_file(abi_file)
        self.contract_abi = self.data_parser.contract_abi
        self.contract_address = contract_address
    def fisco_add_data(self, func_name, args):
        client = BcosClient()
        try:
            print('start')
            # 发送交易
            receipt = client.sendRawTransactionGetReceipt(self.contract_address, self.contract_abi, func_name, args)
            print("receipt:", receipt)
            # 解析receipt里的log
            print("parse receipt and transaction:--------------------------------------")
            tx_hash = receipt['transactionHash']
            print("transaction hash: ", tx_hash)
            log_result = self.data_parser.parse_event_logs(receipt["logs"])
            i = 0
            for log in log_result:
                if func_name in log:
                    i = i + 1
                    print("{}): log name: {} , data: {}".format(i, log[func_name], log['eventdata']))
            # 获取对应的交易数据，解析出调用方法名和参数
            tx_response = client.getTransactionByHash(tx_hash)
            input_result = self.data_parser.parse_transaction_input(tx_response['input'])
            print("transaction input parse:", tx_hash)
            print(input_result)
            # 解析该交易在receipt里输出的output,即交易调用的方法的return值
            output_result = self.data_parser.parse_receipt_output(input_result['name'], receipt['output'])
            print("receipt output :", output_result)
            return output_result,tx_hash
        except:
            pass
        finally:
            # 关闭连接
            client.finish()


    def fisco_select_data(self, func_name, args):
        client = BcosClient()
        try:
            print('start')
            res = client.call(self.contract_address, self.contract_abi, func_name, args)
            print("call get result:", res)
            # 关闭连接
            client.finish()
            return res
        except:
            return None
if __name__=='__main__':
    f_client = Client('precompile/CNS', '0x1004')
    f_client.fisco_add_data('insertStudent',['01234','tom','qinghua','sdfsfswedvccvf'])