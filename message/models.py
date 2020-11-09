from django.db import models
from users.models import UsersProfile
from topics.models import Topic
# Create your models here.

class Message(models.Model):
    content = models.CharField('留言内容',max_length=100)
    created_time = models.DateTimeField('留言创建时间',auto_now_add=True)
    parent_message = models.IntegerField('留言父ID',default=0)
    # 外建关联用户
    publisher = models.ForeignKey(UsersProfile)
    # 外建关联文章
    topic = models.ForeignKey(Topic)

    class Meta:
        db_table = 'message'

    def __str__(self):
        return '<留言：{}>'.format(self.content)
