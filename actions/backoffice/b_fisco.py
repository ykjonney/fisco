# !/usr/bin/python
# -*- coding:utf-8 -*-
from tornado.web import url
from enums import PERMISSION_TYPE_USER_MANAGEMENT
from logger import log_utils
from web import BaseHandler, decorators
from commons import fisco_utils
import time

logger = log_utils.get_logging()


class FiscoListViewHandler(BaseHandler):
    """
    用户列表
    """

    @decorators.render_template('backoffice/fisco/list_view.html')
    @decorators.permission_required(PERMISSION_TYPE_USER_MANAGEMENT)
    async def get(self):
        search_name = self.get_argument('search_name', '')
        lang = self.get_argument('lang', '')
        if lang == 'en':
            lang = 'en'
        else:
            lang = 'cn'
        data_list = []
        args = [search_name]
        res = fisco_utils.fisco_select_data('UserTempInfo', '0x2b042831e72894e292507629bec3ae4886f6fe06', 'select',
                                            args)
        print(res)
        if res:
            list1 = list(res[0])
            if len(list1) > 0:
                list2 = list(res[1])
                list3 = list(res[2])
                for i in range(len(list1)):
                    data_list.append({'user_id_no': search_name, 'position': list1[i],
                                      'temperature': list2[i],
                                      'time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(list3[i]))})
        return locals()


class FiscoAddViewHandler(BaseHandler):
    """
    新增用户
    """

    @decorators.render_template('backoffice/fisco/add_view.html')
    @decorators.permission_required(PERMISSION_TYPE_USER_MANAGEMENT)
    async def get(self):
        return locals()

    @decorators.permission_required(PERMISSION_TYPE_USER_MANAGEMENT)
    @decorators.render_json
    async def post(self):
        res = dict(code=0)

        id_number = self.get_argument('id_number')
        position = self.get_argument('position')
        temperature = self.get_argument('temperature')
        print(id_number, position, temperature)
        args = [id_number, position, temperature, int(time.time())]
        fisco_utils.fisco_add_data('UserTempInfo', '0x2b042831e72894e292507629bec3ae4886f6fe06', 'insert', args)
        res['code'] = 1
        return res


URL_MAPPING_LIST = [
    url(r'/backoffice/fisco/list/', FiscoListViewHandler, name='backoffice_fisco_list'),
    url(r'/backoffice/fisco/add/', FiscoAddViewHandler, name='backoffice_fisco_add'),

]
