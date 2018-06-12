from flask import (Blueprint, redirect, request)

from search.commands import CommandFactory, ResultType

import search.google

search = Blueprint('search', 'bunnysearch', url_prefix='/search')
commands = CommandFactory.export()

@search.route('/')
def show():
    if request.args and 'query' in request.args:
        query = request.args['query']
        split = query.split(' ', 1)
        if len(split) == 1:
            method = split[0]
            margs = ''
        else:
            method, margs = split
        result, rtype = (None, None)
        if not method or method not in commands.cmd_list:
            for cmd in commands.dynamic_commands:
                result, rtype = cmd(query)
                if result:
                    break
        else:
            cmd = commands.cmd_list.get(method, None)
            result, rtype = cmd(margs)

        if rtype == ResultType.REDIRECTION:
            return redirect(result)
        elif rtype == ResultType.CONTENT:
            # TODO: Add support to directly rendering content
            return result
        else:
            return "nothing doing"
    elif request.args and 'suggest' in request.args:
        return ''
    else:
        return ''

