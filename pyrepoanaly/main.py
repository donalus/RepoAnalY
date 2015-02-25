# Copyright 2015 Donal Heidenblad
#
# This file is part of RepoAnalY.
#
# RepoAnalY is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# RepoAnalY is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with RepoAnalY.  If not, see <http://www.gnu.org/licenses/>.
#
# Authors : Donal Heidenblad <dheidenb@umd.edu>


"""
The place where everything happens.

@author:       Donal Heidenblad
@copyright:    2015 Donal Heidenblad
@license:      GNU GPL version 3 or any later version
@contact:      dheidenb@umd.edu
"""

import os
import getopt
import subprocess

def usage():
    print "Usage: repoanaly [options] [PROJECT]"
    print """
RepoAnalY is provided under the GNU General Public License version 3.
For more details see the file `COPYING' that should have been
distributed with this program. If not, see <http://www.gnu.org/licenses>.
"""

def main(argv):
    # Short (one letter) options. Those requiring argument followed by :
    short_opts = "hVl:"
    # Long options (all started by --). Those requiring argument
    # followed by =
    long_opts = ["help", "version", "skip-to="]

    try:
        opts, args = getopt.getopt(argv, short_opts, long_opts)
    except getopt.GetoptError, e:
        printerr(str(e))
        return 1

    skipn = 0
    
    for opt, value in opts:
        if opt in ("-h", "--help", "-help"):
            usage()
            return 0
        elif opt in ("-V", "--version"):
            print VERSION
            return 0
        elif opt in ("-l", "--skip-to"):
            skipn = int(value)

    if len(args) <= 0:
        project  = os.getcwd()
    else:
        project = args[0]

    fullpath = os.path.join(project, ".repo/project.list")

    if os.path.isfile(fullpath):
        f = open(fullpath, "r")

        projects = []

        cnt = 0
        for line in f:
            if cnt >= skipn:
                proj = line.replace("\n", "")
                print proj
                subprocess.call(["cvsanaly2", "-uresearcher", "-pcvsanaly",
                "-dcvsanaly-aosp", os.path.join(project, proj)])

            cnt += 1

        print cnt
    else:
        print "Directory is not a Repo Project"

