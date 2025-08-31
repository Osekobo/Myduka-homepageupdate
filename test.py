# A class defines what an object should look like, and it defines the properties (attributes) and behaviors (methods) an object should have. And object is created based on that class. 
# Classes group data and behaviors into reusable components.
class MyClass:
  def __init__(self,name,age): #executed when the class is being initiated.
    self.name = name
    self.age = age

x = MyClass("John", 25)
# print(x.name)  # Output: John
# print(x.age)   # Output: 25



class MyClass2:
  def __init__(self,name,age): #It runs automatically when you create a new object from that class. It's called the constructor and  initializes each new object.
    self.name = name
    self.age = age

a = MyClass2("Jane", 30) # print(a.name)  # Output: Jane
# print(a.age)   # Output: 30

class MyClass3:
  def __init__(self,name,age):
    self.name = name
    self.age = age

  def __str__(self): #  controls what should be returned when the class object is represented as a string. If not set, the string representation of the object is returned
    return f"Name: {self.name}, Age: {self.age}"
b = MyClass3("Alice", 28)
# print(b)   Output: Name: Alice, Age: 28


# Object Methods
# Methods in objects are functions that belong to the object.

# The self Parameter
# used to access variables that belong to the class.
# has to be the first parameter of any function in the class

# Delete Object Properties
del b.age
# print(b)   Output: Name: Alice, Age: 28

# Delete Objects
del b

# The pass Statement to avoid getting an error.
















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










