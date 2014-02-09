import urllib2
import json
from config import GITHUB_KEY
from collaborator import Collaborator

BASE_URL = 'https://api.github.com'

def get_user_repos(username):
    req = urllib2.Request(BASE_URL + '/users/' + username + '/repos')
    req.add_header('Accept', 'application/json')
    req.add_header('Authorization', 'token ' + GITHUB_KEY)
    res = urllib2.urlopen(req)
    return json.loads(res.read())

def get_repo(owner, repo):
    req = urllib2.Request(BASE_URL + '/repos/' + owner + '/' + repo)
    req.add_header('Accept', 'application/json')
    req.add_header('Authorization', 'token ' + GITHUB_KEY)
    res = urllib2.urlopen(req)
    return json.loads(res.read())

def get_repo_commits(owner, repo):
    req = urllib2.Request(BASE_URL + '/repos/' + owner + '/' + repo + '/commits')
    req.add_header('Accept', 'application/json')
    req.add_header('Authorization', 'token ' + GITHUB_KEY)
    res = urllib2.urlopen(req)
    return json.loads(res.read())

def get_repo_collaborators(owner, repo):
    req = urllib2.Request(BASE_URL + '/repos/' + owner + '/' + repo + '/collaborators')
    req.add_header('Accept', 'application/json')
    req.add_header('Authorization', 'token ' + GITHUB_KEY)
    res = urllib2.urlopen(req)
    return json.loads(res.read())

def get_commit(owner, repo, sha):
    req = urllib2.Request(BASE_URL + '/repos/' + owner + '/' + repo + '/commits/' + sha)
    req.add_header('Accept', 'application/json')
    req.add_header('Authorization', 'token ' + GITHUB_KEY)
    res = urllib2.urlopen(req)
    return json.loads(res.read())

def get_commit_data(owner, repo, collaborators):
    data = dict()
    commits = get_repo_commits(owner, repo)
    for commit in commits:
        commit_data = get_commit(owner, repo, commit['sha'])
        cur_collab = commit_data['committer']['login']
        if cur_collab in collaborators:
            if cur_collab not in data.keys():
                data[cur_collab] = Collaborator(cur_collab)
            data[cur_collab].num_commits += 1
            data[cur_collab].lines_contributed += commit_data['stats']['total']
    return data

