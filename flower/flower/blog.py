from flask import (Blueprint, request, jsonify)
from flower.db import get_db
from flower.auth import check_status
from flower.exdata import strToImage, imageToStr
import datetime
import json
import os

BLOG_IMAGE = '/image/blog_image/'

bp = Blueprint('blog', __name__, url_prefix='/blog')


@bp.route('/get_all', methods=['GET'])
def get_all():
    msg = '获取成功'
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, nickname,'
        ' like, liker, image, comment'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC').fetchall()
    blogs = {}
    for i, post in enumerate(posts):
        blog = {}
        infos = [
            'id', 'title', 'body', 'created', 'author_id', 'nickname', 'like',
            'liker', 'comment'
        ]
        for info in infos:
            blog[info] = post[info]
        blog['image'] = ''
        if post['image']:
            blog['image'] = imageToStr(os.getcwd() + post['image'])
        comments = blog['comment'].split('||')[:-1]
        blog['comment'] = []
        for comment in comments:
            comment = comment.split('|')
            nickname = db.execute('SELECT * FROM user WHERE id = ?',
                                  (int(comment[0]), )).fetchone()['nickname']
            blog['comment'].append([nickname, comment[1]])
        blogs[i] = blog
    return jsonify(blogs=blogs, msg=msg)


ALLOWED_EXTENTIONS = ["jpg", "png", "JPG", "PNG", "GIF", "gif"]


@bp.route('/get_one', methods=['POST'])
def get_one():
    form = json.loads(request.data)
    p_id = int(form['p_id'])
    msg = '获取失败'
    error = None
    db = get_db()
    post = db.execute(
        'SELECT p.id, nickname, liker, like, title, body, created, image'
        ', comment, author_id'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?', (p_id, )).fetchone()
    if post is None:
        error = '该blog不存在'
    if error is None:
        msg = '获取成功'
        blog = {}
        infos = [
            'id', 'title', 'body', 'created', 'author_id', 'nickname', 'like',
            'liker', 'comment'
        ]
        for info in infos:
            blog[info] = post[info]
        blog['image'] = ''
        if post['image']:
            blog['image'] = imageToStr(os.getcwd() + post['image'])
        comments = blog['comment'].split('||')[:-1]
        blog['comment'] = []
        for comment in comments:
            comment = comment.split('|')
            nickname = db.execute('SELECT * FROM user WHERE id = ?',
                                  (int(comment[0]), )).fetchone()['nickname']
            blog['comment'].append([nickname, comment[1]])
        return jsonify(blog=blog, msg=msg, error=error)
    return jsonify(error=error, msg=msg)


@bp.route('/create', methods=['POST'])
def create():
    form = json.loads(request.data)
    id, user = check_status(request)
    title = form['title']
    body = form['body']
    img = form['image']
    error = None
    msg = '发表失败'

    if user is None:
        error = '请先登录'
    if not title:
        error = '请输入标题'

    if error is None:
        msg = '发表成功'
        create_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        image = ''
        if img:
            image = BLOG_IMAGE + str(id) + '_' + create_time + '.jpg'
            strToImage(img, os.getcwd() + image)
        db = get_db()
        db.execute(
            'INSERT INTO post (title, body, author_id, like, liker'
            ', image, comment) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (title, body, id, 0, '', image, ''))
        db.commit()
        # return jsonify(msg=msg)
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
        comment = post['comment'] + str(user['id']) + '|' + comment + '||'
        db = get_db()
        db.execute('UPDATE post SET comment = ?'
                   ' WHERE id = ?', (comment, p_id))
        db.commit()
        # return jsonify(msg=msg, error=error)
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
        if str(u_id) not in post['liker'].split(','):
            liker = post['liker'] + str(u_id) + ','
            msg = '点赞成功'
        else:
            msg = '取消赞成功'
            liker = post['liker'].split(',')[:-1]
            liker.remove(str(u_id))
            liker = ','.join(liker)
        like = len(liker.split(',')) - 1
        db.execute('UPDATE post SET liker = ?, like = ?'
                   ' WHERE id = ?', (liker, like, p_id))
        db.commit()
        return jsonify(msg=msg, error=error)
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
