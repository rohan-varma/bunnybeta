from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

from functools import wraps
from requests.models import Request

from keywords import aliased_commands, repos

import re

GITHUB_URL = 'https://github.com'
GITHUB_REPO = 'https://github.com/Affirm/%s'
GITHUB_ALL_SEARCH = 'https://github.com/search?q=%s+%s&unscoped_q=%s'
GITHUB_REPO_SEARCH = 'https://github.com/Affirm/%s/search?q=%s'


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

    @classmethod
    def register_redirection_command(self, cmd, name=None):
        name = name or cmd.__name__
        wrapped = self.register_redirection(cmd)
        CommandFactory.REGISTERED_COMMANDS[name] = wrapped
        return wrapped

    @classmethod
    def register_dynamic_redirection(self, cmd):
        wrapped = self.register_redirection(cmd)
        CommandFactory.REGISTERED_DYNAMIC_COMMANDS.append(wrapped)
        return wrapped

    @classmethod
    def register_redirection(self, cmd):
        @wraps(cmd)
        def wrapped(*args, **kwargs):
            ret = cmd(*args, **kwargs)
            return ret, ResultType.REDIRECTION
        return wrapped

    @classmethod
    def register_content_command(self, cmd):
        @wraps(cmd)
        def wrapped(*args, **kwargs):
            ret = cmd(*args, **kwargs)
            return ret, ResultType.CONTENT
        return wrapped

# TODO: separate core functions apart from additional functions


@CommandFactory.register_redirection_command
def gh(arg):
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

@CommandFactory.register_content_command
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

@CommandFactory.register_dynamic_redirection
def alias(arg):
    if arg in aliased_commands:
        return aliased_commands[arg]
    return False
