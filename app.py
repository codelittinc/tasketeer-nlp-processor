from flask import Flask
from src.controllers.file_index_controller import file_index_bp
import os

app = Flask(__name__)

app.register_blueprint(file_index_bp)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)