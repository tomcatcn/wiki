from django.db import models
from users.models import UsersProfile
# Create your models here.

# TODO:增加阅读数，点赞功能
class Topic(models.Model):
    title = models.CharField('文章标题',max_length=60)
    category = models.CharField('文章分类',max_length=20)
    limit = models.CharField('文章权限',max_length=10)
    introduce = models.CharField('文章简介',max_length=90)
    content = models.TextField('文章内容')
    created_time = models.DateTimeField('文章创建时间',auto_now_add=True)
    updated_time = models.DateTimeField('文章修改时间',auto_now=True)

    # 与用户表关联外建，一对多
    author = models.ForeignKey(UsersProfile)

    class Meta:
        db_table = 'topic'

    def __str__(self):
        return '<文章标题：{}>'.format(self.title)

