
'''
The script use to wrap the Java project into one single Java class.
Author:  Haotao Lai (Eric)
Contact: haotao.lai@gmail.com or h_lai@cs.concordia.ca
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Before you run:

- you MUST make sure there is no syntax error before you use this script
- the script should will put inside the root directory of your java project

- input:
    1. the project directory
    2. the destination of the output Java class
    3. the full name of the main class [optional]
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
'''

import sys
import os
import re
import argparse
import logging


def _wrap(_args_map):
    # a dict contains all the java files
    _targets_map = {}
    # a dict contains all the java file with a main method
    _mains_map = {}

    _find_java_files(_args_map, _targets_map)
    _key_list = _find_main_class(_targets_map, _mains_map)
    _main_key = _check_entry(_args_map, _mains_map, _key_list)
    _wrap_code(_args_map.get('out_path'), _main_key, _targets_map)


def _wrap_code(_out_dir, _main_key, _targets_map):
    _main_class = _targets_map.get(_main_key)
    _out_path = _out_dir[1:] + _main_class.name

    _import = re.compile(r'import\s+.*')
    _java_import = re.compile(r'import\s+java')
    _regx = re.compile(r'public\s+(class\s+.*\{*)')
    
    with open(_out_path, 'w') as otf, open(_main_class.path, 'r') as inf:
        for line in inf:
            is_import = re.match(_import, line)
            if is_import is not None:
                is_java_import = re.match(_java_import, line)
                if is_java_import is not None:
                    otf.write(line)
            else:
                otf.write(line)
        for k, c in _targets_map.items():
            if k != _main_key:
                with open(c.path, 'r') as another_class:
                    for line in another_class:
                        target = re.match(_regx, line)
                        if target is not None:
                            logging.debug('found public class')
                            otf.write(target.group(1))
                        else:
                            otf.write(line)
    logging.info('finish, the output locate in: ' + _out_path)
        

def _find_java_files(_args_map, _targets_map):
    _unique_suffix = 0
    for root, dirs, files in os.walk(_args_map.get('in_path'), topdown=True):
        for name in files:
            target_path = os.path.join(root, name)
            if target_path.endswith('.java'):
                # need to make the name unique, since different package
                # may have class with the same name
                key = name + '__' + str(_unique_suffix)
                a_class = ClassStruct(name, target_path)
                _targets_map[key] = a_class
                _unique_suffix += 1
    for target in _targets_map.keys():
        logging.debug(target)

def _find_main_class(_targets_map, _mains_map):
    key_list = []
    # regular expression to find the main class
    regx = re.compile(r'^public static void main(\w*).*')
    for key, class_struct in _targets_map.items():
        with open(class_struct.path, 'r') as f:
            for line in f:
                if re.match(regx, line.strip()):
                    _mains_map[key] = class_struct
                    key_list.append(key)

    # - - - - - debug message block - - - - -
    for class_struct in _targets_map.values():
        logging.debug('[file name]: ' + class_struct.name +
                      ' \n\t\t[file path]: ' + class_struct.path)
    logging.debug('* * * [main] * * *')
    for class_struct in _mains_map.values():
        logging.debug('[file name]: ' + class_struct.name +
                      ' \n\t\t[file path]: ' + class_struct.path)
    logging.debug('* * * [main] * * *')
    # - - - - - end of debug message - - - - -
    return key_list


def _check_entry(_args_map, _mains_map, _key_list):
    entry = _args_map.get('entry')
    if entry is not None:
        logging.info('user speciiedy the entry of the program [' + entry + ']')
        if not entry.endswith('.java'):
            entry += '.java'
    
    _main_class = None
    if entry is None and len(_mains_map) == 1:
        _main_class = _mains_map[_key_list[0]]
        logging.info('user didn\'t specify the entry of the program ' + 'take the [' + _main_class.name + '] as the entry')
    
    if entry is None and len(_mains_map) > 1:
        logging.error('too many main methods, please specify one as entry !')
        for a_class in _mains_map.values():
            logging.error('duplicate found: ' + a_class.path)
        sys.exit(1)
    
    else:
        if entry is None:
            entry = _main_class.name
        _key, _main_class = _check_duplicate_entry(entry, _mains_map)
        return _key

def _check_duplicate_entry(entry_name, mains_map):
    # loop over main targets, if more than one class with
    # that name, issue an error message
    duplicate = []
    entry_regx = re.compile(entry_name + r'__\d')
    for key, class_struct in mains_map.items():
        if re.match(entry_regx, key):
            duplicate.append(class_struct)
    if len(duplicate) > 1:
        logging.error('too many classes with the same specified entry name')
        for a_class in duplicate:
            logging.error('duplicate found: ' + a_class.path)
        sys.exit(1)
    if len(duplicate) == 1:
        return key, duplicate[0]


def _add_args():
    _parser.add_argument('-i', nargs='?', default='.',
                         action='store', dest='in_path',
                         help='the root of the Java project')
    _parser.add_argument('-o', nargs='?', default='.',
                         action='store', dest='out_path',
                         help='the destination of the wrapped Java program')
    _parser.add_argument('-m', nargs='?', action='store', dest='entry',
                         help='the entry of the source Java program')


class ClassStruct:
    
    def __init__(self, name, path):
        self._file_name = name
        self._file_path = path

    def __str__(self):
        print('name: ' + self._file_name + ', path: ' + self._file_path)

    @property
    def path(self):
        return self._file_path

    @property
    def name(self):
        return self._file_name

if __name__ == '__main__':
    # logging.basicConfig(level='DEBUG')
    logging.basicConfig(level='INFO')
    _parser = argparse.ArgumentParser(description='Java Wrapper Script')
    _add_args()
    _args_map = vars(_parser.parse_args())
    _wrap(_args_map)
    sys.exit(0)
else:
    pass

# end of file