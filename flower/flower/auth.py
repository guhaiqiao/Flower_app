from flask import (Blueprint, request, jsonify)
from werkzeug.security import check_password_hash, generate_password_hash
from flower.db import get_db
from flower.exdata import imageToStr, strToImage
import os
import json

bp = Blueprint('auth', __name__, url_prefix='/auth')
USER_IMAGE = '\\image\\user_image\\'
PHONE_PREFIX = [
    130, 131, 132, 155, 156, 185, 186, 145, 176, 134, 135, 136, 137, 138, 139,
    147, 150, 151, 152, 157, 158, 159, 178, 182, 183, 184, 187, 188, 133, 153,
    189
]


def check_phone(phone_number):
    if len(phone_number) == 11 and int(
            phone_number[:3]) in PHONE_PREFIX and phone_number.isdigit():
        return True
    else:
        return False


@bp.route('/register', methods=['POST'])
def register():
    form = json.loads(request.data)
    phone_number = form['phone_number']
    password = form['password']
    db = get_db()
    error = None
    # id = None
    msg = 'Failed register.'

    if not phone_number:
        error = 'Phone number is required.'
    elif not check_phone(phone_number):
        error = 'Incorrect phone number.'
    elif not password:
        error = 'Password is required'
    elif db.execute('SELECT id FROM user WHERE phone_number = ?',
                    (phone_number, )).fetchone() is not None:
        error = 'This phone number {} is already registered'.format(
            phone_number)

    if error is None:
        db.execute(
            'INSERT INTO user (ip, phone_number, password, nickname, head,'
            ' level, EXPoint, friend, personal_description, sex, age, region)'
            'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
            (request.remote_addr, phone_number,
             generate_password_hash(password), 'None',
             USER_IMAGE + 'default.jpg', 1, 0, '', '这个人很懒，什么也没有留下', '未知', '0',
             '未知'))
        db.commit()
        msg = 'Successfully registered.'

    return jsonify({
        'msg': msg,
        # 'id': id,
        # 'phone_number': phone_number,
        'error': error
    })


@bp.route('/login', methods=['POST'])
def login():
    form = json.loads(request.data)
    phone_number = form['phone_number']
    password = form['password']
    db = get_db()
    error = None
    msg = '登陆失败'
    user = db.execute('SELECT * FROM user WHERE phone_number = ?',
                      (phone_number, )).fetchone()

    if user is None:
        error = 'This user doesn\'t exist.'
    elif not check_password_hash(user['password'], password):
        error = 'Incorrect password.'

    if error is None:
        if user['ip'] != '':
            error = 'But this user is already online at another ip {}.'.format(
                user['ip'])
        db.execute('UPDATE user SET ip = ?'
                   ' WHERE id = ?', (request.remote_addr, user['id']))
        db.commit()
        head = imageToStr(os.getcwd() + user['head'])

        msg = '登陆成功.'
        return jsonify({
            'msg': msg,
            'id': user['id'],
            'phone_number': phone_number,
            'password': password,
            'error': error,
            'nickname': user['nickname'],
            'level': user['level'],
            'EXPoint': user['EXPoint'],
            'friend': user['friend'],
            'personal_description': user['personal_description'],
            'sex': user['sex'],
            'age': user['age'],
            'region': user['region'],
            'head': head
        })

    return jsonify({'msg': msg, 'phone_number': phone_number, 'error': error})


def check_status(request):
    form = json.loads(request.data)
    id = int(form['id'])
    db = get_db()
    user = db.execute('SELECT * FROM user WHERE id = ?', (id, )).fetchone()
    if user is None or user['ip'] != request.remote_addr:
        return id, None
    return id, user


@bp.route('/check_status', methods=['POST'])
def check_user_status():
    flag = True
    id, user = check_status(request)
    if user is None:
        flag = False
    return jsonify(flag=flag)


def check_nickname(nickname):
    length = len(nickname)
    if length == 0 or length > 20:
        return False
    return True


@bp.route('/personal_info', methods=['POST'])
def update_personal_info():
    form = json.loads(request.data)
    id, user = check_status(request)  # 判断用户是否登陆
    msg = '修改失败。'
    error = None
    db = get_db()
    phone_number = form['phone_number']
    nickname = form['nickname'].strip()
    img = form['head']
    personal_description = form['personal_description']
    sex = form['sex']
    age = int(form['age'])
    region = form['region']
    if user is None:
        error = '请先登录。'
    elif not check_nickname(nickname):
        error = '昵称有误'
    elif len(personal_description) > 200:
        error = '个人描述过长'
    elif sex not in ['男', '女', '未知']:
        error = '性别有误'
    elif age < 0:
        error = '年龄有误'
    if error is None:
        head = USER_IMAGE + str(id) + '.jpg'
        strToImage(img, os.getcwd() + head)
        db.execute(
            'UPDATE user SET nickname = ?, head = ?, personal_description = ?,'
            'sex = ?, age = ?, region = ?, phone_number = ? WHERE id = ?',
            (nickname, head, personal_description, sex, age, region,
             phone_number, id))
        db.commit()
        msg = '修改成功'

        return jsonify({
            'msg': msg,
            # 'error': error,
            'id': id,
            'head': img,
            'phone_number': phone_number,
            'nickname': nickname,
            'personal_description': personal_description,
            'sex': sex,
            'age': age,
            'region': region
        })

    return jsonify({'msg': msg, 'id': id, 'error': error})


@bp.route('/password_update', methods=['POST'])
def update_password():
    form = json.loads(request.data)
    id, user = check_status(request)
    old_password = form['old_password']
    new_password = form['new_password']
    error = None
    msg = '修改失败'
    db = get_db()
    if user is None:
        error = '请先登录'
    elif not check_password_hash(user['password'], old_password):
        error = '原密码错误'

    if error is None:
        db.execute('UPDATE user SET password = ?'
                   ' WHERE id = ?', (generate_password_hash(new_password), id))
        db.commit()
        msg = '修改成功'
        return jsonify({
            'msg': msg,
            'id': id,
            'password': new_password,
            # 'error': error
        })

    return jsonify({'msg': msg, 'id': id, 'error': error})


@bp.route('/query', methods=['POST'])
def query_user():
    form = json.loads(request.data)
    id, user = check_status(request)
    type = form['type']  # 按昵称或手机号查询
    User_index = form['User']  # 昵称或手机号
    msg = '查询失败'
    error = None
    if user is None:
        error = '请先登录'
    elif type not in ['nickname', 'phone_number']:
        error = '查询方式错误'
    elif not User_index or User_index == 'None':
        error = '请输入用户'
    if error is None:
        db = get_db()
        User = db.execute('SELECT * FROM user WHERE ' + type + ' = ?',
                          (User_index, )).fetchone()
        if User is None:
            error = '用户不存在'

    if error is None:
        msg = '查询成功'
        head = imageToStr(os.getcwd() + User['head'])
        return jsonify({
            'msg': msg,
            # 'error': error,
            # 'id': id,
            'phone_number': User['phone_number'],
            'nickname': User['nickname'],
            'level': User['level'],
            'EXPoint': User['EXPoint'],
            'personal_description': User['personal_description'],
            'sex': User['sex'],
            'age': User['age'],
            'region': User['region'],
            'head': head
        })

    return jsonify({'msg': msg, 'id': id, 'error': error})


@bp.route('/friend', methods=['POST'])
def update_friends():
    form = json.loads(request.data)
    id, user = check_status(request)
    method = form['method']  # 添加或删除好友
    type = form['type']  # 按昵称或手机号添加
    friend_index = form['friend']  # 昵称或手机号
    msg = '朋友更新失败.'
    error = None
    if user is None:
        error = '请先登录。'
    elif type not in ['phone_number', 'nickname']:
        error = '查找方式错误，按手机号或昵称查找.'
    if error is None:
        db = get_db()
        friend = db.execute('SELECT id FROM user WHERE ' + type + ' = ?',
                            (friend_index, )).fetchone()
        if friend is None:
            error = '该用户不存在.'

    if error is None:
        friend_id = friend['id']
        friends = user['friend'].split(',')[:-1]
        if method == 'add':
            if str(friend_id) in friends:
                error = '该用户已是好友.'
                msg = '添加失败'
            else:
                friends = ','.join(friends) + str(friend_id) + ','
                db.execute('UPDATE user SET friend = ? WHERE id = ?',
                           (friends, id))
                db.commit()
                msg = '添加成功'
        elif method == 'delete':
            if str(friend_id) not in friends:
                error = '该用户不是好友.'
                msg = '删除失败'
            else:
                friends.remove(str(friend_id))
                friends = ','.join(friends)
                db.execute('UPDATE user SET friend = ? WHERE id = ?',
                           (friends, id))
                db.commit()
                msg = '删除成功'
        return jsonify({
            'msg': msg,
            # 'id': id,
            'friend': friends,
            # 'error': error
        })

    return jsonify({'msg': msg, 'id': id, 'error': error})


@bp.route('/logout', methods=['POST'])
def logout():
    id, user = check_status(request)
    msg = '下线失败。'
    error = None
    db = get_db()
    if user is None:
        error = '请先登录。'

    if error is None:
        db.execute('UPDATE user SET ip = ? WHERE id = ?', ('', id))
        db.commit()
        msg = '下线成功'
    return jsonify({'msg': msg, 'id': id, 'error': error})
