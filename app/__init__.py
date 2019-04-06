from flask import Flask, render_template
from config import Config
from flask_bootstrap import Bootstrap

concise
bootstrap = Bootstrap(app)

@app.route('/')
def sayHello():
    return render_template('index.html')

print(app.config['SECRET_KEY'])

