import json
import time
import traceback

import ipfshttpclient
import redis
from tornado.web import url
import requests

from commons.common_utils import get_random_str
from db import STATUS_USER_ACTIVE
from db.models import User, Student, Company, Teacher, School, Score, Subject, Cpt, Credential
from logger import log_utils
from web import decorators, RedisCache, md5, NonXsrfBaseHandler
from web.base import WechatAppletHandler
from commons import fisco_utils
from actions.backoffice.weid_request_args import Args

host = 'http://192.168.1.119:6001/weid/api/invoke'
fisco_client = fisco_utils.Client('test1', '0x73abb55230ad251b9bf2cf3fcce8d27130750d53')
issuer = 'did:weid:1:0x685e69ba2202faa5b232eb1e7c1467699c8fa74b'
r = redis.Redis(host='localhost', port=6379, decode_responses=True)
logger = log_utils.get_logging()
api = ipfshttpclient.connect('/ip4/183.2.223.53/tcp/5001/http')


class AccessTokenGetViewHandler(NonXsrfBaseHandler):
    """
    获取Access Token
    """

    @decorators.render_json
    async def post(self):
        r_dict = {'code': 0}
        try:
            args = json.loads(self.request.body.decode('utf-8'))
            access_id = self.get_argument('access_key_id')
            if not access_id:
                access_id = args.get('access_key_id')
            access_secret = self.get_argument('access_key_secret')
            if not access_secret:
                access_secret = args.get('access_key_secret')
            if access_id and access_secret:
                token = await self.generate_new_token(access_id, access_secret)
                if token:
                    r_dict['code'] = 1000
                    r_dict['token'] = token
                else:
                    r_dict['code'] = 1001  # access_key_id、access_key_secret 无效
            else:
                r_dict['code'] = 1002  # access_key_id、access_key_secret 为空
        except RuntimeError:
            logger.error(traceback.format_exc())

        return r_dict

    async def generate_new_token(self, access_id, access_secret):
        """
        生成新的TOKEN
        :param access_id: ACCESS KEY ID
        :param access_secret: ACCESS KEY SECRET
        :return:
        """
        if access_id and access_secret:
            count = await User.count(dict(access_secret_id=access_id, access_secret_key=access_secret,
                                          status=STATUS_USER_ACTIVE))
            if count > 0:
                token = get_random_str(32)
                key = md5(token)
                # RedisCache.set(key, token, 60 * 60 * 2)
                RedisCache.set(key, token)
                return token
        return None


class userRegisterHanler(WechatAppletHandler):

    @decorators.render_json
    async def post(self):
        """
        注册weid，其中kyc认证部分暂时忽略，后续可自行调整
        :return:
        """
        r_dict = {'respBody': '', 'errorCode': 200, 'errorMessage': 'success'}
        category = int(self.get_i_argument('category'))
        if category == 0:
            stuId = self.get_i_argument('stuId')
            name = self.get_i_argument('name')
            school = self.get_i_argument('school')
            id_card = self.get_i_argument('id_card')
            try:
                res = requests.post(host, json=Args.register_weid).json()
                print(res)
                _, tx_hash = fisco_client.fisco_add_data('insertStudent',
                                                         [res['respBody'], stuId, id_card, name, school])
                student = Student()
                student.weid = res['respBody']
                student.school = school
                student.name = name
                student.stuId = stuId
                student.idCard = id_card
                student.tx_hash = tx_hash
                await student.save()
                r_dict['respBody'] = res['respBody']
            except Exception:
                logger.error(traceback.format_exc())
            return r_dict
        elif category == 1:
            name = self.get_i_argument('name')
            location = self.get_i_argument('location')
            business = self.get_i_argument('business')
            try:
                res = requests.post(host, json=Args.register_weid).json()
                print(res)
                _, tx_hash = fisco_client.fisco_add_data('insertCompany', [res['respBody'], name, location, business])
                company = Company()
                company.name = name
                company.location = location
                company.business = business
                company.weid = res['respBody']
                company.tx_hash = tx_hash
                await company.save()
                r_dict['respBody'] = res['respBody']
            except Exception:
                logger.error(traceback.format_exc())
            return r_dict
        else:
            name = self.get_i_argument('name')
            school = self.get_i_argument('school')
            teacher_id = self.get_i_argument('teacher_id')
            try:
                res = requests.post(host, json=Args.register_weid).json()
                # fisco_client.fisco_add_data('insetCompany', [name, location, business, res['respBody']])
                teacher = Teacher()
                teacher.weid = res['respBody']
                teacher.school = school
                teacher.name = name
                teacher.teacher_id = teacher_id
                await teacher.save()
                res['user_cid'] = teacher.cid
                res['category'] = 2
                r_dict['respBody'] = res['respBody']
            except Exception:
                pass
            return r_dict


class LoginHandler(WechatAppletHandler):
    @decorators.render_json
    async def post(self, *args, **kwargs):
        r_dict = {'respBody': '', 'errorCode': 200, 'errorMessage': 'success'}
        category = int(self.get_i_argument('category'))
        name = self.get_i_argument('name')
        print(name)
        if category == 0:
            student = await Student.find_one(dict(name=name))
            r_dict['respBody'] = student.weid
        elif category == 1:
            company = await Company.find_one(dict(name=name))
            r_dict['respBody'] = company.weid
        else:
            teacher = await Teacher.find_one(dict(name=name))
            r_dict['respBody'] = teacher.weid
        return r_dict


class SubjectHandler(WechatAppletHandler):

    @decorators.render_json
    async def post(self, *args, **kwargs):
        """
        注册科目
        :param args:
        :param kwargs:
        :return:
        """
        r_dict = {'respBody': '', 'errorCode': 200, 'errorMessage': 'success'}
        issuer = self.get_i_argument('issuer')
        category = int(self.get_i_argument('category'))
        title = self.get_i_argument('title')
        max_score = int(self.get_i_argument('maxscore'))
        id_number = self.get_i_argument('idNumber')
        try:

            res, tx_hash = fisco_client.fisco_add_data('createSubject', [id_number, issuer, category, max_score])
            print('tx_hash:', tx_hash)
            subject = Subject()
            subject.title = title
            subject.issuer = issuer
            subject.category = category
            subject.max_score = max_score
            subject.id_number = id_number
            subject.tx_hash = tx_hash
            await subject.save()
            r_dict['respBody'] = res
        except Exception as e:
            print(e)
        return r_dict

    @decorators.render_json
    async def get(self, *args, **kwargs):
        """
        获取所有科目
        :param args:
        :param kwargs:
        :return:
        """
        status = int(self.get_i_argument('status', 0))
        r_dict = {'respBody': '', 'errorCode': 200, 'errorMessage': 'success'}
        try:
            subject_list = await Subject.find(dict(status=status)).to_list(None)
            r_dict['respBody'] = subject_list
        except Exception:
            pass
        return r_dict

    @decorators.render_json
    async def put(self, *args, **kwargs):
        r_dict = {'respBody': '', 'errorCode': 200, 'errorMessage': 'success'}
        subject_id = self.get_i_argument('subject_id')
        try:
            subject = await Subject.find_one(id_number=subject_id)
            subject.status = 1
            await subject.save()
        except Exception:
            pass
        return r_dict


class ExamHandler(WechatAppletHandler):
    @decorators.render_json
    async def post(self, *args, **kwargs):
        r_dict = {'respBody': '', 'errorCode': 200, 'errorMessage': 'success'}
        exam = self.get_i_argument('exam')
        print(exam)
        subject = exam['subject']
        student = exam['student']
        r.hset(subject, student, exam)
        return r_dict

    @decorators.render_json
    async def get(self, *args, **kwargs):
        r_dict = {'respBody': '', 'errorCode': 200, 'errorMessage': 'success'}
        issuer = self.get_i_argument('issuer')
        print(issuer)
        subjects = await Subject.find(dict(issuer=issuer)).to_list(None)
        s_list = [r.hgetall(i.id_number) for i in subjects if r.hgetall(i.id_number) is not None]
        s_list = [eval(v) for i in s_list for v in i.values()]
        print(s_list)
        r_dict['respBody'] = s_list
        return r_dict


class StudentScoreHandler(WechatAppletHandler):

    @decorators.render_json
    async def post(self, *args, **kwargs):
        r_dict = {'respBody': '', 'errorCode': 200, 'errorMessage': 'success'}
        weid = self.get_i_argument('weid')
        subject = self.get_i_argument('subject')
        start_time = int(self.get_i_argument('start_time'))
        end_time = int(self.get_i_argument('end_time'))
        scores = int(self.get_i_argument('score'))
        # todo: upload to ipfs
        exam = eval(r.hget(subject, weid))
        print(exam)
        exam['score'] = scores
        print('score post:', weid, subject, scores)
        try:
            hash_link = api.add_json(exam)
            print('hash_link:', hash_link)
            res, tx_hash = fisco_client.fisco_add_data('insertScore',
                                                       [weid, subject, scores, start_time, end_time, hash_link])
            score = Score()
            score.stu_weid = weid
            score.subject = subject
            score.hash_link = hash_link
            score.start_time = start_time
            score.end_time = end_time
            score.score = scores
            score.tx_hash = tx_hash
            await score.save()
            r_dict['respBody'] = res
        except Exception as e:
            print(e)
        return r_dict

    @decorators.render_json
    async def get(self, *args, **kwargs):
        r_dict = {'respBody': '', 'errorCode': 200, 'errorMessage': 'success'}
        weid = self.get_i_argument('weid')
        subject = self.get_i_argument('subject')
        print('score get:', weid, subject)
        if subject:
            # res = fisco_client.fisco_select_data('selectOne',[weid,subject])
            score = await Score.find_one(dict(stu_weid=weid, subject=subject))
            print('score:', score)
            cpt = await Cpt.find_one(dict(subject=subject))
            score.cpt =cpt if cpt else None
            print('CPT:', cpt)
            r_dict['respBody'] = score
        else:
            res = fisco_client.fisco_select_data('selectAll', [weid, ])
            cptIds = []
            for i in res[0]:
                cpt = await Cpt.find_one(dict(subject=i))
                if cpt:
                    cptIds.append(cpt.cptId)
            l_res = list(res)
            l_res.append(tuple(cptIds))
            r_dict['respBody'] = l_res
        return r_dict

    @decorators.render_json
    async def delete(self, *args, **kwargs):
        pass

    @decorators.render_json
    async def put(self, *args, **kwargs):
        r_dict = {'respBody': '', 'errorCode': 200, 'errorMessage': 'success'}
        weid = self.get_i_argument('weid')
        subject = self.get_i_argument('subject')
        score = int(self.get_i_argument('score'))
        res = fisco_client.fisco_add_data('updateScore', [weid, subject, score])
        r_dict['respBody'] = res
        return r_dict


class TeacherHandler(WechatAppletHandler):
    @decorators.render_json
    async def get(self, *args, **kwargs):
        r_dict = {'respBody': '', 'errorCode': 200, 'errorMessage': 'success'}
        weid = self.get_i_argument('weid')
        subjects = await Subject.find(dict(issuer=weid)).to_list(None)
        r_dict['respBody'] = subjects
        return r_dict

    @decorators.render_json
    async def post(self, *args, **kwargs):
        r_dict = {'respBody': '', 'errorCode': 200, 'errorMessage': 'success'}
        subject = self.get_i_argument('subject')
        print(subject)
        scores = await Score.find(dict(subject=subject)).to_list(None)
        r_dict['respBody'] = scores
        print(r_dict)
        return r_dict


class issuerHandler(WechatAppletHandler):

    @decorators.render_json
    async def post(self, *args, **kwargs):
        weid = self.get_i_argument('weid')
        Args.register_authority_issuer['functionArg']['weid'] = weid
        try:
            res = requests.post(host, json=Args.register_authority_issuer).json()
        except Exception as e:
            print(e)
        return res

    @decorators.render_json
    async def get(self, *args, **kwargs):
        weid = self.get_i_argument('weid')
        Args.select_authority_issuer['functionArg']['weid'] = weid
        try:
            res = requests.post(host, json=Args.select_authority_issuer).json()
        except Exception:
            pass
        return res

    @decorators.render_json
    async def put(self, *args, **kwargs):
        pass


class cptHandler(WechatAppletHandler):
    @decorators.render_json
    async def post(self, *args, **kwargs):
        functionArg = self.get_i_argument('functionArg')
        transactionArg = self.get_i_argument('transactionArg')
        subject = self.get_i_argument('subject')
        Args.create_cpt['functionArg'] = functionArg

        Args.create_cpt['transactionArg'] = transactionArg
        print(functionArg, transactionArg)
        try:
            res = requests.post(host, json=Args.create_cpt).json()
            cpt = Cpt()
            cpt.cptId = str(res['respBody']['cptId'])
            cpt.cptVersion = str(res['respBody']['cptVersion'])
            cpt.cptTitle = functionArg["cptJsonSchema"]['title']
            cpt.subject = subject
            await cpt.save()
        except Exception as e:
            print(e)
        return res

    @decorators.render_json
    async def get(self, *args, **kwargs):
        cptId = self.get_i_argument('cptId')
        r_dict = {'respBody': '', 'errorCode': 200, 'errorMessage': 'success'}
        if cptId:
            Args.select_cpt['functionArg']['cptId'] = int(cptId)
            try:
                res = requests.post(host, json=Args.select_cpt).json()
                r_dict['respBody'] = res
            except Exception:
                pass
        else:
            res = await Cpt.find().to_list(None)
            res = [{'cptId': i.cptId, 'cptVersion': i.cptVersion, 'subject': i.subject} for i in res]
            r_dict['respBody'] = res
        return r_dict


class credentialHandler(WechatAppletHandler):

    @decorators.render_json
    async def post(self, *args, **kwargs):
        r_dict = {'respBody': '', 'errorCode': 200, 'errorMessage': 'success'}
        cptId = self.get_i_argument('cptId')
        subject = self.get_i_argument('subject')
        weid = self.get_i_argument('weid')
        score = fisco_client.fisco_select_data('selectOne', [weid, subject])
        if score[0] >= 60:
            Args.select_cpt['functionArg']['cptId'] = int(cptId)
            res = requests.post(host, json=Args.select_cpt).json()
            print(res)
            student = await Student.find_one(dict(weid=weid))
            Args.create_credential['functionArg']['cptId'] = cptId
            Args.create_credential['functionArg']['issuer'] = issuer
            Args.create_credential['functionArg']['claim'] = {
                'name': student.name, 'stuId': student.stuId, 'school': student.school}
            Args.create_credential['transactionArg']["invokerWeId"] = issuer
            try:
                res = requests.post(host, json=Args.create_credential).json()
                print(res)
                if res['errorCode'] == 200:
                    score = await Score.find_one(dict(subject=subject))
                    score.credential = 1
                    await score.save()
                    credential = Credential()
                    credential.res = res['respBody']
                    credential.student = weid
                    await credential.save()
                    return res
                else:
                    r_dict['errorCode'] = 400
                    r_dict['errorMessage'] = '创建失败'
                    return r_dict
            except Exception:
                pass
        r_dict['errorCode'] = 400
        r_dict['errorMessage'] = '科目分数不及格'
        return r_dict

    @decorators.render_json
    async def get(self, *args, **kwargs):
        r_dict = {'respBody': '', 'errorCode': 200, 'errorMessage': 'success'}
        weid = self.get_i_argument('weid')
        credentials = await Credential.find(dict(student=weid)).to_list(None)
        for credential in credentials:
            Args.select_cpt['functionArg']['cptId'] = credential.res['cptId']
            res = requests.post(host, json=Args.select_cpt).json()
            credential.title = res['respBody']['cptJsonSchema']['title']
        r_dict['respBody'] = credentials
        return r_dict


class VeriferHander(WechatAppletHandler):
    @decorators.render_json
    async def get(self, *args, **kwargs):
        r_dict = {'respBody': '', 'errorCode': 200, 'errorMessage': 'success'}
        cid = self.get_i_argument('cid')
        credential = await Credential.find_one(dict(cid=cid))
        if credential:
            Args.verify_credential['functionArg'] = credential.res
            res = requests.post(host, json=Args.verify_credential).json()
            r_dict['respBody'] = credential if res['errorCode'] == 0 else res['respBody']
            Args.select_cpt['functionArg']['cptId'] = credential.res['cptId']
            res = requests.post(host,json=Args.select_cpt).json()
            r_dict['respBody'].title = res['respBody']['cptJsonSchema']['title']
            return r_dict
        else:
            r_dict['errorCode'] = 400
            r_dict['errorMessage'] = 'not have this credential'
        return r_dict


URL_MAPPING_LIST = [
    url(r'/api/user/register/', userRegisterHanler, name='userRegisterHanler'),
    url(r'/api/score/', StudentScoreHandler, name='StudentScoreHandler'),
    url(r'/api/cpt/', cptHandler, name='cptHandler'),
    url(r'/api/issuer/', issuerHandler, name='issuerHandler'),
    url(r'/api/credential/', credentialHandler, name='credentialHandler'),
    url(r'/api/token/', AccessTokenGetViewHandler, name='AccessTokenGetViewHandler'),
    url(r'/api/subject/', SubjectHandler, name='SubjectHandler'),
    url(r'/api/user/login/', LoginHandler, name='LoginHandler'),
    url(r'/api/exam/', ExamHandler, name='ExamHandler'),
    url(r'/api/teacher/', TeacherHandler, name='TeacherHandler'),
    url(r'/api/verifer/', VeriferHander, name='VeriferHander')
]
