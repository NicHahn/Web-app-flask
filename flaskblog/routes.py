import secrets, os
from PIL import Image
from datetime import date
from flask import render_template, request, url_for, flash, redirect, abort
from flaskblog.forms import RegistrationForm, LogInForm, UpdateAccountForm, PostForm
from flaskblog import app, db, bcrypt
from flaskblog.models import User, Post
from flask_login import login_user , current_user, logout_user, login_required


@app.route("/")
@app.route("/home")
def home():
    # Pagination
    # default page is 1, error if someone put anything else than an integer
    page = request.args.get('page', 1, type=int)
    # post per page - if page would no parameter it would always be page 1 
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=2)  
    # posts = Post.query.all()
    # argument can be any name, which we can access by his name in the template
    return render_template("home.html", posts=posts)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') # deocde to have a string and not bites
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created! You are now able to log in.', 'success')
        return redirect(url_for("login"))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LogInForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next') # return the 'next' paramater from the url if it exists
            flash(f'You are looged in!', 'success')
            return redirect(url_for("account")) if next_page else redirect(url_for("home"))
        else:
            flash(f'Wrong Email or Password. Please try again!', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    flash(f'You are successfully logged out!', 'success')
    return redirect(url_for("home"))

def save_picture(form_picture):
    #create own file name with a length of 8 hex
    random_hex = secrets.token_hex(8)
    _, file_ext = os.path.splitext(form_picture.filename) # _, -> filename is not used/needed
    picture_fn = random_hex + file_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    #resize image to max 125 pixel to reduce storage on server 
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size) 
    i.save(picture_path)
    return picture_fn

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash(f'Updated your account!', 'success')
        return redirect(url_for("account"))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html', title='Account', image=image_file, form=form)

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        new_post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(new_post)
        db.session.commit()
        flash(f'Your post has been created', 'success')
        return redirect(url_for("home"))
    return render_template("new_post.html", title='New Post', legend='New Post', form=form)


@app.route("/post/<int:post_id>", methods=['GET'])
def post(post_id):
    post = Post.query.get_or_404(post_id)  # Give the post with this post_id or return 404 page
    return render_template("post.html", title='Post', post=post)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)  # manually abort and show 403 for a forbidden route 
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash(f'Updated your post!', 'success')
        return redirect(url_for("post", post_id= post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template("new_post.html", title='Update Post', form=form, post=post, legend='Update Post')

@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    
    db.session.delete(post)
    db.session.commit()
    flash(f'Post deleted!', 'success')
    return redirect(url_for('home'))


@app.route("/user/<string:username>")
def user_posts(username):
    # Pagination
    # default page is 1, error if someone put anything else than an integer
    page = request.args.get('page', 1, type=int)
    # post per page - if page would no parameter it would always be page 1 
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=2)  
    # posts = Post.query.all()
    # argument can be any name, which we can access by his name in the template
    return render_template("user_posts.html", posts=posts, user=user)