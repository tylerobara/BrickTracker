from flask import Flask, request, jsonify, render_template
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html') 

#'Welcome to the Flask App'


@app.route('/saveNumber', methods=['POST'])
def save_number():
    data = request.get_json()
    number = request.form.get('numberInput')

    if number is not None:
        # Save number to JSON file
        with open('data.json', 'w') as json_file:
            json.dump({'number': number}, json_file)
        return jsonify({'message': 'Number saved successfully'}), 200
    else:
        return jsonify({'error': 'Invalid data provided'}), 400

if __name__ == '__main__':
    app.run(debug=True)
