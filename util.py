#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import os.path

def run_command(command):
    p = subprocess.Popen(command,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    return iter(p.stdout.readline, b'')

def findDict(dictionary, keyName):
    """
    Find a value in nest dictionary with some key name not known.
    https://stackoverflow.com/questions/19688078/how-to-access-a-nested-dict-without-knowing-sub-dicts-names
    """

    if not isinstance(dictionary, dict):
        return None

    if keyName in dictionary:
        return dictionary[keyName]

    for subdict in dictionary.values():
        ret = findDict(subdict, keyName)
        if ret:
            return ret


def _solidity_path():
    result = None
    compile_path = os.path.dirname(os.path.abspath(__file__))
    solidity_path = os.path.join(compile_path, "solidity")
    if os.path.exists(solidity_path):
        result = solidity_path

    return result

def _just_filename(file_name):
    basepath = os.path.dirname(file_name)
    return basepath is None or basepath == ""


def solidity_file_dirname(solidity_filename):
    just_filename = _just_filename(solidity_filename)
    if just_filename:
        solidity_path = _solidity_path()
        file_path = os.path.join(solidity_path, solidity_filename)
        is_exist = os.path.isfile(file_path)
        if is_exist:
            full_path_name =  os.path.abspath(file_path)
            return (solidity_filename,  os.path.dirname(file_path), full_path_name)
        else:
            print ("solidity file {} may be wrong format or not in folder 'solidity'".format(solidity_filename))
            return None
    else:
        return (os.path.basename(solidity_filename), os.path.dirname(solidity_filename), solidity_filename)
