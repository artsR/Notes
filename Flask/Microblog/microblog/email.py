from flask import render_template
from flask_mail import Message
from microblog import app, mail
from threading import Thread


def send_async_email(app, msg):
    with app.app_context():
    # the application context that is created here makes the application instance
    # accessible via 'current_app' variable from Flask.
        mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=mail.send, args=(app, msg)).start()
                                    # the application instance 'app' need to be sent
                                    # argument because many extensions (in this case 'Flask-Mail')
                                    # has their configuration stored in the 'app.config' object.
                                    # The 'mail.send()' method needs to access the configuration
                                    # values for 'email server', and that can only be done
                                    # by knowing what the application is.
                                        # 'msg' standard argument using by 'mail.send()'
def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email('[Microblog] Reset Your Password',
            sender=app.config['ADMINS'][0],
            recipients=[user.email],
            text_body=render_template('/email/reset_password.txt',
                                    user=user, token=token),
            html_body=render_template('/email/reset_password.html',
                                    user=user, token=token)
)
