from flask import render_template, flash, redirect, url_for, request
from app import app
from app.forms import LoginForm, TextSearchForm
import app.search as appsearch
@app.route('/')#First routes to the local page
@app.route('/index')#Then routes to index
def index():#Defines the index look which is rendered with html @ index.html
    user = {'username': 'Garrison'}
    posts = [
    {
        'author': {'username': 'John'},
        'body': 'The feral chipmunks struck once again, destroying a home in Texas and devastating a few.'
    },
    {
        'author': {'username': 'Blasto'},
        'body': 'Police force brutality continues to rise after an investigation led to police finding 3 weeds.'
    }
    ]
    return render_template('index.html', title='What''s the Sitch?', user=user, posts=posts)


@app.route('/login', methods=['GET', 'POST'])#On click for login, routes to the login page
def login():#Defines the login look which is rendered with html @ login.html
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/search', methods=['GET', 'POST'])#On click for searech, routes to the search page
def search():#Defines the search look which is rendered with html @ search.html
    form = TextSearchForm()
    return render_template('search.html', title = 'Search Final Statements', form=form)

@app.route('/results', methods=['GET', 'POST'])
def results():
    if request.method == 'POST':
        query = request.form.get('query')
    query, ranking, totaldocs, totalwords, timetaken  = appsearch.search(query)
    return render_template('results.html', title = 'Results', query = query, doclist = ranking, totaldocs = totaldocs, totalwords = totalwords, timetaken = timetaken)