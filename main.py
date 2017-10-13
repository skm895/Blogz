from flask import Flask, request, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:password@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text(1000))

    def __init__(self, title, body):
        self.title = title
        self.body = body
        

@app.route('/', methods=['POST', 'GET'])
def index():

    blogs = Blog.query.all()
    return render_template('blog.html', title="Build-a-Blog", blogs=blogs)

@app.route('/blog', methods=['POST', 'GET'])
def main_page():
    return redirect('/')

@app.route('/new-post', methods=['POST', 'GET'])
def new_post():

    if request.method == 'POST':
        blog_title = request.form['title']
        blog_body = request.form['new-blog']
        post = Blog(blog_title, blog_body)
        db.session.add(post)
        db.session.commit()
        return redirect('/single_blog?id=' + str(post.id))
    
    else:
    
        return render_template('newpost.html')

@app.route('/single_blog')
def singleblog():

    id = request.args.get('id')
    blog = Blog.query.filter_by(id=id).first()
       
    return render_template('single-blog.html', blog=blog)

if __name__ == '__main__':
    app.run()




