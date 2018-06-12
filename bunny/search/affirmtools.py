from lib.commands import CommandFactory
from requests.models import Request

CONFLUENCE_URL = 'https://confluence.team.affirm.com/dosearchsite.action'
ASKBOT_URL = 'https://askbot.team.affirm.com/'
ASKBOT_QUERY_URL = 'https://askbot.team.affirm.com/questions/scope:all/sort:activity-desc/page:1/query:%s/'

PHABRICATOR_REGEX = re.compile('^D[0-9]+$')
PHABRICATOR_URL = 'https://phabricator.team.affirm.com/%s'

# This is a super permissive regex, will match any CAPITAL-3049823
# might want to restrict it to just (INFRA|AFJS etc)
JIRA_REGEX = re.compile('^[A-Z]+-[0-9]+$')
JIRA_URL = 'https://jira.team.affirm.com/browse/%s'


@CommandFactory.register_redirection_command
def confluence(arg):
    """
    Search Confluence
    """
    payload = {'queryString': arg}
    return Request(url=CONFLUENCE_URL, params=payload).prepare().url


@CommandFactory.register_redirection_command
def wiki(arg):
    return confluence(arg)[0]


@CommandFactory.register_redirection_command
def askbot(arg):
    if not arg:
        return ASKBOT_URL
    return ASKBOT_QUERY_URL % arg


@CommandFactory.register_dynamic_redirection
def jira(arg):
    if not JIRA_REGEX.search(arg):
        return False
    return JIRA_URL % arg


@CommandFactory.register_dynamic_redirection
def phabricator(arg):
    if not PHABRICATOR_REGEX.search(arg):
        return False
    return PHABRICATOR_URL % arg
