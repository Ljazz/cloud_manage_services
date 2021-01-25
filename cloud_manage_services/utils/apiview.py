from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response

import time


class AuthorityError(Exception):
    pass


class Base(object):
    """
    API基类
    """

    def __init__(self):
        self.request = None
        self.start = self.end = time.time()
        self.data_dict = None  # js 请求参数
        self.next_page = '/'
        self.code = 200  # 状态码
        self.result = '请求'  # 状态信息
        self.count = 0  # 处理数据条数
        self.total = 0  # 总条数数据条数
        self.page_count = 0  # 分页请求 的 总页数
        self.data = {}  # 数据域
        self.times = 0  # 请求时长
        self.is_cache = 0  # 是否加入缓存（0：是，1,：否）
        self.is_login = True
        self.user = None
        self.must_param = None
        self.all_param = None

    def main(self):
        """
        主函数
        :return:
        """
        self.set_permissions()

    def victim(self):
        """
        逻辑函数  可重写
        :return:
        """
        pass

    # TODO 异步
    def save_log(self):
        """
        保存日志
        :return:
        """
        pass

    def set_permissions(self):
        """
        获取用户权限
        :return:
        """
        try:
            self.user = self.request.user
            if self.is_login:
                if self.request.user.is_authenticated:
                    pass
                else:
                    raise AuthorityError('[40302] 用户不存在')
            else:
                pass

            self.victim()

        except AuthorityError:
            self.code = 403
            self.result = '用户权限不足'


class GomAPIView(Base, APIView):
    """
    API基类
    """

    def get(self, request, *args, **kwargs):
        """
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        self.request = request
        self.data_dict = request.GET.dict()
        self.main()

        result = {
            'code': self.code,
            'total': self.total,
            'count': self.count,
            'result': self.result,
            'page_count': self.page_count,
            'ret': self.data,
            'times': self.times,
            '_app_id': self.app_id,
            'username': self.user.username
        }
        return Response(result)

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        """
        post
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        self.request = request
        self.data_dict = request.POST.dict()
        if 'csrfmiddlewaretoken' in self.data_dict:
            self.data_dict.pop('csrfmiddlewaretoken')
        self.main()
        result = {
            'code': self.code,
            'total': self.total,
            'count': self.count,
            'result': self.result,
            'page_count': self.page_count,
            'ret': self.data,
            'times': self.times,
            '_app_id': self.app_id,
            'username': self.user.username
        }
        return Response(result)
