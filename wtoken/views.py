from django.http import JsonResponse
from django.shortcuts import render
import json
import hashlib

from users.models import UsersProfile
# Create your views here.

def str_hash(str):
    salt = 'iuhgeh'
    str += salt
    m = hashlib.md5()
    m.update(str.encode())
    return m.hexdigest()

# 获取令牌
def get_token(username):
    import jwt
    import time
    payload = {'exp':time.time()+86400}
    payload['username'] = username
    key = 'lkjuio'
    token = jwt.encode(payload,key,algorithm='HS256')
    return token.decode()

#校验令牌
def check_token(token,username):
    import jwt
    import time

    key = 'lkjuio'
    try:
        payload = jwt.decode(token.encode(),key,algorithms='HS256')
    except Exception as e:
        print(e)
        return False
    exp = payload['exp']
    username_origin = payload['username']
    if time.time() > exp:
        return False
    if username != username_origin:
        return False
    return True





def tokens_view(request):
    request_data = request.body.decode()
    request_data = json.loads(request_data)

    username = request_data['username']
    # 用户名为空
    if not username:
        data = data = {'code':100102,'error':'the username data is empty'}
        return JsonResponse(data)
    password = request_data['password']
    # 密码为空
    if not password:
        data = data = {'code': 100106, 'error': 'the password data is empty'}
        return JsonResponse(data)
    password_hash = str_hash(password)
    try:
        password_origin = UsersProfile.objects.get(username=username).password
    except Exception as e :
        print(e)
        data = data = {'code': 100107, 'error': 'the user is not existed'}
        return JsonResponse(data)


    #密码不正确
    if password_hash != password_origin:
        data = data = {'code': 100105, 'error': 'the password is not true'}
        return JsonResponse(data)
    # 验证正常
    token = get_token(username)
    data = {'code': 200, 'username': username, 'data': {'token': token}}
    return JsonResponse(data)



