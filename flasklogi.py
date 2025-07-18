from flask import Flask
from flask_login import LoginManager, UserMixin, login_required, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hjyfwe34689ijkyurdgjnmm'
login_manager = LoginManager() #initializing the login manager(instance of LoginManager class)
login_manager.init_app(app) #binding it to the app



class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/dashboard')
@login_required
def dashboard():
    return f'Hello, {current_user.username}!'