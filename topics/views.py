import json

from django.db.models import Q
from django.shortcuts import render
from django.http import JsonResponse
from users.models import UsersProfile
from topics.models import *
from tools.logging_check import get_user_by_request
# Create your views here.

# 组织回复数据
def organize_message(topic):
    list_data =[]
    messages = topic.message_set.all()
    for message in messages:
        d = {}
        d['id'] = message.id
        d['content'] = message.content
        d['publisher'] = message.publisher.username
        d['publisher_avatar'] = str(message.publisher.avatar)
        d['reply'] = []
        d['created_time'] = message.created_time.strftime('%y-%m-%d %H:%M:%S')
        list_data.append(d)

    return list_data,len(messages)


def topics_view(request,username=None):
    if request.method == 'GET':
        # 获取用户文章列表
        # /api/v1/tom?category=tec|no-tec - tom 的技术文章和非技术
        author = UsersProfile.objects.get(username=username)
        visitor_username = get_user_by_request(request)
        # 规避大小写问题
        visitor_username = visitor_username.lower()
        username = username.lower()
        if not author:
            data = {'code': 30104, 'error': 'The author is not existed'}
            return JsonResponse(data)
        # 有查询字符串
        if request.GET.keys():
            # 返回技术，非技术类型文章
            if 'category' in request.GET.keys():
                if 'tec' == request.GET['category']:
                    # 访问者是作者
                    if username == visitor_username:
                        topics = author.topic_set.filter(category='tec')
                        topics_list = []
                        # 组织数据
                        for topic in topics:
                            d = {}
                            d['id'] = topic.id
                            d['title'] = topic.title
                            d['category'] = topic.category
                            # 把datetime类型转化为字符串
                            d['created_time'] = topic.created_time.strftime('%Y-%m-%d %H:%M:%S')
                            d['introduce'] = topic.introduce
                            d['author'] = author.nickname
                            topics_list.append(d)
                        data = {'code': '200', 'data': {'nickname': author.nickname, 'topics': topics_list}}
                        return JsonResponse(data)
                    else:
                        # 是游客
                        topics = author.topic_set.filter(category='tec',limit='public')
                        topics_list = []
                        # 组织数据
                        for topic in topics:
                            d = {}
                            d['id'] = topic.id
                            d['title'] = topic.title
                            d['category'] = topic.category
                            # 把datetime类型转化为字符串
                            d['created_time'] = topic.created_time.strftime('%Y-%m-%d %H:%M:%S')
                            d['introduce'] = topic.introduce
                            d['author'] = author.nickname
                            topics_list.append(d)
                        data = {'code': '200', 'data': {'nickname': author.nickname, 'topics': topics_list}}
                        return JsonResponse(data)
                if 'no-tec' == request.GET['category']:
                    # 是作者
                    if username == visitor_username:
                        topics = author.topic_set.filter(category='no-tec')
                        topics_list = []
                        # 组织数据
                        for topic in topics:
                            d = {}
                            d['id'] = topic.id
                            d['title'] = topic.title
                            d['category'] = topic.category
                            # 把datetime类型转化为字符串
                            d['created_time'] = topic.created_time.strftime('%Y-%m-%d %H:%M:%S')
                            d['introduce'] = topic.introduce
                            d['author'] = author.nickname
                            topics_list.append(d)
                        data = {'code': '200', 'data': {'nickname': author.nickname, 'topics': topics_list}}
                        return JsonResponse(data)
                    # 是游客
                    else:
                        topics = author.topic_set.filter(category='no-tec',limit='public')
                        topics_list = []
                        # 组织数据
                        for topic in topics:
                            d = {}
                            d['id'] = topic.id
                            d['title'] = topic.title
                            d['category'] = topic.category
                            # 把datetime类型转化为字符串
                            d['created_time'] = topic.created_time.strftime('%Y-%m-%d %H:%M:%S')
                            d['introduce'] = topic.introduce
                            d['author'] = author.nickname
                            topics_list.append(d)
                        data = {'code': '200', 'data': {'nickname': author.nickname, 'topics': topics_list}}
                        return JsonResponse(data)
                else:
                    return JsonResponse({'code':'30111','error':'The query_str is wrong,not the data'})
            # 返回具体文章的内容
            if 't_id' in request.GET.keys():
                t_id = request.GET['t_id']
                # 记得要把他t_id转化为数字，因为数据库中主键是int类型
                t_id = int(t_id)
                # 是作者，可以返回所有自己文章里选择
                if visitor_username == username:

                    topics = Topic.objects.filter(id=t_id,author_id=username)
                    topic = topics[0]
                    # 组织数据
                    # 下一篇文章
                    next_id = None
                    next_title = None
                    next_topic = Topic.objects.filter(id__gt=t_id,author_id=username).last()
                    if next_topic:
                        next_id = next_topic.id
                        next_title = next_topic.title
                    # 上一篇文章
                    last_id = None
                    last_title = None
                    last_topic = Topic.objects.filter(id__lt=t_id,author_id=username).first()

                    if last_topic:
                        last_id = last_topic.id
                        last_title = last_topic.title
                    message_data,message_count = organize_message(topic)
                    print(message_data)
                    topic_data = {
                        'nickname':topic.author.nickname,
                        'title':topic.title,
                        'category':topic.category,
                        'created_time':topic.created_time.strftime('%Y-%m-%d %H:%M:%S'),
                        'content':topic.content,
                        'introduce':topic.introduce,
                        'author':topic.author.nickname,
                        'next_id':next_id,
                        'next_title':next_title,
                        'last_id':last_id,
                        'last_title':last_title,
                        'messages':message_data,
                        'messages_count':message_count,
                    }
                    return JsonResponse({'code':200,'data':topic_data})
                # 游客，从共有权限类文章里选择文章
                else:
                    topics = Topic.objects.filter(id=t_id, author_id=username,limit='public')

                    topic = topics[0]
                    # 组织数据
                    # 下一篇文章
                    next_id = None
                    next_title = None
                    next_topic = Topic.objects.filter(id__gt=t_id, author_id=username,limit='public').last()
                    if next_topic:
                        next_id = next_topic.id
                        next_title = next_topic.title
                    # 上一篇文章
                    last_id = None
                    last_title = None
                    last_topic = Topic.objects.filter(id__lt=t_id, author_id=username,limit='public').first()

                    if last_topic:
                        last_id = last_topic.id
                        last_title = last_topic.title
                    topic_data = {
                        'nickname': topic.author.nickname,
                        'title': topic.title,
                        'category': topic.category,
                        'created_time': topic.created_time.strftime('%Y-%m-%d %H:%M:%S'),
                        'content': topic.content,
                        'introduce': topic.introduce,
                        'author': topic.author.nickname,
                        'next_id': next_id,
                        'next_title': next_title,
                        'last_id': last_id,
                        'last_title': last_title,
                        'message': [],
                        'messages_count': 0,
                    }
                    return JsonResponse({'code': 200, 'data': topic_data})
        # 无查询字符串
        else:

            # /api/v1/tom - tom 的所有文章
            # author = UsersProfile.objects.get(username=username)
            # if not author:
            #     data = {'code': 30104, 'error': 'The author is not existed'}
            #     return JsonResponse(data)
            # 1.访问当文章的访问者 visitor


            # 2.当前访问文章的作者 author
            if username == visitor_username:
                topics = author.topic_set.all()
                print(topics)
                topics_list = []
                # 组织数据
                for topic in topics:
                    d = {}
                    d['id'] = topic.id
                    d['title'] = topic.title
                    d['category'] = topic.category
                    d['created_time'] =  topic.created_time
                    d['introduce'] = topic.introduce
                    d['author'] = author.nickname
                    topics_list.append(d)
                data = {'code':'200','data':{'nickname':author.nickname,'topics':topics_list}}
                return JsonResponse(data)
            # 游客返回的文章
            else:
                topics = author.topic_set.filter(limit='public')
                topics_list = []
                # 组织数据
                for topic in topics:
                    d = {}
                    d['id'] = topic.id
                    d['title'] = topic.title
                    d['category'] = topic.category
                    d['created_time'] = topic.created_time.strftime('%Y-%m-%d %H:%M:%S')
                    d['introduce'] = topic.introduce
                    d['author'] = author.nickname
                    topics_list.append(d)
                data = {'code': '200', 'data': {'nickname': author.nickname, 'topics': topics_list}}
                return JsonResponse(data)

    if request.method == 'POST':
        # 转化post数据为字典
        request_data = request.body.decode()
        request_data = json.loads(request_data)

        # 查找作者也就是用户
        user = UsersProfile.objects.get(username=username)
        title = request_data['title']
        # 注意xss攻击，将用户的输入进行转义
        import html
        title = html.escape(title)
        category = request_data['category']
        category = html.escape(category)
        limit = request_data['limit']
        limit = html.escape(limit)
        content = request_data['content']
        introduce = request_data['content_text'][:30]
        topic = Topic.objects.create(
            title=title,
            category=category,
            content = content,
            introduce = introduce,
            author = user,
            limit = limit,
        )



        return JsonResponse({'code':200,'error':'test'})

    if request.method == 'DELETE':
        topic_id = request.GET['topic_id']
        if not topic_id:
            return JsonResponse({'code':30112,'error':'Not the query_str'})
        print(topic_id)
        try:
            topic = Topic.objects.get(id=topic_id)
            topic.delete()

        except Exception as e:
            print(e)
            return JsonResponse({'code':30109,'erroe':'Delete failed,try again'})
        return JsonResponse({'code':200,'username':username})

