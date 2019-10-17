from datetime import datetime
from flaskblogmy import db, login_manager
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app


# user_loader is for reloading user from user_id stored in the session (from website). Function to get a user by id for loginManager to find by decorator
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) #

# class as a database structure, each class own table in database
class User(db.Model, UserMixin): # db.Model lets know this is a table. 4 methods expected in loginManager - is_authenticated, is_active, is_anonymous, get_id - instead class from extention UserMixin
    # now adding columns for this table
    id = db.Column(db.Integer, primary_key = True) # - primary key = "unique id for user"
    username = db.Column(db.String(20), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    image_file = db.Column(db.String(20), nullable = False, default = 'default.jpg')
    password = db.Column(db.String(60), nullable = False)
    posts = db.relationship('Post', backref = 'author', lazy = True) # Cant be seen in SQL file 1 - relation to post model, 2 - get author from post, 3 - ability to get all post by user

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            # load basically loads what was dumped. Dumping means creating token from some value, by some rule, which is aecret key
            user_id = s.loads(token)['user_id'] # meaning if I know token I get to know the value in  the key 'user_id' which is self.id.
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    date_posted = db.Column(db.DateTime, nullable = False, default = datetime.utcnow) #not utcnow() - need to import as a function
    content = db.Column(db.Text, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False) # lower case u! for table.column name, not class

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

