from flask import render_template, request, Blueprint
from flaskblog.models import Post

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    # Pagination
    # default page is 1, error if someone put anything else than an integer
    page = request.args.get('page', 1, type=int)
    # post per page - if page would no parameter it would always be page 1 
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=2)  
    # posts = Post.query.all()
    # argument can be any name, which we can access by his name in the template
    return render_template("home.html", posts=posts)