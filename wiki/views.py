from django.http import JsonResponse
from users.models import UsersProfile
import redis
def test(request):
    # r = redis.Redis(host='127.0.0.1',port=6379,db=0)
    # while True:
    #     try:
    #         with r.lock('hhhhh',blocking_timeout=3) as lock:
    #             # 对score字段加1操作
    #             u = UsersProfile.objects.get(username='xiao')
    #             u.score += 1
    #             u.save()
    #         break
    #     except Exception as e:
    #         print('lock failed')
    u = UsersProfile.objects.get(username='xiao')
    u.score += 1
    u.save()

    return JsonResponse({'code':200,'data':{}})