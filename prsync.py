#!/usr/bin/python

import argparse
from Queue import Queue
from threading import Thread
import os
import time
import sys
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("--workers", type=int,  help="number of workers", default=1)
parser.add_argument("--dirs", help="synchronize only dirs from file", default=False)
parser.add_argument("src", help="source directory")
parser.add_argument("dst", help="destination directory")
parser.add_argument("--debug", action="store_true", help="increase output verbosity")
args = parser.parse_args()

RSYNC = ['rsync', '-lptgoDxWd', '--inplace', '--size-only']
start = time.time()

def worker():
    while True:
        item = q.get()

        if args.debug:
            print "Syncing {0}/{2} to {1}/{2} ...".format(args.src, args.dst, item)

        src = ['{0}/{1}/'.format(args.src, item)]
        dst = ['{0}/{1}/'.format(args.dst, item)]
        subprocess.call(RSYNC + src + dst)

        if not args.dirs:
            for dir in next(os.walk("{0}/{1}".format(args.src, item)))[1]:
                q.put("{0}/{1}".format(item, dir))
        q.task_done()

def status():
    while True:
        sys.stdout.write("Directories left: {0}, Time: {1} s\r".format(q.qsize(), int(time.time() - start)))
        sys.stdout.flush()
        time.sleep(1)

q = Queue()
for i in range(args.workers):
    t = Thread(target=worker)
    t.daemon = True
    t.start()

t = Thread(target=status)
t.daemon = True
t.start()

if args.dirs:
    for file in open(args.dirs).read().splitlines():
        q.put(file)
else:
    q.put('/')

q.join()

print("\nTotal time: {0} s".format(int(time.time()- start)))