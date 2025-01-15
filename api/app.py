# from flask import Flask, render_template, request, jsonify

# app = Flask(__name__)

# # Route for the frontend
# @app.route('/')
# def home():
#     return render_template('index.html')

# # API endpoint to process user input
# @app.route('/api/message', methods=['POST'])
# def process_message():
#     data = request.get_json()
#     user_message = data.get('message', '')
#     response_message = f"You said: {user_message}"
#     return jsonify(response=response_message)

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, render_template_string, request, jsonify
from flask import send_from_directory
import threading

# Flask App Setup
app = Flask(__name__)

# HTML Template (Frontend)
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Interactive Message App</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            background-color: #f4f4f9;
            color: #333;
            margin: 0;
            padding: 0;
        }
        #app {
            margin-top: 100px;
        }
        input {
            padding: 10px;
            font-size: 16px;
            width: 300px;
            margin-right: 10px;
        }
        button {
            padding: 10px 20px;
            font-size: 16px;
            cursor: pointer;
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 5px;
        }
        button:hover {
            background-color: #0056b3;
        }
        p {
            margin-top: 20px;
            font-size: 18px;
        }
    </style>
</head>
<body>
    <div id="app">
        <h1>Interactive Message App</h1>
        <input type="text" id="userInput" placeholder="Enter your message" />
        <button id="sendButton">Send Message</button>
        <p id="response"></p>
    </div>
    <script>
        document.getElementById('sendButton').addEventListener('click', () => {
            const userInput = document.getElementById('userInput').value;

            if (userInput.trim() === '') {
                document.getElementById('response').textContent = 'Please enter a message.';
                return;
            }

            fetch('/api/message', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: userInput }),
            })
                .then(response => response.json())
                .then(data => {
                    document.getElementById('response').textContent = data.response;
                })
                .catch(error => {
                    console.error('Error sending message:', error);
                    document.getElementById('response').textContent = 'An error occurred.';
                });
        });
    </script>
</body>
</html>
"""

# Flask Routes
@app.route('/')
def home():
    return render_template_string(html_template)

@app.route('/api/message', methods=['POST'])
def process_message():
    data = request.get_json()
    user_message = data.get('message', '')
    response_message = f"You said: {user_message}"
    return jsonify(response=response_message)

# Run Flask App in a Separate Thread
def run_app():
    app.run(debug=False, use_reloader=False)

thread = threading.Thread(target=run_app)
thread.start()
