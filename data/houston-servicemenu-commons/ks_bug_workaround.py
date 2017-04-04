#!/usr/bin/python3

#these files exists because of a very strong bug on konsole since 16.08 version : https://bugs.kde.org/show_bug.cgi?id=366793

import sys
import subprocess
import tempfile
import pickle

tmpfile = tempfile.mktemp()

arg_list = sys.argv[1:]

before_e = True
pre_e_list  = ['konsole']
post_e_list = []

for arg in arg_list:
    if before_e:
        pre_e_list.append(arg)
        
        if arg == '-e':
            before_e = False
    else:
        post_e_list.append(arg)

f = open(tmpfile, 'wb')
pickle.dump(post_e_list, f)
f.close()



self_dir_list = sys.argv[0].split('/')
self_dir_str  = ''

for i in range(len(self_dir_list)-1):
    self_dir_str += self_dir_list[i] + '/'
    
pre_e_list.append(self_dir_str + 'ks_bug_workaround_sub.py')
pre_e_list.append(tmpfile)

subprocess.run(pre_e_list)

