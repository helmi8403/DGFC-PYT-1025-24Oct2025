from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta, date

app = Flask(__name__)

# -------- Sample data --------
today = date.today()
tasks = [
    {
        "id": 1,
        "title": "Submit Project Report",
        "description": "Upload project deliverables to the portal.",
        "priority": "High",
        "deadline": today + timedelta(days=10),
        "completed": False,
    },
    {
        "id": 2,
        "title": "Prepare Final Presentation",
        "description": "Tighten slides; rehearse demo flow.",
        "priority": "Medium",
        "deadline": today,
        "completed": False,
    },
    {
        "id": 3,
        "title": "Prepare documentation",
        "description": "clean up docs",
        "priority": "Low",
        "deadline": today - timedelta(days=1),
        "completed": False,
    },
]

def days_left_for(d):
    return (d - date.today()).days

# -------- Routes --------
@app.route("/")
def index():
    active = [t for t in tasks if not t.get("completed")]
    for t in active:
        t["days_left"] = days_left_for(t["deadline"])
    return render_template("index.html", tasks=active)

@app.route("/add", methods=["GET", "POST"])
def add_task():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        priority = request.form.get("priority", "").strip()
        deadline = request.form.get("deadline", "").strip()
        if not title or not deadline or not priority:
            return "All fields are required.", 400
        try:
            deadline_date = datetime.strptime(deadline, "%Y-%m-%d").date()
        except ValueError:
            return "Invalid date format (YYYY-MM-DD).", 400

        new_id = max([t["id"] for t in tasks]) + 1 if tasks else 1
        tasks.append({
            "id": new_id,
            "title": title,
            "description": description,
            "priority": priority,
            "deadline": deadline_date,
            "completed": False,
        })
        return redirect(url_for("index"))
    return render_template("add_task.html")

@app.route("/edit/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        return "Task not found", 404
    if request.method == "POST":
        task["title"] = request.form.get("title", "").strip()
        task["description"] = request.form.get("description", "").strip()
        task["priority"] = request.form.get("priority", "").strip()
        task["deadline"] = datetime.strptime(request.form.get("deadline"), "%Y-%m-%d").date()
        return redirect(url_for("index"))
    return render_template("edit_task.html", task=task)

@app.route("/complete/<int:task_id>")
def complete_task(task_id):
    for t in tasks:
        if t["id"] == task_id:
            t["completed"] = True
            break
    return redirect(url_for("index"))

@app.route("/completed")
def completed_tasks():
    done = [t for t in tasks if t.get("completed")]
    return render_template("completed_tasks.html", tasks=done)

@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    global tasks
    tasks = [t for t in tasks if t["id"] != task_id]
    return redirect(url_for("index"))

@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def api_delete_task(task_id):
    global tasks
    before = len(tasks)
    tasks = [t for t in tasks if t["id"] != task_id]
    deleted = len(tasks) < before
    return {"ok": deleted}


@app.route("/profile")
def profile():
    p = {
        "name": "Muhammad Ismani Helmi",
        "avatar": "helmi.jpg",  # put this image in /static
        "certs": ["AWS", "Azure", "ITIL", "SCRUM Master"],
        "skills": [
            "AWS (EC2, VPC, RDS, ELB, SQS, Lambda, Route 53)",
            "Azure (AKS, VNet, VM, Storage)",
            "Windows Server 2016/2019 & RHEL",
            "VMware, Hyper-V, KVM",
            "Terraform, Ansible",
            "Monitoring: Grafana, Prometheus, CloudWatch",
            "Security Hardening & VAPT remediation",
        ],
        "achievements": [
            "HDB Infoweb & e-Service (July 2025)",
            "MHA NS Portal (July 2024)",
            "GovTech (Data Science and AI Division) jupyter notebook (Jun 2023)",
            "GovTech (Data Science and AI Division) centralise Automated Baseline Log Review (Dec 2023)",
            "Consumer Product Safety & Accuracy+ portal (Dec 2021)",
            "Enterprise Singapore website (Mar 2022)",
            "Enterprise Singapore Incentive Portal (Oct 2022)",
            "Spearheaded Cumulus (PGP) & SFTP automation",
            "AWS GCC ops at GovTech; VAPT remediation",
            "AAP + Prometheus + Grafana integration demo",
        ],
    }
    return render_template("profile.html", p=p)


if __name__ == "__main__":
    app.run(debug=True)
