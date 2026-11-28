from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__)


@bp.route('/')
def index():
    user_id = g.user['id'] if g.user else None
    
    db = get_db()
    posts = db.execute(
        '''
        SELECT p.id, p.title, p.body, p.created, p.author_id, is_published, u.username,
               COALESCE(likes.total, 0) AS likes_count,
               EXISTS(SELECT 1 FROM like l WHERE l.user_id = ? AND l.post_id = p.id) AS is_liked_by_me
        FROM post p
        JOIN user u ON p.author_id = u.id
        LEFT JOIN (SELECT post_id, COUNT(*) as total FROM like GROUP BY post_id) likes 
            ON p.id = likes.post_id
        ORDER BY p.created DESC
        ''',
        (user_id,)
    ).fetchall()
    
    return render_template('blog/index.html', posts=posts)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        is_published = 'is_published' in request.form
        error = None

        if not title:
            error = 'Title is required.'
        elif len(title) < 3:
            error = 'Title must be at least 3 characters long.'

        if not body:
            error = 'Body is required.' if error is None else error
        elif len(body) < 10:
            error = 'Body must be at least 10 characters long.' 

        print("--- DEBUG ---")
        print(f"Form keys: {request.form.keys()}")
        print(f"Is checkbox present in form? {'is_published' in request.form}")
        print(f"Value of is_published variable: {is_published}") 

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id, is_published)'
                ' VALUES (?, ?, ?, ?)',
                (title, body, g.user['id'], is_published)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")
    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        is_published = 'is_published' in request.form

        error = None

        if not title:
            error = 'Title is required.'
        elif len(title) < 3:
            error = 'Title must be at least 3 characters long.'

        if not body:
            error = 'Body is required.' if error is None else error
        elif len(body) < 10:
            error = 'Body must be at least 10 characters long.' 


        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?, is_published = ? WHERE id = ?',
                (title, body, is_published, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))

def get_likes_count(post_id):
    db = get_db()
    row = db.execute(
        'SELECT COUNT(*) AS count FROM like WHERE post_id = ?',
        (post_id,)
    ).fetchone()
    return row['count']

def is_liked(user_id, post_id):
    if user_id is None:
        return False
    db = get_db()
    row = db.execute(
        'SELECT id FROM like WHERE user_id = ? AND post_id = ?',
        (user_id, post_id)
    ).fetchone()
    return row is not None

@bp.route('/<int:id>/like', methods=('POST',))
@login_required
def like(id):
    post = get_post(id)
    db = get_db()
    
    try:
        db.execute(
            'INSERT INTO like (user_id, post_id) VALUES (?, ?)',
            (g.user['id'], id)
        )
        db.commit()
    except sqlite3.IntegrityError:
        pass 
        
    return redirect(url_for('blog.index'))

@bp.route('/<int:id>/unlike', methods=('POST',))
@login_required
def unlike(id):
    post = get_post(id)
    db = get_db()
    db.execute('DELETE FROM like WHERE user_id = ? AND post_id = ?', (g.user['id'], id))
    db.commit()
    return redirect(url_for('blog.index'))


