from flask import Flask, request, jsonify, render_template_string
import random
import string

app = Flask(__name__)

# Store HTML code temporarily (in-memory for demo purposes)
html_storage = {}

# Function to generate a random temporary URL
def generate_random_url():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

# Route to serve the HTML form for users to input their HTML
@app.route('/html', methods=['GET'])
def index():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Test Your HTML</title>
      <style>
        body {
          font-family: Arial, sans-serif;
          background: #f4f4f4;
          color: #333;
          text-align: center;
          margin: 0;
          padding: 20px;
        }

        h1 {
          font-size: 2rem;
        }

        textarea {
          width: 80%;
          height: 200px;
          margin: 20px 0;
          padding: 10px;
          font-size: 1rem;
          border: 1px solid #ccc;
          border-radius: 5px;
        }

        button {
          padding: 10px 20px;
          font-size: 1rem;
          cursor: pointer;
          background-color: #007BFF;
          color: white;
          border: none;
          border-radius: 5px;
        }

        button:hover {
          background-color: #0056b3;
        }

        .link {
          margin-top: 20px;
          font-size: 1.1rem;
          color: #007BFF;
        }
      </style>
    </head>
    <body>
      <h1>Test Your HTML</h1>
      <form action="/html/testhtml" method="post">
        <textarea name="html_code" placeholder="Paste your HTML code here..."></textarea><br>
        <button type="submit">Make Temporary Webpage</button>
      </form>
    </body>
    </html>
    ''')

# Route to handle HTML code submission and generate the temporary URL
@app.route('/html/testhtml', methods=['POST'])
def test_html():
    html_code = request.form.get("html_code", "")
    if not html_code:
        return jsonify({"error": "No HTML code provided!"}), 400

    # Generate a random URL for the test
    temp_url = generate_random_url()

    # Store the HTML code in the dictionary (you might want to use a database for production)
    html_storage[temp_url] = html_code

    # Return the test URL
    return jsonify({"link": f"/html/{temp_url}"}), 200

# Route to show HTML code from the temporary URL
@app.route('/html/<temp_url>', methods=['GET'])
def show_html(temp_url):
    # Retrieve the HTML code from storage using the temp URL
    html_code = html_storage.get(temp_url)

    if not html_code:
        return "This URL is not valid or has expired.", 404

    # Display the stored HTML code
    return html_code

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
