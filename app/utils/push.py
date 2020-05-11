from firebase_admin import messaging

from app.utils.constants import NOTIFICATION_ID, TITLE, BODY, FILE_ID
from app.utils.messages import TITLE_CONVERSION_SUCCESS, BODY_CONVERSION_SUCCESS

# NOTIFICATION IDs
CONVERT_NOTIFICATION_ID = '301'


# Send Push on file conversion
def file_convert_push(tokens, file_id, file_name, from_ext, to_ext):
    return messaging.Message(
        data={
            NOTIFICATION_ID: CONVERT_NOTIFICATION_ID,
            TITLE: TITLE_CONVERSION_SUCCESS,
            BODY: BODY_CONVERSION_SUCCESS.format(file_name, from_ext, file_name, to_ext),
            FILE_ID: f'{file_id}',
        }, token=tokens)


# Send Test Push
def demo(tokens, ):
    return messaging.Message(
        notification=messaging.Notification(
            title='$GOOG up 1.43% on the day',
            body='$GOOG gained 11.80 points to close at 835.67, up 1.43% on the day.',
        ),
        data={
            'score': '850',
            'time': '2:45',
        }, token=tokens)
