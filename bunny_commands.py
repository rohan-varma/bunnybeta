from __future__ import re
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

from functools import wraps
from requests.models import Request

PYTHON2_REF = 'https://docs.python.org/2/search.html'
PYTHON3_REF = 'https://docs.python.org/3/search.html'
GOOGLE_SEARCH = 'https://www.google.com/search'
GOOGLE_MAIL = 'https://mail.google.com/mail/u/'
CONFLUENCE_URL = 'https://confluence.team.affirm.com/dosearchsite.action'
ASKBOT_URL = 'https://askbot.team.affirm.com/'
ASKBOT_QUERY_URL = 'https://askbot.team.affirm.com/questions/scope:all/sort:activity-desc/page:1/query:%s/'
GITHUB_URL = 'https://github.com'
GITHUB_REPO = 'https://github.com/Affirm/%s'
GITHUB_ALL_SEARCH = 'https://github.com/search?q=%s+%s&unscoped_q=%s'
GITHUB_REPO_SEARCH = 'https://github.com/Affirm/%s/search?q=%s'

PHABRICATOR_REGEX = re.compile('^D[0-9]+$')
PHABRICATOR_URL = 'https://phabricator.team.affirm.com/%s'

# This is a super permissive regex, will match any CAPITAL-3049823
# might want to restrict it to just (INFRA|AFJS etc)
JIRA_REGEX = re.compile('^[A-Z]+-[0-9]+$')
JIRA_URL = 'https://jira.team.affirm.com/browse/%s'

class ResultType(object):
    REDIRECTION = 'redirection'
    CONTENT = 'content'


class BunnyCommands(object):
    def __init__(self, cmd_list, dynamic_list):
        self.cmd_list = cmd_list
        self.dynamic_commands = dynamic_list



class CommandFactory(object):
    REGISTERED_COMMANDS = {}
    REGISTERED_DYNAMIC_COMMANDS = []

    @classmethod
    def export(cls):
        # TODO: Use cmd_list to have configurable command list
        # commands = [x for x in cls.REGISTERED_COMMANDS if x.__name__ in cmd_list]
        commands = cls.REGISTERED_COMMANDS
        return BunnyCommands(cls.REGISTERED_COMMANDS, cls.REGISTERED_DYNAMIC_COMMANDS)


def register_command(cmd):
    CommandFactory.REGISTERED_COMMANDS[cmd.__name__] = cmd
    return cmd

def register_dynamic(cmd):
    # These will be called in the order they are defined
    CommandFactory.REGISTERED_DYNAMIC_COMMANDS.add(cmd)
    return cmd


def register_redirection_command(cmd):
    @wraps(cmd)
    def wrapped(*args, **kwargs):
        ret = cmd(*args, **kwargs)
        return ret, ResultType.REDIRECTION
    register_command(wrapped)
    return wrapped


def register_content_command(cmd):
    @wraps(cmd)
    def wrapped(*args, **kwargs):
        ret = cmd(*args, **kwargs)
        return ret, ResultType.CONTENT
    register_command(wrapped)
    return wrapped


# TODO: separate core functions apart from additional functions


@register_redirection_command
def py(arg):
    # TODO: Implement feeling lucky search
    payload = {'q': arg}
    return Request(url=PYTHON2_REF, params=payload).prepare().url


@register_redirection_command
def py3(arg):
    # TODO: Implement feeling lucky search
    payload = {'q': arg}
    return Request(url=PYTHON3_REF, params=payload).prepare().url


@register_redirection_command
def g(arg):
    payload = {'q': arg}
    return Request(url=GOOGLE_SEARCH, params=payload).prepare().url


@register_redirection_command
def glucky(arg):
    payload = {'q': arg}
    return Request(url=GOOGLE_SEARCH, params=payload).prepare().url + '&btnI'

@register_redirection_command
def gmail(arg):
    """
    Go to gmail, with account number arg
    :param arg: Account #
    :return:
    """
    if not arg:
        return GOOGLE_MAIL
    try:
        account_num, search_content = arg.split(None, 1)
    except ValueError:
        account_num, search_content = arg, None
    return GOOGLE_MAIL + account_num + ('/#search/' + search_content) if search_content else ''

@register_redirection_command
def confluence(arg):
    """
    Search Confluence
    """
    payload = {'queryString': arg}
    return Request(url=CONFLUENCE_URL, params=payload).prepare().url

@register_redirection_command
def askbot(arg):
    if not arg:
        return ASKBOT_URL
    return ASKBOT_QUERY_URL % arg

@register_redirection_command
def gh(arg):
    repos = {
        'att': 'all-the-things',
        'ds': 'data-science',
        'wx': 'web-ux'
    }
    if not arg:
        return GITHUB_URL
    split = arg.split(' ', 1)
    repo = split[0]
    if repo in repos:
        """one of the known abbreviations"""
        repo = repos[repo]
    if len(split) == 1:
        """jump to repo"""
        return GITHUB_REPO % repo
    elif repo == '*':
        """Search all"""
        return GITHUB_ALL_SEARCH % ('org:Affirm', split[1], split[1])
    else:
        return GITHUB_REPO_SEARCH % (repo,split[1])

@register_content_command
def _debug(*args, **kwargs):
    try:
        method, margs = args[0].split(None, 1)
        margs = [margs] + list(args[1:])
    except ValueError:
        method = args[0]
        margs = args[1:]
    real_cmd = CommandFactory.REGISTERED_COMMANDS.get(method, None)
    if not callable(real_cmd):
        return 'Error, {method} not found!'.format(method=method)
    else:
        result, _ = real_cmd(*margs, **kwargs)
        return "<code><b>poorbunny</b><br/> DEBUG: redirect to <a href='{url}'>{url}</a></code>".format(url=result)

@register_redirection_command
def cpp(arg):
    payload = {'q': arg}
    return Request(url=CPLUSPLUS, params=payload).prepare().url

@register_dynamic
def phabricator(arg):
    if not PHABRICATOR_REGEX.search(arg):
        return False
    return PHABRICATOR_URL % arg

@regsiter_dynamic
def jira(arg):
    if not JIRA_REGEX.search(arg):
        return False
    return JIRA_URL % arg

@register_dynamic
def google_default(arg):
    """Default fallback to google search"""
    # Leave this at the bottom
    return g(arg)
