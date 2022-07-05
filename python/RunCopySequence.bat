if not exist "output" mkdir output
copy "G:\.shortcut-targets-by-id\1L9Iud7qS4SmO_696Y15FRTHgKeIuPCJ9\Laxmi Manandhar Book Publication\references\final-merged-bibtex\Bibliography.bib" .\output\
robocopy "G:\.shortcut-targets-by-id\1L9Iud7qS4SmO_696Y15FRTHgKeIuPCJ9\Laxmi Manandhar Book Publication\LatexSrc\ChromosomeNumberReportsBook_Laxmi_2021" .\output\ /E
python -m ChromosomeAtlas.LatexGenerator
python CompileChapters.py
For /f "tokens=1,2,3,4,5 delims=/. " %%a in ('date/T') do set CDate=%%d-%%b-%%c
For /f "tokens=1,2 delims=:" %%f in ('time /t') do set CTime=%%f%%g
copy .\output\mainA.pdf "G:\.shortcut-targets-by-id\1L9Iud7qS4SmO_696Y15FRTHgKeIuPCJ9\Laxmi Manandhar Book Publication\output_pdfs\%CDate%-%CTime%-A.pdf"
copy .\output\mainB.pdf "G:\.shortcut-targets-by-id\1L9Iud7qS4SmO_696Y15FRTHgKeIuPCJ9\Laxmi Manandhar Book Publication\output_pdfs\%CDate%-%CTime%-B.pdf"
copy .\output\mainC.pdf "G:\.shortcut-targets-by-id\1L9Iud7qS4SmO_696Y15FRTHgKeIuPCJ9\Laxmi Manandhar Book Publication\output_pdfs\%CDate%-%CTime%-C.pdf"