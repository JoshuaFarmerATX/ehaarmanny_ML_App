from flask import Flask, url_for, render_template, request, redirect
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from covidSource import *


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        req = request.form
        qtype = req["qtype"]
        duration = req["duration"]
        region = req["region"]
        print(qtype, duration, region)
        return redirect(request.url)

    return render_template(
        "index.html",
        cases=apiData("global_totals/most_recent").get("cases"),
        recoveries=apiData("global_totals/most_recent").get("recoveries"),
        deaths=apiData("global_totals/most_recent").get("deaths"),
    )


@app.route("/team")
def team():
    return render_template("team.html")


@app.route("/community")
def community():
    return render_template("community.html")


if __name__ == "__main__":
    app.run(debug=True)
