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

def reverse_mappings(folder_in, folder_out):
    pass;

def main():
    parser = DefaultHelpParser(description='Reverses enigma mappings, to use them to reobfurscate code.');
    parser.add_argument('-i', '--in', help="Directory of input mappings.", required=True);
    parser.add_argument('-o', '--out', help="Directory to put new mappings to.", required=True);
    args = vars(parser.parse_args());
    
    assert check_dir(args["in"]), "Input folder doesn't exist, aborting!";
    assert check_dir(args["out"], True), "Can't create output folder, aborting!";

if __name__ == "__main__":
   main();
