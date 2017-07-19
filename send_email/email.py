
from flask_mail import Message

from server import app
from server.extensions import mail
from threading import Thread


def async(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
    return wrapper


def send_mail(subject, recipients, text_body, html_body=None):
    msg = Message(subject, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    send_async_email(app.app, msg)


@async
def send_async_email(flask_app, msg):
    with flask_app.app_context():
        mail.send(msg)
