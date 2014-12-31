import json
import github3

def github_set_ref(repo, ref, sha, *, force=False):
    url = repo._build_url('git', 'refs', ref, base_url=repo._api)
    data = {'sha': sha, 'force': force}

    js = repo._json(repo._patch(url, data=json.dumps(data)), 200)

    return github3.git.Reference(js, repo) if js else None

class Status(github3.repos.status.Status):
    def __init__(self, info):
        super(Status, self).__init__(info)

        self.context = info.get('context')

def github_iter_statuses(repo, sha):
    url = repo._build_url('statuses', sha, base_url=repo._api)
    return repo._iter(-1, url, Status)

def github_create_status(repo, sha, state, target_url='', description='', *,
                         context=''):
    data = {'state': state, 'target_url': target_url,
            'description': description, 'context': context}
    url = repo._build_url('statuses', sha, base_url=repo._api)
    js = repo._json(repo._post(url, data=data), 201)
    return Status(js) if js else None

def sha_cmp(short, full):
    return len(short) >= 4 and short == full[:len(short)]

def parse_commands(body, username, reviewers, state, my_username, *, realtime=False, sha=''):
    if username not in reviewers:
        return False

    mentioned = '@' + my_username in body
    if not mentioned: return False

    state_changed = False

    words = re.findall(r'\S+', body)
    for i, word in enumerate(words):
        found = True

        if word in ['r+', 'r=me']:
            if not sha and i+1 < len(words):
                sha = words[i+1]

            if sha_cmp(sha, state.head_sha):
                state.approved_by = username
            elif realtime:
                state.add_comment(':scream_cat: You have a wrong number! Please try again with `{:.4}`.'.format(state.head_sha))

        elif word.startswith('r='):
            if not sha and i+1 < len(words):
                sha = words[i+1]

            if sha_cmp(sha, state.head_sha):
                state.approved_by = word[len('r='):]
            elif realtime:
                state.add_comment(':scream_cat: You have a wrong number! Please try again with `{:.4}`.'.format(state.head_sha))

        elif word == 'r-':
            state.approved_by = ''

        elif word.startswith('p='):
            try: state.priority = int(word[len('p='):])
            except ValueError: pass

        elif word == 'retry' and realtime:
            state.status = ''

        elif word == 'try' and realtime:
            state.try_ = True

        elif word == 'rollup':
            state.rollup = True

        elif word == 'rollup-':
            state.rollup = False

        else:
            found = False

        if found:
            state_changed = True

    return state_changed
