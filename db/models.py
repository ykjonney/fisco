# !/usr/bin/python
# -*- coding:utf-8 -*-
from datetime import datetime
from commons.decorators import lazy_property
from db import STATUS_USER_LIST, SEX_LIST, STATUS_ROLE_LIST, STATUS_USER_ACTIVE, STATUS_ROLE_ACTIVE, \
    CATEGORY_UPLOAD_FILE_LIST, \
    CATEGORY_UPLOAD_FILE_OTHER
from motorengine import DESC
from motorengine.document import AsyncDocument, SyncDocument
from motorengine.fields import IntegerField, StringField, DateTimeField, ListField, BooleanField, DictField, FloatField


class BaseModel(AsyncDocument, SyncDocument):
    """
    基础模型
    """
    created_id = StringField()  # 创建_id
    created_dt = DateTimeField(default=datetime.now)  # 创建时间
    updated_id = StringField()  # 更新_id
    updated_dt = DateTimeField(default=datetime.now)  # 更新时间
    record_flag = IntegerField(default=1)  # 记录标记, 0: 无效的, 1: 有效的
    needless = DictField(default={})  # 冗余字段

    # 索引
    _indexes = [('created_dt', DESC), ('updated_dt', DESC), 'record_flag']


class InstantMail(BaseModel):
    mail_server = DictField(required=True)  # 邮件配置
    mail_from = StringField(required=True)  # 发件人
    mail_to = ListField(required=True)  # 收件人
    post_dt = DateTimeField(default=datetime.now)  # 邮件发送时间
    status = IntegerField(required=True)  # 状态
    subject = StringField(default='')  # 主题
    content = StringField(default='')  # 内容
    content_images = DictField(default={})  # 图片资源
    attachments = ListField(default=[])  # 附件

    exception = StringField()  # 异常信息

    _indexes = ['mail_from', 'mail_to', 'status', 'subject']


class InstantSms(BaseModel):
    sms_server = StringField(required=True)  # 短信服务
    account = StringField(required=True)  # 账号
    post_dt = DateTimeField(default=datetime.now)  # 发送时间
    status = IntegerField(required=True)  # 状态
    mobile = StringField(default='')  # 手机号
    content = StringField(default='')  # 内容

    exception = StringField()  # 异常信息

    _indexes = ['sms_server', 'account', 'status', 'post_dt', 'mobile']

class AdministrativeDivision(BaseModel):
    """
    行政区划
    """
    code = StringField(db_field='post_code', required=True)  # 区划编号（邮编）
    parent_code = StringField(default=None)  # 父级区划编号
    title = StringField(required=True)  # 区划名
    en_title = StringField()  # 区划英文名
    level = StringField()  # 所属行政级别（P：省，C：市，D：区、县）

    @lazy_property
    async def parent(self):
        """
        父级行政区划
        :return:
        """
        if self.parent_code:
            return await AdministrativeDivision.find_one(dict(code=self.parent_code))
        return None

    async def children(self, filter_code_list=None):
        """
        筛选子一级行政区划
        :param filter_code_list: 筛选的子集code
        :return:
        """
        if filter_code_list:
            if not isinstance(filter_code_list, list):
                raise ValueError('"filter_code_list" must be a tuple or list.')
        match = {
            'parent_code': self.code
        }
        if filter_code_list:
            match['code'] = {'$in': filter_code_list}
        return await AdministrativeDivision.find(match).to_list(None)

    # 索引
    _indexes = ['code', 'parent_code', 'title', 'en_title', 'level']



class UploadFiles(BaseModel):
    code = StringField(required=True, max_length=64)  # 文件编号
    title = StringField(required=True, max_length=64)  # 文件名
    source_title = StringField(required=True, max_length=256)  # 源标题
    category = IntegerField(default=CATEGORY_UPLOAD_FILE_OTHER, choice=CATEGORY_UPLOAD_FILE_LIST)  # 类别
    content_type = StringField()  # 附件类型
    size = IntegerField(required=True)  # 文件大小

    _indexes = ['code', 'category', 'size']

class Score(BaseModel):
    stu_weid = StringField()
    subject = StringField()
    score = FloatField()
    start_time = IntegerField()
    end_time = IntegerField()
    hash_link = StringField()
    tx_hash = StringField()
    credential = IntegerField(default=0)

class Subject(BaseModel):
    issuer = StringField()
    category = IntegerField()
    title = StringField()
    max_score = FloatField(default=0)
    status = IntegerField(default=0)
    id_number = StringField()
    tx_hash = StringField()

class Teacher(BaseModel):
    weid = StringField()
    name = StringField()
    teacher_id = StringField()
    school = StringField()

class School(BaseModel):
    name = StringField()

class Company(BaseModel):
    name = StringField()
    location = StringField()
    business = StringField()
    weid = StringField()
    status = IntegerField(default=0)
    tx_hash = StringField()

class Student(BaseModel):
    name = StringField()
    stuId = StringField()
    idCard = StringField()
    school = StringField()
    weid = StringField()
    tx_hash = StringField()

class Cpt(BaseModel):
    cptTitle = StringField()
    cptId = StringField()
    cptVersion = StringField()
    subject = StringField()

class Credential(BaseModel):
    res = DictField()
    student = StringField()

class User(BaseModel):
    """
    用户
    """
    code = StringField()  # 用户编号
    name = StringField()  # 用户姓名
    sex = IntegerField(choice=SEX_LIST)  # 性别
    email = StringField()  # 电子邮箱
    mobile = StringField(max_length=24)  # 手机号
    phone = StringField(max_length=24)  # 固话
    status = IntegerField(default=STATUS_USER_ACTIVE, choice=STATUS_USER_LIST)  # 状态
    content = StringField()  # 备注
    superuser = BooleanField(default=False)  # 是否超管

    login_name = StringField(required=True, max_length=64)  # 登录名
    login_password = StringField(required=True, max_length=32)  # 登录密码
    login_times = IntegerField(default=0)  # 登录次数
    login_datetime = DateTimeField(default=datetime.now)  # 最近登录时间
    access_secret_id = StringField(max_length=32)  # Access Secret ID
    access_secret_key = StringField(max_length=128)  # Access Secret KEY

    permission_code_list = ListField(default=[])  # 拥有的权限
    role_code_list = ListField(default=[])  # 所属的角色

    manage_region_code_list = ListField(default=[])  # 可管理的地区
    city = StringField()  # 城市标题
    province = StringField()  # 省份标题
    __lazy_all_permission_code_list = None
    __lazy_role_list = None

    def has_perm_sync(self, perm_code):
        """
        判断是否有对应的权限(同步的)
        :param perm_code: 权限编码或编码LIST或编码TUPLES
        :return: True or False
        """
        if perm_code:
            if self.superuser:
                return True
            if isinstance(perm_code, (tuple, list)):
                code_list = perm_code
            else:
                code_list = [perm_code]
            for code in code_list:
                all_permission_codes = self.__lazy_all_permission_code_list
                perm = self.superuser or (all_permission_codes and code in all_permission_codes)
                if perm:
                    return True
        return False

    async def has_perm(self, perm_code):
        """
        判断是否有对应的权限
        :param perm_code: 权限编码或编码LIST或编码TUPLES
        :return: True or False
        """
        if perm_code:
            if self.superuser:
                return True
            if isinstance(perm_code, (tuple, list)):
                code_list = perm_code
            else:
                code_list = [perm_code]
            for code in code_list:
                all_permission_codes = await self.all_permission_codes()
                perm = self.superuser or (all_permission_codes and code in all_permission_codes)
                if perm:
                    return True
        return False

    async def all_permission_codes(self):
        """
        用户所有权限编号
        :return:
        """
        if self.__lazy_all_permission_code_list is not None:
            return self.__lazy_all_permission_code_list
        self.__lazy_all_permission_code_list = []
        if self.permission_code_list:
            self.__lazy_all_permission_code_list.extend(self.permission_code_list)
        role_list = await self.roles_list()
        if role_list:
            for role in role_list:
                if role and role.permission_code_list:
                    self.__lazy_all_permission_code_list.extend(role.permission_code_list)
        return self.__lazy_all_permission_code_list

    async def roles_list(self):
        """
        所属所有角色
        :return:
        """
        if self.__lazy_role_list is not None:
            return self.__lazy_role_list
        self.__lazy_role_list = await Role.find(
            dict(code={'$in': self.role_code_list}, status=STATUS_ROLE_ACTIVE)).to_list(length=None)
        return self.__lazy_role_list

    _indexes = ['code', 'email', 'status', 'login_name', 'login_password', 'access_secret_id',
                'access_secret_key', 'permission_code_list', 'role_code_list']


class Role(BaseModel):
    """
    角色
    """
    code = StringField(required=True)  # 角色编码
    title = StringField(required=True)  # 角色名
    status = IntegerField(default=STATUS_ROLE_ACTIVE, choice=STATUS_ROLE_LIST)  # 状态
    permission_code_list = ListField(default=[])  # 角色权限列表
    content = StringField()  # 备注

    _indexes = ['code', 'status']
