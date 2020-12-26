import subprocess, sys
import glob

if __name__ == '__main__':
    subprocess.call('xelatex main')
    aux_files = glob.glob("./*.aux")
    for af in aux_files:
        subprocess.call(f'bibtex {af}')
    subprocess.call('xelatex main')
    subprocess.call('xelatex main')