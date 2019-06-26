from flask import (Blueprint, request, jsonify)
from flower.db import get_db
from flower.exdata import imageToStr
from flower.auto_match import auto_match
import os
import json

FLOWER_IMAGE = '/image/flower_image/'
bp = Blueprint('flower', __name__, url_prefix='/flower')


# @bp.route('/add', methods=['POST'])
# def add_flower():
#     msg = '添加失败'
#     error = None
#     cn_name = request.form['cn_name']
#     en_name = request.form['en_name']
#     type = request.form['type']
#     image = request.form['image']
#     description = request.form['description']
#     similar_flower = request.form['similar_flower']
#     combined_flower = ','.join(request.form['combined_flower'])
#     price = 0
#     return
@bp.route('/query', methods=['POST'])  # 按中文名查找
def query_flower():
    import_flower('玫瑰花', 'rose', '主花', '爱情', '1.jpg', '暂无描述', '康乃馨', '满天星, 百合',
                  10)
    form = json.loads(request.data)
    msg = '查询失败'
    error = None
    flower_name = form['flower_name']
    db = get_db()
    Flower = db.execute('SELECT * FROM flower WHERE cn_name = ?',
                        (flower_name, )).fetchone()
    if Flower is None:
        error = '该花不存在'

    if error is None:
        msg = '查询成功'
        image = imageToStr(os.getcwd() + Flower['image'])
        return jsonify({
            'msg': msg,
            'error': error,
            'cn_name': Flower['cn_name'],
            'en_name': Flower['en_name'],
            'type': Flower['type'],
            'flower_language': Flower['flower_language'],
            'similar': Flower['similar'],
            'combined': Flower['combined'],
            'image': image,
            'description': Flower['description'],
            'price': Flower['price']
        })

    return jsonify({'msg': msg, 'error': error})


@bp.route('/auto_match', methods=['POST'])
def match():
    msg = '搭配失败'
    data = json.loads(request.data)
    like = data['like']
    dislike = data['dislike']
    price = data['price']
    error = None
    if not like or price <= 0:
        error = '请输入合适的条件'
    if error is None:
        msg = '搭配成功'
        methods = auto_match(like, dislike, price)
        return jsonify(methods=methods, msg=msg, error=error)
    return jsonify(msg=msg, error=error)


def import_flower(cn_name, en_name, type, flower_language, image, description,
                  similar_flower, combined_flower, price):
    db = get_db()
    db.execute(
        'INSERT INTO flower (cn_name, en_name, type, flower_language, image,'
        ' description, similar_flower, combined_flower, price)'
        'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
        (cn_name, en_name, type, flower_language, FLOWER_IMAGE + image,
         description, similar_flower, combined_flower, price))
    db.commit()
    return '添加成功'
