#!/bin/sh

FOLDER=~/Library/CloudStorage/GoogleDrive-engineer.manandhar@gmail.com/.shortcut-targets-by-id/1L9Iud7qS4SmO_696Y15FRTHgKeIuPCJ9/Laxmi\ Manandhar\ Book\ Publication
mkdir -p output
cp "$FOLDER"/references/final-merged-bibtex/Bibliography.bib ./output/
cp -r "$FOLDER"/LatexSrc/ChromosomeNumberReportsBook_Laxmi_2021/* ./output/
python3.9 -m ChromosomeAtlas.LatexGenerator
python3.9 CompileChapters.py
#For /f "tokens=1,2,3,4,5 delims=/. " %%a in ('date/T') do set CDate=%%d-%%b-%%c
#For /f "tokens=1,2 delims=:" %%f in ('time /t') do set CTime=%%f%%g
NOW=`date '+%F-%l%M %p'`
cp ./output/mainA.pdf "$FOLDER"/output_pdfs/"$NOW-A".pdf
cp ./output/mainB.pdf "$FOLDER"/output_pdfs/"$NOW-B".pdf
cp ./output/mainC.pdf "$FOLDER"/output_pdfs/"$NOW-C".pdf
