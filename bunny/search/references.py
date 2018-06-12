from lib.commands import CommandFactory
from requests.models import Request

PYTHON2_REF = 'https://docs.python.org/2/search.html'
PYTHON3_REF = 'https://docs.python.org/3/search.html'
SALT_REF = 'https://cse.google.com/cse'


@CommandFactory.register_redirection_command
def py(arg):
    # TODO: Implement feeling lucky search
    payload = {'q': arg}
    return Request(url=PYTHON2_REF, params=payload).prepare().url

@CommandFactory.register_redirection_command
def py3(arg):
    # TODO: Implement feeling lucky search
    payload = {'q': arg}
    return Request(url=PYTHON3_REF, params=payload).prepare().url

@CommandFactory.register_redirection_command
def ss(arg):
    payload = {
        'cx':'004624818632696854117:yfmprrbw3pk',
        'q': arg
    }
    return Request(url=SALT_REF, params=payload).prepare().url

