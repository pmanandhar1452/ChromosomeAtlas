 robocopy "C:\Users\Prakash\Dropbox (MIT)\Apps\Overleaf\ChromosomeNumberReportsBook_Laxmi_2020" ./output /MIR /XX
 python -m ChromosomeAtlas.LatexGenerator
 robocopy .\output "C:\Users\Prakash\Dropbox (MIT)\Apps\Overleaf\ChromosomeNumberReportsBook_Laxmi_2020" /MIR /XX /XO