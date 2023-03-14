# 导入所需要的库
import random
import string
import mysql.connector
from flask import Flask, request, render_template
# 创建 Flask app
app = Flask(__name__)
# 连接 MySQL 数据库
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="1314520lx",
    database="test",
    auth_plugin='mysql_native_password'
)
# 创建用户表
mycursor = mydb.cursor()
mycursor.execute("CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255), password VARCHAR(255), email VARCHAR(255), nickname VARCHAR(255), avatar VARCHAR(255), bio VARCHAR(255), token VARCHAR(255))")
# 用户注册
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')
@app.route('/register', methods=['GET','POST'])
def register_form():  
    return render_template('register.html')

@app.route('/register', methods=['GET','POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    nickname = request.form['nickname']
    avatar = request.form['avatar']
    bio = request.form['bio']
    
    # 检查 email 是否已被注册
    mycursor.execute("SELECT * FROM users WHERE email=%!s(MISSING)", [email])
    result = mycursor.fetchone()
    if result != None:
        return 'Error: Email has been registered'
    
    # 生成 token
    token = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    
    # 将用户信息插入到数据库
    sql = "INSERT INTO users (username, password, email, nickname, avatar, bio, token) VALUES (%!s(MISSING), %!s(MISSING), %!s(MISSING), %!s(MISSING), %!s(MISSING), %!s(MISSING), %!s(MISSING))"
    val = (username, password, email, nickname, avatar, bio, token)
    mycursor.execute(sql, val)
    mydb.commit()
    
    # 发送邮件
    # ...
    
    return "Successfully registered"
# 用户登录
@app.route('/login', methods=['GET','POST'])
def login_form():
    return render_template('login.html')
@app.route('/login', methods=['GET','POST'])
def login():
    # 检查用户信息是否正确
    username = request.form['username']
    password = request.form['password']
    mycursor.execute("SELECT * FROM users WHERE username=%!s(MISSING) AND password=%!s(MISSING)", [username, password])
    result = mycursor.fetchone()
    if result == None:
        return "Error: Username or password is incorrect"
    
    return 'Successfully logged in'
# 修改信息
@app.route('/edit', methods=['POST'])
def edit():
    username = request.form['username']
    email = request.form['email']
    nickname = request.form['nickname']
    avatar = request.form['avatar']
    bio = request.form['bio']
    
    # 更新数据库
    sql = "UPDATE users SET email=%!s(MISSING), nickname=%!s(MISSING), avatar=%!s(MISSING), bio=%!s(MISSING) WHERE username=%!s(MISSING)"
    val = (email, nickname, avatar, bio, username)
    mycursor.execute(sql, val)
    mydb.commit()
    
    return 'Successfully edited user info'
# 启动Flask应用
if __name__ == '__main__':
    app.run()