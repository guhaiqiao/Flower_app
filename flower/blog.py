import time
import json
import os
import base64
from flask import Blueprint, jsonify, request, make_response

from flower.auth import check_status
from flower.db import get_db
from flower.exdata import (imageToStr, strToImage, get_outfile, get_size,
                           resize)
from flower.Request import Request
BLOG_IMAGE = '/image/blog_image/'
IMAGE_SIZE = 50  # KB
LIMIT = 400  # 长宽最大像素
bp = Blueprint('blog', __name__, url_prefix='/blog')


@bp.route('/get_image', methods=['GET'])
def get_image():
    p_id, index = Request(request, 'GET', 'p_id', 'index').load()

    msg = '获取失败'
    error = None
    db = get_db()
    post = db.execute('SELECT id, image FROM post WHERE id = ?',
                      (p_id, )).fetchone()
    if post is None:
        error = '该blog不存在'
    imgs = post['image'].split(',')
    if imgs is None or len(imgs) <= index:
        error = '图片不存在'

    if error is None:
        img = imgs[index]
        img_type = img.split('.')[-1]
        if img_type == 'jpg':
            img_type = 'jpeg'
        img_data = open(os.getcwd() + img, "rb").read()
        response = make_response(img_data)
        response.headers['Content-Type'] = 'image/' + img_type
        return response
    return jsonify(error=error, msg=msg)


@bp.route('/get_all', methods=['GET'])
def get_all():
    msg = '获取成功'
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, nickname,'
        ' like, liker, image, image_size, image_compressed, comment'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC').fetchall()
    blogs = []
    print(len(posts))
    for post in posts:
        blog = {}
        infos = [
            'id', 'title', 'body', 'created', 'author_id', 'nickname', 'like',
            'comment'
        ]
        for info in infos:
            blog[info] = post[info]
        blog['image'] = []
        blog['image_size'] = post['image_size']
        if post['image']:
            print(blog['image_size'])
            img_compressed = post['image_compressed'].split(',')
            for index, img in enumerate(post['image'].split(',')):
                # print(img_compressed[index])
                if int(img_compressed[index]):
                    blog['image'].append(
                        imageToStr(get_outfile(os.getcwd() + img)))
                else:
                    blog['image'].append(imageToStr(os.getcwd() + img))
        # blog['image'] = ','.join(blog['image'])
        blog['likers'] = []
        if post['like'] != 0:
            likers = post['liker'].split(',')[1:]
            for liker in likers:
                u_id = int(liker)
                nickname = db.execute('SELECT * FROM user WHERE id = ?',
                                      (u_id, )).fetchone()['nickname']
                blog['likers'].append({'id': u_id, 'nickname': nickname})

        comments = blog['comment'].split('||')[:-1]
        blog['comment'] = []
        for comment in comments:
            comment = comment.split(',')
            u_id = int(comment[0])
            nickname = db.execute('SELECT * FROM user WHERE id = ?',
                                  (u_id, )).fetchone()['nickname']
            blog['comment'].append({
                'id': u_id,
                'nickname': nickname,
                'comment': base64.b64decode(comment[1])
            })
        blogs.append(blog)
    return jsonify(blogs=blogs, msg=msg)


ALLOWED_EXTENTIONS = ["jpg", "png", "JPG", "PNG", "GIF", "gif"]


@bp.route('/get_one', methods=['POST'])
def get_one():
    p_id = Request(request, 'p_id').load()
    # form = json.loads(request.data)
    # p_id = int(form['p_id'])
    msg = '获取失败'
    error = None
    db = get_db()
    post = db.execute(
        'SELECT p.id, nickname, liker, like, title, body, created, image'
        ', image_size, image_compressed, comment, author_id'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?', (p_id, )).fetchone()
    if post is None:
        error = '该blog不存在'
    if error is None:
        msg = '获取成功'
        blog = {}
        infos = [
            'id', 'title', 'body', 'created', 'author_id', 'nickname', 'like',
            'comment'
        ]
        for info in infos:
            blog[info] = post[info]

        blog['image'] = []
        blog['image_size'] = post['image_size']
        img_compressed = post['image_compressed'].split(',')
        for i, img in enumerate(post['image'].split(',')):
            if img_compressed[i]:
                blog['image'].append(imageToStr(get_outfile(os.getcwd() +
                                                            img)))
            else:
                blog['image'].append(imageToStr(os.getcwd() + img))
        # blog['image'] = ','.join(blog['image'])

        blog['likers'] = []
        if post['like'] != 0:
            likers = post['liker'].split(',')[1:]
            for liker in likers:
                u_id = int(liker)
                nickname = db.execute('SELECT * FROM user WHERE id = ?',
                                      (u_id, )).fetchone()['nickname']
                blog['likers'].append({'id': u_id, 'nickname': nickname})

        comments = post['comment'].split('.')[:-1]
        blog['comment'] = []
        for comment in comments:
            comment = comment.split(',')
            u_id = int(comment[0])
            nickname = db.execute('SELECT * FROM user WHERE id = ?',
                                  (u_id, )).fetchone()['nickname']
            blog['comment'].append({
                'id': u_id,
                'nickname': nickname,
                'comment': base64.b64decode(comment[1])
            })
        return jsonify(blog=blog, msg=msg)
    return jsonify(error=error, msg=msg)


@bp.route('/create', methods=['POST'])
def create():
    form = json.loads(request.data)
    id, user = check_status(request)
    # title, body, imgs = Request(request, 'POST', 'title', 'body', 'image')
    title = form['title']
    body = form['body']
    # imgs = imgs.split(',')
    imgs = form['image'].split(',')
    print(len(imgs))
    error = None
    msg = '发表失败'

    if user is None:
        error = '请先登录'
    if not title:
        error = '请输入标题'

    if error is None:
        msg = '发表成功'
        create_time = time.strftime("%Y%m%d%H%M%S")
        image = []
        img_compress = []
        image_size = []
        for index, img in enumerate(imgs):
            if img:
                image.append(BLOG_IMAGE + str(id) + '_' + create_time + '_' +
                             str(index) + '.jpg')
                image_path = os.getcwd() + image[index]
                strToImage(img, image_path)
                image_size.append(str(round(get_size(image_path), 3)))
                img_compress.append(str(resize(image_path, LIMIT)))
        db = get_db()
        print(image_size)
        db.execute(
            'INSERT INTO post (title, body, author_id, like, liker'
            ', image, image_size, image_compressed, comment) VALUES (?, ?, ?, '
            '?, ?, ?, ?, ?, ?)',
            (title, body, id, 0, '', ','.join(image), ','.join(image_size),
             ','.join(img_compress), ''))
        db.commit()
        return jsonify(msg=msg)
    return jsonify(msg=msg, error=error)


@bp.route('/comment', methods=['POST'])
def comment():
    u_id, user = check_status(request)
    data = json.loads(request.data)
    p_id = data['p_id']
    msg = '评论失败'
    error = None
    comment = data['comment']
    if comment == '':
        error = '请输入评论'
    if error is None:
        msg = '评论成功'
        db = get_db()
        post = db.execute(
            'SELECT p.id, title, body, nickname, created, liker, like, comment'
            ' FROM post p JOIN user u ON p.author_id = u.id'
            ' WHERE p.id = ?', (p_id, )).fetchone()
        comment = post['comment'] + str(
            user['id']) + ',' + base64.b64encode(comment) + '.'
        db = get_db()
        db.execute('UPDATE post SET comment = ?'
                   ' WHERE id = ?', (comment, p_id))
        db.commit()
        return jsonify(msg=msg)
    return jsonify(msg=msg, error=error)


@bp.route('/like', methods=['POST'])
def like():
    form = json.loads(request.data)
    msg = '点赞失败'
    u_id, user = check_status(request)
    p_id = form['p_id']
    error = None
    if user is None:
        error = '请先登录'

    if error is None:
        db = get_db()
        post = db.execute(
            'SELECT p.id, nickname, liker, like'
            ' FROM post p JOIN user u ON p.author_id = u.id'
            ' WHERE p.id = ?', (p_id, )).fetchone()
        like = post['like']
        likers = post['liker'].split(',')
        if str(u_id) not in likers:
            likers.append(str(u_id))
            msg = '点赞成功'
        else:
            msg = '取消赞成功'
            likers.remove(str(u_id))
        liker = ','.join(likers)
        like = len(liker.split(',')) - 1
        db.execute('UPDATE post SET liker = ?, like = ?'
                   ' WHERE id = ?', (liker, like, p_id))
        db.commit()
        print(msg)
        return jsonify(msg=msg)
    return jsonify(msg=msg, error=error)


# @bp.route('/<int:id>/update', methods=('GET', 'POST'))
# @login_required
# def update(id):
#     post = get_post(id)

#     if request.method == 'POST':
#         title = request.form['title']
#         body = request.form['body']
#         error = None

#         if not title:
#             error = 'Title is required.'

#         if error is not None:
#             flash(error)
#         else:
#             db = get_db()
#             db.execute('UPDATE post SET title = ?, body = ?'
#                        ' WHERE id = ?', (title, body, id))
#             db.commit()
#             return redirect(url_for('blog.index'))

#     return render_template('blog/update.html', post=post)

# @bp.route('/<int:id>/delete', methods=('POST', ))
# @login_required
# def delete(id):
#     get_post(id)
#     db = get_db()
#     db.execute('DELETE FROM post WHERE id = ?', (id, ))
#     db.commit()
#     return redirect(url_for('blog.index'))
