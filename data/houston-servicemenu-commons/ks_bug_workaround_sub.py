#!/usr/bin/python3

import sys
import subprocess
import pickle

tmpfile = sys.argv[1]
f = open(tmpfile, 'rb')
post_e_list = pickle.load(f)
f.close()

subprocess.run(post_e_list)
