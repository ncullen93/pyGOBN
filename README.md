# pyGOBNILP

<h2>Overview</h2>
This is a project to create Python bindings for the amazing GOBNILP code
for Bayesian Network structure learning. This is the work of Nicholas Cullen
and is not affiliated with GOBNILP. Still, all credit for this work goes to
Dr. James Cussens and Dr. Mark Bartlett for the creation of GOBNILP.

<h3>GOBNILP Usage</h3>

GOBNILP is distributed under the GNU Public Licence (version 3) and is available
for download via http://www.cs.york.ac.uk/aig/sw/gobnilp. The following
installation instructions assume that you are using Linux. (We suspect
it would not be too hard to install under Windows or Mac as long as you have
a C compiler and the ‘make’ utility.)
1. Assuming you meet the relevant licence conditions ( http://scip.zib.
de/licence.shtml ), download SCIP ( http://scip.zib.de) if you do
not already have it installed. GOBNILP 1.6.2 has only been tested using
SCIP 3.2.0 (the current SCIP version at time of writing) so please use that
version. We expect that it will work with future versions of SCIP.
2. Install SCIP following the instructions that come with it. If you have
CPLEX installed be sure to make a CPLEX-linked version of SCIP.
3. Let <version> denote the GOBNILP version that you have downloaded.
Do tar zxf gobnilp<version>.tar.gz (if you downloaded the .tgz
archive) or unzip gobnilp<version>.zip (if you downloaded the .zip
file) to put the GOBNILP distribution in a directory of your choosing. This
directory will be called $(GOBNILPDIR) in what follows.
4. Ensure $(GOBNILPDIR) is your current working directory and run
./configure.sh $(SCIPDIR) where $(SCIPDIR) is the directory where
you installed SCIP. For example,
./configure.sh /opt/scipoptsuite-3.2.0/scip-3.2.0 . This will create
a soft link scip in $(GOBNILPDIR) that links to $(SCIPDIR), which is
needed by the GOBNILP make file to find the SCIP files. This script will
also copy $(SCIPDIR)/examples/LOP/src/cons_linearordering.c and
$(SCIPDIR)/examples/LOP/src/cons_linearordering.h into
$(GOBNILPDIR)/src.
5. Ensure $(GOBNILPDIR) is your current working directory. Type make or,
if you have CPLEX installed, make LPS=cpx.
3
6. An executable $(GOBNILPDIR)/bin/gobnilp will be created. This will be
a symbolic link to a file with a much longer name.
7. If you have doxygen installed you can use it to create HTML documentation
for the GOBNILP source code. To do this do make docs and then
point your web browser at $(GOBNILPDIR)/docs/html/index.html. You
can edit the file Doxyfile in the GOBNILP distribution to alter the sort
of HTML documentation you get.
8. If you have any problems installing you may need to run make clean
which will remove everything the other make targets create.
If you are using GOBNILP we would appreciate it if you let us know. Please
do so by email to james.cussens@york.ac.uk and put gobnilp somewhere in
the subject header. We are particularly keen to hear about any problems you
may have with GOBNILP.