# _*_ encoding:utf-8 _*_

# 频率控制类
import time

from rest_framework.throttling import BaseThrottle, SimpleRateThrottle


"""自定义的节流类
VISIT_RECORD = {}  # 放入缓存里


class VisitThorttle(BaseThrottle):

    def __init__(self):
        self.history = None

    def allow_request(self, request, view):
        # 60s内只能访问3次
        # 1、获取用户ip
        remote_addr = self.get_ident(request)
        ctime = time.time()
        if remote_addr not in VISIT_RECORD:
            VISIT_RECORD[remote_addr] = [ctime, ]
            return True
        self.history = VISIT_RECORD.get(remote_addr)

        # 把超出时间外的时间数据pop掉
        while self.history and self.history[-1] < ctime - 60:
            self.history.pop()

        if len(self.history) < 3:
            self.history.insert(0, ctime)
            return True

        # return True   # 表示可以继续访问
        # return False    # return False表示访问频率太高，被限制，不返回也是False。

    def wait(self):
        # 提示还需要多少秒可以访问
        ctime = time.time()
        return 60 - (ctime - self.history[-1])
"""


# 继承django的类，原理跟上面自定义差不多
class VisitThorttle(SimpleRateThrottle):
        """匿名用户节流"""
        scope = 'Lufei'

        def get_cache_key(self, request, view):
                return self.get_ident(request)


class UserThorttle(SimpleRateThrottle):
        """基于用户节流"""
        scope = 'LufeiUser'

        def get_cache_key(self, request, view):
                return request.user.username
