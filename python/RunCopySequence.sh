#!/bin/sh

FOLDER=~/Library/CloudStorage/GoogleDrive-engineer.manandhar@gmail.com/.shortcut-targets-by-id/1L9Iud7qS4SmO_696Y15FRTHgKeIuPCJ9/Laxmi\ Manandhar\ Book\ Publication
mkdir -p output
cp "$FOLDER"/references/final-merged-bibtex/Bibliography.bib ./output/
# rm -f output/*.aux
# rm -f output/*.bbl
# rm -f output/*.blg

cp -r "$FOLDER"/LatexSrc/ChromosomeNumberReportsBook_Laxmi_2021/* ./output/
python3.9 -m ChromosomeAtlas.LatexGenerator
python3.9 CompileChapters.py
NOW=`date '+%F-%l%M %p'`
# cp ./output/mainA.pdf "$FOLDER"/output_pdfs/"ChromosomeNumberReportsBook_Laxmi_$NOW-A".pdf
# cp ./output/mainB.pdf "$FOLDER"/output_pdfs/"ChromosomeNumberReportsBook_Laxmi_$NOW-B".pdf
cp ./output/mainC.pdf "$FOLDER"/output_pdfs/"ChromosomeNumberReportsBook_Laxmi_$NOW-C".pdf
# cp ./output/mainD.pdf "$FOLDER"/output_pdfs/"ChromosomeNumberReportsBook_Laxmi_$NOW-D".pdf
cp ./output/species_count.csv "$FOLDER"/output_pdfs/"ChromosomeNumberReportsBook_SpeciesCount_$NOW".csv
cp ./output/all_use_codes.csv "$FOLDER"/output_pdfs/"ChromosomeNumberReportsBook_UseCodes_$NOW".csv