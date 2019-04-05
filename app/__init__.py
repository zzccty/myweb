from flask import Flask, render_template
from config import Config
from flask_bootstrap import Bootstrap


app = Flask('app')
app.config.from_object(Config)
bootstrap = Bootstrap(app)

@app.route('/')
def sayHello():
    return render_template('index.html')

print(app.config['SECRET_KEY'])

