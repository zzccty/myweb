from flask import Flask
from config import Config


app = Flask('app')
app.config.from_object(Config)

@app.route('/')
def sayHello():
    return r'Hello world!'

print(app.config['SECRET_KEY'])

