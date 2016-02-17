# prsync
Prsync is parallel wrapper for rsync written in python which use Thread and Queue module.
The main idea is to rsync each directory separately without recursion and add all subdirectories to queue.
The number of workers is configured from command line as parameter.

## Usage
```
usage: prsync.py [-h] [--workers WORKERS] [--dirs FILE] [--debug] src dst

positional arguments:
  src                source directory
  dst                destination directory

optional arguments:
  -h, --help         show this help message and exit
  --workers WORKERS  number of workers
  --debug            increase output verbosity
  --dirs FILE        synchronize only dirs from file  
```

## Example
prsync.py --workers 16 /home/old /home/new