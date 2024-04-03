# Chatmeleon

![chatmeleon](https://github.com/Eliolocin/Chatmeleon/assets/65227425/a0d8e9e3-ac2e-4e8f-a677-a55ef3326c44)

Flask Web application based around Empathic Computing principles. Users communicate in a chat room that detects emotions through AI. Changes color based on 28 different emotions, promoting positive conversation.
## Setup
1. Clone or download Chatmeleon (Main Branch).
2. Ensure you have python 3.6+ installed in your system.
3. Install requirements
```bash
pip install -r requirements.txt
```

## Running the Server
1. Navigate to 'website' folder and run main.py
```bash
cd website
python main.py
```
2. *NOTE: First run will download the emotion classification model, which is about 500 MB*
3. Once server is ready, go to 'http://127.0.0.1:5000/' in your browser

## Clearing Database
1. To clear all messages simply delete the `messages.db` file.

## Credits

This Chatmeleon prototype is based on a fork of the following repository by **techwithtim**:
https://github.com/techwithtim/Chat-Web-App/tree/master
