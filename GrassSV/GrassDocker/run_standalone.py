#!/usr/local/bin/python

import shlex
from subprocess import Popen, PIPE
import os, shutil, sys
from enum import Enum, IntEnum

def run_standalone(genome, genome_lengths, index, reads1, reads2):
    cmd = os.path.dirname(__file__) + f"/run_standalone.sh -g {genome} -i {index} -l {genome_lengths} -r {reads1} -R {reads2}"
    args = shlex.split(cmd)

    proc = Popen(args, stdout=sys.stdout, stderr=sys.stderr, )


    out, err = proc.communicate()
    exitcode = proc.returncode
    if exitcode == 0:
        print("Pipeline exited without errors")
    else:
        print("Pipeline failed")
    return exitcode