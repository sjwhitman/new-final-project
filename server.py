from flask import Flask, render_template, request, session, redirect, flash
from crud import get_tasks, add_task, delete_task, update_task, add_user,get_user_by_email
from model import db, connect_to_db, Task, User


app = Flask(__name__)
app.secret_key = "dev"
# app.jinja_env.undefined = StrictUndefined


@app.route("/")
def homepage():
    """View homepage."""
    tasks = get_tasks()
    return render_template('homepage.html', tasks=tasks)

#routes for task list
@app.route("/add_task", methods=['POST'])
def add_tasks_route():
    task_name = request.form.get('task_name')
    add_task(name=task_name)
    return redirect('/')

@app.route("/delete_task/<int:task_id>", methods=['GET', 'POST'])
def delete_task_route(task_id):
    delete_task(task_id=task_id)
    return redirect('/')

#routes for user accounts
@app.route("/create_user", methods=["POST"])
def register_user():
    """Create a new user."""

    email = request.form.get("email")
    password = request.form.get("password")
    username = request.form.get("username")

    user = get_user_by_email(email)
    if user:
        flash("Cannot create an account with that email. Try again.")
    else:
        add_user(username, email, password)
        # db.session.add(user)
        # db.session.commit()
        flash("Account created! Please log in.")

    return redirect("/")

@app.route("/login", methods=["GET","POST"])
def process_login():
    """Process user login."""

    email = request.form.get("email")
    password = request.form.get("password")

    user = get_user_by_email(email)
    if not user or user.password != password:
        flash("The email or password you entered was incorrect.")
    else:
        # Log in user by storing the user's email in session
        session["user_email"] = user.email
        flash(f"Welcome back, {user.username}!")

    return redirect("/")
@app.route("/profile")
def profile():
    """Route to view user profile."""
    if "user_email" not in session:
        flash("You must be logged in to view your profile.")
        return redirect("/login")

    # is this grabbing user.email?
    email = session["user_email"]
    user = get_user_by_email(email)

    if not user:
        flash("User not found.")
        return redirect("/")

    return render_template('profile.html', user=user)

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
    app.app_context().push()