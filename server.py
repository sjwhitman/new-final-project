from flask import Flask, render_template, request, session, redirect, flash, jsonify
from crud import get_tasks, add_task, delete_task, update_task, add_user,get_user_by_email
from model import db, connect_to_db, Task, User


app = Flask(__name__)
app.secret_key = "dev"
# app.jinja_env.undefined = StrictUndefined


@app.route("/")
def homepage():
    """View homepage."""
    return render_template('homepage.html')

#routes for task list
@app.route("/add_task", methods=['POST'])
def add_tasks_route():
    task_name = request.json.get('name_input')
    task_description = request.json.get('description_input')
    timer_type = request.json.get('type_input')
    duration = request.json.get('duration_input')
    print("Form info from AJAX call *****************************************************************")
    print(task_name, task_description, timer_type, duration)
    #add task to db
    object_name = add_task(task_name=task_name, task_description=task_description, timer_type=timer_type, duration=duration, user_id=session['user_id'])
    
    #turn info into dictionary so it can be used with jsonify
    task_info = {
            "task_id": object_name.task_id,
            "task_name": object_name.task_name,
            "task_description": object_name.task_description,
            "timer_type": object_name.timer_type,
            "duration": object_name.duration
        }
    print("Our dictionary")
    print(task_info)
    return jsonify(task_info)

@app.route("/delete_task/<int:task_id>", methods=['POST'])
def delete_task_route(task_id):
    delete_task(task_id=task_id)
    return redirect('/profile')

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

@app.route("/login", methods=["POST"])
def process_login():
    """Process user login."""
    #triggers when user enters in email and password

    email = request.form.get("email")
    password = request.form.get("password")

    user = get_user_by_email(email)
    #in the case of incorrect credentials
    if not user or user.password != password:
        flash("The email or password you entered was incorrect.")
    else:
        # stored the user's email in session object
        session["user_email"] = user.email
        session["user_id"] = user.user_id
        flash(f"Welcome back, {user.username}!")
        print(session["user_email"])
        print("************************************************************************************")
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

    tasks = get_tasks(session['user_id'])

    if not user:
        flash("User not found.")
        return redirect("/")
    
    return render_template('profile.html', tasks=tasks, user=user)
    # return render_template('profile.html', tasks=tasks, user=user)

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
    
@app.route("/logout", methods=["POST"])
def logout():
    #get the user info fromm the session
    # session["user_email"]
    #is the user logged in? is the users data in the session
    if "user_email" in session:
        #if the user is logged in, remove their email and username from the session?
        #notify the user that they are logged out
        session.pop('user_email', None)
        flash("You are logged out")
    #redirect to homepage
    return redirect("/")

#view function for all user info
@app.route("/api/user_info")
def get_user_info():
    #check if user is logged in
    if "user_email" not in session:
        return flash("user not logged in")

    #grab user email from session and user object from db
    email = session["user_email"]
    user = get_user_by_email(email)

    # jsonify searches db for user instance and constructs a json response if user is found
    return jsonify({
        "email": user.email,
        "username": user.username,
        "theme_preference": user.theme_preference,
        "work_session_time": user.work_session_time,
        "break_session_time": user.break_session_time
    })

@app.route("/get_tasks", methods=['GET'])
#used get instead of post
def get_tasks_route():
    """Fetch tasks for the logged-in user."""
    if "user_id" not in session:
        return jsonify([])  # Return an empty list if the user is not logged in

    #get user_id from session object
    user_id = session["user_id"]

    #get tasks by selecting via user id
    tasks = get_tasks(user_id)

    # store data as list
    task_data = []
    for task in tasks:
        task_info = {
            "task_id": task.task_id,
            "task_name": task.task_name,
            "task_description": task.task_description,
            "timer_type": task.timer_type,
            "duration": task.duration
        }
    task_data.append(task_info)

    #return task data as json
    return jsonify(task_data)

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
    app.app_context().push()