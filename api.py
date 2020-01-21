from flask import Flask, render_template

from server.run import TextGenerator

app = Flask(__name__)


@app.route("/bibleGen")
def hello():
    wc = TextGenerator()
    context = {
        'Novo Evangelho': wc.get_text()
    }
    return render_template('index.html', context=context)


if __name__ == "__main__":
    app.run(debug=True, threaded=False)
