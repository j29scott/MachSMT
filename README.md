# SMTZILLA

This is the repo for SMTZILLA. 

SMTZILLA can be installed easily via the command `sudo python3 setup.py install` (as requirements.txt is not prepared, you may need to install a few pip3 packages). This will install two scripts:

* smtzilla_select - the primary interface to SMTZILLA's algorithm selection
* smtzilla_build  - a script to learn models for algorithm selection in SMTZILLA's pipeline.

# smtzilla_select
The algorithm selection script can be ran with the following syntax: `smtzilla_select --file FILE --theory THEORY --track TRACK`. SMTZilla will then print the name of the solver it selects to have the shortest runtime. 

# smtzilla_build
