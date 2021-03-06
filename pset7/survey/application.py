import cs50
import csv

from flask import Flask, jsonify, redirect, render_template, request

# Configure application
app = Flask(__name__)


# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    """Disable caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
def get_index():
    return redirect("/form")


@app.route("/form", methods=["GET"])
def get_form():
    return render_template("form.html")


@app.route("/form", methods=["POST"])
def post_form():
    # file = open("survey.csv","a")
    # writer = csv.writer(file)
    # writer.writerow((request.form.get("fn"),request.form.get("ln"),request.form.get("un"),request.form.get("ph"),
    # request.form.get("bd"),request.form.get("ea"),request.form.get("jp")))
    # file.close()
    if(not request.form.get("jp")):
        return render_template("error.html")
    with open("survey.csv","a") as file:
        writer = csv.writer(file)
        writer.writerow((request.form.get("fn"),request.form.get("ln"),request.form.get("un"),
            request.form.get("ph"),request.form.get("bd"),request.form.get("ea"),request.form.get("jp")))

    return render_template("success.html", message="TODO")


@app.route("/sheet", methods=["GET"])
def get_sheet():
    with open("survey.csv","r") as file:
        reader = csv.reader(file)
        mbs = list(reader)
    return render_template("sheet.html",mbs = mbs)
