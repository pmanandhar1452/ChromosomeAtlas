import subprocess, sys
import glob
import os
if __name__ == '__main__':
    os.chdir("output")
    subprocess.Popen('xelatex main', shell=True)
    aux_files = glob.glob("./*.aux")
    for af in aux_files:
        subprocess.Popen(f'bibtex {af}', shell=True)
    subprocess.Popen('xelatex main', shell=True)
    subprocess.Popen('xelatex main', shell=True)