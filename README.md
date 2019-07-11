## 关于这个网站  

这个网站采用的是：后端框架[flask](http://flask.pocoo.org/) + 前端框架[Bootstrap](https://getbootstrap.com/)。本来打算做一个自己的博客系统。初步写好网站之后却发现在国内搭建一个网站有点麻烦（阻力主要来自于备案）。于是就把这个网站开源出来，主要目的是让那些学习完[官方教程](http://flask.pocoo.org/docs/1.0/)之后想做出一点东西却无从下手的同学，那么这个网站就会给你一点点参考价值。  

这个网站目前实现的功能：  
1. 在线编辑发布文章；  
2. 编辑器markdown预览；  
3. 标签和分类管理;  
4. 主页个性化站长显示（主要是在网站导航栏上方有一个站长资料卡，下拉之后会被影藏掉）；   
5. 文章支持markdown排版；  
6. 文章管理功能（删除和编辑/存稿）；  
7. 登录功能（没有提供登录入口。需要在主页网址后添加`/login`的url后缀）；
8. 登录之后在导航栏下面有一个站长常用的工具栏（增加文章/文章管理/分类管理/注销）。  

## 如何安装这个网站？  

安装之前你得保证你的电脑已经安装python3版本。这里建议安装[anaconda](https://www.anaconda.com/),anaconda能够减少你很多配置成本。而编辑器我以vscode为例。  

### linux系统  

首先你得将这个网站clone到你电脑本地，然后进入`myweb`目录下：  
```
[busui@qing ~]$ git clone git@github.com:Busui/myweb.git
[busui@qing ~]$ cd myweb/
```

首先，安装pipenv(关于pipenv如何使用，如果你不会，强烈安利你去学一下)：    
```
[busui@qing myweb]$ pip install pipenv
```

pipenv安装完成之后，我们利用conda（集成在anaconda了）创建一个`python 3.6`版本的独立python环境，独立环境的好处是这个环境不会影响你本机的python环境，一般一个项目对应一个python环境：  
```
[busui@qing myweb]$ conda create -n "web" python=3.6
```
注意：`-n "web"`中的"web"是你创建的python环境的名称。你可以改为你喜欢的名称。  

（这步只是说明作用，你可以不配置）这时候你可以查看当前系统你的python环境有多少：  
```
[busui@qing myweb]$ conda env list
# conda environments:
#
web                      /home/busui/.conda/envs/web
base                  *  /opt/anaconda

```
注：对于anaconda而言，当前系统有两个python环境。一个是“web”，一个是“base”。“web”就是我们上一步创建的python环境。而"base"是anaconda自己创建的。“base”右边的“×”星号说明当前处于“base”环境中。 

创建完python3.6版本的环境之后，我们得激活环境：  
```
[busui@qing myweb]$ source activate web
(web) [busui@qing myweb]$ 
```

这时候你在终端输入python，就会发现python版本是3.6:  
```
(web) [busui@qing myweb]$ python
Python 3.6.8 |Anaconda, Inc.| (default, Dec 30 2018, 01:22:34) 
[GCC 7.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> exit()
```

退出python解释器之后，我们在命令行终端输入（注意，要在myweb/目录下）：  
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

`export PIPENV_VENV_IN_PROJECT=1`的作用是让pipenv在当前目录（即../myweb/）下创建`.venv`环境。