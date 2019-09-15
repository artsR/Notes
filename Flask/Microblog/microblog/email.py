from threading import Thread
from flask import current_app
from flask_mail import Message
from microblog import mail



def send_async_email(app, msg):
    with app.app_context():
    # the application context that is created here makes the application instance
    # accessible via 'current_app' variable from Flask.
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=mail.send, args=(current_app._get_current_object(), msg)).start()
                                    # TODO: write about proxy object etc...
