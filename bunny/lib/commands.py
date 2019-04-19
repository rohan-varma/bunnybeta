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
GITHUB_ALL_SEARCH = 'https://github.com/search?q=%s'
GITHUB_REPO_SEARCH = 'https://github.com/Affirm/%s/search?q=%s'

lines = open('/Users/rohan/desktop/bunnybeta/bunny/lib/do_not_commit.txt').readlines()
lines = [line.rstrip() for line in lines]
bad_terms = set(lines)


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
        # hack for amazon and robinhood
        if name == 'amzn':
            CommandFactory.REGISTERED_COMMANDS["amazon"] = wrapped
        elif name == 'robinhood':
            CommandFactory.REGISTERED_COMMANDS["robin"] = wrapped
            CommandFactory.REGISTERED_COMMANDS["rbnhd"] = wrapped


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
    split = arg.split(" ")
    print(split)
    retval = GITHUB_ALL_SEARCH % (" ".join(split))
    print('returning {}'.format(retval))
    return retval

@CommandFactory.register_redirection_command
def yt(arg):
    if not arg:
        return 'https://youtube.com'
    else:
        # https://www.youtube.com/results?search_query=third+leg+studios
        YOUTUBE_URL = 'https://youtube.com'
        search_url = '/results?search_query=%s'
        arg_list = arg.split(" ")
        arg_str = "+".join(arg_list)
        complete_url = YOUTUBE_URL + (search_url % (arg_str))
        print('returning {}'.format(complete_url))
        return complete_url

@CommandFactory.register_redirection_command
def reddit(arg):
    if not arg:
        return 'https://reddit.com'
    else:
        # https://www.reddit.com/search?q=personal%20finance
        REDDIT_URL = 'https://reddit.com'
        search_url = '/search?q=%s'
        arg_list = arg.split(" ")
        arg_str = "+".join(arg_list)
        complete_url = REDDIT_URL + (search_url % arg_str)
        print('retuning {}'.format(complete_url))
        return complete_url

@CommandFactory.register_redirection_command
def quora(arg):
    if not arg:
        return 'https://quora.com'
    else:
        # https://www.quora.com/search?q=machine+learning
        QUORA_URL = 'https://quora.com'
        search_url = '/search?q=%s'
        arg_list = arg.split(" ")
        arg_str = "+".join(arg_list)
        complete_url = QUORA_URL + (search_url % arg_str)
        print('returning {}'.format(complete_url))
        return complete_url

@CommandFactory.register_redirection_command
def amzn(arg):
    if not arg:
        return 'https://amazon.com'
    else:
        # https://www.amazon.com/s?k=basketball+shoes
        AMZN_URL = 'https://amazon.com'
        search_url = '/s?k=%s'
        arg_list = arg.split(" ")
        arg_str = "=".join(arg_list)
        complete_url = AMZN_URL + (search_url % arg_str)
        return complete_url

@CommandFactory.register_redirection_command
def maps(arg):
    if not arg:
        return 'https://maps.google.com'
    else:
        MAPS_URL = 'https://google.com/maps'
        place_url = '/place/%s'
        arg_list = arg.split(" ")
        arg_str = " ".join(arg_list)
        print(arg_str == arg)
        complete_url = MAPS_URL + (place_url % arg_str)
        print('returning {}'.format(complete_url))
        return complete_url


@CommandFactory.register_redirection_command
def flare(arg):
    return 'https://dash.cloudflare.com/a15f589687872ed0f79023fa68776db3/rohanvarma.me'

# @CommandFactory.register_redirection_command
# def amazon(arg):
#     return amzn(arg)

# @CommandFactory.register_redirection_command
# def rbnhd(arg):
#     return robinhod(arg)


@CommandFactory.register_redirection_command
def fb(arg):
    if not arg:
        return 'https://facebook.com'
    else:
        FB_URL = 'https://facebook.com'
        # https://www.facebook.com/search/str/rohan+varma/keywords_search
        search_url = '/search/str/%s/keywords_search'
        arg_list = arg.split(" ")
        arg_str = "+".join(arg_list)
        complete_url = FB_URL + (search_url % arg_str)
        print('returning {}'.format(complete_url))
        return complete_url

@CommandFactory.register_redirection_command
def wiki(arg):
    if not arg:
        return 'https://wikipedia.org'
    else:
        # https://en.wikipedia.org/w/index.php?search=computer+science
        arg_list = arg.split(" ")
        arg_str = "+".join(arg_list)
        WIKI_URL = 'https://en.wikipedia.org/w/index.php'
        search_url = '?search=%s'
        complete_url = WIKI_URL + (search_url % arg_str)
        print('returning {}'.format(complete_url))
        return complete_url

@CommandFactory.register_redirection_command
def ucla(arg):
    if not arg:
        return "https://my.ucla.edu"
    else:
        if 'wooden' in arg:
            return 'https://www.recreation.ucla.edu/facilityhours#618141774-john-wooden-center-jwc-and-strength--conditioning-zones-scz'
        elif 'bfit' in arg:
            return 'https://www.recreation.ucla.edu/facilityhours#618141817-bruin-fitness-center-bfit'
        # dining halls
        elif 'bplate' in arg:
            if 'hours' in arg:
                return 'http://menu.dining.ucla.edu/Hours'
            else:
                return 'http://menu.dining.ucla.edu/Menus/BruinPlate/'
        elif 'covel' in arg:
            if 'hours' in arg:
                return 'http://menu.dining.ucla.edu/Hours'
            else:
                return 'http://menu.dining.ucla.edu/Menus/Covel/'
        elif 'covel' in arg:
            if 'hours' in arg:
                return 'http://menu.dining.ucla.edu/Hours'
            else:
                return 'http://menu.dining.ucla.edu/Menus/Covel/'

        # no one goes to these anyways...
        elif 'feast' in arg:
            if 'hours' in arg:
                return 'http://menu.dining.ucla.edu/Hours'
            else:
                return 'http://menu.dining.ucla.edu/Menus/FeastAtRieber/'
        elif 'de neve' in arg or 'deneve' in arg:
            if 'hours' in arg:
                return 'http://menu.dining.ucla.edu/Hours'
            else:
                return 'http://menu.dining.ucla.edu/Menus/DeNeve/'        




@CommandFactory.register_redirection_command
def twitter(arg):
    if not arg:
        return "https://twitter.com"
    else:
        TWITTER_URL = 'https://twitter.com'
        #https://twitter.com/search?q=rohan%20varma&src=typd&lang=en
        search_url = '/search?q=%s&src=typd&lang=en'
        arg_list = arg.split(" ")
        arg_str = "%20".join(arg_list)
        complete_url = TWITTER_URL + (search_url % arg_str)
        print('retuning {}'.format(complete_url))
        return complete_url

@CommandFactory.register_redirection_command
def robinhood(arg):
    # robinhood stock search
    if not arg:
        return "https://robinhood.com"
    else:
        RBNHD_URL = "https://robinhood.com"
        stocks_url = "/stocks/%s"
        arg_list = arg.split(" ")
        stock_to_search = arg_list[0]
        complete_url = RBNHD_URL + (stocks_url % stock_to_search)
        print('returning {}'.format(complete_url))
        return complete_url


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
