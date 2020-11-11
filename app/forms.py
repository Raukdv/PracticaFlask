from wtforms import Form, HiddenField
from wtforms import validators
from wtforms import StringField, PasswordField, BooleanField, TextAreaField
from wtforms.fields.html5 import EmailField

from .models import User

def any_validator(form, field):
	if field.data == '' or field.data == '':
		raise validators.ValidationError('Este username no esta permitido.')

def length_honeypot(form, field):
    if len(field.data) > 0:
        raise validators.ValidationError('Solo los humanos pueden completar el registro!')


class LoginForm(Form):

	username = StringField('Username', [
		validators.length(min=4, max=50, message='El usuario se encuentra fuera de rango.'),
		])
	password = PasswordField('Password', [
		validators.Required(message='Es obligatorio colocar una contraseña, por favor especifiquela.')
		])

class RegisterForm(Form):

	username = StringField('Username', [
		validators.length(min=4, max=50, message='El usuario se encuentra fuera de rango.')
		])
	email = EmailField('Email', [
		validators.length(min=6, max=100,), 
		validators.Required(message='Es obligatorio colocar el correo, por favor especifiquelo.'),
		validators.Email(message='Ingrese un correo electronico valido.')
		])
	password = PasswordField('Password', [
		validators.Required(message='la contraseña es obligatoria, por favor especifiquelo'),
		validators.EqualTo('confirm_password', message='La contraseña no coincide, intente de nuevo.')
		])
	confirm_password = PasswordField('Confirm password')

	accept = BooleanField([validators.DataRequired()])

	honeypot = HiddenField("", [length_honeypot] )

	def validate_username(self, username):
		if User.get_by_usr(username.data):
			raise validators.ValidationError('El usuario ya ha sido registrado previamente.')

	def validate_email(self, email):
		if User.get_by_eml(email.data):
			raise validators.ValidationError('El correo ya ha sido registrado previamente.')

	def validate(self):
		if not Form.validate(self):
			return False

		if len(self.password.data) < 3:
			self.password.errors.append('La contraseña es demasiada corta.')
			return False

		return True

class TaskForm(Form):
	title = StringField('Titulo', [
		validators.length(min=4, max=50, message='Titulo Fuera de rango.'),
		validators.DataRequired(message='Se requiere de un titulo.')
		])
	description = TextAreaField('Descripcion', [
		validators.DataRequired(message='Se requiere de un descripcion.')
		], render_kw={'rows': 5})