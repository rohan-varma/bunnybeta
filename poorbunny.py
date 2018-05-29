from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

import argparse

import cherrypy

from bunny_commands import CommandFactory, ResultType


DEFAULT_PORT = 10086
DETAULT_CMD = 'g'


class PoorBunny(object):
    def __init__(self, commands=None):
        if not commands:
            commands = CommandFactory.export()
        self.commands = commands

    @cherrypy.expose
    def default(self, *args, **kwargs):
        return self.do_command(*args, **kwargs)

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
    return cherrypy.quickstart(bunny)


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

