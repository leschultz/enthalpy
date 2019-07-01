#!/usr/bin/env python3

import subprocess
import os

runname = 'steps.in'

paths = []
count = 0
for path, subdirs, files in os.walk('./'):

    if runname not in files:
        continue

    paths.append(path)
    count += 1

newcount = 1
for path in paths:

    print(r'('+str(newcount)+'/'+str(count)+'): '+path)
    subprocess.run(['lmp_daily', '-in', runname], cwd=path)
    newcount += 1
