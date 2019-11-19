# -*- coding:utf-8 -*-
import os
from ConfigParser import ConfigParser, NoOptionError, NoSectionError

config = ConfigParser()
WORK_DIR = os.path.abspath(os.path.dirname(__file__))
CONFIG_FILE = os.path.join(WORK_DIR, 'config.ini')
if not os.path.exists(CONFIG_FILE):
    print("file {} is not exists.".format(CONFIG_FILE))
else:
    config.read(CONFIG_FILE)
try:
    HOST = config.get('common', 'HOST')
    PORT = config.getint('common', 'PORT')
    NUMBER_PER_PAGE = config.getint('common', 'NUMBER_PER_PAGE')

    FIX_DICT_PATH = os.path.join(WORK_DIR, config.get("fix", 'FIX_DICT_PATH'))
    STANDARD_FIX_LIST = str(config.get('fix', 'STANDARD_FIX')).split(",")
    STANDARD_FIX_LIST = [item.strip(" ") for item in STANDARD_FIX_LIST]
    CUSTOM_FIX_LIST = str(config.get('fix', 'CUSTOM_FIX')).split(",")
    CUSTOM_FIX_LIST = [item.strip(" ") for item in CUSTOM_FIX_LIST]
    DELIMITER_PATTERN = r'[;|?,\x01]+?'
    MESSAGE_PATTERN = r'8=FIX.\d.\d{}9=\d+{}35=\w{}.+?10=\d\d\d{}|8=FIX.\d.\d\^A9=\d+\^A35=\w\^A.+?10=\d\d\d\^A'\
        .format(DELIMITER_PATTERN, DELIMITER_PATTERN, DELIMITER_PATTERN, DELIMITER_PATTERN)
    FIELD_PATTERN = r'\d+=.+?{}|\d+=.+?\^A'.format(DELIMITER_PATTERN)

except NoSectionError as e:
    print("{} NoSection: {}".format(CONFIG_FILE, e))
except NoOptionError as e:
    print("{} NoOption: {}".format(CONFIG_FILE, e))
except Exception as e:
    print("Parse config.ini failed: {}".format(e))


