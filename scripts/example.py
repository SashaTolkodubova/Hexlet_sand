from flask import Flask, render_template, request, redirect, url_for, flash,\
    get_flashed_messages, make_response, session
import json

app = Flask(__name__)
app.secret_key = "secret_key"


@app.route('/')
def hellow_world():
    session.clear()
    error = False
    return render_template(
        'users/enter.html',
        error=error
    )


@app.post('/')
def enter():
    user_email = request.form.get('email')
    if not user_email:
        error = True,
        return render_template(
        'users/enter.html',
            error=error
    )
    session['name'] = user_email
    return redirect(url_for('get_users'))


# 1 list users
@app.route('/users')
def get_users():
    term = request.args.get('term')
    users = session.get('users', [])
    if term:
        filtered_users = filtered(users, term)
    else:
        filtered_users = users
        term = ''
    messages = get_flashed_messages(with_categories=True)
    print(messages)
    user_email = session.get('name')
    return render_template(
        'users/index.html',
        users=filtered_users,
        search=term,
        messages=messages,
        namex=user_email

    )


# 2 user info
@app.route('/users/<id>')
def get_user_info(id):
    users = session.get('users')
    user = get_user_by_id(users, id)
    if not user:
        return 'Page not found', 404
    return render_template('users/show.html',
                           name=user['name'],
                           user_id=user['id'])


# 3 form for create new user
@app.route('/users/new')
def new_user():
    errors = {}
    flash('This is a message', 'success')
    return render_template(
        'users/new.html',
        errors=errors
    )


# 4 create new user
@app.post('/users')
def users_post():
    user = request.form.to_dict()
    user_id = user['name']
    user['id'] = user_id
    errors = validate(user)
    if errors:
        return render_template(
            'users/new.html',
            user=user,
            errors=errors
        )
    if session.get('users') is None:
        session['users'] = [user]
    else:
        users = session['users']
        users.append(user)
        session['users'] = users
    response = make_response(redirect(url_for('get_users', code=302)))
    return response


# 5 edit user
@app.route('/users/<id>/edit')
def edit_user(id):
    users = session.get('users')
    # users_cookies = request.cookies.get('users')
    # if users_cookies:
    #     repo = json.loads(users_cookies)
    # else:
    #     repo = []
    user = get_user_by_id(users, id)
    errors = []
    return render_template(
        'users/edit.html',
        user=user,
        user_id=user['id'],
        errors=errors
    )


# 6 update user
@app.route('/users/<id>/patch', methods=['POST'])
def patch_user(id):
    users = session.get('users')

    user = get_user_by_id(users, id)
    users.remove(user)
    data = request.form.to_dict()
    errors = validate(data)
    if errors:
        return render_template(
            'users/edit.html',
            user=user,
            errors=errors
        ), 422
    user['name'] = data['name']
    user['email'] = data['email']
    user['paid'] = data['paid']
    users.append(user)
    session['users'] = users
    response = make_response(redirect(url_for('get_users', code=302)))
    return response

@app.route('/users/<id>/confirm')
def confirm_delete(id):
    users = session.get('users')
    user = get_user_by_id(users, id)
    response = make_response(render_template('users/delete.html',
                           user=user))

    return response

# 7 delete user
@app.route('/user/<id>/delete', methods=['POST'])
def delete_user(id):
    users = session.get('users')
    user = get_user_by_id(users, id)
    users.remove(user)
    session['users'] = users
    response = make_response(redirect(url_for('get_users')))
    flash('User has dalated')
    return response


def validate(user):
    errors = {}
    if not user['name']:
        errors['name'] = "Can't be blank"
    if not user['email']:
        errors['email'] = "Can't be blank"
    if not user['paid']:
        errors['paid'] = "Can't be blank"
    return errors


def filtered(users, term):
    def contain(word, term):
        len_term = len(term)
        len_word = len(word)
        if len_term <= len_word:
            if term.upper() == word.upper()[:len_term]:
                return True
        return False

    return list(filter(lambda x: contain(x['name'], term), users))


def get_user_by_id(users, id):
    for i in users:
        if i["id"] == id:
            return i

