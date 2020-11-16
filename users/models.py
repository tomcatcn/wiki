from django.db import models
import random
# Create your models here.
def default_sign():
    signs = ['我爱中国','我是最帅的','我是沙雕,我快乐']
    return random.choice(signs)

class UsersProfile(models.Model):
    username = models.CharField('用户名',max_length=30,primary_key=True)
    nickname = models.CharField('昵称',max_length=50)
    email = models.EmailField('邮箱')
    password = models.CharField('密码',max_length=32)
    sign = models.CharField('个人签名',max_length=50,default=default_sign)
    info = models.CharField('个人描述',max_length=150)
    # avatar = models.ImageField('头像',upload_to='')
    created_time = models.DateTimeField('创建时间',auto_now_add=True)
    updated_time = models.DateTimeField('修改时间',auto_now=True)
    isActived = models.BooleanField('激活',default=True)
    # upload_to 指定位置存储位置 MEDIA_ROOT + upload_to 的值
    avatar = models.ImageField('头像',upload_to='avatar',default='')
    # 测试字段
    score = models.IntegerField('分数',null=True,default=0)

    class Meta:
        db_table = 'user_profile'

    def __str__(self):
        return '<用户:{}>'.format(self.username)

