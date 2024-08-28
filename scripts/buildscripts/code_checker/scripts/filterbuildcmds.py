#!/usr/bin/python

#TODO: Add comments for methods

import argparse
import json
import re
import sys


def add_arguments():
    parser = argparse.ArgumentParser(
        description='Filter out duplicated compile commands')
    parser.add_argument('-o', '--outputfile',
                        help='Output file of filtered commands',
                        metavar='OutFile', dest='outFile', default=None,
                        required=True)
    parser.add_argument('-i', '--inputfile',
                        help='File of the generated build commans file',
                        metavar='InFile', dest='inputFile', default=None,
                        required=True)
    return parser


def parse_arguments(parser):
    args = parser.parse_args()
    return args


def load_original_file(inputFile):
    with open(inputFile, mode='r') as json_file:
        compilation_database = json.load(json_file)
    return compilation_database


def filter_compilation_actions(actions):
    return filter(lambda action: re.match('.*.\.(cc?|cxx|cpp)$',
                                          action['file']),
                  actions)

def remove_werror_flags_from_commands(actions):
    for action in actions:
        action['command'] = action['command'].replace(' -Werror', '')
        yield action


def main():
    parser = add_arguments()
    args = parse_arguments(parser)

    actions = load_original_file(args.inputFile)
    # Filter out duplicated compiler commands of a particular source
    actions = {action['file']: action for action in actions}.values()
    actions = filter_compilation_actions(actions)
    actions = remove_werror_flags_from_commands(actions)

    with open(args.outFile, mode='w') as json_file:
        json.dump(list(actions), json_file, indent=4)
    return 0


if __name__ == "__main__":
    sys.exit(main())
