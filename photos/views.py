import json

from django.http import JsonResponse
from django.shortcuts import render
from photos.models import *
from users.models import UsersProfile
from tools.logging_check import *
# Create your views here.

# post方法验证令牌
@logging_check('POST','PUT','DELETE')
def photos_view(request,username=None):
    try:
        user = UsersProfile.objects.get(username=username)
    # 无用户，返回错误类型
    except Exception as e:
        print(e)
        return JsonResponse({'code': 700101, 'error': 'not the user'})
    # GET请求，获取资源
    if request.method == 'GET':
        # 无参数 返回相册列表
        if not request.GET:
            photos_all = user.photos_set.all()
            # 如果没有创建相册，返回空
            if not photos_all:
                return JsonResponse({'code': 200,'username':username,'data':[]})
            data = []
            for p in photos_all:
                d = {}

                d['photos_id'] = p.id
                d['photos_name'] = p.photos_name
                # 处理相册为空的情况
                if not p.photo_set.all():
                    d['photos_cover'] = None
                # 数据库对象IMage..字段，不是字符串，需要转化
                else:
                    d['photos_cover'] = str(p.photo_set.all()[0])
                data.append(d)
            print(photos_all)
            return JsonResponse({'code': 200,'username':username,'data':data})
        # 有参数
        else:
            # 返回相册所有图片
            # 处理相册没有创建的情况
            try:
                photos = Photos.objects.get(id=request.GET['photos_id'])
                print(photos,request.GET['photos_id'])
            except Exception as e:
                print(e)
                return JsonResponse({'code': 700102, 'error': 'please create photos'})
            # 返回相册所有的图片
            if 'photos_id' in request.GET and 'photo_id' not in request.GET:

                # 相册无图片,返回的数据类型
                if not photos.photo_set.all():
                    return JsonResponse({'code':200,'username':username,'photos_id':request.GET['photos_id'],'photos_name':photos.photos_name,'data':[]})
                # 有图片 组织数据
                data = []
                for p in photos.photo_set.all():
                    d = {}
                    d['photo_id'] = p.id
                    # Image类型，需要转化
                    d['photo_url'] = str(p.photo_url)
                    data.append(d)
                return JsonResponse({'code':200,'username':username,'photos_id':request.GET['photos_id'],'photos_name':photos.photos_name,'data':data})
            # 返回具体某张图片
            elif 'photos_id' in request.GET and 'photo_id' in request.GET:
                # 处理图片不存在的情况
                try:
                    photo_one = photos.photo_set.get(id=request.GET['photo_id'])
                except Exception as e:
                    print(e)
                    return JsonResponse({'code':700103,'error':'not the picture'})
                # 下一张
                next_id = None
                next_url = None
                next_photo = photos.photo_set.filter(id__gt=request.GET['photo_id'],photos=photos).first()
                print(photos.photo_set.filter(id__gt=request.GET['photo_id'],photos=photos).first())
                if next_photo:
                    next_id = next_photo.id
                    next_url = next_photo.photo_url
                # 上一张
                last_id = None
                last_url = None
                last_photo = next_photo = photos.photo_set.filter(id__lt=request.GET['photo_id'],photos=photos).last()
                if last_photo:
                    last_id = last_photo.id
                    last_url = last_photo.photo_url
                # 组织数据
                data = [
                    {'photo_id': photo_one.id, 'photo_url': 'http:xxxxxx'},
                    {'next_id':next_id , 'next_url':str(next_url) },
                    {'last_id':last_id , 'last_url':str(last_url)},
                ]
                return JsonResponse({ 'code': 200,
                                      'username':'abc',
                                      'photos_id':photos.id,
                                      'photos_name':photos.photos_name,
                                       'data': data,
                                    })
            else:
                return JsonResponse({'code':700105,'error':'please input the correct query'})
    # POST请求，创建资源
    if request.method == 'POST':
        # 获取post提交数据
        # 转化post数据为字典
        request_data = request.body.decode()
        # 如果数据为空，返回错误类型
        if not request_data:
            return JsonResponse({'code':700111,'error':'The submit data is empty'})
        request_data = json.loads(request_data)
        # 创建用户相册
        try:
            photos = Photos.objects.create(photos_name=request_data['photos_name'],user_id=username)
        except Exception as e:
            print(e)
            return JsonResponse({'code':700123,'error':'create failed'})
        return JsonResponse({'code':200,'username':username})
        # 创建用户相册
    # PUT请求，修改资源
    if request.method == 'PUT':
        # 获取put提交数据
        # 转化put数据为字典
        request_data = request.body.decode()
        # 如果数据为空，返回错误类型
        if not request_data:
            return JsonResponse({'code': 700111, 'error': 'The submit data is empty'})
        request_data = json.loads(request_data)
        photos_name = request_data['photos_name']
        photos_id = request_data['photos_id']
        # 创建失败返回的错误类型
        try:
            photos = Photos.objects.get(id=photos_id)
        except Exception as e:
            print(e)
            return JsonResponse({'code':700125,'error':'Change failed'})
        photos.photos_name = photos_name
        photos.save()
        return JsonResponse({'code': 200, 'data': 'Change success'})

    # DELETE请求，删除资源
    if request.method == 'DELETE':
        # 删除相册
        if 'photos_id' in request.GET and 'photo_id' not in request.GET:
            photos_id = request.GET['photos_id']

            # 查找失败返回的错误类型
            try:
                photos = Photos.objects.get(id=photos_id)
            except Exception as e:
                print(e)
                return JsonResponse({'code': 700125, 'error': 'Change failed'})
            photos.delete()
            return JsonResponse({'code': 200, 'data': 'Delete success'})
        # 删除具体某一张图片
        if 'photos_id' in request.GET and 'photo_id'  in request.GET:
            photo_id = request.GET['photo_id']
            # 查找失败返回的错误类型
            try:
                photo = Photo.objects.get(id=photo_id)
            except Exception as e:
                print(e)
                return JsonResponse({'code': 700125, 'error': 'Change failed'})
            photo.delete()
            return JsonResponse({'code': 200, 'data': 'Delete success'})


# 图片上传接口，单独使用一个视图，方便提取数据
@logging_check('POST')
def upload_view(request,username=None):
    # 只允许post方法
    if request.method != 'POST':
        data = {'code':'700160','error':'Please use method'}
        return JsonResponse(data)
    photos_id = request.GET['photos_id']
    photos = Photos.objects.get(id=photos_id)
    photo = Photo.objects.create(photos=photos)
    photo.photo_url = request.FILES['picture']
    photo.save()
    data = {'code': 200, 'username': username}
    return JsonResponse(data)










