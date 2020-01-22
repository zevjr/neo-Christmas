from flask import Flask, render_template

from server.run import TextGenerator

app = Flask(__name__)


@app.route("/")
def menu():
    return render_template('index.html')


@app.route("/bibleGen")
def bible_gen():
    wc = TextGenerator()
    context = {
        'Novo Evangelho': wc.get_text()
    }
    return render_template('bible.html', context=context)


if __name__ == "__main__":
    app.run(debug=True, threaded=False)
