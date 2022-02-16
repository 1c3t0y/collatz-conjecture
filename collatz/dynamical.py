from optparse import Values
from tkinter import HORIZONTAL
from collatz import functions, plot
from itertools import groupby
from operator import itemgetter

def orbit(x0, function, iterations, *args, **kwargs):
	"""This function computes the orbit of a initial value x_0 over a 
	map f(x) and returns it as a list.

	Args:
		x0: Initial value.
		
		iterations: (int) Number of iterations to apply over x0.
		
		function: (function) Function on which the discrete dynamical 
		system is defined.
	Returns:
		list: list with the orbit of x0 over f(x)
	"""

	orbit_list = [] 
	orbit_list.append(x0) #adding the initial value to the orbit (iteration 0)
	
	#iterating over the function.
	x = x0
	for i in range(iterations):
		# Calculates and adds the next element of the orbit.
		x = function(x, *args, **kwargs)
		orbit_list.append(x)

	return orbit_list


def is_periodic(orbit_list, function, *args, **kwargs):
	return orbit_list[0] == function(orbit_list[-1], *args, **kwargs)


def periodic_orbit(x0, function, stop_iterations = 100, *args, **kwargs):
	"""This function computes the periodic orbit of a initial value $x_0$ 
	over a map $f(x)$ and returns two elements: a *list* with the orbit 
	and an integer that represents the *period*. If stop_iterations is 
	reached whithout finding a periodic orbit, it returns a period of -1. 
	If the initial value $x_0$ converges to a periodic orbit, the function 
	returns the periodic orbit and its period.


	Args:
		x0: Initial value

		function (function): Function on which the discrete dynamical system 
		is defined.
		
		stop_iterations (int, optional): Max number of iterations before stop.
		Defaults to 100.

	Returns:
		(list, int): Orbit and period of x0 over f(x). if stop_iterations is 
		reached, period i set to -1.
	"""
	orbit_list = []
	orbit_list.append(x0)

	x = x0
	for i in range(stop_iterations):
		x = function(x, *args, **kwargs)
		
		if x in orbit_list:
			index = orbit_list.index(x)
			orbit_list = orbit_list[index:]
			period = len(orbit_list)
			return orbit_list, period
		
		orbit_list.append(x)

	period = -1

	return orbit_list, period


def search_periodic_orbits(values, function, stop_iterations = 100, *args, **kwargs):
	periodic_orbits = dict()
	for value in values:
		orbit_list, period = periodic_orbit(value, function, stop_iterations = 100, *args, **kwargs)
		
		if period != -1:
			orbit_tuple = tuple(orbit_list)

			try:
				periodic_orbits[value].add(orbit_tuple)
			except:
				periodic_orbits[value] = {orbit_tuple}

	return periodic_orbits


def is_fixed(x, function, *args, **kwargs):
	return x == function(x, *args, **kwargs)


def fixed_point(x0, function, stop_iterations = 100, *args, **kwargs):
	x = x0
	for i in range(stop_iterations):
		if is_fixed(x, stop_iterations = 100, *args, **kwargs):
			return x, i
		x = function(x, *args, **kwargs)
	return x, None


def same_orbit_length(values, function, stop_iterations, *args, **kwargs):	 
	len_dict = {}
	for x in values:
		orbit, period = periodic_orbit(x)

		if period == -1:
			continue

		try:
			len_dict[period].append(x)
		except:
			len_dict[period] = [x]
	
	return len_dict


def consecutive_orbits_length(values, function, stop_iterations, *args, **kwargs):
	same_len = same_orbit_length(values, function, stop_iterations, *args, **kwargs)
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


class DDS:
	"""
		Class for analyze Discrete dynamical systems
	"""

	def __init__(self, values, function, iterations, stop_iterations, start = None,*args, **kwargs) -> None:
		self.values = values
		self.function = function
		self.iterations = iterations
		self.stop_iterations = stop_iterations
		self.args = args
		self.kwargs = kwargs

		self.orbits = None

		if start == 'orbit':
			self.orbits = self.orbit()
		elif start == 'periodic':
			self.orbits = self.periodic_orbit()


	def f(self, inplace = False):
		f_of_values = [self.function(value, *self.args, **self.kwargs) for value in self.values]
		return f_of_values


	def orbit(self, values = None, inplace = False):
		if values is None:
			values = self.values

		orbits_values = [orbit(value, self.function, self.iterations, *self.args, **self.kwargs) for value in values]

		if inplace:
			self.values = values
			self.orbits = orbits_values
			return None

		return orbits_values
		
	
	def is_periodic(self, orbits_list = None):
		if orbits_list is None and self.orbits is None:
			orbits_list = self.orbit()
		elif orbits_list is None:
			orbits_list = self.orbits

		is_periodic_list = [is_periodic(orbits_value, self.function, *self.args, **self.kwargs) for orbits_value in orbits_list]
		
		return is_periodic_list


	def periodic_orbit(self, values = None, inplace = False):
		if values is None:
			values = self.values

		orbits_values = [periodic_orbit(value, self.function, self.iterations, *self.args, **self.kwargs) for value in values]

		if inplace:
			self.values = values
			self.orbits = orbits_values
			return None

		return orbits_values


	def search_periodic_orbits(self, inplace = False):
		periodic_orbits = search_periodic_orbits(self.values, self.function, self.stop_iterations, *self.args, **self.kwargs)
		if inplace:
			self.orbits = [orbit[0] for orbit in periodic_orbits]
		else:
			return periodic_orbits


	def is_fixed(self):
		return [is_fixed(x, self.function, *self.args, **self.kwargs) for x in self.values]


	def fixed_point(self, stop_iterations = None):
		if stop_iterations is None:
			stop_iterations = self.stop_iterations
		return [fixed_point(x0, self.function, stop_iterations, *self.args, **self.kwargs) for x0 in self.values]


	def plot_f(self, display_mode = 'show', savefig_name = '', title = None, range = (-10,10), num = 100, figsize=(10,8)):
		
		plot.plot_function(self.function, display_mode, savefig_name = savefig_name, title = title, 
							range = range, num = num, figsize=figsize, *self.args, **self.kwargs)


	def plot_orbits(self, function_name = 'f', display_mode = 'show', label_data = False, savefig_name = '', legend = True, markers = None, title ='', figsize = (8,6)):
		
		orbits_label = ["Orbit of " + "{:.2f}".format(value) for value in self.values]
		plot.plot_orbits(self.orbits, orbits_label, 
					function_name = function_name, display_mode = display_mode, 
					label_data = label_data, savefig_name = savefig_name, legend = legend, 
					markers = markers, title = title, figsize = figsize)


	def plot_vertical_orbits(self, display_mode = 'show', savefig_name = '', title ='', figsize = (8,6)):

		plot.plot_vertical_orbits(self.values, self.orbits, display_mode = display_mode, 
				savefig_name = savefig_name, title = title, figsize = figsize)