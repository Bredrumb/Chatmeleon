from flask import Blueprint
from flask import Flask, render_template, url_for, redirect, request, session, jsonify, flash, Blueprint
from .database import DataBase

view = Blueprint("views", __name__) # Register blueprint as 'view'

NAME_KEY = 'name'
MSG_LIMIT = 20 # Maximum messages in display

@view.route("/login", methods=["POST", "GET"]) # When going to /login...
def login(): # The Login Page, inputted 'name' will serve as user's session identifier
    if request.method == "POST":  # If user inputs a name...
        name = request.form["inputName"]
        if len(name) >= 3:  # Name has to be longer than 2 characters
            session[NAME_KEY] = name # Signifies that user is logged in
            flash(f'You were successfully logged in as {name}.') # Displays pop-up (green by default)
            return redirect(url_for("views.home"))
        else:
            flash("1Sorry, your username has to be at least 3 characters!") # '1' prefix displays red alert pop-up

    return render_template("login.html", **{"session": session})


@view.route("/logout") # When going to /logout...
def logout(): # Logs user out, popping user's session identifier
    session.pop(NAME_KEY, None)
    flash("0You were logged out.") # '0' prefix displays red alert pop-up
    return redirect(url_for("views.login"))


@view.route("/")
@view.route("/home") # When going to / or /home...
def home(): # Displays chatroom, redirects to Login if user is not logged in
    if NAME_KEY not in session:
        return redirect(url_for("views.login"))

    return render_template("index.html", **{"session": session})

@view.route("/about") # When going to /about...
def about(): # Displays about page of Chatmeleon

    return render_template("about.html")


@view.route("/history")
def history(): # Displays history of user's messages 
    if NAME_KEY not in session:
        flash("0Please login before viewing message history")
        return redirect(url_for("views.login"))

    json_messages = get_history(session[NAME_KEY])
    print(json_messages)
    return render_template("history.html", **{"history": json_messages})


@view.route("/get_name") # Called by jquery in .static/index.js
def get_name(): # Get the name of logged in user 
    data = {"name": ""}
    if NAME_KEY in session:
        data = {"name": session[NAME_KEY]}
    return jsonify(data)


@view.route("/get_messages") # Called by jquery in .static/index.js
def get_messages(): # Get all messages from database, return as .jsonified list
    db = DataBase()
    msgs = db.get_all_messages(MSG_LIMIT)
    messages = remove_seconds_from_messages(msgs)
    # messages contains array of 20 messages
    return jsonify(messages)


@view.route("/get_history")
def get_history(name): # Gets all user's past messages from database, return as list
    db = DataBase()
    msgs = db.get_messages_by_name(name)
    messages = remove_seconds_from_messages(msgs)

    return messages








@view.route("/get_color")
def get_color(): # Returns the color code for chat's background using an algorithm (Adaptive Color Feature)
    db = DataBase()
    msgs = db.get_all_messages(MSG_LIMIT) # Get last 20 messages from database (messages.db)
    messages = remove_seconds_from_messages(msgs)

    # 'messages' is an object array of the last 20 messages of chat, each object in the array is structured like:
    # {'name': 'Jeff', 'message': 'Hello there guys!', 'time': '2024-03-03 23:48'}
    # Based on 'messages', get the appropriate rgb value and store it in 'color' as a string
    color = "rgb(153,255,221)" # Sample rgb color

    return jsonify(color)

@view.route("/check_message")
def check_message(): # Checks if message sent is appropriate using an algorithm (Suppressor Feature)
    message = request.args.get('message')
    message.replace("_", " ") # 'message' is the message string send by a user like "Hello there!"
    
    if "crap" in message.lower() : # Sample condition for "inappropriate message"
        return jsonify('FALSE')  # Return 'FALSE' if 'message' is inappropriate
    else: 
        return jsonify('TRUE') # Return 'TRUE' if 'message' is appropriate








def remove_seconds_from_messages(msgs): # Simple 'seconds' removal
    messages = []
    for msg in msgs:
        message = msg
        message["time"] = remove_seconds(message["time"])
        messages.append(message)
    return messages

def remove_seconds(msg):
    return msg.split(".")[0][:-3]
