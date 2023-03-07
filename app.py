from flask import Flask, json
import os

app = Flask(__name__)

@app.route('/')
def home():
    response = app.response_class(
        response=json.dumps({'success':'true'}),
        mimetype='application/json'
    )
    return response


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)