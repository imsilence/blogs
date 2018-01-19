#encoding: utf-8

# 导入Flask类
from flask import Flask
from flask import render_template
from flask import request

# 创建Flask实例
app = Flask(__name__)

# 定义路由, 由index函数处理url为/的GET请求
@app.route('/')
def index():
    # 返回响应内容
    return 'Hello, Silence' 



@app.route('/users/', methods=["GET", "POST"])
def users():
    if request.method == 'GET':
        return 'GET ID:%s' % request.args.get('id')
    else:
        return 'POST ID:%s' % request.form.get('id')

# 脚本运行执行代码
if __name__ == '__main__':
    # 启动Flask实例, 设置监听0.0.0.0:9001, 开启调试模式
    app.run(host='0.0.0.0', port=9001, debug=True)