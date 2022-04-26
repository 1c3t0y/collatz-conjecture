from ast import arg
from numpy import argsort
from collatz import functions, plot
from itertools import groupby
from operator import itemgetter
from math import log


def orbit(n, f, *args, **kwargs):
	orbit_list = []
	orbit_list.append(n)

	n0 = n
	while(n0 != 1):
		n0 = f(n0, *args, **kwargs)
		orbit_list.append(n0)

	return orbit_list


def orbit_and_period(n, f, *args, **kwargs):
	orbita = []
	orbita.append(n)

	n0 = n
	i = 0
	while(n0 != 1):
		n0 = f(n0, *args, **kwargs)
		orbita.append(n0)
		i += 1

	return i, orbita


def stoping_time_ratio(n, f, *args, **kwargs):
	i, trajectory = orbit_and_period(n, f, *args, **kwargs)
	return (i) / log(n)


def parity_sequence(n, f, *args, **kwargs):
	trajectory = orbit(n, f, *args, **kwargs)
	sequence = [i % 2 for i in trajectory]
	sequence[-1] = 0
	return sequence


def ones_ratio(n, f, *args, **kwargs):
	sequence = parity_sequence(n, f, *args, **kwargs)
	return sum(sequence) / len(sequence)


def same_orbit_length(list_initial):
	len_dict = {}
	for i in list_initial:
		len, orbit_len = orbit_and_period(i)
		
		try:
			len_dict[len].append(i)
		except:
			len_dict[len] = [i]
	
	return len_dict


def consecutive_orbits_length(initial_values):
	same_len = same_orbit_length(initial_values)
	consecutive_same_len = {}

	for key in same_len:
		data = same_len[key]
		for k, g in groupby(enumerate(data), lambda ix : ix[0] - ix[1]):
			consecutive = list(map(itemgetter(1), g))
			n = len(consecutive)

			try:
				consecutive_same_len[n].append(consecutive)

			except:
				consecutive_same_len[n] = [consecutive]

	return (consecutive_same_len)


class CollatzProblem:
	def __init__(self, initial_values, start = 'orbit', f = functions.collatz_function, *args, **kwargs) -> None:
		self.values = initial_values
		self.orbits = None
		self.periods = None
		self.function = f
		self.args = args
		self.kwargs = kwargs

		if start == 'orbit':
			self.orbits = self.orbit()
		elif start == 'periods':
			self.periods, self.orbits  = self.orbits_and_periods()
		pass

	def f(self):
		f_of_values = [self.function(value, *self.args, **self.kwargs) for value in self.values]
		return f_of_values


	def orbit(self, values = None, inplace = False):
		if values is None:
			values = self.values

		orbits_values = [orbit(value, self.function, *self.args, **self.kwargs) for value in values]

		if inplace:
			self.values = values
			self.orbits = orbits_values
			return None

		return orbits_values
	
	def orbits_and_periods(self, values = None, inplace = False):
		if values is None:
			values = self.values

		orbits_values = []
		period_values = []

		for value in values:
			period_value, orbit_value = orbit_and_period(self.function, *self.args, **self.kwargs)
			orbits_values.append(orbit_value)
			period_values.append(period_value)

		if inplace:
			self.values = values
			self.orbits = orbits_values
			self
			return None

		return period_values, orbits_values

	def plot_orbits(self, function_name = '$Collatz(x)$', display_mode = 'show', label_data = False, savefig_name = '', legend = True, markers = None, title ='', figsize = (8,6)):
		
		orbits_label = ["Orbit of " + "{:.0f}".format(value) for value in self.values]
		plot.plot_orbits(self.orbits, orbits_label, 
					function_name = function_name, display_mode = display_mode, 
					label_data = label_data, savefig_name = savefig_name, legend = legend, 
					markers = markers, title = title, figsize = figsize)

	def plot_vertical_orbits(self, display_mode = 'show', savefig_name = '', title ='', figsize = (8,6)):

		plot.plot_vertical_orbits(self.values, self.orbits, display_mode = display_mode, 
				savefig_name = savefig_name, title = title, figsize = figsize)

	def plot_directed_orbit(self, value, prog = 'neato', figsize = (10,8), connectionstyle = 'arc3, rad = 0', display_mode = 'show', savefig_name = '',
						node_size = 500, font_size = 12, node_color = 'white', edgecolors = 'black', width = 2):

		i = self.values.index(value)
		plot.plot_directed_orbit(self.orbits[i], prog = prog, figsize = figsize, connectionstyle = connectionstyle, display_mode = display_mode, savefig_name = savefig_name,
						node_size = node_size, font_size = font_size, node_color = node_color, edgecolors = edgecolors, width = width)

	def plot_directed_orbits(self, prog  = 'dot', figsize = (10,8), connectionstyle = 'arc3, rad = 0', display_mode = 'show', savefig_name = '',
						node_size = 500, font_size = 12, node_color = 'white', edgecolors = 'black', width = 2):

		plot.plot_directed_orbits(self.orbits, prog = prog, value_format = "{:.0f}", figsize = figsize, connectionstyle = connectionstyle, display_mode = display_mode, savefig_name = savefig_name,
						node_size = node_size, font_size = font_size, node_color = node_color, edgecolors = edgecolors, width = width)

	def plot_iterations(self, *args, **kwargs):

		plot.plot_iterations(self.values, self.orbits, *args, **kwargs)

