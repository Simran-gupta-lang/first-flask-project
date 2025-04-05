from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'  # Database will be created in project root
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy with Flask app
db = SQLAlchemy(app)

# Define Todo model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Todo {self.id} - {self.title}>"

# Define routes
@app.route("/", methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        title = request.form.get('title')
        desc = request.form.get('desc')
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
        return redirect("/")  # Prevent form resubmission

    # Only run this for GET requests
    allTodo = Todo.query.all()
    return render_template('index.html', allTodo=allTodo)


@app.route("/show")
def products():
    allTodo = Todo.query.all()
    print(allTodo)
    return "This is the product page"

# Run the application
if __name__ == "__main__":
    app.run(debug=True, port=3000)
