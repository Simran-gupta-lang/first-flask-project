from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define the Todo model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Todo {self.id} - {self.title}>"

# Home route: add & display todos
@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        title = request.form.get('title')
        desc = request.form.get('desc')
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
        return redirect("/")

    allTodo = Todo.query.all()
    return render_template('index.html', allTodo=allTodo)

# Example route: just shows all todos in console
@app.route("/show")
def show():
    allTodo = Todo.query.all()
    print(allTodo)
    return "This is the show page"

# Update route placeholder
@app.route("/update")
def update():
    return "This is the update page"

# Delete a todo
@app.route("/delete/<int:id>")
def delete(id):
    todo = Todo.query.filter_by(id=id).first()
    if todo:
        db.session.delete(todo)
        db.session.commit()
    return redirect("/")

# Run the application
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Ensure tables are created
    app.run(debug=True, port=3000)
