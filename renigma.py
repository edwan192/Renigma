#!/bin/env python3
# -*- coding: utf-8 -*-

## Renigma, reverses enigma mappings, to use them to reobfurscate code.

##    Copyright (c) 2019 Edwan192
##
##    This program is free software: you can redistribute it and/or modify
##    it under the terms of the GNU General Public License as published by
##    the Free Software Foundation, either version 3 of the License, or
##    (at your option) any later version.
##
##    This program is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU General Public License for more details.
##
##    You should have received a copy of the GNU General Public License
##    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import sys, os;
import argparse;

class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)

class DefaultHelpParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)

def check_dir(name, create = False):
    if (os.path.isdir(name)):
        return True;
    else:
        if create and  not os.path.isfile(name):
            os.mkdir(name);
            return True;
        else:
            return False;

def create_parents_dirs(filename):
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

def reverse_mappings(folder_in, folder_out):
    walked = None;
    
    walked = os.walk(folder_in);
    
    for root, dirs, files in walked:
        if (root != folder_in):
            without_in = os.path.join(*(root.split(os.path.sep)[1:]));
        else:
            without_in = "";
        
        for file in files:
            mapping = os.path.join(without_in, file);
            if (mapping.endswith(".mapping")):
                reverse_mapping(folder_in, folder_out, mapping);

def reverse_mapping(folder_in, folder_out, file):
    create_parents_dirs(os.path.join(folder_out, file));
    
    with open(os.path.join(folder_in,  file), mode='r', encoding='UTF-8') as in_file, \
         open(os.path.join(folder_out, file), mode='w', encoding='UTF-8') as out_file:
        data = in_file.read();
        for line in data.splitlines():
            rline = reverse_line(line);
            print(rline, file=out_file);

def handle_class(line):
    line[1], line[2] = line[2], line[1];
    return line;

def handle_field(line):
    line[1], line[2] = line[2], line[1];
    return line;

def handle_method(line):
    if (len(line) == 3):
        return line;
    line[1], line[2] = line[2], line[1];
    return line;

def handle_arg(line):
    return line;

handlers = {
    "CLASS":  handle_class,
    "FIELD":  handle_field,
    "METHOD": handle_method,
    "ARG":    handle_arg,
};

def reverse_line(line):
    tabs = len(line) - len(line.lstrip('\t'));
    line = line.lstrip('\t');
    line = line.split(" ");
    
    assert line[0] in handlers, "No handler for type " + line[0] + ", aborting!";
    
    new_line = handlers[line[0]](line);
    new_line = ' '.join(new_line);
    new_line = ('\t' * tabs) + new_line;
    return new_line;

def main():
    parser = DefaultHelpParser(description='Reverses enigma mappings, to use them to reobfurscate code.');
    parser.add_argument('-i', '--in', help="Directory of input mappings.", required=True);
    parser.add_argument('-o', '--out', help="Directory to put new mappings to.", required=True);
    args = vars(parser.parse_args());
    
    assert check_dir(args["in"]), "Input folder doesn't exist, aborting!";
    assert check_dir(args["out"], True), "Can't create output folder, aborting!";

    reverse_mappings(args["in"], args["out"]);

if __name__ == "__main__":
   main();
