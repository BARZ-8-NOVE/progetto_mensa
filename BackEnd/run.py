from flask_cors import CORS
from server import app

if __name__ == '__main__':
    CORS(app)
    app.run(debug=True)