from lib.commands import CommandFactory
from requests.models import Request

GOOGLE_SEARCH = 'https://www.google.com/search'
GOOGLE_MAIL = 'https://mail.google.com/mail/u/'

@CommandFactory.register_redirection_command
def g(arg):
    payload = {'q': arg}
    return Request(url=GOOGLE_SEARCH, params=payload).prepare().url

@CommandFactory.register_redirection_command
def glucky(arg):
    payload = {'q': arg}
    return Request(url=GOOGLE_SEARCH, params=payload).prepare().url + '&btnI'


@CommandFactory.register_redirection_command
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
    return GOOGLE_MAIL + account_num + (('/#search/' + search_content) if search_content else '')

@CommandFactory.register_dynamic_redirection
def google_default(arg):
    """Default fallback to google search"""
    # Leave this at the bottom
    return g(arg)[0]
