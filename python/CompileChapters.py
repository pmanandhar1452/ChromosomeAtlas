import subprocess, sys
import glob
import os
if __name__ == '__main__':
    os.chdir("output")
    subprocess.call('xelatex main')
    aux_files = glob.glob("./*.aux")
    for af in aux_files:
        subprocess.call(f'bibtex {af}')
    subprocess.call('xelatex main')
    subprocess.call('xelatex main')