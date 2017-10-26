from flask import Flask, request, redirect, render_template, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:password@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = '1234'


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text(1000))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))


    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120))
    password = db.Column(db.String(120))
    email = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'index', 'main_page', 'individual', 'singleblog']
    if request.endpoint not in allowed_routes and 'email' not in session:
        return redirect('/login')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            session['email'] = email
            session['username'] = username
            return redirect('/')
        else:
            return '<h1>Error!</h1>'

    return render_template('login.html')

@app.route('/', methods=['POST', 'GET'])
def index():   

    authors = User.query.all()
    return render_template('index.html', title="Blog users!", authors=authors)

@app.route('/blog', methods=['POST', 'GET'])
def main_page():
    
    blogs = Blog.query.all()
    

    return render_template('blog.html', blogs=blogs)

@app.route('/individual', methods=['POST', 'GET']) 
def individual():

    if request.method == 'GET':
        id =  request.args.get('id')
        owner = User.query.filter_by(id=id).first()
        blogs = Blog.query.filter_by(owner=owner).all()
        return render_template('individual_user.html', title = 'Your Blogs', blogs = blogs)
    
    else:
        return render_template('individual_user.html')


@app.route('/new-post', methods=['POST', 'GET'])
def new_post():

    owner = User.query.filter_by(username=session['username']).first()

    if request.method == 'POST':
        blog_title = request.form['title']
        blog_body = request.form['new-blog']       
        title_error = ''
        body_error = ''
        post = Blog(blog_title, blog_body, owner)
        db.session.add(post)
        db.session.commit()
        
        def empty(x):
            if x=='':
                return True
        if empty(blog_title):
            title_error ="please fill"
        if empty(blog_body):
            body_error = 'please fill'
        if not title_error and not body_error:
            return redirect('/single_blog?id=' + str(post.id))

        else:
            return render_template('newpost.html', title=blog_title, title_error=title_error, body=blog_body, body_error=body_error, owner=owner)
    else:
        return render_template('newpost.html')




@app.route('/sign_up', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        verify = request.form['verify']

        # TODO-validate user's data

        existing_user = User.query.filter_by(email=email).first()
        if not existing_user:
            new_user = User(username, email, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = request.form['username']
            session['email'] = request.form['email']
            return redirect('/')
        else:
            return '<h1>Duplicate user</h1>'

    return render_template('signup.html')

@app.route('/logout')
def logout():
    del session['email']
    return redirect('/')


@app.route('/single_blog')
def singleblog():

    id = request.args.get('id')
    blog = Blog.query.filter_by(id=id).first()
       
    return render_template('single-blog.html', blog=blog)

if __name__ == '__main__':
    app.secret_key = '1234'
    app.run()




