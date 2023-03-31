from flask import Flask
from azan_scheduler import AzanScheduler

app = Flask(__name__)

azan_scheduler = AzanScheduler()


@app.route("/")
def hello():
    job_list = azan_scheduler.get_scheduled_job_list()
    return f"<h1>Azan App</h1><h3>Job List: {job_list}</h3>"


if __name__ == "__main__":
    app.run(port=9000)
