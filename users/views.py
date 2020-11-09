import json
import hashlib
from django.http import JsonResponse
from django.shortcuts import render
from users.models import *
from tools.logging_check import *

# Create your views here.
from wtoken.views import get_token

def str_hash(_str):
    salt = 'iuhgeh'
    _str += salt
    m = hashlib.md5()
    m.update(_str.encode())
    return m.hexdigest()





@logging_check('PUT')
def users_view(request,username=None):
    if request.method == 'GET':
        # 返回全部用户数据
        if username == None:
            users_data = []
            all_users = UsersProfile.objects.all()
            for user in all_users:
                dic = {}
                dic['username'] = user.username
                dic['nickname'] = user.nickname
                dic['sign'] = user.sign
                dic['info'] = user.info
                # 数据库对象IMage..字段，不是字符串，需要转化
                dic['avatar'] = str(user.avatar)
                users_data.append(dic)
            data = {'code':'200','data':users_data}
            return JsonResponse(data)
        else:
            try:
                single_user = UsersProfile.objects.get(username=username)
            # 没有用户数据
            except Exception as e:
                print(e)
                data = {'code': 100108, 'error': 'the username is not existed'}
                return JsonResponse(data)
            user_data = {}
            user_data['nickname'] = single_user.nickname
            user_data['sign'] = single_user.sign
            user_data['info'] = single_user.info
            user_data['avatar'] = str(single_user.avatar)

            print(single_user.avatar,type(single_user.avatar))
            # 获取指定用户全部数据
            if not request.GET:
                data = {'code':200,'username':username,'data':user_data}
                return JsonResponse(data)
            else:
                user_query = {}
                query_str = request.GET.keys()
                for _str in query_str:
                    if _str == 'password':
                        continue
                    if _str in user_data:
                        user_query[_str] = user_data[_str]
                data = {'code':200,'username':username,'data':user_query}
                return JsonResponse(data)

    elif request.method == 'POST':
        request_data = request.body.decode()
        request_data = json.loads(request_data)
        # 提交数据为空
        if not len(request_data):
            data = {'code':100101,'error':'the submit data is empty'}
            return JsonResponse(data)
        username = request_data.get('username')
        # 用户名为空
        if not username:
            data = {'code':100102,'error':'the username data is empty'}
            return JsonResponse(data)
        email = request_data.get('email','')
        password1 = request_data.get('password_1')
        password2 = request_data.get('password_2')
        # 处理两次密码不一致
        if password1 != password2:
            data = {'code':100103,'error':'the two password must be the same '}
            return JsonResponse(data)

        # 数据验证成功

        try:
            password = str_hash(password1)
            print(password)
            user = UsersProfile.objects.create(username=username,email=email,password=password)
        # 创建失败
        except Exception as e:
            print(e)
            data = {'code':100103,'error':'the username is existed'}
            return JsonResponse(data)
        # 获取令牌
        token = get_token(username)
        data = {'code':200,'username':username,'data':{'token':token}}
        return JsonResponse(data)
    elif request.method == 'PUT':
        if username:
            # body中拿数据并转化为字典
            request_data = request.body.decode()
            request_data = json.loads(request_data)
            # 修改用户数据
            user = UsersProfile.objects.get(username=username)
            # 判断修改的数据是否与原来一样
            to_update = False
            if user.sign != request_data['sign']:
                to_update = True
            if user.info != request_data['info']:
                to_update = True
            if user.nickname != request_data['nickname']:
                to_update = True
            if to_update:
                user.sign = request_data['sign']
                user.info = request_data['info']
                user.nickname = request_data['nickname']
                user.save()
            data = {'code':200,'username':username}
            return JsonResponse(data)
        else:
            data ={'code':100109,'error':'must be give me a username'}
            return JsonResponse(data)



# 因为PUT方法，对于取出文件比较麻烦，改动代码较多
#为了开发简单，可以给一个视图函数，方便上传文件
#处理头像上传
@logging_check('POST')
def avatar_view(request,username):
    if request.method != 'POST':
        data = {'code':'10100','error':'Please use method'}
        return JsonResponse(data)
    user = UsersProfile.objects.get(username=username)
    user.avatar = request.FILES['avatar']
    # 用户名错误
    print(username,user.username)
    # 全部转为小写比较，因为数据库是大小写都可以查到
    username = username.lower()
    user.username = user.username.lower()
    if user.username != username:
        data = {'code': '10112', 'error': 'Please wrong user'}
        return JsonResponse(data)
    # 检验用户成功
    user.save()
    data = {'code':200,'username':username}
    return JsonResponse(data)




if __name__ == '__main__':
    print(str_hash('456789'))
