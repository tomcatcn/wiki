import jwt
from django.http import JsonResponse
from wtoken.views import check_token
from users.models import UsersProfile

# 装饰器，检验指定请求类型
def logging_check(*methods):
    def check_method(func):
        def wrapper(request,username=None,*args,**kwargs):

            # 没有传方法，那就返回原来的函数
            if not methods:
                return func(request,username,*args,**kwargs)
            # 有需要校验的方法
            if request.method not in methods:
                return func(request,username,*args,**kwargs)
            else:
                # 取出token
                token = request.META.get('HTTP_AUTHORIZATION')
                print(token)
                # 没有令牌
                if not token:
                    data = {'code':20102,'error':'Please login'}
                    return JsonResponse(data)
                # 检查令牌
                if check_token(token,username):
                    print('成功响应')
                    return func(request,username,*args,**kwargs)
                else:

                    data = {'code':20106,'error':'maybe the expire time have gone please relogin'}
                    return JsonResponse(data)
        return wrapper
    return check_method

#尝试获取用户身份，返回访客用户名
def get_user_by_request(request):

    token = request.META.get('HTTP_AUTHORIZATION')

    if not token:
        return None
    try:
        key = 'lkjuio'
        res = jwt.decode(token,key,algorithms='HS256')

    except Exception as e:
        print(e)
        return None
    return res['username']
