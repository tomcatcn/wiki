#技术文档收集平台

## 目录
[TOC]

## 一、概述
&emsp;&emsp;&emsp;&emsp;随着技术的不断学习,不断总结，不断地书写技术文档，会发现

文档的收集与归纳越来越麻烦，查找起来也是很不方便，所有为了解决这个情况

特地打造了这个文档收集平台，方便大家收集文档，分享，评论等等。

总体框架采用前后端分离，后端只负责数据的处理，前端负责渲染页面与用户交互。

后端负责处理的项目模块设计如下
模块|功能|API
-|-|
用户模块|负责处理用户数据|users
文章模块|负责处理文章数据|topic

留言模块|负责处理留言数据|
评论模块|负责处理评论数据|

## 二、开发规范
1. 后端环境

Python 3.6.9 + django 1.11.8 + mysql 5.7.28 + Ubuntu18.04.3 LTS + vim
2. 通信协议

http
3. 通信格式

json
4. API规范

一定成都上符合RESTful定义

## 三、使用技术
### 3.1 token

### 3.2 CORS

## 四、用户模块
### 4.1 数据库结构
```python
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

    class Meta:
        db_table = 'user_profile'

    def __str__(self):
        return '<用户:>'.format(self.username)
```
### 4.2 API
#### 4.2.1 注册接口
- URL:http://127.0.0.1:8000/api/v1/users
- 请求方式 POST
- 请求格式 json 
>{‘username’: jack, ‘email’: ‘abc@qq.com’, ‘password1’: ‘abcdef’,‘password2’: ‘abcdef’}
- 响应格式
>{‘code’: 200 , ‘username’: ‘abc’, ’data’: {‘token’:‘asdadasd.cvreijvd.dasdadad’} }
- 异常码
>异常码|含义|备注
-----|----|----
100101|无用户名|xxxx
100102|两次输入密码不一致|xxxx

#### 4.2.2 获取用户信息接口
- URL:http://127.0.0.1:8000/api/v1/users/<username>
- 请求方式 GET
- 请求格式  
> 直接 GET 请求，可获取全部用户数据

> GET 请求后添加查询字符串，可根据具体查询字符串 查询：http://127.0.0.1:8000/v1/users/<username>?nickname=1
- 响应格式
> 全量响应： {‘code’:200,‘username’:’xiaoming’,‘data’:{‘nickname’:’abc’, ’sign’:’hellow’, ‘avatar’: ’abc.jpg’, ‘info’: ‘hahahahah’}}

> 局部响应：{‘code’:200, ‘username’:’123’, ‘data’:{‘nickname’:’abcde’} }
- 异常码
>异常码|含义|备注
-----|----|----
100101|无用户名|xxxx

#### 4.2.3 修改个人用户接口
- URL:http://127.0.0.1:8000/api/v1/users/<username>
- 请求方式 PUT
- 请求格式 json
>  该请求需客户端在 HTTP header 里添加 token, 格式如：Authorization ： token

> {‘sign’:xxx, ‘info’:xxxx, ‘nickname’:xxxx}
- 响应格式 json
>{‘code’:200, ‘username’:’char’}
- 异常码
>异常码|含义|备注
-----|----|----
100103|空提交|xxxx


#### 4.2.4 上传用户头像接口
- URL:http://127.0.0.1:8000/api/v1/users/<username>/avatar
- 请求方式 POST multipart/form-data
- 请求格式 json 
>  该请求需客户端在 HTTP header 里添加 token, 格式如：Authorization ： token

> {‘avatar’:表单中图片的名字}
- 响应格式
>{‘code’:200, ‘username’:’char’}
- 异常码
>异常码|含义|备注
-----|----|----
100103|空提交|xxxx


#### 4.2.5 登录接口
- URL:http://127.0.0.1:8000/api/v1/tokens
- 请求方式 POST 
- 请求格式 json 
> {‘username’: ‘xxx’, ‘password’: ‘yyy’}
- 响应格式
>{‘code’: 200, ‘username’: ‘asc’, ‘data’: {‘token’: ‘zdsadasd’}}
- 异常码
>异常码|含义|备注
-----|----|----
100103|空提交|xxxx

#### 4.2.6 注意问题
1. 注意个别客户端请求需要添加 token 传回服务器端，否则异
常
2. 如何保证同时只有一个客户端使用
>1.在用户表中添加字段logtime DatetimeField

>2.用户登录时候，把logtime字段更新为登录时间，生成token时候，私有声明里添加logtime

>3.用户再另一个客户端登录时候，检查token中的logtime是否与用户表的一致，

>>如果不相等，则返回用户重新登录，更新用户表登录时间，签发新的token。

      
      
## 五、文章模块
### 5.1数据结构
### 5.2 API

#### 5.2.1 发表文章接口
- URL:http://127.0.0.1:8000/api/v1/topics/<username>
- 请求方式 POST 
- 请求格式 json
>该请求需客户端在 HTTP header 里添加 token, 格式如：Authorization ： token 

> {‘title: ‘haha’, ‘category’: ‘tec’, ‘limit’: ‘public’, ‘content’: ‘abcdef<p>’ ,‘content_text’: ‘abcdef’}
- 响应格式
>{‘code’: 200 , ‘username’: ‘abc’, }
- 异常码
>异常码|含义|备注
-----|----|----
300101|未登录|xxxx

#### 5.2.2 获取用户文章列表接口
- URL:http://127.0.0.1:8000/api/v1/topics/<username>?category=[tec|no-tec]
- 请求方式 GET 
- 请求格式 
>http://127.0.0.1:8000/api/v1/topics/<username> 可获取用户全量数据

> http://127.0.0.1:8000/v1/topics/<username>?category=[tec|no-tec]可获取用户具体分类的数据， 技术(tec) 或 非技术 (no-tec)
- 响应格式
```json
{‘code’:200,’data’:{‘nickname’:’abc’, ’topics’:[{‘id’:1,’title’:’a’,‘category’: ‘tec’, ‘created_time’: ‘2018-09-03 10:30:20’, ‘introduce’:‘aaa’, ‘nickname’:’abc’}]}}
```
- 异常码
>异常码|含义|备注
-----|----|----
300101|未登录|xxxx

#### 5.2.3 获取用户具体文章内容接口
- URL:http://127.0.0.1:8000/api/v1/topics/<username>?t_id=1111
- 请求方式 GET 
- 请求格式 
> http://127.0.0.1:8000/api/v1/topics/<username> 地址后方添加查询字符串 t_id , 值为具体博客文章的 id

- 响应格式
```json
{ "code": 200, 
"data": {
     "nickname": "guoxiaonao",
     "title": "我的第一次", 
    "category": "tec", 
    "created_time": "2019-06-03", 
    "content": "<p>我的第一次，哈哈哈哈哈<br></p>", 
    "introduce": "我的第一次，哈哈哈哈哈", 
    "author": "guoxiaonao", "next_id": 2, 
    "next_title": "我的第二次", 
    "last_id": null, 
    "last_title": null, 
    "messages": [
        {"id": 1, "content": "<p>写得不错啊，大哥<br></p>", "publisher": "guoxiaonao", 
        "publisher_avatar": "avatar/头像 2.png", 
        "reply": [
            { "publisher": "guoxiaonao", 
            "publisher_avatar": "avatar/头像 2.png", 
            "created_time": "2019-06-03 07:52:16", 
            "content": "谢谢您的赏识", 
            "msg_id": 2
             }
                ],
         "created_time": "2019-06-03 07:52:02"
        }
    ],
    "messages_count": 2
   }
}
```
- 异常码
>异常码|含义|备注
-----|----|----
300106|无文章|xxxx

#### 5.2.4 删除文章接口
- URL:- URL:http://127.0.0.1:8000/api/v1/topics/<username>?t_id=1111
- 请求方式 DELETE 
- 请求格式 
>该请求需客户端在 HTTP header 里添加 token, 格式如：Authorization ： token 

>http://127.0.0.1:8000/v1/topcis/<username> 地址后方添加查询字符串 t_id , 值为具体博客文章的 id
- 响应格式
>{‘code’: 200 , ‘username’: ‘abc’, }
- 异常码
>异常码|含义|备注
-----|----|----
300107|文章不存在|xxxx

#### 5.2.5 常见问题
1. 注意个别客户端请求需要添加 token 传回服务器端，否则异常

## 六、留言模块
### 6.1数据结构

#### 6.2.1 发表文章留言接口
- URL:- URL:http://127.0.0.1:8000/api/v1/messages/<topic_id>
- 请求方式 POST
- 请求格式 json
```json
{‘content’:'asdfgc',’parent_id’:1}
```
- 响应格式
>{‘code’: 200 , ‘data’: ‘{}’, }
- 异常码
>异常码|含义|备注
-----|----|----
400107|留言为空|xxxx






