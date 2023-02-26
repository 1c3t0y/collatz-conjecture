from collatz import functions, plot
from itertools import groupby
from operator import itemgetter
from math import log


def orbit(n, f, *args, **kwargs):
	"""Function to calculate the orbit an period of a given value under a given function.
	f must reach 1 after some iterations, it will go into an infinite loop otherwise.

	Args:
		n (positive integer): Value to calculate orbit
		f (function): function to iterate orbit
		*args and *kwars: parameters of the function

	Returns:
		list: list with the orbit of n under f
	"""
	orbit_list = []
	orbit_list.append(n)

	n0 = n
	while(n0 != 1):
		n0 = f(n0, *args, **kwargs)
		orbit_list.append(n0)

	return orbit_list


def orbit_and_period(n, f, *args, **kwargs):
	"""Function to calculate the orbit an period of a given value under a given function.
	f must reach 1 after some iterations, it will go into an infinite loop otherwise.
	Args:
		n (positive integer): Value to calculate orbit.
		f (function): function to iterate orbit.
		*args and *kwars: parameters of the function.
		
	Returns:
		tuple: integer with the period of orbit and list with the orbit of n under f
	"""
	orbita = []
	orbita.append(n)

	n0 = n
	i = 0
	while(n0 != 1):
		n0 = f(n0, *args, **kwargs)
		orbita.append(n0)
		i += 1

	return i, orbita

def period(n, f, *args, **kwargs):
	"""Function to calculate the period of a given value under a given function.
	f must reach 1 after some iterations, it will go into an infinite loop otherwise.

	Args:
		n (positive integer): Value to calculate orbit.
		f (function): function to iterate orbit.
		*args and *kwars: parameters of the function.

	Returns:
		integer: integer with the period of orbit
	"""
	orbita = []
	orbita.append(n)

	n0 = n
	i = 0
	while(n0 != 1):
		n0 = f(n0, *args, **kwargs)
		orbita.append(n0)
		i += 1

	return i


def stopping_time_ratio(n, period):
	""" function to calculate the stopping time ratio of a goven value under f.

	Args:
		n (positive integer): Value to calculate stopping time ratio.
		period (integer): period of the orbit of n under a function f.

	Returns:
		float: float number with the stopping time ratio
	"""
	return (1.0*period) / log(n)


def parity_sequence(trajectory):
	"""Function to calculate the parity sequence of a trajetctory.
	x mod 2 is calculated for each element of the trajectory. Last value is always set to 0.

	Args:
		trajectory (list): List with the orbit of a value n under f.

	Returns:
		list: List with parity sequence of trajectory.
	"""
	sequence = [i % 2 for i in trajectory]
	sequence[-1] = 0
	return sequence


def ones_ratio(n, f, *args, **kwargs):
	"""Gets the ratio of parity sequence of a given value n under function f

	Args:
		n (integer): Value to calculate the ones ratio.
		f (function): F to calculate orbit under n.
		*args and *kwars: parameters of the function.

	Returns:
		float: ones ratio
	"""
	trajectory = orbit(n, f, *args, **kwargs)
	sequence = parity_sequence(trajectory)
	return sum(sequence) / len(sequence)


def stopping_time(n, f, *args, **kwargs):
	"""function to calculate the stopping time of a value n under f, i.e., 
	the number of iterations k such that f^k(n) < n. 

	Args:
		n (integer): Value to calculate the ones ratio.
		f (function): F to calculate orbit under n.
		*args and *kwars: parameters of the function.

	Returns:
		integer: number k such that f^k(n) < n
	"""
	n0 = f(n, *args, **kwargs)
	i = 1
	while(n < n0):
		n0 = f(n0, *args, **kwargs)
		i += 1
	return i


def same_orbit_period(initial_list):
	"""function to group numbers with the same orbit lenght (period)

	Args:
		initial_list (list): list with the numbers to calculate its period

	Returns:
		dict: dictionary with numbers grouped by period, e.g., same_orbit_length[10] has all
		numbers from initial list with period equal to 10.
	"""
	len_dict = {}
	for i in initial_list:
		len = period(i)
		
		if len in len_dict.keys():
			len_dict[len].append(i)
		else:
			len_dict[len] = [i]
	
	return len_dict


def consecutive_orbits_length(initial_values):
	"""function to group consecutive numbers with the same orbit lenght.

	Args:
		initial_values (list): List with the numbers to group by orbit lenght (period)

	Returns:
		dict: dict with consecutive numbers grouped by period, e.g., consecutive_orbits_lenght[10] has all
		consecutive numbers from initial list with period equal to 10.
	"""
	same_len = same_orbit_period(initial_values) # Groups initial list by period
	
	consecutive_same_len = {}
	for values in same_len.values():
		data = list(values)
		for _, g in groupby(enumerate(data), lambda ix : ix[0] - ix[1]):
			consecutive = list(map(itemgetter(1), g))
			n = len(consecutive)

			if n in consecutive_same_len.keys():
				consecutive_same_len[n].append(consecutive)
			else:
				consecutive_same_len[n] = [consecutive]

	return consecutive_same_len


class CollatzProblem:
	"""
	Class to explore the Collatz conjecture, a.k.a 3x + 1 problem.
	"""
	def __init__(self, initial_values, start = 'orbit', f = functions.collatz_function, *args, **kwargs) -> None:
		"""init method of CollatzProblem calss

		Args:
			initial_values (list): list with the values to explore
			start (str, optional): operation to start with, options are:
									- 'orbit': calculates only the orbits of initial values.
									- 'periods': calculates only the periods of initial values.
									- 'orbits_and_periods: calculates orbits and periods of initial values.
									Defaults to 'orbit'.
			f (function, optional): function to iterate over. Defaults to collatz_function.
			*args and *kwars: parameters of the function.
		"""
		self.values = initial_values
		self.orbits = None
		self.periods = None
		self.stopping_times = None
		self.stopping_time_ratios = None
		self.function = f
		self.args = args
		self.kwargs = kwargs

		if start == 'orbit':
			self.orbits = self.orbit()
		elif start == 'orbits_and_periods':
			self.periods, self.orbits  = self.orbits_and_periods()
		elif start == 'periods':
			self.periods = self.period()

		if start == 'periods' or start == 'orbits_and_periods':
			self.stopping_times = self.stopping_time()
			self.stopping_time_ratios = self.stopping_time_ratio()
		pass


	def f(self):
		"""Method to evaluate all self.values over self.function

		Returns:
			list: list of f(x) over each x in self.values
		"""
		f_of_values = [self.function(value, *self.args, **self.kwargs) for value in self.values]
		return f_of_values


	def orbit(self):
		"""Method to calculate the orbits of self.values

		Returns:
			dict: dictionary with self.values as keys and orbits (list) as dict values
		"""
		orbits_values = {}
		for value in self.values:
			orbits_values[value] = orbit(value, self.function, *self.args, **self.kwargs)
		return orbits_values


	def period(self):
		"""Method to calculate the periods of the orbits of self.values. If self.orbits is not none or empty dict, 
		the calculation is made over the lenght of each orbit. Otherwise is calculated.

		Returns:
			dictionary: dictionary with self.values as keys and periods as values
		"""
		period_values = {}

		if self.orbits == {} or self.orbits is None:
			for value in self.values:
				period_values[value] = period(value, self.function, *self.args, **self.kwargs)
		else:
			for value in self.orbits.keys():
				period_values[value] = len(self.orbits[value])

		return period_values


	def orbits_and_periods(self):
		"""Method to calculate the orbits and periods of self.values

		Returns:
			tuple: tuple of dictionaries, first with self.values as keys and orbits (list) as dict values
			and second with self.values as keys and periods as dict values.
		"""
		orbits_values = {}
		period_values = {}

		for value in self.values:
			period_value, orbit_value = orbit_and_period(value, self.function, *self.args, **self.kwargs)
			orbits_values[value] = orbit_value
			period_values[value] = period_value

		return period_values, orbits_values


	def stopping_time(self):
		"""Method to calculate the stopping times for all values. Self.values must exist

		Returns:
			dict: dictionary with values as key and stopping time as values
		"""
		stopping_times = {}
		for value in self.values:
			stopping_times[value] = stopping_time(value, self.function, *self.args, *self.kwargs)
		return stopping_times


	def stopping_time_ratio(self):
		"""Calculates the stopping time ratio for all values. self.values must exist

		Returns:
			dict: dictionary with values as key and stopping time ratio as values
		"""

		if not self.periods:
			self.periods = self.period()
		
		stopping_times_ratio = {}
		for value in self.values:
			stopping_times_ratio[value] = stopping_time_ratio(value, self.periods[value])
		return stopping_times_ratio
		

	def same_orbit_period(self):
		"""method to group values with the same orbit lenght (period). self.values must exist and not empty.

		Returns:
			dict: dictionary with numbers grouped by period, e.g., same_orbit_length[10] has all
			numbers from initial list with period equal to 10.
		"""
		if not self.periods:
			self.periods = self.period()

		len_dict = {}
		for value in self.values:
			period_orbit = self.periods[value]
			if period_orbit in len_dict.keys():
				len_dict[period_orbit].append(value)
			else:
				len_dict[period_orbit] = [value]
		
		return len_dict

	
	def consecutive_orbits_length(self):
		"""Method to group consecutive numbers with the same orbit lenght. self.values must exists

		Returns:
			dict: dict with consecutive numbers grouped by period, e.g., consecutive_orbits_lenght[10] has all
			consecutive numbers from initial list with period equal to 10.
		"""
		same_len = self.same_orbit_period() # Groups values list by period
		
		consecutive_same_len = {}
		for values in same_len.values():
			data = list(values)
			for _, g in groupby(enumerate(data), lambda ix : ix[0] - ix[1]):
				consecutive = list(map(itemgetter(1), g))
				n = len(consecutive)

				if n in consecutive_same_len.keys():
					consecutive_same_len[n].append(consecutive)
				else:
					consecutive_same_len[n] = [consecutive]

		return consecutive_same_len



	def plot_orbits(self, function_name = 'Collatz', display_mode = 'show', label_data = False, savefig_name = None, 
			legend = True, markers = None, title = None, figsize = (8,6), fontsize = (12,9)):
		"""Method to plot the iterations on x axis and value orbit on y value

		Args:
			function_name (str, optional): Function name to display. Defaults to '$Collatz(x)$'.
			display_mode (str, optional): Way to show the image:
										- 'show' to print the image otherwise stores image on path given
											by savefig_name. Defaults to 'show'.
			label_data (bool, optional): if True, adds a label to each point in the plot. Defaults to False.
			savefig_name (str, optional): path and name to store the image. Defaults to None.
			legend (bool, optional): If True shows the legend for each value. Defaults to True.
			markers (list, optional): List of strings with the type of marker to show. Defaults to 'o' for all values.
			title (str, optional): Title of the plot. Defaults to ''.
			figsize (tuple, optional): size (x,y) of the plot. Defaults to (8,6).
			fontsize (tuple, optional): size of the text in x axis and y axis. Defaults to (12,9).
		"""
		
		orbits_label = ["Orbit of " + "{:.0f}".format(value) for value in self.values]
		orbits_ordered = [self.orbits[value] for value in self.values]
		plot.plot_orbits(orbits_ordered, orbits_label, 
					function_name = function_name, display_mode = display_mode, 
					label_data = label_data, savefig_name = savefig_name, legend = legend, 
					markers = markers, title = title, figsize = figsize, fontsize=fontsize)

	def plot_vertical_orbits(self, display_mode = 'show', savefig_name = None, title ='', figsize = (8,6), fontsize = (12,9)):
		"""Method to plot the values in x axis and a dot for each iteration in y axis

		Args:
			display_mode (str, optional): Way to show the image:
										- 'show' to print the image otherwise stores image on path given
											by savefig_name. Defaults to 'show'.
			savefig_name (str, optional): path and name to store the image. Defaults to None.
			title (str, optional): _description_. Defaults to ''.
			figsize (tuple, optional): size (x,y) of the plot. Defaults to (8,6).
			fontsize (tuple, optional): size of the text in x axis and y axis. Defaults to (12,9).
		"""
		orbits_ordered = [self.orbits[value] for value in self.values]
		plot.plot_vertical_orbits(self.values, orbits_ordered, display_mode = display_mode, 
				savefig_name = savefig_name, title = title, figsize = figsize, fontsize = fontsize)

	def plot_directed_orbit(self, value, prog = 'neato', figsize = (10,8), connectionstyle = 'arc3, rad = 0', display_mode = 'show', savefig_name = '',
						node_size = 500, font_size = 12, node_color = 'white', edgecolors = 'black', width = 2):
		"""Method to plot the directed graph of an orbit from a given value

		Args:
			value (integer): Value to calculate the orbit from, bot self.value and self.orbit[value] must exist.
			prog (str, optional): Type of plot from graphviz_layout function. Defaults to 'neato'.
			figsize (tuple, optional): size (x,y) of the plot. Defaults to (10,8).
			connectionstyle (str, optional): type of connection between nodes. Defaults to 'arc3, rad = 0'.
			display_mode (str, optional): Way to show the image:
										- 'show' to print the image otherwise stores image on path given
											by savefig_name. Defaults to 'show'.
			savefig_name (str, optional): path and name to store the image. Defaults to ''.
			node_size (int, optional): Size of the node. Defaults to 500.
			font_size (int, optional): Size of label inside node. Defaults to 12.
			node_color (str, optional): color of the node. Defaults to 'white'.
			edgecolors (str, optional): color of the edge. Defaults to 'black'.
			width (int, optional): width of the connectors. Defaults to 2.
		"""

		plot.plot_directed_orbit(self.orbits[value], prog = prog, figsize = figsize, connectionstyle = connectionstyle, display_mode = display_mode, savefig_name = savefig_name,
						node_size = node_size, font_size = font_size, node_color = node_color, edgecolors = edgecolors, width = width)

	def plot_directed_orbits(self, prog  = 'dot', figsize = (10,8), connectionstyle = 'arc3, rad = 0', display_mode = 'show', savefig_name = '',
						node_size = 500, font_size = 12, node_color = 'white', edgecolors = 'black', width = 2):
		"""Method to plot a set of directed orbits, if the orbit converges into another orbit, the same path of convergence is used.

		Args:
			prog (str, optional): Type of plot from graphviz_layout function. Defaults to 'dot'.
			figsize (tuple, optional): size (x,y) of the plot. Defaults to (10,8).
			connectionstyle (str, optional): type of connection between nodes. Defaults to 'arc3, rad = 0'.
			display_mode (str, optional): Way to show the image:
										- 'show' to print the image otherwise stores image on path given
											by savefig_name. Defaults to 'show'.
			savefig_name (str, optional): path and name to store the image. Defaults to ''.
			node_size (int, optional): Size of the node. Defaults to 500.
			font_size (int, optional): Size of label inside node. Defaults to 12.
			node_color (str, optional): color of the node. Defaults to 'white'.
			edgecolors (str, optional): color of the edge. Defaults to 'black'.
			width (int, optional): width of the connectors. Defaults to 2.
		"""

		plot.plot_directed_orbits(list(self.orbits.values()), prog = prog, value_format = "{:.0f}", figsize = figsize, connectionstyle = connectionstyle, display_mode = display_mode, savefig_name = savefig_name,
						node_size = node_size, font_size = font_size, node_color = node_color, edgecolors = edgecolors, width = width)

	def plot_iterations(self, display_mode = 'show', savefig_name = 'image.png',figsize = (10,8), *args, **kwargs):
		"""plots the number of of iterations (y axis) to reach 1 by each value (x axis)

		Args:
			display_mode (str, optional): Way to show the image:
										- 'show' to print the image otherwise stores image on path given
											by savefig_name. Defaults to 'show'.
			savefig_name (str, optional): path and name to store the image. Defaults to None.
			figsize (tuple, optional): size (x,y) of the plot. Defaults to (10,8).
		"""
		if self.periods is None:
			self.periods = self.period()
		ordered_periods = [self.periods[value] for value in self.values]
		plot.plot_iterations(self.values, ordered_periods, display_mode = display_mode, savefig_name = None, 
							figsize=figsize, *args, *kwargs)