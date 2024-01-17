from flask import Flask, render_template, request, session, redirect
from db_init import get_tasks, add_task, update_task, delete_task

app = Flask(__name__)
app.secret_key = "dev"
# app.jinja_env.undefined = StrictUndefined


@app.route("/")
def homepage():
    """View homepage."""
    tasks = get_tasks()
    return render_template('homepage.html', tasks=tasks)

@app.route("/add_task", methods=['POST'])
def add_tasks_route():
    task_name = request.form.get('task_name')
    add_task(name=task_name)
    return redirect('/')

@app.route("/delete_task/<int:task_id>", methods=['GET', 'POST'])
def delete_task_route(task_id):
    delete_task(task_id=task_id)
    return redirect('/')

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)