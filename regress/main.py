# -*- coding: utf-8 -*-

import logging
import multiprocessing

from gunicorn.app.base import BaseApplication

from regress.server import app
from regress.database import init_database

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(name)s.%(module)s - %(message)s')
logger = logging.getLogger()


app.debug = True


def number_of_workers():
    return (multiprocessing.cpu_count() * 2) + 1


def main():
    init_database()
    if app.debug:
        logger.setLevel(logging.DEBUG)
        app.run(host='0.0.0.0')
    else:
        BaseApplication(app, {'timeout': 120, 'bind': ':5000', 'workers': number_of_workers()}).run()

if __name__ == '__main__':
    main()
