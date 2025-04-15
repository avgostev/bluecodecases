from flask import Flask, jsonify, make_response, request, render_template, redirect, url_for, flash
from app import app
from app.forms import LoginForm, RegisterForm, SLRCaseForm
import app.db as db
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
import re
import math

@app.route('/')
def index():
    
    count_slr_cases = db.get_slrcases_count(None)
    result_slr_cases = db.get_slrcases_result(None)

    template_context = dict(current_user = current_user,
                            count_slr_cases = count_slr_cases,
                            result_slr_cases = result_slr_cases,
                            title = 'Главная')
    return render_template('index.html', **template_context)


@app.route('/login/', methods=['post',  'get'])
def login():

    title = "Вход"

    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.get_user_from_login(form.username.data)
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('profile'))

        flash("Неверный логин или пароль!", 'error')
        return redirect(url_for('login'))
    return render_template('login.html', form = form, title = title)


@app.route('/register/', methods=['post',  'get'])
def register():

    title = "Регистрация"

    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = db.get_user_from_login(form.username.data)

        if user is not None:
            flash("Пользователь с таким E-mail уже существует!", 'error')
            return render_template('register.html', form=form)
        
        if not re.match(r'[^@]+@[^@]+\.[^@]+', form.username.data):
            flash("Некорректный E-mail!", 'error')
            return render_template('register.html', form=form)
        
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', form.password.data):
            flash("Пароль должен содержать минимум 8 символов, буквы, цифры и спецсимволы", 'error')
            return render_template('register.html', form=form)
        
        db.register_user({"name": form.name.data, "email": form.username.data, "password": form.password.data})
        
        flash("Пользователь зарегистрирован, авторизуйтесь пожалуйста!", 'info')
        return redirect(url_for('login'))
    return render_template('register.html', form = form, title = title)


@app.route('/logout/')
@login_required
def logout():
    logout_user()
    flash("Вы вышли")
    return redirect(url_for('index'))


@app.route('/profile/')
@login_required
def profile():
    
    title = 'Личная страница'

    count_slr_cases = db.get_slrcases_count(user_id = current_user.id)


    template_context = dict(current_user = current_user, 
                            count_slr_cases = count_slr_cases,
                            title = title)
    return render_template('profile.html', **template_context)


@app.route('/slrcases/')
@login_required
def slrcases():
    page = request.args.get('page', 1, type=int)

    title = 'Случаи СЛР'

    count_per_page = 17

    count_slr_cases = db.get_slrcases_count(user_id = current_user.id)

    max_page = math.ceil(float(count_slr_cases)/float(count_per_page))

    if max_page == 0:
        max_page = 1

    if page > max_page:
        redirect(url_for('not_found'))
    
    offset = (page - 1) * count_per_page

    pages=[]

    for i in range(1, max_page + 1):
        pages.append(i)

    slr_cases = db.get_slrcases(current_user.id, offset = offset, limit = count_per_page)

    next_page = page + 1
    prev_page = page - 1
    if next_page > max_page:
        next_page = None
    if prev_page < 1:
        prev_page = None

    template_context = dict(current_user = current_user, 
                            slr_cases = slr_cases,
                            page = page,
                            pages = pages,
                            max_page = max_page, 
                            next_page = next_page, 
                            prev_page = prev_page,
                            title = title)
    return render_template('slrcases.html', **template_context)



@app.route('/slrcase/delete/<id>', methods=['get'])
@login_required
def slr_delete(id):
    if id is not None:
        db.delete_slrcase(id, current_user.id)

    return redirect(url_for('operations'))

@app.route('/slrcase/add/', methods=['get', 'post'])
@login_required
def slr_add():
    return slr(None)


@app.route('/slrcase/<id>', methods=['get', 'post'])
@login_required
def slr(id):

    slr_id = id

    genders = db.get_genders()
    gender_choices = [(g.id, g.s_name) for g in genders]

    results = db.get_results()
    result_choices = [(g.id, g.s_name) for g in results]

    places = db.get_places()
    place_choices = [(g.id, g.s_name) for g in places]

    locates = db.get_locates()
    locate_choices = [(g.id, g.s_name) for g in locates]
    
    form = SLRCaseForm()
    form.sex.choices = gender_choices
    form.result.choices = result_choices
    form.place.choices = place_choices
    form.locate.choices = locate_choices

    if form.validate_on_submit():
        d_slr = form.d_slr.data
        sex = form.sex.data
        result = form.result.data
        place = form.place.data
        locate = form.locate.data
        d_bdate = form.d_bdate.data
        
        item = dict(id = slr_id,
                    d_slr = d_slr,
                    sex = sex,
                    result = result,
                    place = place,
                    locate = locate,
                    d_bdate = d_bdate,
                    user_id = current_user.id)
        
        db.save_slrcase(item)
        
        return redirect(url_for('slrcases'))
    
    title = 'Добавить случай'

    if slr_id is not None:

        title = 'Редактировать случай'

        item = db.get_slrcase(id = id, user_id = current_user.id)
        if item is None:
            return redirect(url_for('not_found'))

        form.d_slr.data = item.d_slr
        if item.d_bdate is not None:
            form.d_bdate.data = item.d_bdate
        form.sex.data = item.sex_id
        form.result.data = item.result_id
        form.place.data = item.place_id
        form.locate.data = item.locate_id
    
    template_context = dict(current_user = current_user,
                            form=form,
                            slr_id=slr_id,
                            title = title)

    return render_template('slrcase.html', **template_context)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)