from flask import Flask
from my_app.product.views import product


app = Flask(__name__)
app.register_blueprint(product)

@app.template_filter('mydouble')
def mydouble_filter(n:int):
    return n*2

