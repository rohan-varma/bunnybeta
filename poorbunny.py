from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

import argparse
import os

import cherrypy

from .bunny_commands import CommandFactory, ResultType

DEFAULT_PORT = 10086

file = open('public/index.html', 'r')
index = file.read()
file.close

class PoorBunny(object):
    def __init__(self, commands=None):
        if not commands:
            commands = CommandFactory.export()
        self.commands = commands

    @cherrypy.expose
    def default(self, *args, **kwargs):
        return index

    @cherrypy.expose
    def search(self, *args, **kwargs):
        return self.do_command(*args, **kwargs)

    @cherrypy.expose
    def help(self, *args, **kwargs):
        return """
            Available Commands:

            <br /><b>gmail [1|2..]</b>: Go to gmail (Defaults to account 0)
            <br /><b>namely</b>: Goes to namely
            <br /><b>gh [*|reponame|att.. [searchterm]]</b>: Goes to github, optionally jump to a repo or search that codebase for a term
            <br /><b>confluence searchterm</b>: searches the Confluence wiki for the given search term
            <br /><b>wiki</b>: alias for confluence
            <br /><b>jira</b>: Jump to JIRA, a ticket and task manager
            <br /><b>grafana</b>: Metrics portal for visualizing the metrics from InfluxDB
            <br /><b>askbot searchterm</b>: Searches askbot, an internal question/answer service (like StackOverflow)
            <br />
            <br /><b>{JIRA TICKET NUMBER} </b>: jump to ticket number
            <br /><b>{Phabricator diff number} </b>: Jump to diff

        """

    def do_command(self, *args, **kwargs):
        if kwargs and 'query' in kwargs:
            split = kwargs['query'].split(' ', 1)
            if len(split) == 1:
                method = split[0]
                margs = ''
            else:
                method, margs = split
            result, rtype = (None, None)
            if not method or method not in self.commands.cmd_list:
                for cmd in self.commands.dynamic_commands:
                    result, rtype = cmd(kwargs['query'])
                    if result:
                        break
            else:
                cmd = self.commands.cmd_list.get(method, None)
                result, rtype = cmd(margs)
            if rtype == ResultType.REDIRECTION:
                print("redirecting")
                raise cherrypy.HTTPRedirect(result)
            elif rtype == ResultType.CONTENT:
                # TODO: Add support to directly rendering content BEAUTIFULLY..
                return result


def start_bunny_server(bunny, port=None, host='0.0.0.0', errorlog=None, accesslog=None):
    if not port:
        port = DEFAULT_PORT
    if not host:
        host = '127.0.0.1'
    cherrypy.server.socket_host = host
    cherrypy.server.socket_port = port
    cherrypy.config['log.error_file'] = errorlog
    cherrypy.config['log.access_file'] = accesslog
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.on' : True,
            'tools.staticdir.root': os.path.abspath(os.getcwd()),
            'tools.staticdir.dir': './public',
            'tools.staticdir.index' : "public/index.html"
        },
        '/static':
            {
                'tools.staticdir.on': True,
                'tools.staticdir.dir': './public'
            }
    }
    return cherrypy.quickstart(bunny, '', conf)


def parse_args():
    parser = argparse.ArgumentParser(description='Poor Bunny Server.')
    parser.add_argument('--port', type=int, required=False,
                        help='Port to run')
    parser.add_argument('--host', type=str, required=False,
                        help='accesslog path')
    parser.add_argument('--errorlog', type=str, required=False,
                        help='errorlog path')
    parser.add_argument('--accesslog', type=str, required=False,
                        help='accesslog path')
    return parser.parse_args()


def main():
    args = parse_args()
    start_bunny_server(PoorBunny(), args.port, args.host, args.errorlog, args.accesslog)


if __name__ == '__main__':
    main()

