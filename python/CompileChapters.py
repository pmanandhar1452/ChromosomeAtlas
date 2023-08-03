import subprocess, sys
import glob
import os

RUN_BIBTEX_FRONT = True
RUN_BIBTEX_PARTS = True
RUN_PART_A = False
RUN_PART_B = False
RUN_PART_C = True


def process_part_frontmatter(partName):
    if RUN_BIBTEX_FRONT:
        p = subprocess.Popen(f"bibtex Introduction.aux", shell=True)
        p.wait()
        p = subprocess.Popen(f"bibtex Preface.aux", shell=True)
        p.wait()

    if RUN_BIBTEX_PARTS:
        if RUN_PART_A:
            p = subprocess.Popen(f"xelatex {partName}", shell=True)
            p.wait()
        if RUN_PART_B:
            p = subprocess.Popen(f"xelatex {partName}", shell=True)
            p.wait()
        if RUN_PART_C:
            p = subprocess.Popen(f"xelatex {partName}", shell=True)
            p.wait()


def process_part(partName):
    p = subprocess.Popen(f"xelatex {partName}", shell=True)
    p.wait()
    aux_files = glob.glob("./*.aux")
    for af in aux_files:
        p = subprocess.Popen(f"bibtex {af}", shell=True)
        p.wait()
    p = subprocess.Popen(f"xelatex {partName}", shell=True)
    p.wait()
    p = subprocess.Popen(f"xelatex {partName}", shell=True)
    p.wait()


if __name__ == "__main__":
    os.chdir("output")
    process_part_frontmatter("mainA")
    if RUN_PART_A:
        process_part("mainA")
    if RUN_PART_B:
        process_part("mainB")
    if RUN_PART_C:
        process_part("mainC")
