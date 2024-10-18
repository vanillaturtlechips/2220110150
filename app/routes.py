from flask import render_template, url_for, flash, redirect, request
from app import app, db
from app.models import Post, Comment

@app.route("/")
@app.route("/home")
def home():
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template('index.html', posts=posts)

@app.route("/post/<int:post_id>", methods=['GET', 'POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    if request.method == 'POST':
        comment = Comment(content=request.form.get('content'), post_id=post.id)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been added!', 'success')
        return redirect(url_for('post', post_id=post.id))
    return render_template('post.html', title=post.title, post=post)

@app.route("/post/new", methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        post = Post(title=request.form.get('title'), content=request.form.get('content'))
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post')
