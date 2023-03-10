from flask import Flask
from src.controllers.file_index_controller import file_index_bp
from src.controllers.search_controller import search_bp
import os

# set flask app
app = Flask(__name__)

# register blueprints (controllers)
app.register_blueprint(file_index_bp)
app.register_blueprint(search_bp)

# start server
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)