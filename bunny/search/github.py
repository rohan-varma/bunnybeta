from lib.commands import CommandFactory
from requests.models import Request

import re

GITHUB_URL = 'https://github.com'
GITHUB_REPO = 'https://github.com/Affirm/%s'
GITHUB_ALL_SEARCH = 'https://github.com/search?q=%s+%s&unscoped_q=%s'
GITHUB_REPO_SEARCH = 'https://github.com/Affirm/%s/search?q=%s'

