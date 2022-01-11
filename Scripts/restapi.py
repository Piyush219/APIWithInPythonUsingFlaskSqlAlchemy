
from datetime import date
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
 
 
 

app = Flask(__name__) #initializing flask app
 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://sql6464698:rKktgJpZmj@sql6.freesqldatabase.com/sql6464698' #It's a free online database created for the project
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 
 
db = SQLAlchemy(app)
ma = Marshmallow(app)
 
 
#this is our database model
class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    checked = db.Column(db.Boolean)
    name = db.Column(db.String(100))
    type = db.Column(db.String(100))
    age = db.Column(db.Numeric)
    description = db.Column(db.String(200))
    date = db.Column(db.Date)
 
 
    def __init__(self, checked, name, type, age, description, date):
        self.checked = checked
        self.name = name
        self.type = type
        self.age = age
        self.description = description
        self.date = date
 
 
class PostSchema(ma.Schema):
    class Meta:
        fields = ("checked", "name", "type", "age", "description", "date")
 
 
post_schema = PostSchema()
posts_schema = PostSchema(many=True)
 
 
 
 
 
#adding a post

@app.route('/')
def hello_world():
    return 'Use get request to see all the data'

@app.route('/post', methods = ['POST'])
def add_post():
    checked = request.json['checked']
    name = request.json['name']
    type = request.json['type']
    age = request.json['age']
    description = request.json['description']
    date = request.json['date']
 
    my_posts = Post(checked, name, type, age, description, date)
    db.session.add(my_posts)
    db.session.commit()
 
    return post_schema.jsonify(my_posts)
 
 
 
 
#getting posts
@app.route('/get', methods = ['GET'])
def get_post():
    all_posts = Post.query.all()
    result = posts_schema.dump(all_posts)
 
    return jsonify(result)
 
 
#getting particular post
@app.route('/post_details/<id>/', methods = ['GET'])
def post_details(id):
    post = Post.query.get(id)
    return post_schema.jsonify(post)
 
 
#updating post
@app.route('/post_update/<id>/', methods = ['PUT'])
def post_update(id):
    post = Post.query.get(id)
 
    checked = request.json['checked']
    name = request.json['name']
    type = request.json['type']
    age = request.json['age']
    description = request.json['description']
    date = request.json['date']
 
 
    post.checked = checked
    post.name = name
    post.type = type
    post.age = age
    post.description = description
    post.date = date
 
    db.session.commit()
    return post_schema.jsonify(post)
 
 
 
#deleting post
@app.route('/post_delete/<id>/', methods = ['DELETE'])
def post_delete(id):
    post = Post.query.get(id)
    db.session.delete(post)
    db.session.commit()
 
    return post_schema.jsonify(post)
 
 
 
 
if __name__ == "__main__":
    app.run(debug=True)
