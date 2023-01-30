import subprocess, sys
import glob
import os

def process_part_frontmatter(partName):
    p = subprocess.Popen(f'xelatex {partName}', shell=True)
    p.wait()
    p = subprocess.Popen(f'bibtex Introduction.aux', shell=True)
    p.wait()
    p = subprocess.Popen(f'bibtex Preface.aux', shell=True)
    p.wait()
    p = subprocess.Popen(f'xelatex {partName}', shell=True)
    p.wait()
    p = subprocess.Popen(f'xelatex {partName}', shell=True)
    p.wait()

def process_part(partName):
    p = subprocess.Popen(f'xelatex {partName}', shell=True)
    p.wait()
    aux_files = glob.glob("./*.aux")
    for af in aux_files:
        p = subprocess.Popen(f'bibtex {af}', shell=True)
        p.wait()
    p = subprocess.Popen(f'xelatex {partName}', shell=True)
    p.wait()
    p = subprocess.Popen(f'xelatex {partName}', shell=True)
    p.wait()

if __name__ == '__main__':
    os.chdir("output")
    process_part_frontmatter("mainA")
    process_part("mainA")
    process_part("mainB")
    process_part("mainC")