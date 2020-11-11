from threading import Thread

from flask_mail import Message

from flask import current_app, render_template

from . import mail, app

def send_async_mail(message):
	with app.app_context():
		mail.send(message)

def test_mail(user):
	message = Message('Bienvenido Esto es una prueba:', 
					sender=current_app.config['MAIL_USERNAME'],
					recipients=[user.email])

	message.html = render_template('email/test.html', user=user)

	thread = Thread(target=send_async_mail, args=[message])
	thread.start()
	

def send_task(task, usern, em):
	message = Message('Este es su Solicitud:', 
					sender=current_app.config['MAIL_USERNAME'],
					recipients=[em])

	message.html = render_template('email/send_task.html', task=task, usern=usern)

	thread = Thread(target=send_async_mail, args=[message])
	thread.start()
