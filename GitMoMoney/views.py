from GitMoMoney import app
from flask import render_template, flash, redirect, session, url_for, request, g
from models import User
from forms import RepositoryForm, CollaboratorsForm, OptionsForm
from github import get_repo, get_repo_collaborators, get_repo_commits, get_commit_data
from wtforms import TextField

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_started', methods=["GET", "POST"])
def get_started():
    form = RepositoryForm(request.form)
    repo_error = False
    if request.method == 'POST' and form.validate():
        try:
            repo = get_repo(form.repo_owner.data, form.repo_name.data)
            session['repo'] = repo
            return redirect(url_for('repo_collaborators'))
        except:
            repo_error = True
    return render_template('get_started.html', form=form, repo_error=repo_error)

@app.route('/repo_collaborators', methods=["GET", "POST"])
def repo_collaborators():
    if not 'repo' in session:
        return render_template('error.html')
    try:
        form = CollaboratorsForm(request.form)
        if request.method == 'POST' and 'collaborators' in session:
            session['collab_data'] = {}
            for collab in form.collaborators.data:
                session['collab_data'][session['collaborators'][collab]['login']] = session['collaborators'][collab]
            return redirect(url_for('options'))
        repo = session['repo']
        collaborators = get_repo_collaborators(repo['owner']['login'], repo['name'])
        form.collaborators.choices = []
        for (i, collaborator) in enumerate(collaborators):
            form.collaborators.choices.append((i, collaborator['login']))
        session['collaborators'] = collaborators
        return render_template('collaborators.html', form=form, collaborators=collaborators)
    except:
        return render_template('error.html')

@app.route('/options', methods=["GET", "POST"])
def options():
    if not 'collaborators' in session or not 'collab_data' in session:
        return render_template('error.html')
    class F(OptionsForm):
        pass
    for collab in session['collab_data'].keys():
        setattr(F, collab, TextField("%s's Venmo Key" % collab))
    form = F(request.form)
    if request.method == 'POST' and form.validate():
        try:
            session['options'] = {}
            session['options']['max_money'] = form.max_money.data
            session['options']['num_commits'] = form.num_commits.data
            session['options']['num_lines'] = form.num_lines.data
            for collab in session['collab_data'].keys():
                session['collab_data'][collab]['venmo'] = getattr(form, collab)
            return redirect(url_for('results'))
        except:
            return render_template('error.html')
    return render_template('options.html', form=form, collaborators=session['collab_data'].keys())

@app.route('/results')
def results():
    if not 'repo' in session or not 'collab_data' in session:
        return render_template('error.html')
    git_results = get_commit_data(session['repo']['owner']['login'], session['repo']['name'], session['collab_data'].keys())
    collab_data = session['collab_data']


    return render_template('results.html', collab_data=collab_data)
