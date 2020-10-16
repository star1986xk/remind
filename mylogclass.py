# -*- coding: utf-8 -*-
import logging
import logging.handlers
from datetime import datetime


class MyLogClass(object):
    def __init__(self):
        time_name = datetime.now().strftime("%Y-%m-%d, %H_%M_%S")
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        fh = logging.FileHandler(time_name + '.log', encoding='utf-8')
        formatter = logging.Formatter('%(asctime)s - %(message)s',
            '%Y/%m/%d %H:%M:%S')
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)
