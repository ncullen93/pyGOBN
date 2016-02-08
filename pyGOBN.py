"""
Code for installing, making, and calling GOBNILP solver for 
Bayesian Network Structure learning from Python. 

The advantage of using this file is that the source 
code will be automatically compiled, error handling can be 
done automatically at all steps of the process, and most importantly,
GOBNILP functionality can now be included in any Python library.


Please note that this re-distribution of GOBNILP is
done under the GNU Public License - ALL credit for that
solver goes to its creators Dr. James Cussens and 
Dr. Mark Bartlett.

SCIP may be retrieved for ACADEMIC purposes only, and
therefore this code may only be retrieved as such unless
the user of this code has a personal/commercial SCIP license.

References
----------
[1] Tobias Achterberg, SCIP: solving constraint integer programs,
Mathematical Programming Computation, v1, n1, pgs 1-41, 2009.

[2] Mark Bartlett and James Cussens. Advances in Bayesian network learning
using integer programming. In Proceedings of the 29th Conference on
Uncertainty in Artificial Intelligence (UAI 2013). AUAI Press, 2013. To
appear.

[3] James Cussens. Bayesian network learning with cutting planes. In Fabio G.
Cozman and Avi Pfeffer, editors, Proceedings of the 27th Conference on
Uncertainty in Artificial Intelligence (UAI 2011), pages 153-160. 
AUAI Press, 2011.

[4] James Cussens, Mark Bartlett, Elinor M. Jones, and Nuala A. Sheehan.
Maximum likelihood pedigree reconstruction using

[5] Milan Studeny. How matroids occur in the context of learning Bayesian 
network structure. Proceedings of the 31st Conference on Uncertainty 
in Artificial Intelligence (UAI-15) July 2015.

[6] James Cussens, David Haws and Milan Studeny. Polyhedral aspects of score 
equivalence in Bayesian network structure learning. Arkiv 1503.00829, March 2015.

[7] Tommi Jaakkola, David Sontag, Amir Globerson, and Marina Meila. Learning
Bayesian network structure using LP relaxations. In Proceedings of the
13th International Conference on Artificial Intelligence and Statistics (AISTATS
2010), volume 9 of Journal of Machine Learning Research: Workshop
and Conference Proceedings, pages 358-365. Society for Artificial Intelligence
and Statistics, 2010.

Acknowledgements from GOBNILP
-----------------------------
- GOBNILP version 1.2-1.6 and higher was supported by MRC Project Grant G1002312.
- Many thanks are due to the SCIP developers for writing and distributing SCIP and 
also helping with queries. Particular thanks are due to: Tobias Achterberg, 
Timo Berthold, Ambros Gleixner, Gerald Gamrath, Stefan Heinz, Michael Winkler 
and Kati Wolter.
- Marc Pfetsch wrote the cons_linearordering.c constraint handler which provided 
- useful 'template' which helped JC write cons_dagcluster.c.
- The most important part of the separation routine in cons_dagcluster.c 
uses the 'cluster constraint' introduced in [6]. Additional thanks to 
Tommi Jaakkola and David Sontag for providing data and encouragement-to- 
distribute, respectively.


"""
__author__ = """Nicholas Cullen <ncullen.th@dartmouth.edu>"""

import os
import subprocess
import time
import sys
import re

import numpy as np
import pandas as pd



class GOBN(object):
	"""
	This class is a wrapper for almost anything you would want to
	do in order to install, make, and run GOBNILP - except that
	you can do it unified Python commands instead of from the tedious
	and confusing command line.

	Command-Line GOBNILP Overview
	-----------------------------

	Command Line Arugments:

		GOBNILP current recognizes five command line arguments:
			
			1. "-g = filename"

				Sets the file from which the settings are read. For example,
				if a settings file is created, you would enter the following:
					bin/globnilp -g=mysettings.txt data/asia_100.data

			2. "-f = format"

				Sets the input file format - note that you must use "-f=dat" flag
				if data file ends in something other than .dat, otherwise it will
				think its a local scores file. Any common delimiter can be used by
				simply specifying as such in the settings file.

			3. "-x"

				Create the model and exit before solving it.

			4. "-q = filename"

				Sets the frequency file for pedigree learning.

			5. "-v = level"

				The verbosity level of the output.
				Verbosity can be set to any value between 0 and 5, where
				levels 0 and 1 just display error and warning messages. Level 2
				gives additional info about system run and output. Level 3 is the
				default and gives information about the progress of the search.
				Level 4 gives a more detailed progress of the search, and Level 5
				displays statistics about the search once the BN has been found.

	Global Behavior Settings:

		A 'settings' file is used to change the global behavior of GOBNILP. Lines
		beginning with a # are treated as comments and blank lines are permitted. 

		The settings take the form of paramter = value, e.g:
			gobnilp.outputfile/solution = "output.txt"




	Python GOBNILP Overview
	-----------------------
	This codebase includes (or plans to include) the following main functionality:

		- Downloading and Extracting the GOBNILP and SCIP source code tar files.
		- Making the GOBNILP and SCIP source code and linking them.
		- Altering and Setting global parameter settings for GOBNILP.
		- Calling GOBNILP to learn BN structure from discrete data.
		- Printing/returning/writing various output formats.

	Additionally, this code includes the following utility functionality:

		- converting various file formats to GOBNILP's '.dat' format.
		- linking GOBNILP/SCIP to existing source code or directories.


	"""


	def __init__(self,
			GOBN_DIR='gobn/gobnilp1.6.1', 
			SCIP_DIR='scip/scipoptsuite-3.1.1',
			GOBN_VERSION='1.6.1',
			SCIP_VERSION='3.1.1',
			SETTINGS_FILE='mysettings.txt', 
			CONSTRAINTS_FILE='dag.constraints',
			VERBOSE=False):
		"""
		NOTE: 
			By not passing any values to the above directory arguments,
			this is basically assuming that this "pyGOBN.py" file is
			being run from a main directory, and both the GOBNILP and SCIP
			main directories are located ONE directory below this file. Also,
			note that by not passing any directory values, it is assumed that
			the user holds ONLY the tar.gz files, which must be Unpackedred and
			then we must try to make them.

			If values are passed to the above directory arguments, it can
			be any valid absolute or relative path, but it is assumed that
			the user has already downloaded/installed/run make on the
			GOBNILP and/or SCIP source code.


		"""
		self.GOBN = {
				'DIR': GOBN_DIR, # main GOBNILP directory
				'TAR_FILE' : 'gobnilp/gobnilp1.6.1.tar.gz',
				'UNPACKED' : False,
				'MADE' : False}

		self.SCIP = {
				'DIR' : SCIP_DIR, # main SCIPOPTSUITE directory
				'SCIP_DIR' : 'scip/scipoptsuite-3.1.1/scip-3.1.1', # main SCIP dir
				'TAR_FILE' : 'scip/scipoptsuite-3.1.1.tgz',
				'UNPACKED' : False,
				'MADE' : False}

		self.SETTINGS_FILE = SETTINGS_FILE
		self.CONSTRAINTS_FILE = CONSTRAINTS_FILE
		self.VERBOSE = VERBOSE
		self.DATA_DIR = os.path.join(self.GOBN['DIR'], 'data')

	###############################
	##### SETTING UP GOBNILP ######
	###############################

	### MAIN EXECUTION COMMAND ###

	def execute(self, command, _str=None, verbose=None, cwd=None):
		"""
		Main function to execute a command from the command line.

		Arguments
		---------
		*command* : a python list,
			The commands to run on the command line, separated in a list.

		*_str* : a python string
			What to print to the console before running this command, unless
			self.VERBOSE=True, in which case the actual command line stdout will
			be printed to the command line.

		*verbose* : None or Boolean
			Whether to print the actual command line stdout to the console.

		*cwd* : None or a string (file path)
			Whether to change the working directory before running the command. This
			is only used for linking SCIP to GOBNILP right now because that must be done
			from inside the GOBNILP directory instead of the main pyGOBN directory.
		"""
		if verbose is None:
			verbose = self.VERBOSE

		command = ' '.join(command)
		process = subprocess.Popen(command, 
			shell=True, 
			stdout=subprocess.PIPE, 
			stderr=subprocess.STDOUT,
			cwd=cwd)

		if verbose:
			# Print command line output to console while it's happening
			while True:
				line = process.stdout.readline()
				if nextline == '' and process.poll() != None:
					break
				sys.stdout.write(line)
				sys.stdout.flush()
		else:
			# only print what is passed in as _str.
			if _str is not None:
				sys.stdout.write(_str)
				sys.stdout.flush()

		output = process.communicate()[0]
		returncode = process.returncode

		if returncode == 0:
			return True, output
		else:
			return False, output

	### UNPACK TAR FILES ###

	def unpack(self):
		"""
		Unpack SCIP and GOBNILP from one command.
		See the docs of the associated functions.

		This has been validated on my machine.
		"""
		self.unpack_GOBN()
		self.unpack_SCIP()

	def unpack_GOBN(self,_str=None):
		"""
		Unpack the GOBNILP tar file, which should exist at SELF.GOBN['TAR_FILE']

		Because GOBNILP unpacks into the existing directory,
		a new directory will be created into which GOBNILP can
		be unpacked.

		This has been validated on my machine.
		"""
		dir_proc = subprocess.call(['mkdir', self.GOBN['DIR']])
		unpack_command = ['tar', '-xzvf', self.GOBN['TAR_FILE'], '-C', self.GOBN['DIR']]
		successful, output = self.execute(unpack_command,_str=_str)
		if not successful:
			print 'Unpack SCIP Failed for the following reason:'
			print output
			self.GOBN['UNPACKED'] = False
		else:
			if self.VERBOSE:
				print 'Unpack GOBN successful'
			self.GOBN['UNPACKED'] = True


	def unpack_SCIP(self, _str=None):
		"""
		Unpack the SCIP tar file. 

		This differs a little from unpacking GOBNILP, because
		this tar file unpacks into its own directory - whereas
		GOBNILP unpacks into the existing directory and thus a
		directory must be MADE for it. That is not the case here.

		This has been validated on my machine.
		"""
		unpack_command = ['tar', '-xzvf', self.SCIP['TAR_FILE'], '-C', 'scip']
		successful, output = self.execute(unpack_command,_str=_str)
		if not successful:
			print 'Unpack SCIP Failed for the following reason:'
			print output
			self.SCIP['UNPACKED'] = False
		else:
			if self.VERBOSE:
				print 'Unpack SCIP successful'
			self.SCIP['UNPACKED'] = True
		
	### MAKE SOURCE CODE ###

	def make(self, CPLEX=False, verbose=None):
		self.make_SCIP(verbose=verbose)
		self.make_GOBNILP(CPLEX, verbose=verbose)
		

	def make_SCIP(self, test=False, verbose=None, from_gobn=False):
		"""
		Steps:
			1. Unpack SCIP if necessary
			2. make
		"""
		if verbose is None:
			verbose = self.VERBOSE

		### CHECK THAT SCIP HAS BEEN UNPACKED ###
		if not self.SCIP['UNPACKED']:
			_str = 'SCIP needs to be unpacked.. Trying that now. \n'
			self.unpack_SCIP(_str)
		
		### If still not unpacked, it failed - so exit. ###
		if not self.SCIP['UNPACKED']:
			return None

		if from_gobn:
			_str = 'SCIP must be MADE before GOBNILP.. May take a few minutes.\n'
		else:
			_str = 'Making SCIP.. This may take a few minutes.\n'
		
		### EXECUTE MAKE COMMAND ###
		make_command = ['make', '-C', self.SCIP['DIR']]
		successful, output = self.execute(make_command, _str=_str, verbose=verbose)
		
		if not successful:
			print 'Make SCIP Failed for the following reason:'
			print output
			self.SCIP['UNPACKED'] = False
		else:
			if verbose:
				print 'Make SCIP successful'
			self.SCIP['UNPACKED'] = True


		self.SCIP['MADE'] = True

		if test:
			test_out = subprocess.check_output(['make', 'test', '-C', self.SCIP['DIR']])
	
	def make_GOBNILP(self, CPLEX=False, verbose=None):
		"""
		Make the GOBNILP source code.

		IMPORTANT: You must make SCIP before GOBNILP.
		Steps:
			1. Unpack GOBN if necessary
			2. ./configure.sh SCIP_DIR
			3. make (LPS=cpx if possible)
		"""
		if verbose is None:
			verbose = self.VERBOSE

		### CHECK THAT SCIP HAS BEEN MADE ###
		if not self.SCIP['MADE']:
			self.make_SCIP(verbose=verbose, from_gobn=True)
		# if still not made, it failed - so exit
		if not self.SCIP['MADE']:
			return None
		
		### CHECK THAT GOBNILP HAS BEEN UNPACKED ###
		if not self.GOBN['UNPACKED']:
			_str = 'GOBNILP needs to be unpacked .. Trying that now.\n'
			self.unpack_GOBN(_str)
			

		### LINK SCIP TO GOBNILP ###

		_str = 'Linking SCIP to GOBNILP..\n'
		scip_dir = os.path.join('../../', self.SCIP['SCIP_DIR'])
		config_command = ['./configure.sh', scip_dir]
		successful, output = self.execute(config_command, _str=_str, cwd=self.GOBN['DIR'])
		if 'SUCCEEDED' in output:
			print 'SCIP Linking was successful.'
			subprocess.call(['cd' , '../../']) # change back to main dir
		elif 'exists' in output:
			print 'SCIP already Linked to GOBNILP.. Moving on.'
			subprocess.call(['cd' , '../../']) # change back to main dir
		else:
			print 'SCIP Linking was unsuccessful for the following reason: \n'
			print output
			print '\n EXITING WITHOUT MAKING GOBNILP.\n'
			subprocess.call(['cd' , '../../']) # change back to main dir
			return None

		### MAKE GOBNILP ###

		
		if CPLEX:
			make_command = ['make', 'LPS=cpx', '-C', self.GOBN['DIR']]
		else:
			make_command = ['make', '-C', self.GOBN['DIR']]
		_str = 'Making GOBNILP..\n'
		successful, output = self.execute(make_command,_str=_str, verbose=verbose)
		
		if successful:
			print 'GOBNILP Make was Successful. You can now use pyGOBN freely.'
			self.GOBN['MADE'] = True
			 = True
		else:
			print 'GOBNILP Make was UNSUCCESSFUL for the following reason: \n'
			print output
			print 'EXITING WITHOUT MAKING GOBNILP.'


	def clean(self):
		"""
		Remove/Delete the main SCIP and GOBNILP directories.
		"""
		gobn_proc = subprocess.call(['rm', '-r', self.GOBN['DIR']])
		scip_proc = subprocess.call(['rm', '-r', self.SCIP['DIR']])


	################################
	####### RUNNING GOBNILP ########
	################################


	### GOBNILP SETTINGS ###

	def set_settings(self, settings):
		"""
		Create the "gobnilp.set" file that will be passed in
		as an argument on the command-line run of GOBNILP using
		the "-g=mysettings.txt" flag.

		For now, I think it's best to allow the user to just pass
		in the normal paramter name, and add on the GOBNILP
		settings preceeding path - i.e. the user can pass in
		'delimeter = "whitespace"' instead of 
		'gobnilp/delimeter = "whitespace"'.

		Arguments
		---------
		*settings* : a dictionary, where
			key = setting and value = setting value.

		SETTINGS 
		OPTIONS
		--------
		(gobnilp/) 
			*dagconstraintsfile* : a string - file name
				the file where any dag constraints on edges/independencies
				are stored.
			*delimiter* : delimiter for passed-in data file
			*mergedelimiters* : whether to merge delimiters
			*minfounders* : min number of prior variables
			*edge_penality* : positive value will bias the solver
				toward sparser graphs.
			*nbns* : an integer,
				how many BNs to learn - e.g. if nbns = 10, the solver
				will return the 10 unqiue BNs with the highest score.


		(gobnilp/outputfile/) 
			*solution* : a string - file name
				the file to which stdout will be written
			*adjacencymatrix* : a string (ending in '.mat') - file name
				the file to which the adjacency matrix result will
				be written.
			*dot* : a string (ending in '.dot') - file name
				whether/where the result will be output as a dot file
				to be used with graphviz.
			*scoreandtime* : a string - file name
				whether to only output the score and the time it took
				to get that score - useful when comparing GOBNILP to
				other structure learning methods.
			*mec* : a string - file name
				whether to print out the markov equivalence class of the
				learned BN.
			*pedigree* : a string - file name
				whether to output the learned BN as a pedigree - only useful
				when using GOBNILP for finding perdigrees.

		(gobnilp/scoring/) 
			*alpha* : equivalent sample size
			*arities* : boolean, variable cardinalities
			*names* : boolean, whether variable names are given
			*palim* : max number of parents for each node
			*prune* : whether to prune during scoring
			*fast* : whether to use fast gamma function,
				which may be numerically instable for high equivalent samples

		(heuristics/sinks/) 
			*probing* : set to True if solver is failing to
					find any solution at all.
			*maxdivedepth* : increase this value if solver
					is failing to find any solution at all.

		(limits/) 
			*time* : max time limit for search
			*gap* : min optimality gap until termination


		"""
		# Read mysettings.txt into one big string
		with open(self.SETTINGS_FILE, 'r') as f:
			txt = f.read()

		# For all of the passed-in settings, replace the
		# existing values in mysettings.txt
		for s_name, s_val in settings.items():
			start_idx = txt.find(s_name)
			if start_idx == -1:
				print '%s is not a valid setting.. Moving on.' % s_name
			else:
				temp_sv = txt[start_idx:].rsplit('\n')[0]
				val_start = start_idx + temp_sv.index('=') + 1
				val_end = start_idx + len(temp_sv)
				if '"'  in txt[val_start:val_end]:
					txt = txt[:val_start+1] + '"' + str(s_val) + '"' + txt[val_end:]
				else:
					txt = txt[:val_start+1] + str(s_val) + txt[val_end:]

		# Write the altered text back to mysettings.txt
		with open(self.SETTINGS_FILE, 'w') as f:
			f.write(txt)

	### EDGE AND INDEPENDENCE CONSTRAINTS

	def set_constraints(self, edge_reqs={}, ind_reqs={}, nonedge_reqs={}, append=False):
		"""
		Set constraints/requirements on certain edges,
		parent-child relationships, or conditional independencies
		in the learned network.

		Since there are three types of constraints -- those for on/off edges and
		those on conditional independence relationships -- there are
		two arguments to pass into this function: *edges*, *independencies*,
		and *nonedges*.
		The format of these arguments is explained below.

		Arguments
		---------
		*edges* : a dictionary,
			where key = main rv and value = list of rvs which are REQUIRED
			to be the main rv's children.
			Examples:
				edges = {'C':['A','B']} means that there MUST be edges from
					C -> A and from C -> B in the learned network.

		*independencies* : a list of 2-tuples or 3-tuples,
			where each tuple element can be another tuple representing a 
			set of random variables.
			Examples:
				- (('A','B'), 'C') means that A,B _|_ C.
				- ('A',('B','C'),'D') means that A _|_ B,C | D
				- ('A','B','C') means that A _|_ B | C
				- ('B', 'C') means that B _|_ C

		*nonedges* : a dictionary,
			the same format as *edges*, except the interpretation is that
			the rv is NOT a parent of any of the rvs in the list.
			Examples:
				nonedges = {'C',['A','B']} means that there must NOT be edges
				from C -> A or from C -> B in the learned network.

		*append* : a boolean
			Whether to append these constraints to the existing constraint file,
			or overwrite the existing constraint file. The default is to overwrite
			the existing constraint file.

		"""
		if append:
			f = open(self.CONSTRAINTS_FILE,	'a')
		else:
			f = open(self.CONSTRAINTS_FILE, 'w')
			
		# EDGE CONSTRAINTS
		for rv, children in edges.items():
			for child in children:
				e_cons = '%s<-%s' % (child, rv)
				f.write(e_cons)

		# INDEPENDENCIES CONSTRAINTS
		for i in independencies:
			if len(i) == 2:
				lhs = ','.join(i[0])
				rhs = ','.join(i[1])
				i_cons = '%s_|_%s' % (lhs, rhs)
			elif len(i) == 3:
				lhs = ','.join(i[0])
				rhs = ','.join(i[1])
				cond = ','.join(i[2])
				i_cons = '%s_|_%s|%s' % (lhs, rhs, cond)
			f.write(i_cons)

		# NON-EDGE CONSTRAINTS
		for rv, children in nonedges.items():
			for child in children:
				e_cons = '~%s<-%s' % (child, rv)
				f.write(e_cons)

		f.close()

	def write_data(self, data, names=None):
		"""
		Write data to file in order to be read by GOBNILP solver, and
		return the path to which the passed-in data file was written.

		This function should support numpy ndarray and pandas dataframe.
		"""
		settings = {'delimiter': ','}
		data_path = os.path.join(self.DATA_DIR, 'userdata.dat')

		if isinstance(data, np.ndarray):
			if names is not None:
				np.savetxt(data_path, data, sep=',', header=names)
				settings['names'] = 'TRUE'
			else:
				np.savetxt(data_path, data)
		elif isinstance(data, pd.dataframe):
			data.to_csv(data_path, sep=',')
			settings['names'] = 'TRUE'

		self.set_settings(settings)

		return data_path
		

	### RUN METHODS ###

	def learn(self, 
			data, 
			names=None,
			settings=None,
			edge_reqs=None, 
			ind_reqs=None, 
			nonedge_reqs=None, 
			append=False):
		"""
		Main function to run GOBNILP.

		Score Metric
		------------
		By default, GOBNILP searches for the BN with the highest
		BDeu score (log marginal likelihood) subject to no node
		having more than 3 parents. The default effective sample
		size is equal to 1.

		Settings
		--------
		GOBNILP has the ability to set and alter many global settings,
		along with constraints on the structure search - i.e. stipulating
		that a given variable MUST be the parent of another variable, etc.
		This is done by changing the settings file, which we store in the
		"mysettings.txt" file. This settings file is then included in
		the command line run by passing it in with "-g=gobnilp.set". See
		the "set_settings" function for more information.

		Output
		------
		By default, GOBNILP prints out the learned BN structure
		with one line for each node specifying its parents and
		the local score for that choice of parents.
		"""
		if settings is not None:
			self.set_settings(settings)
		if edge_reqs is not None or ind_reqs is not None or nonedge_reqs is not None:
			self.set_constraints(edge_reqs, ind_reqs, nonedge_reqs)

		if isinstance(data, str):
			DATA_PATH = data
		else:
			DATA_PATH = self.write_data(data, names)

		bin_path = os.path.join(self.GOBN['DIR'], 'bin/gobnilp')
		learn_cmd = [bin_path, '-g=', self.SETTINGS_FILE, '-f=dat', DATA_PATH]
		_str = 'Running GOBNILP Solver.. This may take a few minutes.'
		successful, output = self.execute(learn_cmd, _str=_str)

		if successful:
			print 'Solver run was SUCCESSFUL'
		else:
			print 'Solver run was UNSUCCESSFUL for the following reason: \n'
			print output





































