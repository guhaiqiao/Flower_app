from flask import (Blueprint, request, jsonify)
from flower.db import get_db
import datetime
import os
from flower.exdata import strToImage, imageToStr

BLOG_IMAGE = '\\image\\blog_image\\'

bp = Blueprint('blog', __name__, url_prefix='/blog')


@bp.route('/get_all', methods=['GET'])
def index():
    msg = '获取成功'
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, nickname,'
        ' good, gooder, image, comment'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC').fetchall()
    blogs = {}
    for i, post in enumerate(posts):
        blog = {}
        infos = [
            'id', 'title', 'body', 'created', 'author_id', 'nickname', 'good',
            'gooder', 'comment'
        ]
        for info in infos:
            blog[info] = post[info]
        if post['image']:
            blog['image'] = imageToStr(os.getcwd() + post['image'])
        blog['image'] = ''
        blogs[i] = blog
    return jsonify(blogs=blogs, msg=msg)


ALLOWED_EXTENTIONS = ["jpg", "png", "JPG", "PNG", "GIF", "gif"]


@bp.route('/create', methods=['POST'])
def create():
    id = request.form['id']  # 用户id
    title = request.form['title']
    body = request.form['body']
    img = request.form['image']
    error = None
    msg = '发表失败'

    if not title:
        error = 'Title is required.'

    if error is None:
        msg = '发表成功'
        create_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        image = ''
        if img:
            image = strToImage(os.getcwd() + BLOG_IMAGE + str(id) + '_' +
                               create_time)
        db = get_db()
        db.execute(
            'INSERT INTO post (title, body, author_id, good, gooder'
            ', image, comment) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (title, body, id, 0, '', image, ''))
        db.commit()
    return jsonify(msg=msg, error=error)


# return jsonify(
#             msg=msg,
#             error=error,
#             nickname=nickname,
#             title=title,
#             body=body,
#             good=0,
#             gooder='',
#             image=image,
#             comment='',
#             create_time=create_time
#             )

# @bp.route('/<int:id>/comment', methods=['GET', 'POST'])
# @login_required
# def comment(id):
#     db = get_db()
#     post = db.execute(
#         'SELECT p.id, title, body, username, created, gooder, good, comment'
#         ' FROM post p JOIN user u ON p.author_id = u.id'
#         ' WHERE p.id = ?', (id, )).fetchone()

#     if request.method == 'POST':
#         comment = request.form['comment']
#         comment = post['comment'] + comment + '|' + g.user['username'] + '|'
#         db = get_db()
#         db.execute('UPDATE post SET comment = ?'
#                    ' WHERE id = ?', (comment, id))
#         db.commit()

#         return redirect(url_for('blog.index'))

#     return render_template('blog/comment.html', post=post)


@bp.route('/good', methods=['POST'])
def good():
    msg = '点赞成功'
    u_id = request.form['u_id']
    p_id = request.form['p_id']
    db = get_db()
    post = db.execute(
        'SELECT p.id, nickname, gooder, good'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?', (p_id, )).fetchone()
    if str(u_id) not in post['gooder'].split(','):
        gooder = post['gooder'] + ',' + str(u_id)
    else:
        msg = '取消赞成功'
        gooder = post['gooder'].split(',')
        gooder.remove(str(u_id))
        gooder = ','.join(gooder)
    good = len(gooder.split(','))
    db.execute('UPDATE post SET gooder = ?, good = ?'
               ' WHERE id = ?', (gooder, good, p_id))
    db.commit()
    return jsonify(id=p_id, msg=msg)


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
