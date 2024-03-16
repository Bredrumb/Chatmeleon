from flask import Blueprint
from flask import Flask, render_template, url_for, redirect, request, session, jsonify, flash, Blueprint
from .database import DataBase
from transformers import RobertaTokenizerFast, TFRobertaForSequenceClassification, pipeline
from better_profanity import profanity


view = Blueprint("views", __name__) # Register blueprint as 'view'

NAME_KEY = 'name'
MSG_LIMIT = 20 # Maximum messages in display

categorized_emotions = {
    "Positive": ["admiration", "amusement", "approval", "caring", "curiosity", "desire", "excitement",
                 "gratitude", "joy", "love", "optimism", "pride", "realization", "relief"],
    
    "Negative": ["anger", "annoyance", "disappointment", "disapproval", "disgust", "embarrassment", 
                 "fear", "grief", "nervousness", "remorse", "sadness"],
    
    "Neutral": ["confusion", "neutral"]
}

tokenizer = RobertaTokenizerFast.from_pretrained("arpanghoshal/EmoRoBERTa")
model = TFRobertaForSequenceClassification.from_pretrained("arpanghoshal/EmoRoBERTa")
emotion = pipeline('sentiment-analysis', model='arpanghoshal/EmoRoBERTa')

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
    msgs = db.get_all_messages(MSG_LIMIT) 
    messages = remove_seconds_from_messages(msgs)

    # Initialize emotion counts for each category
    emotion_counts = {"Positive": 0, "Negative": 0, "Neutral": 0}

    # Iterate through each message and calculate the sentiment score
    for msg in messages:
        emotion_labels = emotion(msg["message"])  # Get emotion labels for the message
        top_emotion = emotion_labels[0]["label"]  # Get the top emotion label

        # Increment the count for the corresponding emotion category
        for category, emotion_list in categorized_emotions.items():
            if top_emotion in emotion_list:
                emotion_counts[category] += 1
                break

    # Determine the predominant emotion category
    predominant_emotion = max(emotion_counts, key=emotion_counts.get)

    # Map the predominant emotion category to its corresponding color
    color = {"Positive": "rgb(153,255,221)", "Negative": "rgb(255,153,153)", "Neutral": "rgb(240,240,240)"}.get(predominant_emotion)

    return jsonify(color)



@view.route("/check_message")
def check_message():
    message = request.args.get('message')
    message = message.replace("_", " ")  # Clean up the message

    if profanity.contains_profanity(message):
        return jsonify('FALSE')  # Return 'FALSE' if profanity is detected
    else:
        return jsonify('TRUE')   # Return 'TRUE' if no profanity is detected

def remove_seconds_from_messages(msgs): # Simple 'seconds' removal
    messages = []
    for msg in msgs:
        message = msg
        message["time"] = remove_seconds(message["time"])
        messages.append(message)
    return messages

def remove_seconds(msg):
    return msg.split(".")[0][:-3]
