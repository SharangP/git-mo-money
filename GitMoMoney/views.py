from GitMoMoney import app
from flask import render_template, flash, redirect, session, url_for, request, g
from models import User
from forms import RepositoryForm, CollaboratorsForm, OptionsForm
from github import get_repo, get_repo_collaborators, get_repo_commits, get_commit_data
from wtforms import TextField, IntegerField
from venmo import Venmo
import math

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
        setattr(F, collab, TextField("%s's Venmo Key:" % collab))
        setattr(F, collab + '-phone', IntegerField("Phone:"))
    form = F(request.form)
    if request.method == 'POST' and form.validate():
        try:
            session['options'] = {}
            session['options']['max_money'] = form.max_money.data
            session['options']['num_commits'] = form.num_commits.data
            session['options']['num_lines'] = form.num_lines.data
            for collab in session['collab_data'].keys():
                session['collab_data'][collab]['venmo'] = getattr(form, collab).data
                session['collab_data'][collab]['phone'] = getattr(form, collab + '-phone').data
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
    total_lines = 0
    max_lines = [0, '']
    total_commits = 0
    max_commits = [0, '']
    for collab in git_results.keys():
        collab_data[collab]['commit_data'] = git_results[collab]
        total_commits += git_results[collab].num_commits
        total_lines += git_results[collab].num_lines
        if git_results[collab].num_commits > max_commits[0]:
            max_commits[0] = git_results[collab].num_commits
            max_commits[1] = collab
        if git_results[collab].num_lines > max_lines[0]:
            max_lines[0] = git_results[collab].num_lines
            max_lines[1] = collab

        collab_data[collab]['commit_data'] = {}
        collab_data[collab]['commit_data']['num_commits'] = git_results[collab].num_commits
        collab_data[collab]['commit_data']['num_lines'] = git_results[collab].num_lines
    total_money = session['options']['max_money']*len(git_results.keys())*(session['options']['num_commits']+session['options']['num_lines'])
    for collab in git_results.keys():
        commit_money = float(session['options']['num_commits']) / (session['options']['num_commits'] + session['options']['num_lines']) * total_money *\
                (git_results[collab].num_commits/(total_commits+0.001))
        lines_money = float(session['options']['num_lines']) / (session['options']['num_commits'] + session['options']['num_lines']) * total_money *\
                (git_results[collab].num_lines+0.01)/(total_lines+0.01)
        money = (float(commit_money + lines_money) - (total_money / len(git_results.keys()))) / (session['options']['num_commits']+session['options']['num_lines'])
        collab_data[collab]['money'] = math.ceil(money * 100) / 100.0
    session['collab_data'] = collab_data
    return render_template('results.html', collab_data=collab_data, total_commits=total_commits, total_lines=total_lines)

@app.route('/pay_up')
def pay_up():
    if 'repo' not in session or not 'collab_data' in session:
        return render_template('error.html')
    venmo = Venmo()
    balances = {}
    payments = {}
    for collab in session['collab_data'].keys():
        balances[collab] = session['collab_data'][collab]['money']
        payments[collab] = []
    for collab in balances.keys():
        if balances[collab] < 0:
            for collab2 in balances.keys():
                if collab != collab2 and balances[collab2] > 0:
                    if balances[collab2] > -1*balances[collab]:
                        payments[collab].append((-1*balances[collab], session['collab_data'][collab]['venmo'], session['collab_data'][collab2]['phone']))
                        balances[collab2] -= balances[collab]
                        balances[collab] = 0
                    else:
                        payments[collab].append((balances[collab2], session['collab_data'][collab]['venmo'], session['collab_data'][collab2]['phone']))
                        balances[collab] += balances[collab2]
                        balances[collab2] = 0
    print payments
    note = 'You can Git-Mo-Money by committing to the repo %s more!' % session['repo']['url']
    for collab in payments.keys():
        for payment in payments[collab]:
            venmo.pay(payment[1], payment[2], note, payment[0])
    #del session['repo']
    #del session['collab_data']
    return render_template('pay_up.html')
