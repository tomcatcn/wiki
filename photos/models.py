from django.db import models
from users.models import UsersProfile

# Create your models here.

#相册类
class Photos(models.Model):
    photos_name = models.CharField('相册名称',max_length=30)
    # TODO:添加修改相册封面功能
    # photos_cover = models.ImageField('相册封面',upload_to='photo')

    # 外建与用户关联一对多，级联关系关联表删除，从表也删除
    user = models.ForeignKey(UsersProfile,on_delete=models.CASCADE)

    class Meta:
        db_table = 'photos'

    def __str__(self):
        return '<相册名称：{}>'.format(self.photos_name)

#图片类
class Photo(models.Model):
    photo_url = models.ImageField('图片名称',upload_to='photo')

    # 外建关联相册表，级联关系，主删从删
    photos = models.ForeignKey(Photos,on_delete=models.CASCADE)

    class Meta:
        db_table = 'photo'

    def __str__(self):
        return '{}'.format(self.photo_url)


