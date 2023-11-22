from flask import Flask, request
import yaml

config = None
with open("config.yaml", "r") as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)


app = Flask(__name__)


@app.route("/")
def hello_world():
    search = request.args.get("search")
    page = request.args.get("page")
    return f"<p>Hello, World!<br><br>{search} --> {page}</p>"


@app.route(config["post_endpoint"], methods=['POST'])
def receive_new_request():
    if request.method == "POST":
        user = request.form.get('user')
        pasw = request.form.get('pass')
        return f"{user} --> {pasw}"


# main driver function
if __name__ == '__main__':
    # run() method of Flask class runs the application
    # on the local development server.
    app.run(port=config['port'])
