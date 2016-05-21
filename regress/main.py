# -*- coding: utf-8 -*-

import sys
import argparse
import logging

from regress.server import app
from regress.database import init_database

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(name)s.%(module)s - %(message)s')
logger = logging.getLogger()
app.debug = True


def main():
    parser = argparse.ArgumentParser("regress")
    parser.add_argument("--init", action="store_true", help="initialize the database")
    args = parser.parse_args()
    if args.init:
        init_database()
        sys.exit(0)
    init_database()
    logger.setLevel(logging.DEBUG)
    app.run(host='0.0.0.0')

if __name__ == '__main__':
    main()
