import csv
import io
import pygal
from pygal.style import CleanStyle

from flask import Flask, render_template, Response, request, redirect

from regress import RegressException
from regress.database import create_model, read_model, read_all_models
from regress.model import Model


app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


def model_to_svg(model):
    chart = pygal.XY(stroke=False, style=CleanStyle, x_title=model.x_title, y_title=model.y_title)
    chart.add("data", list(zip(model.x_val, model.y_val)))
    chart.add("predictions", list(zip(model.x_val, model.p_val)), stroke=True)
    return chart.render()


def model_to_csv(model):
    fp = io.StringIO()
    writer = csv.DictWriter(fp, fieldnames=[model.x_title, model.y_title, "p_value"])
    writer.writeheader()
    for entry in model.data():
        writer.writerow({model.x_title: entry[0], model.y_title: entry[1], "p_value": entry[2]})
    return fp.getvalue()


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html", section="home", model=None, models=None)


@app.route("/upload", methods=["POST"])
def upload_csv():
    file = request.files["file"]
    if file and file.filename.split(".")[-1] in ["csv"]:
        model = Model(
            name=request.form["name"],
            x_title=request.form["x_field"],
            y_title=request.form["y_field"],
            description=request.form["description"]
        )
        for row in csv.DictReader(io.TextIOWrapper(file, encoding="utf-8")):
            x_val = float(row.get(model.x_title))
            y_val = float(row.get(model.y_title))
            model.add(x_val=x_val, y_val=y_val)
        model.regress()
        create_model(model)
    return redirect("/models/{}".format(request.form["name"]))


@app.route("/download/<name>", methods=["GET"])
def download_csv(name):
    try:
        model = read_model(name)
    except RegressException:
        return render_template("index.html", section="not_found"), 404
    return model_to_csv(model)


@app.route("/models", methods=["GET"])
def render_models():
    return render_template("index.html", section="models", model=None, models=read_all_models())


@app.route('/models/<name>', methods=["GET"])
def render_model(name):
    model = None
    try:
        model = read_model(name)
    except RegressException:
        render_template("index.html", section="not_found")
    return render_template("index.html", section="models", model=model)


@app.route('/1/models/<name>/chart', methods=["GET"])
def chart_svg(name):
    try:
        return Response(model_to_svg(read_model(name)), mimetype="image/svg+xml")
    except RegressException:
        return "", 404


