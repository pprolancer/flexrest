from flask import Flask, Blueprint, redirect, url_for
from flask_login import LoginManager, current_user, login_user, logout_user, \
    login_required
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Unicode

from flexrest import RestApiResource, RestApiHandler, FlexRestManager

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(64), unique=True)
    password = Column(String(88))
    firstname = Column(Unicode(256))
    lastname = Column(Unicode(256))

    def get_id(self):
        return str(self.id)

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def is_active(self):
        return True

    def __repr__(self):
        return '<User %r>' % (self.username)


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True)
    author = Column(String(88))

    def __repr__(self):
        return '<book %r>' % (self.name)


engine = create_engine('sqlite:///:memory:', echo=True)
DBSession = sessionmaker(bind=engine)
Base.metadata.create_all(engine)


def get_session():
    return DBSession()

dbs = get_session()
u1 = User(username='user1')
u2 = User(username='user2')
b1 = Book(name='book1')
b2 = Book(name='book2')
dbs.add_all([u1, u2, b1, b2])
dbs.commit()


def load_user(uid):
    dbs = get_session()

    user = dbs.query(User).get(uid)
    if not user or not user.is_active():
        return None
    return user

app = Flask(__name__)
app.secret_key = 'secret'
lm = LoginManager()
lm.init_app(app)
lm.user_loader(load_user)
lm.session_protection = "strong"

flex = FlexRestManager(db_base=Base, db_session_callback=get_session)
flex.init_app(app)

user_bp = Blueprint('user_rest', __name__)


class UserRestApiHandler(RestApiHandler):
    resource_class = User

user_resource = RestApiResource(
    name="user",
    route="/user",
    app=user_bp,
    decorators=[login_required],
    handler=UserRestApiHandler())


book_bp = Blueprint('book_rest', __name__)


class BookRestApiHandler(RestApiHandler):
    resource_class = Book

book_resource = RestApiResource(
    name="book",
    route="/book",
    app=book_bp,
    handler=BookRestApiHandler())

app.register_blueprint(user_bp, url_prefix='/api/v1')
app.register_blueprint(book_bp, url_prefix='/api/v1')


@app.route('/login')
def login():
    dbs = get_session()
    user = dbs.query(User).first()
    login_user(user)
    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/')
def index():
    username = current_user.username if current_user.is_authenticated() \
        else 'N/A'
    return '''
    <h3> an example for flexrest </h3>
    <a href="/login"> login </a> | <a href="/logout"> logout </a>
    <p>Login by: <b>{username}</b></p>
    Books:
    <ul>
        <li><a href='/api/v1/book/'>Books list</a></li>
        <li><a href='/api/v1/book/1/'>Book#1</a></li>
        <li><a href='/api/v1/book/2/'>Book#2</a></li>
    </ul>
    Users(Need authorization):
    <ul>
        <li><a href='/api/v1/user/'>Users list</a></li>
        <li><a href='/api/v1/user/1/'>User#1</a></li>
        <li><a href='/api/v1/user/2/'>User#2</a></li>
    </ul>
    '''.format(username=username)

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=False)
