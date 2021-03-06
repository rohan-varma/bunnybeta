from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

from flask import (Flask, request, render_template)

from search import search


def create_app(test_config=None):
    # create and configure
    app = Flask('Bunny', instance_relative_config=True)
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    app.register_blueprint(search)

    @app.route('/')
    def home():
        return render_template('index.html', base_url = request.url_root)

    @app.route('/bunnysearch.xml')
    def search_xml():
        return render_template('bunnysearch.xml', base_url = request.url_root)


    return app
