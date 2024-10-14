import os

from loguru import logger

if os.name == 'nt':
    dir_name = os.path.dirname(os.path.realpath(__file__)).split('\\')
    path_dir = '\\'.join(i for i in dir_name[:len(dir_name)-1]) + '\\'
elif os.name == 'posix':
    dir_name = os.path.dirname(os.path.realpath(__file__)).split('/')
    path_dir = '/'.join(i for i in dir_name[:len(dir_name)-1]) + '/'


logger.add(
            f'{path_dir}logs.log',
            encoding='utf8',
            format='[{time:YYYY-MM-DD HH:mm:ss}] {level} {message}',
            level='INFO', rotation="5 MB")
