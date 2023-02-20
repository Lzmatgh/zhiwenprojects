from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flaskext.mysql import MySQL

import openai

app = Flask(__name__)
app.config['SECRET_KEY'] = "ThisIsMySecret"


CORS(app, origins=['http://localhost:3001'])

# Configure MySQL
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'chatgpt'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql = MySQL(app)

# Configure the OpenAI API key
openai.api_key = "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"


@app.route('/')
def index():
    return 'Hello, World!'


@app.route('/signup', methods=['POST'])
def signup():
    username = request.json.get('username')
    password = request.json.get('password')
    email = request.json.get('email')

    try:
        # Connect to the database
        conn = mysql.connect()
        cursor = conn.cursor()

        # Save the user's sign up information to the database
        sql = "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)"
        cursor.execute(sql, (username, password, email))
        conn.commit()

        # Close the database connection
        cursor.close()
        conn.close()
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

    # Save the user's information in the session
    session['username'] = username
    session['email'] = email

    return jsonify({"success": True, "error": None})


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        # check if user is in session
        username = request.args.get("username")
        if 'username' in session and username in session['username']:
            return jsonify({"username": username, "error": None})
        return jsonify({"username": None, "error": None})

    username = request.json.get('username')
    password = request.json.get('password')

    # TODO: Add code here to check the username and password against the database
    # Return error if it doesn't match
    cur = mysql.connection.cursor()
    cur.execute("SELECT username, password FROM users")
    signup_data = cur.fetchall()
    cur.close()
    flag = 0
    for each_user_data in signup_data:
        if username == each_user_data[0]:
            if password == each_user_data[1]:
                flag = 1
                break
    if flag == 0:
        return jsonify({"success": None, "error": True})

    # TODO: If the username and password are correct, set the username in the session
    if flag == 1:
        session['username'] = username

    return jsonify({"success": True, "error": None})


# TODO: Create logout api
# you should retrieve the username from the request, pop it from the session if it's in the session
# then return a result
@app.route("/logout", methods=['GET', 'POST'])
def logout():
    if request.method == 'GET':
        # check if user is in session
        username = request.args.get("username")
        if 'username' in session and username in session['username']:
            session['username'] = None
            return jsonify({"username": username, "error": None})
        return jsonify({"username": None, "error": None})


@app.route("/chat", methods=["POST"])
def chat():
    # Get the inputs from the request
    # username = request.json["user_id"]
    question = request.json.get("input")

    # Use OpenAI's language generation API to generate a response
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt='You: ' + question,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    ).choices[0].text

    # Remove the "You: " prefix from the response
    response = response.replace("You: ", "")

    # TODO save the chat history into database
    cur = mysql.connection.cursor()
    # create a new column
    cur.execute(f"alter table chat_table add {session['username']} LONGTEXT null;")
    # insert the chat history for the new column
    sql = f"INSERT INTO chat_table ({session['username']}) VALUES (%s)"
    cur.execute(sql, (response))
    mysql.connection.commit()
    cur.close()

    # Return the response as JSON
    return jsonify({"response": response})


# TODO: Create chat_history API that returns chat history for the specified user
@app.route("/chat_history", methods=["POST"])
def chat_history():
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT {session['username']} FROM chat_table")
    chat_history = cur.fetchall()
    cur.close()

    return jsonify({"chat history": chat_history})






if __name__ == "__main__":
    app.run(debug=True, host='localhost',port=4444)




