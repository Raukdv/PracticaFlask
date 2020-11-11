from flask import Blueprint
from flask import render_template, request, flash, redirect, url_for, abort

from flask_login import login_user, logout_user, login_required, current_user

from .forms import LoginForm, RegisterForm, TaskForm
from .models import User, Task
from .email import test_mail, send_task

from . import login_manager
from .consts import *

@login_manager.user_loader
def load_user(id):
	return User.get_by_idU(id)

page = Blueprint('page', __name__)

@page.app_errorhandler(404)
def page_error(error):
	return render_template('errors/404.html'), 404

@page.route('/')
def index():
	return render_template('index.html', title='Index')

@page.route('/logout')
def logout():
	logout_user()
	flash(LOGOUT)
	return redirect(url_for('.login'))

@page.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('.index'))

	form=LoginForm(request.form)

	if request.method == 'POST' and form.validate():
		user = User.get_by_usr(form.username.data)
		if user and user.verify_password(form.password.data):
			login_user(user)
			flash(LOGIN)
			return redirect(url_for('.index'))
		else:
			flash(ERROR_USER_PASSWORD)

	return render_template('auth/login.html', title='Login', form=form)

@page.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('.index'))

	form=RegisterForm(request.form)

	if request.method == 'POST':
		if form.validate():
			user = User.create_element(form.username.data, form.password.data, form.email.data)
			flash(USER_CREATED)
			flash(user.password)
			login_user(user)
			test_mail(user)
			return redirect(url_for('.tasks'))

	return render_template('auth/register.html', title='Registro de Usuario', form=form)


@page.route('/tasks')
@page.route('/tasks/<int:page>')
@login_required
def tasks(page=1, per_page=2):
	pagination = current_user.tasks.paginate(page, per_page=per_page)
	tasks = pagination.items

	usern = current_user.username
	return render_template('tasks/list.html', title='Tareas', tasks=tasks, pagination=pagination, page=page, usern=usern)

@page.route('/tasks/new', methods=['GET', 'POST'])
@login_required
def new_tasks():
	form = TaskForm(request.form)

	if request.method == 'POST' and form.validate():
		task = Task.create_element(form.title.data, form.description.data, current_user.id)

		if task:
			form.title.data=" "
			form.description.data=" "
			flash(TASK_CREATED)
	return render_template('tasks/new.html', title='Registro de Tareas', form=form)

@page.route('/tasks/show/<int:task_id>')
@login_required
def get_task(task_id):
	task = Task.query.get_or_404(task_id)

	usern = current_user.username
	return render_template('tasks/show.html', title='Tarea', task=task, usern=usern)

@page.route('/email/sended_task/<int:task_id>')
@login_required
def sended_task(task_id):

	task = Task.query.get_or_404(task_id)
	usern = current_user.username
	em = current_user.email

	if task.user_id != current_user.id:
		abort(404)
	else:
		send_task(task=task, usern=usern, em=em)
		flash(TASK_SENDED)

	return redirect(url_for('.tasks'))

@page.route('/tasks/edit/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
	task = Task.query.get_or_404(task_id)

	if task.user_id != current_user.id:
		abort(404)

	form = TaskForm(request.form, obj=task)
	
	if request.method == 'POST' and form.validate():
		task = Task.update_element(task.id, form.title.data, form.description.data)

		if task:
			form.title.data=" "
			form.description.data=" "
			flash(TASK_UPDATED)

	return render_template('tasks/edit.html', title='Editar Tarea', form=form)


@page.route('/tasks/delete/<int:task_id>')
@login_required
def delete_task(task_id):
	task = Task.query.get_or_404(task_id)

	if task.user_id != current_user.id:
		abort(404)

	if Task.delete_element(task.id):
		flash(TASK_DELETED)
		
	return redirect(url_for('.tasks'))