#整个项目的工具模块，封装了整个项目中的工具类
import pymysql
import heapq
import random
import re
#获取数据库链接
def get_conn():
    conn = pymysql.connect(
        host = "localhost", port=3306,
        user="root", password="123456",
        database = "newbase",charset="utf8"
    )
    cursor = conn.cursor()
    return conn,cursor

#查询所有
def find_all():
    conn,cursor = get_conn()
    #执行sql
    sql = "select * from user_info"
    cursor.execute(sql)
    #查询所有
    result = cursor.fetchall()
    return result
def find_all_order():
    conn,cursor = get_conn()
    #执行sql
    sql = "select time from order_info"
    cursor.execute(sql)
    #查询所有
    result = cursor.fetchall()
    print(result)
    return result
def check_Volinfo(stu_id):
    conn, cursor = get_conn()
    sql = "select volunteer from user_info where stu_id = %s"
    cursor.execute(sql, (stu_id,))
    result = cursor.fetchone()  # 使用 fetchone() 获取单行结果
    if result:
        volunteer_str = str(result[0])  # 获取 volunteer 字符串
        match = re.search(r'\d+', volunteer_str)  # 使用正则表达式提取数字
        if match:
            volunteer = int(match.group())  # 将提取的数字转换为整数
            print(volunteer)
            return volunteer
    return None
def insert_info(stu_id, password, username, email):
    conn,cursor=get_conn()
    sql = "insert into user_info (stu_id, password, username, email)values(%s,%s,%s,%s)"
    count = cursor.execute(sql, [stu_id,password,username,email])#一定是元组或列表

    if count>0:
        print("注册成功")
    else:
        print("注册失败")



    #提交事务
    conn.commit()
    #释放资源
    conn.close()
    cursor.close()
    return count
def getInfoContent(stu_id, vcode, start, end):
    conn, cursor = get_conn()
    sql = "INSERT INTO order_info (stu_id, vcode, start, end) VALUES (%s, %s, %s, %s)"
    count = cursor.execute(sql, [stu_id, vcode, start, end])
    if count>0:
        message ="发货成功"
        print("发货成功")
    else:
        message = "发货失败"
        print("发货失败")

    #提交事务
    conn.commit()
    #释放资源
    conn.close()
    cursor.close()
    return message
def SubmitMessage(stu_id,content):
    conn, cursor = get_conn()
    sql = "INSERT INTO content (stu_id, content) VALUES (%s, %s)"
    count = cursor.execute(sql, [stu_id, content])
    if count > 0:
        message = "留言成功"
        print("留言成功")
    else:
        message = "留言失败"
        print("留言失败")

    # 提交事务
    conn.commit()
    # 释放资源
    conn.close()
    cursor.close()
    return message
def DelInfoContent(vcode):
    conn, cursor = get_conn()
    sql = "UPDATE order_info SET done = 1 where vcode = %s"
    count = cursor.execute(sql, (vcode))
    if count>0:
        message="取货成功"
        print("取货成功")
    else:
        message = "取货失败"
        print("取货失败")
    #提交事务
    conn.commit()
    #释放资源
    conn.close()
    cursor.close()
    return message
def find_order_info(stu_id):
    #获取数据库链接
    conn,cursor = get_conn()
    #执行sql
    sql = "select * from order_info where stu_id = %s"
    cursor.execute(sql, (stu_id))
    #获取所有学生信息
    result = cursor.fetchall()
    return result
def find_spec_order_info():
    #获取数据库链接
    conn,cursor = get_conn()
    #执行sql
    sql = "select * from order_info where Vol = 0"
    cursor.execute(sql)
    #获取所有学生信息
    result = cursor.fetchall()
    return result
def VolInfo(name,phone_number,stu_id):
    conn, cursor = get_conn()
    sql = "UPDATE user_info SET phonenumber = %s, name = %s, volunteer = 1 WHERE stu_id = %s"
    values = (phone_number, name, stu_id)
    try:
        # 执行SQL查询
        cursor.execute(sql, values)
        conn.commit()
        message="注册成功"
        return message
    except Exception as e:
        # 更新失败时进行回滚
        conn.rollback()
        message = "注册失败"
        return message
    finally:
        # 关闭数据库连接
        cursor.close()
        conn.close()
def Get_order(seq):
    conn, cursor = get_conn()
    sql = "UPDATE order_info SET Vol = 1 WHERE seq = %s"
    select_sql = "SELECT vcode FROM order_info WHERE seq = %s"
    values = (seq,)
    try:
        # 执行SQL查询
        cursor.execute(sql, values)
        conn.commit()
        cursor.execute(select_sql, values)
        result = cursor.fetchone()
        vcode = str(result[0])
        message="接单成功,验证码："+vcode
        return message
    except Exception as e:
        # 更新失败时进行回滚
        conn.rollback()
        message = "接单失败"
        return message
    finally:
        # 关闭数据库连接
        cursor.close()
        conn.close()
def get_username(stu_id):
    #获取数据库链接
    conn,cursor = get_conn()
    #执行sql
    sql = "select username from user_info where stu_id = %s"
    cursor.execute(sql, (stu_id))
    #获取所有学生信息
    username = cursor.fetchall()
    return username
def get_all_items():
    conn, cursor = get_conn()
    sql = "SELECT * FROM items"
    cursor.execute(sql)
    results = cursor.fetchall()
    items = []
    for row in results:
        item = {
            'id':row[0],
            'name': row[1],
            'info': row[2],
            'image_path': row[3]
        }
        items.append(item)
    cursor.close()
    conn.close()
    return items
def get_all_lost_items():
    conn, cursor = get_conn()
    sql = "SELECT * FROM lost_items"
    cursor.execute(sql)
    results = cursor.fetchall()
    items = []
    for row in results:
        item = {
            'id':row[0],
            'name': row[1],
            'info': row[2],
            'image_path': row[3]
        }
        items.append(item)
    cursor.close()
    conn.close()
    return items
def upload_item(name, info, image_path):
    # Get the database connection and cursor
    conn, cursor = get_conn()

    # Define the SQL query
    sql = "INSERT INTO items (name, info, image_path) VALUES (%s, %s, %s)"

    # Execute the query with the item details
    cursor.execute(sql, (name, info, image_path))

    # Commit the changes
    conn.commit()

    # Close the cursor and connection
    cursor.close()
    conn.close()
    message="上传成功"
    return message
def upload_lost_item(name, info, image_path):
    # Get the database connection and cursor
    conn, cursor = get_conn()

    # Define the SQL query
    sql = "INSERT INTO lost_items (name, info, image_path) VALUES (%s, %s, %s)"

    # Execute the query with the item details
    cursor.execute(sql, (name, info, image_path))

    # Commit the changes
    conn.commit()

    # Close the cursor and connection
    cursor.close()
    conn.close()
    message="上传成功"
    return message
# 柜子操作
def initialize_cabinet():
    """初始化外卖柜"""
    cabinet = {i: None for i in range(1, 31)}
    return cabinet


def store_order(cabinet, order_number):
    """存储外卖订单"""
    for slot, order in cabinet.items():
        if order is None:
            cabinet[slot] = order_number
            return slot
    return None


def retrieve_order(cabinet, order_number):
    """取出外卖订单"""
    for slot, order in cabinet.items():
        if order == order_number:
            cabinet[slot] = None
            return slot
    return None


def check_inventory(cabinet):
    """检查当前库存情况"""
    inventory = {slot: order for slot, order in cabinet.items() if order is not None}
    return inventory


def generate_random_number():
    '''生成随机验证码'''
    numbers = set()

    while len(numbers) < 4:
        number = random.randint(0, 9)
        numbers.add(number)
    return ''.join(str(num) for num in numbers)


# 初始化外卖柜
cabinet = initialize_cabinet()


# 存放物品
def insert_cell(cabinet, random_num):
    order_number = generate_random_number()  # 传入四位随机数
    slot = store_order(cabinet, order_number)
    if slot is None:
        result = "抱歉，当前柜子已满，无法存储物品。"
        print("抱歉，当前柜子已满，无法存储物品。")
    else:
        order = f"订单号： {order_number} ，请存储在柜子 {slot} 中。"
    return order
    # 取出物品


def pop_cell(cabinet, order_number):
    """取出外卖订单"""
    for slot, order in cabinet.items():
        if order == order_number:
            cabinet[slot] = None
            return f"柜门已开,请去{slot}号们取件"
        else:
            return "号码不存在，请核实"
    return None
def dijkstra(graph, start):
    distances = {vertex: float('inf') for vertex in graph}
    distances[start] = 0
    heap = [(0, start)]
    previous_vertices = {vertex: None for vertex in graph}
    while heap:
        (current_distance, current_vertex) = heapq.heappop(heap)
        if current_distance > distances[current_vertex]:
            continue
        for neighbor, weight in graph[current_vertex].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_vertices[neighbor] = current_vertex
                heapq.heappush(heap, (distance, neighbor))
    return distances, previous_vertices
def shortest_path(graph, start, end):
    distances, previous_vertices = dijkstra(graph, start)

    path = []
    vertex = end
    while vertex is not None:
        path.append(vertex)
        vertex = previous_vertices[vertex]
    path.reverse()
    return path

