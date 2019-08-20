# ykblog
## 一个django+vue 的博客
>这里感谢github和前辈的指教

## 功能

<p align='center'>
<img src='https://ykblog.oss-cn-beijing.aliyuncs.com/img/博客.png' title='images' style='max-width:600px'></img>
</p>

## 在线地址
www.treequan.com

## 本地开发环境

>Ubuntu18.04 python3.6 django2.0.8(更高的可能Xadmin会出现问题)，
mysql 5.7  Redis 4.0.9 node v10.16.0

所以安装之前请务必安装相关环境，

## 1 克隆代码到本地

```git clone https://github.com/yktimes/ykblog.git```

## 2 前端环境

cd 到 front-end目录下 执行  ```npm install``` 安装依赖包
完成后 
```npm run dev ```
<p align='center'>
<img src='https://ykblog.oss-cn-beijing.aliyuncs.com/img/20190819224144.png' title='images' style='max-width:600px'></img>
</p>
说明成功了。

>这里注意一点在 front-end/src/components/Home.vue下 第235行
<p align='center'>
<img src='https://ykblog.oss-cn-beijing.aliyuncs.com/img/20190819225000.png' title='images' style='max-width:600px'></img>
</p>

>这个是上传图片的url，本机不需要改了。我给写死了。哎，后端萌新，前端布局各种组件是借鉴了github和前辈的帮助，感谢他们。

还有 front-end/src/http.js 
<p align='center'>
<img src='https://ykblog.oss-cn-beijing.aliyuncs.com/img/20190819225008.png' title='images' style='max-width:600px'></img>
</p>

这里也不需要改了

## 3 安装python包

>因为用到了Xadmin组件，但是直接从pip源下载可能会出错，所以

```pip3 install https://codeload.github.com/sshwsfc/xadmin/zip/django2```

安装成功后，再安装requirement.txt的依赖包

cd 到 ykblog/docs 执行
```pip3 install -r requirement.txt```

## 4 配置数据库

>先在你的数据库创建好一个实例。然后填好密码和数据库名
<p align='center'>
<img src='https://ykblog.oss-cn-beijing.aliyuncs.com/img/20190819225012.png' title='images' style='max-width:600px'></img>
</p>

再迁移

```python3 manage.py makemigrations```

```python3 manage.py migrate```

数据库配置成功
## 5 创建超级用户
>因为设置了权限，非管理员无法写博客

```python3 manage.py createsuperuser```

创建成功后接着下一步。

## 6 redis
<p align='center'>
<img src='https://ykblog.oss-cn-beijing.aliyuncs.com/img/20190819225017.png' title='images' style='max-width:600px'></img>
</p>

>我们这里用到了redis，请保证开启了服务

## 7 配置celery
<p align='center'>
<img src='https://ykblog.oss-cn-beijing.aliyuncs.com/img/20190819225021.png' title='images' style='max-width:600px'></img>
</p>

因为在群发私信(管理员才可以发送)用到了异步任务，本机不用修改，但是如果想使用此功能得开启命令

```pip3 install -U Celery```
如果没有安装就先安装下

然后开启  
```celery -A celery_tasks.main worker -l info```
<p align='center'>
<img src='https://ykblog.oss-cn-beijing.aliyuncs.com/img/20190819225026.png' title='images' style='max-width:600px'></img>
</p>
出现这样就成功了


## 8 Elasticsearch
<p align='center'>
<img src='https://ykblog.oss-cn-beijing.aliyuncs.com/img/20190819225035.png' title='images' style='max-width:600px'></img>
</p>

一个博客需要用到这个吗？主要还是自己学习来用，关于这个的安装请自己搜索文档，不安装也只是对搜索功能有影响

安装完成后记得

```python3 manage.py rebuild_index```

## 现在启动 manage.py
> 应该会出现画面了

<p align='center'>
<img src='https://ykblog.oss-cn-beijing.aliyuncs.com/img/20190819225041.png'
 title='images' style='max-width:600px'></img>
</p>



## 后台访问 .../xadmin/

<p align='center'>
<img src='https://ykblog.oss-cn-beijing.aliyuncs.com/img/20190819225047.png'
 title='images' style='max-width:600px'></img>
</p>


**这个博客也是学习实践的过程，其中还有许多不足，欢迎指教。**
