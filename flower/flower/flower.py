from flask import (Blueprint, request, jsonify)
from flower.db import get_db
from flower.exdata import imageToStr
# import flower.auto_match
import os

FLOWER_IMAGE = '\\image\\flower_image\\'
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
    msg = '查询失败'
    error = None
    flower_name = request.form['flower_name']
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
            'similar_flower': Flower['similar_flower'],
            'combined_flower': Flower['combined_flower'],
            'image': image,
            'description': Flower['description'],
            'price': Flower['price']
        })
        # return jsonify(msg=msg, error=error)

    return jsonify({'msg': msg, 'flower_name': flower_name, 'error': error})


@bp.route('/auto_match', methods=['POST'])
def auto_match():
    msg = '搭配成功'
    # error = None
    # total_price = request.form['total_price']
    like = request.form['like'].split(',')
    img = ''
    # dislike = request.form['dislike']
    # matchs = auto_match(like, dislike, total_price)
    # if not match:
    #     error = '无法搭配'
    # if error is None:
    #     return jsonify(matchs=matchs)
    if '1' in like:
        if '2' in like:
            img = imageToStr(os.getcwd() + '\\flower_image\\' + '1_2.jpg')
        elif '12' in like:
            img = imageToStr(os.getcwd() + '\\flower_image\\' + '1_12.jpg')
        elif '15' in like:
            img = imageToStr(os.getcwd() + '\\flower_image\\' + '1_15.jpg')
    if '5' in like:
        img = imageToStr(os.getcwd() + '\\flower_image\\' + '5_15.jpg')

    return jsonify(img=img, msg=msg)


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
