from GitMoMoney import app
from flask import render_template, flash, redirect, session, url_for, request, g
from models import User
from forms import RepositoryForm
from github import get_repo, get_repo_collaborators, get_repo_commits

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_started', methods=["GET", "POST"])
def get_started():
    form = RepositoryForm()
    repo_error = False
    if request.method == 'POST' and form.validate():
        try:
            repo = get_repo(form.repo_owner.data, form.repo_name.data)
            session['repo'] = repo
            return redirect(url_for('repo_collaborators'))
        except:
            repo_error = True
    return render_template('get_started.html', form=form, repo_error=repo_error)

@app.route('/collaborators', methods=["GET", "POST"])
def collaborators():
    if not 'repo' in session:
        return render_template('error.html')
    try:
        repo = session['repo']
        collaborators = get_repo_collaborators(repo['owner']['login'], repo['name'])
        return render_template('collaborators.html', collaborators=collaborators)
    except:
        return render_template('error.html')

