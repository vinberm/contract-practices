#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os.path
from pathlib import Path
from util import run_command, findDict, solidity_file_dirname
from solc import compile_standard, compile_files, compile_source
import json


def save_abi(abi):
    with open("./output/compiled/abi", "w+") as abifile:
        json.dump(abi, abifile, indent=4)


def save_bincode(code):
    with open("./output/compiled/bytecode", "w+") as code_file:
        code_file.write(code)

def save_functions(data):
    with open("./output/compiled/functions", "w+") as func_file:
        json.dump(data, func_file, indent=4)

def save_output(op):
    with open("./output/compiled/outputs", "w+") as op_file:
        json.dump(op, op_file, indent=4)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--source', help="Solidity source code")
    parser.add_argument('-f', '--file', help="path name of solidity file")
    parsed = parser.parse_args()
    print("|-------------------------------|")
    print(parsed)
    print("|-------------------------------|")

    compile_path = Path("./output/compiled")
    if not compile_path.is_dir():
        command = 'mkdir -p ./output/compiled'.split()
        for line in run_command(command):
            print(line)

    if parsed.source:
        solidity_source = parsed.source
        output = compile_standard({
            'language': 'Solidity',
            'sources': {'standard.sol': {'content': solidity_source}}
        })

        print("contract bytecode stored in 'output/compiled/bytecode'")
        save_abi(findDict(output['contracts'], 'abi'))
        print("function signature stored in 'output/compiled/functions'")
        save_functions(findDict(output, 'methodIdentifiers'))
        # save_output(output)

        bytecode = compile_source(parsed.source)
        print("contract bytecode stored in 'output/compiled/bytecode'")
        save_bincode(str(findDict(bytecode, 'bin')))
        save_output(bytecode)
        print(str(findDict(bytecode, 'bin')))

    elif parsed.file:

        print(parsed.file)
        paths = solidity_file_dirname(parsed.file)
        origin_path = os.getcwd()
        if paths is not None:
            filename, basepath, fullpath = paths
            # dir: solidity
            os.chdir(basepath)
            output = compile_standard({
                'language': 'Solidity',
                'sources': {filename: {'urls': [fullpath]}},
            }, allow_paths=basepath)

            # dir: contractool
            os.chdir(origin_path)
            save_output(output)
            print("contract abi stored in 'output/compiled/abi'")
            save_abi(findDict(output['contracts'], 'abi'))

            bytecode = compile_files([parsed.file])
            print('------', bytecode)
            print("contract bytecode stored in 'output/compiled/bytecode'")
            save_bincode(str(findDict(bytecode, 'bin')))

            print("function signature stored in 'output/compiled/functions'")
            save_functions(findDict(output, 'methodIdentifiers'))
            print(str(findDict(bytecode, 'bin')))


if __name__ == "__main__":
    main()
