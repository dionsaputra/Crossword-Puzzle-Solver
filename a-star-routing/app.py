from flask import Flask, render_template, request, jsonify
from graph import Graph
import json

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/shortest_route", methods=["POST"])
def sourtest_route():
    print(json.loads(request.form["heuristicInfo"]))
    input_graph = json.loads(request.form["graph"])
    input_heuristic = json.loads(request.form["heuristicInfo"])
    graph = Graph(input_graph)
    routes = graph.a_star(input_graph, input_heuristic)
    return jsonify(routes)


if __name__ == "__main__":
    app.run(debug=True)