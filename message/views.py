import json

from django.http import JsonResponse
from django.shortcuts import render
from tools.logging_check import get_user_by_request
from message.models import *
# Create your views here.

def message_view(request,topic_id):
    # POST方法,只有用户可以发表
    if request.method == 'POST':
        # 留言者的姓名
        publiser_name = get_user_by_request(request)
        # 没有用户，返回错误类型
        if not publiser_name:
            return JsonResponse({'code': 40112, 'error': 'Please login'})
        publiser = UsersProfile.objects.get(username=publiser_name)
        # 留言的文章
        try:
            topic = Topic.objects.get(id=topic_id)
        except Exception as e:
            print(e)
            return JsonResponse({'code': 40115, 'error': 'The topic have been deleted'})
        # 接受数据
        request_data = request.body.decode()
        # 数据是空，返回错误类型
        if not request_data:
            return JsonResponse({'code':40116,'error':'The message is empty'})

        request_data = json.loads(request_data)

        content = request_data['content']
        # 留言父ID默认0
        parent_id = request_data.get('parent_id',0)
        print(parent_id)
        message = Message.objects.create(content=content,parent_message=parent_id,
                                         publisher=publiser,topic=topic)
        return JsonResponse({'code':200,'data':'{}'})

    if request.method == 'GET':
        messages = Message.objects.filter(topic_id=topic_id)
        messages_list = []
        for m in messages:
            d = {}
            d['id'] = m.id
            d['content'] = m.content
            d['parent_message'] = m.parent_message
            d['publiser'] = m.publisher.username
            d['topic'] = m.topic.id
            messages_list.append(d)
        return JsonResponse({'code':200,'data':messages_list})




