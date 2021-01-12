from flask import Flask, render_template, request, jsonify
import json
from a_star import *

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/runAStar", methods=["POST"])
def runAStar():
    print(json.loads(request.form["heuristicInfo"]))
    # print(AStar(json.loads(request.form['graph']),json.loads(request.form['heuristicInfo'])))
    return jsonify(
        AStar(
            json.loads(request.form["graph"]), json.loads(request.form["heuristicInfo"])
        )
    )
    # return [1,2]


if __name__ == "__main__":
    app.run(debug=True)