## 关于这个网站  

这个网站的后端框架是[flask](http://flask.pocoo.org/)，前端框架是[Bootstrap](https://getbootstrap.com/)。  
本来打算做一个自己的博客系统。初步写好网站之后却发现在国内搭建一个网站有点麻烦（阻力主要来自于备案）。于是就把这个网站开源出来，主要目的是让那些学习完[官方教程](http://flask.pocoo.org/docs/1.0/)之后想做出一点东西却无从下手的同学，那么这个网站就会给你一点点参考价值。里面的代码都是十分简单的。  

### 如何阅读源码？  
建议先从数据库结构（及`models.py`文件）读起，然后是主`__init__.py`文件。之后再深入视图函数，最后看template模板。  


### 实现的功能：  

说实话本人喜欢简洁的风格，写这个网站的初衷就是写出一个符合个人趣味的风格。所以这个网站的风格主观性十分强烈。在阅读代码时如有不适，请立即关闭，即使止损。功能实现如下（还有一些没写出来你自己去挖掘）： 

1. 在线编辑发布文章；  
2. 编辑器markdown预览；  
3. 标签和分类管理;  
4. 主页个性化站长显示（主要是在网站导航栏上方有一个站长资料卡，下拉之后会被隐藏掉）；   
5. 文章支持markdown排版；  
6. 文章管理功能（删除和编辑/存稿）；  
7. 登录功能（没有提供登录入口。需要在主页网址后添加`/login`的url后缀）；
8. 登录之后在导航栏下面有一个站长常用的工具栏（增加文章/文章管理/分类管理/注销）。  


## 如何安装这个网站？  

安装之前你得保证你的电脑已经安装python3版本。这里建议安装[anaconda](https://www.anaconda.com/), anaconda能够减少你很多配置成本。  

把本网站clone下来，只需要在终端操作即可。如果需要修改代码，请自行选择你最爱的IDE/编辑器。  


### linux系统下如何配置：  

简单总结就是：先用conda创建一个环境（不创建也可以，在这里我就创建了，因为我不想搞乱"base"环境，"base"环境是conda的默认环境），然后进入conda创建的环境安装pipenv,再用pipenv创建一个独立的`venv`环境。然后激活pipenv创建的环境，设置对应的环境变量(比如FLASK_APP)。初始化数据库和用户。就可以了。  

当然，详细步骤也有，如下：  

#### 1.首先你得将这个网站clone到你电脑本地，然后进入`myweb`目录下：  
```
[busui@qing ~]$ git clone git@github.com:Busui/myweb.git
[busui@qing ~]$ cd myweb/
```


#### 2.然后，安装pipenv(关于pipenv如何使用，如果你不会，强烈安利你去学一下)：    
```
[busui@qing myweb]$ pip install pipenv
```


#### 3.pipenv安装完成之后，我们利用conda（集成在anaconda了）创建一个`python 3.6`版本的独立python环境，独立环境的好处是这个环境不会影响你本机其它版本的python环境，一般一个项目对应一个python环境：  
```
[busui@qing myweb]$ conda create -n "web" python=3.6
```
**注意**：`-n "web"`中的"web"是你创建的python环境的名称。你可以改为你喜欢的名称。  


#### 4.（**这步只是说明作用，你可以不配置**）这时候你可以查看当前系统你的python环境有多少：  
```
[busui@qing myweb]$ conda env list
# conda environments:
#
web                      /home/busui/.conda/envs/web
base                  *  /opt/anaconda
```
**注**：对于anaconda而言，当前系统有两个python环境。一个是“web”，一个是“base”。“web”就是我们上一步创建的python环境。而"base"是anaconda自己创建的。“base”右边的“*”星号说明当前处于“base”环境中。 


#### 5.创建完python3.6版本的环境之后，我们得激活环境：  
```
[busui@qing myweb]$ source activate web
(web) [busui@qing myweb]$ 
```


#### 6.这时候你在终端输入python，就会发现python版本是3.6:  
```
(web) [busui@qing myweb]$ python
Python 3.6.8 |Anaconda, Inc.| (default, Dec 30 2018, 01:22:34) 
[GCC 7.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> exit()
```


#### 7.退出python解释器之后，我们在命令行终端输入（注意，要在myweb/目录下）：  
```
(myweb) [busui@qing myweb]$ export PIPENV_VENV_IN_PROJECT=1
(web) [busui@qing myweb]$ pipenv install --dev
Creating a virtualenv for this project…
Pipfile: /home/busui/myweb/Pipfile
Using /home/busui/.conda/envs/web/bin/python3.6 (3.6.8) to create virtualenv…
⠼ Creating virtual environment...Already using interpreter /home/busui/.conda/envs/web/bin/python3.6
Using base prefix '/home/busui/.conda/envs/web'
New python executable in /home/busui/myweb/.venv/bin/python3.6
Also creating executable in /home/busui/myweb/.venv/bin/python
Installing setuptools, pip, wheel...
done.
Running virtualenv with interpreter /home/busui/.conda/envs/web/bin/python3.6

✔ Successfully created virtual environment! 
Virtualenv location: /home/busui/myweb/.venv
Installing dependencies from Pipfile.lock (411877)…
  🐍   ▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉ 28/28 — 00:00:09
To activate this project's virtualenv, run pipenv shell.
Alternatively, run a command inside the virtualenv with pipenv run.
```

**注**：`export PIPENV_VENV_IN_PROJECT=1`的作用是让pipenv在当前目录（即../myweb/）下创建`.venv`环境。  


#### 8.这时候，这个网站需要的环境你已经搭建好了。我们先进入pipenv的`venv`中，然后设置FLASK_APP环境变量，之后再初始化数据库：  
```
(web) [busui@qing myweb]$ pipenv shell
Launching subshell in virtual environment…
[busui@qing myweb]$  . /home/busui/myweb/.venv/bin/activate
(myweb) [busui@qing myweb]$ export FLASK_APP=myblog.py
(myweb) [busui@qing myweb]$ flask db upgrade
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> bfd8b06a3bbf, initalized
```


#### 9.到了这里，其实你已经可以启动网站了。但还差一个管理员账号。由于本网站没有实现注册函数，所以你只能到`flask shell`下面去注册一个用户（这里也很妙，用命令行来注册很有趣）：  
```
(myweb) [busui@qing myweb]$ flask shell
Python 3.6.8 |Anaconda, Inc.| (default, Dec 30 2018, 01:22:34) 
[GCC 7.3.0] on linux
App: app [production]
Instance: /home/busui/myweb/instance
>>> user = User(username="lovekernel", password="lovekernel", email="lovekernel@gmail.com")
>>> db.session.add(user)
>>> db.session.commit()
>>> exit()
```

#### 10.到了这一步，就是往事具备，只欠东风了。在终端上输入`flask run`：  
```
(myweb) [busui@qing myweb]$ flask run
 * Serving Flask app "myblog.py"
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```
这时候访问`http://127.0.0.1:5000/`就可以见到初始的网站状态了。（此时一切空空，但在里面你可以写一堆文章）。如下图：  
![](https://github.com/Busui/myweb/blob/master/READMEIMAGE/index.png)


访问`http://127.0.0.1:5000/login`就可以登录管理员账号。正确登入之后，你会在`navbar`导航栏下看到一个简单的管理员工具:  
![](https://github.com/Busui/myweb/blob/master/READMEIMAGE/index.gif)


## 关于配置  
这个网站的一部分配置我已经统一放在了config.py文件：  
```
# 作者签名
AUTHOR_MOTTO = os.environ.get('AUTHOR_MOTTO') or "为天地立心，为生民立命，为往圣继绝学，为万世开太平"
# 网站brand
MYWEB_BRAND = os.environ.get('MYWEB_BRAND') or "Codepool"
# 站长昵称
FLASK_ADMIN = os.environ.get('FLASK_ADMIN') or "Lovekernel"
```
在template文件内调用格式是：`{{ config['AUTHOR_MOTTO'] }}`(以作者签名为例子)。剩下的微博微信链接也可以用同样的办法实现。  



除此之外，如果你按照上面的方法配置下来，那么你可以把环境变量统一写在`.env`文件里，我的文件内容是这样：  
```
FLASK_APP=myblog.py // 这句写下之后，你就不用每次都要重新set/export FLASK_APP环境变量了
FLASK_ENV=production
FLASK_CONFIG=development
SECRET_KEY=换成你自己的密钥。
SQLALCHEMY_TRACK_MODIFICATIONS=False
FLASK_ADMIN_NAME=lovekernel
FLASKY_POSTS_PER_PAGE=10
```


## License  
[GNU General Public License v3.0](https://github.com/Busui/myweb/blob/master/LICENSE)

