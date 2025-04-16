@echo off
echo Running pass1.py...
python pass1.py

echo Running pass2.py...
python pass2.py

echo Running htme.py...
python htme.py

echo -----------------------------------------
echo Contents of output_pass1.txt:
type output_pass1.txt

echo -----------------------------------------
echo Contents of output_pass2.txt:
type output_pass2.txt

echo -----------------------------------------
echo Contents of HTME.txt:
type HTME.txt

echo -----------------------------------------
echo done :D

pause
