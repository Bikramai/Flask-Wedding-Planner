from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user

from .extns import db
from .model import Todo

todo = Blueprint("todo", __name__, url_prefix="/todo")


@todo.route("/")
@login_required
def index():
    return render_template("todo/todo.html")


@todo.post("/add")
@login_required
def add():
    title = request.form.get("title")
    description = request.form.get("description")

    new_todo = Todo(title=title, description=description, account_id=current_user.id)
    db.session.add(new_todo)
    db.session.commit()

    flash("Todo Added Successfully", "success")
    return redirect(url_for("todo.index"))


@todo.post("/update")
@login_required
def update():
    todo_id = request.form.get("todo")
    title = request.form.get("title")
    description = request.form.get("description")

    todo = Todo.query.get(todo_id)
    todo.title = title if title else todo.title
    todo.description = description if description else todo.description
    db.session.commit()

    flash("Todo Updated Successfully", "info")
    return redirect(url_for("todo.index"))


@todo.get("/delete/<todo_id>")
@login_required
def delete(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    db.session.delete(todo)
    db.session.commit()

    flash("Todo Deleted Successfully", "danger")
    return redirect(url_for("todo.index"))
