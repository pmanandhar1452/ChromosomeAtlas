import subprocess, sys
import glob
import os
if __name__ == '__main__':
    os.chdir("output")
    p = subprocess.Popen('xelatex mainA', shell=True)
    p.wait()
    aux_files = glob.glob("./*.aux")
    for af in aux_files:
        p = subprocess.Popen(f'bibtex {af}', shell=True)
        p.wait()
    p = subprocess.Popen('xelatex mainA', shell=True)
    p.wait()
    p = subprocess.Popen('xelatex mainA', shell=True)
    p.wait()

    p = subprocess.Popen('xelatex mainB', shell=True)
    p.wait()
    aux_files = glob.glob("./*.aux")
    for af in aux_files:
        p = subprocess.Popen(f'bibtex {af}', shell=True)
        p.wait()
    p = subprocess.Popen('xelatex mainB', shell=True)
    p.wait()
    p = subprocess.Popen('xelatex mainB', shell=True)
    p.wait()

    p = subprocess.Popen('xelatex mainC', shell=True)
    p.wait()
    aux_files = glob.glob("./*.aux")
    for af in aux_files:
        p = subprocess.Popen(f'bibtex {af}', shell=True)
        p.wait()
    p = subprocess.Popen('xelatex mainC', shell=True)
    p.wait()
    p = subprocess.Popen('xelatex mainC', shell=True)
    p.wait()