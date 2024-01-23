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
    theme_preference = request.form.get("theme_preference")
    work_session_time = int(request.form.get("work_session_time"))
    break_session_time = int(request.form.get("break_session_time"))

    user = get_user_by_email(email)
    if user:
        flash("Cannot create an account with that email. Try again.")
    else:
        add_user(username, email, password, theme_preference, work_session_time, break_session_time)
        # db.session.add(user)
        # db.session.commit()
        flash("Account created! Please log in.")

    return redirect("/")

@app.route("/login", methods=["GET","POST"])
def process_login():
    """Process user login."""
    #triggers when user enters in email and password
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = get_user_by_email(email)
        #in the case of incorrect credentials
        if not user or user.password != password:
            flash("The email or password you entered was incorrect.")
        else:
            # stored the user's email in session object
            session["user_email"] = user.email
            flash(f"Welcome back, {user.username}!")
            return redirect("/profile")
    #if user cannot log in
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

@app.route("/update_profile", methods=["POST"])
def update_profile():
    #second check if user is logged in
    if "user_email" not in session:
        flash("You must be logged in to update your profile.")
        return redirect("/")

    #get user info
    email = session["user_email"]
    user = get_user_by_email(email)

    # update user db from form
    # user.theme_preference = request.form.get("theme_preference")
    # # user.work_session_time = int(request.form.get("work_session_time"))
    # # user.break_session_time = int(request.form.get("break_session_time"))

    # Update password if provided
    new_password = request.form.get("password")
    if new_password:
        user.password = new_password

    new_theme = request.form.get("theme_preference")
    if new_theme:
        user.theme_preference = new_theme
    
    new_work_time = request.form.get("work_session_time")
    if new_work_time:
        user.work_session_time = int(new_work_time)

    new_break_time = request.form.get("break_session_time")
    if new_break_time:
        user.break_session_time = int(new_break_time)

    #commit form data to db
    db.session.commit()
    flash("Profile updated successfully.")
    return redirect("/profile")


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
    app.app_context().push()