class PullReqState:
    num = 0
    priority = 0
    rollup = False
    title = ''
    body = ''
    head_ref = ''
    base_ref = ''
    assignee = ''

    def __init__(self, num, head_sha, status, repo):
        self.head_advanced('')

        self.num = num
        self.head_sha = head_sha
        self.status = status
        self.repo = repo

    def head_advanced(self, head_sha):
        self.head_sha = head_sha
        self.approved_by = ''
        self.status = ''
        self.merge_sha = ''
        self.build_res = {}
        self.try_ = False
        self.mergeable = None

    def __repr__(self):
        return 'PullReqState#{}(approved_by={}, priority={}, status={})'.format(
            self.num,
            self.approved_by,
            self.priority,
            self.status,
        )

    def sort_key(self):
        return [
            1 if self.mergeable is False else 0,
            0 if self.approved_by else 1,
            1 if self.rollup else 0,
            -self.priority,
            self.num,
        ]

    def __lt__(self, other):
        return self.sort_key() < other.sort_key()

    def add_comment(self, text):
        issue = getattr(self, 'issue', None)
        if not issue:
            issue = self.issue = self.repo.issue(self.num)

        issue.create_comment(text)
