from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

tasks = []

# -------------------------------
# Function to add a task
# -------------------------------
@app.route('/add', methods=['GET', 'POST'])
def add_task():
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        priority = request.form.get("priority")
        deadline = request.form.get("deadline")

        if not title or not deadline or not priority:
            return "Error: All fields are required!", 400

        try:
            deadline_date = datetime.strptime(deadline, "%Y-%m-%d").date()
        except ValueError:
            return "Invalid date format!", 400

        task = {
            "id": len(tasks) + 1,
            "title": title,
            "description": description,
            "priority": priority,
            "deadline": deadline_date
        }

        tasks.append(task)
        return redirect(url_for("index"))

    return render_template("add_task.html")

# -------------------------------
# Function to view tasks
# -------------------------------

@app.route('/')
def index():
    today = datetime.today().date()

    for task in tasks:
        days_left = (task["deadline"] - today).days
        task["days_left"] = days_left

    return render_template("index.html", tasks=tasks, current_date=today)


# -------------------------------
# Function to edit/update task
# -------------------------------
@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    task = next((t for t in tasks if t["id"] == task_id), None)

    if not task:
        return "Task not found", 404

    if request.method == "POST":
        task["title"] = request.form.get("title")
        task["description"] = request.form.get("description")
        task["priority"] = request.form.get("priority")
        task["deadline"] = datetime.strptime(request.form.get("deadline"), "%Y-%m-%d").date()

        return redirect(url_for("index"))

    return render_template("edit_task.html", task=task)

# -------------------------------
# Function to remove a task
# -------------------------------
@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task["id"] != task_id]
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)


