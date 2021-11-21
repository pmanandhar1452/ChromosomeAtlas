#!/bin/sh

FOLDER=~/Google\ Drive/Laxmi\ Manandhar\ Book\ Publication
mkdir -p output
cp "$FOLDER"/references/final-merged-bibtex/Bibliography.bib ./output/
cp -r "$FOLDER"/LatexSrc/ChromosomeNumberReportsBook_Laxmi_2021/* ./output/
python3.9 -m ChromosomeAtlas.LatexGenerator
python3.9 CompileChapters.py
#For /f "tokens=1,2,3,4,5 delims=/. " %%a in ('date/T') do set CDate=%%d-%%b-%%c
#For /f "tokens=1,2 delims=:" %%f in ('time /t') do set CTime=%%f%%g
NOW=`date '+%F-%l%M %p'`
cp ./output/main.pdf "$FOLDER"/output_pdfs/"$NOW".pdf
