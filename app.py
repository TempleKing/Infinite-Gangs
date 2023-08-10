from flask import Flask
from flask import render_template
from flask import request #get请求
from flask import redirect#重定向
import util
import os
import uuid
from flask_socketio import SocketIO, join_room, leave_room, emit
from tkinter import *
import json
import re
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app, cookie=None)
# 存储房间和用户信息的字典
rooms = {}
@app.route('/')
def hello_world():
    return render_template("login_page.html")

@app.route("/check_login" , methods=["post","get"])#登录
def check_login():
    # 验证登录
    global stu_id
    stu_id = request.values.get("stu_id")  #html的name属性
    password = request.values.get("password")
    print(f"Stu_id:{stu_id},Password:{password}")#字符串格式
    #查询mysql数据库，验证user表中的用户名和密码
    result = util.find_all()
    global username
    username = util.get_username(stu_id)
    print(username)

    print(result)

    for user in result:
        if stu_id == "" or password == "":
            # 弹出提示框并转到另一个页面
            message = "输入不能为空"
            script = "<script>alert('{}');window.location.href='/';</script>".format(message)
            return script

        if stu_id == str(user[1]) and password == str(user[2]):
            # 登录成功时，重定向到新页面
            return redirect("/homepage")

    else:
        # 用户名或密码错误，弹出提示框并转到另一个页面
        message = "用户名或密码不存在，请核实！"
        script = "<script>alert('{}');window.location.href='/';</script>".format(message)
        return script


@app.route("/register" , methods=["post","get"])#注册页面
def register():
    return render_template("register_page.html")


@app.route("/check_register" , methods=["post","get"])#注册操作
def check_register():
    stu_id = request.values.get("stu_id")
    password = request.values.get("password")
    username = request.values.get("username")
    email = request.values.get("email")

    print(f"stu_info:{stu_id},Password{password},Username{username},email{email}")


    result = util.find_all()

    for user in result:
        if stu_id =="" or  password =="" or username =="" or email == "":
            message = "输入不能为空"
            script = "<script>alert('{}');window.location.href='/register';</script>".format(message)
            return script
        if stu_id == str(user[1]):
            message = "该学号已存在"
            script = "<script>alert('{}');window.location.href='/register';</script>".format(message)
            return script

    else:
        util.insert_info(stu_id, password, username, email)
        return render_template("login_page.html")  # 注册成功后跳转到登录页面



@app.route("/VolInfo" , methods=["post","get"])#志愿者
def VolInfo():
    name = request.form['name']
    phone_number = request.form['number']
    result=util.VolInfo(name,phone_number,stu_id)
    print(result)
    return render_template("home.html", result=result)
@app.route("/SubmitMessage" , methods=["post","get"])#留言
def SubmitMessage():
    content = request.form['message']
    LMC=util.SubmitMessage(stu_id, content)
    print(LMC)
    return render_template("home.html", LMC=LMC)
@app.route("/homepage" , methods=["post","get"])
def homepage():
    return render_template("home.html")
@app.route("/Vol_page" , methods=["post","get"])
def Vol_page():
    result=util.check_Volinfo(stu_id)
    if result == 1:
        order_info = util.find_spec_order_info()
        print(order_info)
        orderData=util.find_all_order()
        # 对订单数据进行处理
        dateCounts = {}

        for order in orderData:
            orderTime = order[0]
            day = orderTime.strftime('%Y-%m-%d')
            hour = orderTime.hour

            # 组合日期和小时，作为字典的键
            dateTime = f"{day} {hour}"

            # 如果该日期和小时还没有在dateCounts中创建对应的键，则创建一个初始值为0的键值对
            if dateTime not in dateCounts:
                dateCounts[dateTime] = 0

            # 将该日期和小时的订单数量加1
            dateCounts[dateTime] += 1

        # 将数据转换为前端所需的格式
        xAxisData = list(dateCounts.keys())  # 横坐标数据，即日期和小时的组合
        seriesData = list(dateCounts.values())  # 柱状图数据，即每个日期和小时的订单数量

        # 将数据转换为JSON格式，并打印输出
        data = {'xAxisData': xAxisData, 'seriesData': seriesData}
        json_data = json.dumps(data)
        print(json_data)
        return render_template("Vol.html", order_info=order_info, json_data=json_data)
    else:
        message="你还不是志愿者"
        return render_template("home.html",message=message)
@app.route("/Get_order" , methods=["post","get"])
def Get_order():
    seq=request.args.get('row_id')
    print(seq)
    message = util.Get_order(seq)
    order_info = util.find_spec_order_info()
    orderData = util.find_all_order()
    # 对订单数据进行处理
    dateCounts = {}

    for order in orderData:
        orderTime = order[0]
        day = orderTime.strftime('%Y-%m-%d')
        hour = orderTime.hour

        # 组合日期和小时，作为字典的键
        dateTime = f"{day} {hour}"

        # 如果该日期和小时还没有在dateCounts中创建对应的键，则创建一个初始值为0的键值对
        if dateTime not in dateCounts:
            dateCounts[dateTime] = 0

        # 将该日期和小时的订单数量加1
        dateCounts[dateTime] += 1

    # 将数据转换为前端所需的格式
    xAxisData = list(dateCounts.keys())  # 横坐标数据，即日期和小时的组合
    seriesData = list(dateCounts.values())  # 柱状图数据，即每个日期和小时的订单数量

    # 将数据转换为JSON格式，并打印输出
    data = {'xAxisData': xAxisData, 'seriesData': seriesData}
    json_data = json.dumps(data)
    print(json_data)
    return render_template("Vol.html", order_info=order_info,message=message, json_data=json_data)
'''
@app.route("/register" , methods=["post","get"])
def register_page():
    return render_template("register_page.html")
'''
@app.route("/register_page", methods=["GET", "POST"])
def register_page():
    return render_template("register_page.html")
@app.route("/home_page", methods=["GET", "POST"])
def home_page():
    return render_template("home.html")
@app.route("/login_page", methods=["GET", "POST"])
def login_page():
    return render_template("login_page.html")
@app.route("/bookcar_page", methods=["GET", "POST"])
def bookcar_page():
    return render_template("bookcar.html")
@app.route("/help_page", methods=["GET", "POST"])
def help_page():
    items = util.get_all_items()
    lost_items = util.get_all_lost_items()
    return render_template("help.html", items=items, lost_items=lost_items, username=username)
@app.route("/user_page", methods=["GET", "POST"])
def user_page():
    return render_template("user.html")
@app.route("/nevigate_page", methods=["GET", "POST"])
def nevigate_page():
    return render_template("nevigate.html")
@app.route("/getInfoContent", methods=["GET", "POST"])
def getInfoContent():
    order=util.getInfoContent(stu_id, vcode, start, end)
    return render_template("home.html", order=order)
graph = {
    '西门': {'敏行楼': 130, '博纳楼': 145,'恭温楼':200},
    '敏行楼': {'西门': 130, '琢玉讲堂': 80, '博远楼':135, '博学楼':250,'文化中心':300,'二食堂':220},
    '博纳楼': {'西门': 145, '琢玉讲堂': 80, '博远楼':150, '南门':345},
    '琢玉讲堂': {'敏行楼': 80, '博纳楼': 80},
    '博远楼': {'敏行楼':135, '博纳楼': 150, '体育馆':335},
    '博学楼': {'敏行楼':250, '三食堂':215,'3，4号公寓':230,'文化中心':185},
    '三食堂': {'博学楼':215, '体育馆':215,'7号公寓':172},
    '体育馆': {'博远楼':335, '三食堂':215, '南门':85},
    '南门': {'体育馆':85, '博纳楼':345},
    '北门': {'诚明楼':140, '慎思楼':150,'经贸广场':135},
    '诚明楼': {'北门':140},
    '慎思楼': {'北门':150, '笃行楼':45, '乒羽馆':160},
    '乒羽馆': {'慎思楼':160},
    '经贸广场': {'行知楼':110, '笃行楼':140, '图书馆':60, '北门':135},
    '行知楼': {'经贸广场':110},
    '笃行楼': {'青春广场':105, '慎思楼':45, '经贸广场':140},
    '6号公寓': {'图书馆':220},
    '图书馆': {'青春广场':60,'经贸广场':60,'6号公寓':220,'文化中心':170},
    '青春广场': {'笃行楼':105,'3，4号公寓':140,'澡堂':140,'图书馆':60},
    '二食堂': {'文化中心':195},
    '文化中心': {'二食堂':192,'敏行楼':300,'3，4号公寓':133,'博学楼':185,'图书馆':170},
    '3，4号公寓': {'青春广场':140,'澡堂':120 ,'文化中心':133,'博学楼':230,'7号公寓':105},
    '澡堂': {'青春广场':140, '3，4号公寓':120},
    '7号公寓': {'3，4号公寓':105, '三食堂':172,'赛欧公寓':270},
    '恭温楼': {'西门':200},
    '赛欧公寓':{'7号公寓':270}
}
@app.route('/process_form.py', methods=['POST'])
def process_form():
    cabinet = util.initialize_cabinet()
    global start
    global end
    start = request.form['start']
    end = request.form['end']
    result = util.shortest_path(graph,start, end)
    cnum = util.generate_random_number()
    global vcode
    order = util.insert_cell(cabinet,cnum)
    vcode = order[5:9]
    return render_template('/nevigate.html', start=start, end=end, result=result, order=order)
    print(result)
    print(order)
@app.route('/DelInfoContent', methods=['POST'])
def DelInfoContent():
    vcode = request.form['vcode']
    message=util.DelInfoContent(vcode)
    return render_template("bookcar.html", message=message)
@app.route('/find_order_info/', methods=["GET", "POST"])
def find_order_info():
    print(stu_id)
    result = util.find_order_info(stu_id)
    print(result)
    return render_template('/order_info.html',  result=result)
@app.route('/upload_item', methods=['POST'])
def upload_item():
    # Retrieve item details from the form
    name = request.form['name']
    info = request.form['info']
    image = request.files['image']  # Assumes the input file field has the name "image"

    # 使用UUID生成一个唯一的文件名
    unique_filename = str(uuid.uuid4())
    image_filename = f"{unique_filename}.jpg"

    # Save the image to a folder or process it as needed
    image_path = os.path.join('static/assets/images', image_filename)
    image_path = image_path.replace('\\', '/')
    image.save(image_path)


    message=util.upload_item(name, info, image_path)
    items = util.get_all_items()
    lost_items = util.get_all_lost_items()
    return render_template("help.html", items=items,lost_items=lost_items,message=message, username=username)
@app.route('/upload_lost_item', methods=['POST'])
def upload_lost_item():
    # Retrieve item details from the form
    name = request.form['name']
    info = request.form['info']
    image = request.files['image']  # Assumes the input file field has the name "image"

    # 使用UUID生成一个唯一的文件名
    unique_filename = str(uuid.uuid4())
    image_filename = f"{unique_filename}.jpg"

    # Save the image to a folder or process it as needed
    image_path = os.path.join('static/assets/images', image_filename)
    image_path = image_path.replace('\\', '/')
    image.save(image_path)


    message=util.upload_lost_item(name, info, image_path)
    items = util.get_all_items()
    lost_items = util.get_all_lost_items()
    return render_template("help.html", items=items,lost_items=lost_items,message=message, username=username)
# 聊天界面路由
@app.route('/chat_page/<item_id>', methods=['GET', 'POST'])
def chat_page(item_id):
    username = request.args.get('username')
    print(username)
    username = re.search(r"'(.+)'", username).group(1)  # 提取中间的内容
    print(username)
    return render_template("chat.html", username=username, item_id=item_id)
@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    emit('message', f'{username} has entered the room.', room=room)

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    emit('message', f'{username} has left the room.', room=room)
    items = util.get_all_items()
    return render_template("help.html", items=items, username=username)
@socketio.on('message')
def handle_message(data):
    username = data['username']
    room = data['room']
    message = data['message']
    emit('message', f'{username}: {message}', room=room)
if __name__ == '__main__':
    socketio.run(app)
