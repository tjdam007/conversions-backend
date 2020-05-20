from datetime import datetime

from firebase_admin import messaging
from flask import jsonify

from app import app
from app.utils.constants import ALLOWED_EXTENSIONS


# Server Response
def server_response(data=None, message=None, error=None):
    jsondata = {}
    if data is not None:
        jsondata['data'] = data
    if message is not None:
        jsondata['message'] = message
    if error is not None:
        jsondata['error'] = error
    return jsonify(jsondata)


# Allowed files
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config[ALLOWED_EXTENSIONS]


# timestamp file name
def get_timestamp():
    return str(datetime.timestamp(datetime.now())).replace(".", '')


#  send notification to token
# def send_to_token():
#     registration_token = 'fSisxdK6RDC2xm1Ixw2yxP:APA91bHJVoJAvNtu5J9jXJPIF1ICHICk7Idp6FMdm6NjZfr2yHzNIf7xdJzQazK4eLfQBPeqH3oQIzEY-mqDCVH1rdRrfizT-wwjphipTee3Q9dhUgRECY9_hWXOfopwP-4d__mWiIM7'
#     message = messaging.Message(
#         notification=messaging.Notification(
#             title='$GOOG up 1.43% on the day',
#             body='$GOOG gained 11.80 points to close at 835.67, up 1.43% on the day.',
#         ),
#         data={
#             'score': '850',
#             'time': '2:45',
#         }, token=registration_token, )
#     # Send a message to the device corresponding to the provided
#     # registration token.
#     response = messaging.send(message)
#     # Response is a message ID string.
#     return f'Successfully sent message {response}'
#     # [END send_to_token]
