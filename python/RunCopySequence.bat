if not exist "output" mkdir output
copy "C:\Users\laxmi\Google Drive\Laxmi Manandhar Book Publication\references\final-merged-bibtex\Bibliography.bib" .\output\
robocopy "C:\Users\laxmi\Google Drive\Laxmi Manandhar Book Publication\LatexSrc\ChromosomeNumberReportsBook_Laxmi_2020" .\output\ /E
python -m ChromosomeAtlas.LatexGenerator
python CompileChapters.py
For /f "tokens=1,2,3,4,5 delims=/. " %%a in ('date/T') do set CDate=%%d-%%b-%%c
For /f "tokens=1,2 delims=:" %%f in ('time /t') do set CTime=%%f%%g
copy .\output\main.pdf "C:\Users\laxmi\Google Drive\Laxmi Manandhar Book Publication\output_pdfs\%CDate%-%CTime%.pdf"