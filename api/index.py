from flask import Flask



app = Flask(__name__)

#home
@app.route('/')
def home():
    return 'Api is running somewhere!'




#dont touch this thing
if __name__ == '__main__':
    app.run(port=3000)
