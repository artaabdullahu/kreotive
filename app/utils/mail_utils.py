from flask_mail import Message

class Mailer(object):
    def __init__(self, mail):
        self.mail = mail
        self.content_collection = 'content'
        self.users_collection = 'users'

    def send_mail(self, subject, sender, recipient, message):
        msg = Message(subject,
                            sender=sender,
                            recipients=[recipient],
                      body=message)
        self.mail.send(msg)
        return {'sent':True}