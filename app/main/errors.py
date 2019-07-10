from flask import render_template
from . import main


# 这里使用app_errorhandler是为了将错误函数注册到全局
# 如果只是使用errorhandler,那么只有main蓝图中的错误才能出发这个函数
@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@main.app_errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
