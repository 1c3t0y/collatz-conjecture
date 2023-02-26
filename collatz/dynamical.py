from collatz import plot
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

		*args and **kwars: parameters of the function.
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
	"""function that checks if a given orbit is periodic

	Args:
		orbit_list (list): orbit with first element as initial value.
		function (function): function that generated the orbit.
		*args and **kwars: parameters of the function.

	Returns:
		bool: True if orbit is periodc, False if not.
	"""
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

		*args and **kwars: parameters of the function.

	Returns:
		(list, int): Orbit and period of x0 over f(x). if stop_iterations is 
		reached, period is set to None.
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
	return orbit_list, None


def search_periodic_orbits(values, function, stop_iterations = 100, *args, **kwargs):
	"""Function that searches for perodic orbits of a list of initial values. Iterates over the initial values 
	and calculates the orbit and it's period, if after the given stop iterations a periodic orbit is not found,
	period is setted to -1. If the period is bigger than 0, then it is added to the final list, skipped otherwise. 

	Args:
		values (list): Initial values to look for periodic orbits.
		
		function (function): Function on which the discrete dynamical system 
		is defined.

		stop_iterations (int, optional): Max number of iterations before stop. Defaults to 100.

		*args and **kwars: parameters of the function.

	Returns:
		dict: dictionary with initial values as key and orbits as value.
	"""
	periodic_orbits = dict()
	for value in values:
		orbit_list, period = periodic_orbit(value, function, stop_iterations, *args, **kwargs)
		
		if period:
			if value in periodic_orbits.keys():
				periodic_orbits[value].add(orbit_list)
			else:
				periodic_orbits[value] = {orbit_list}

	return periodic_orbits


def is_fixed(x, function, *args, **kwargs):
	"""function that checks if a given value is a fixed point

	Args:
		x (int, float, complex): Value to check

		function (function): Function on which the discrete dynamical system 
		is defined.
	
		*args and **kwars: parameters of the function.

	Returns:
		bool: True if x is a fixed point, false otherwise.
	"""
	return x == function(x, *args, **kwargs)


def fixed_point(x0, function, stop_iterations = 100, *args, **kwargs):
	"""Function to look for fixed points

	Args:
		x0 (int, float, complex): value to iterate over
		function (function): Function on which the discrete dynamical system 
		is defined.
		stop_iterations (int, optional): Max of iterations before stop. Defaults to 100.
		*args and **kwars: parameters of the function.

	Returns:
		tuple: if fixed point is found, tuple with value and number of iterations is return, tuple with last f^k(x) and None otherwise
	"""
	x = x0
	for i in range(stop_iterations):
		if is_fixed(x, stop_iterations, *args, **kwargs):
			return x, i
		x = function(x, *args, **kwargs)
	return x, None


def same_orbit_length(values, function, stop_iterations, *args, **kwargs):
	"""Function that groups initial values' periodic orbits by period. If inital value belongs to a periodic orbit,
	it is grouped along with all other values with the same period. If value converges to a periodic orbit, the first value 
	of that orbit will be added to the corresponding period. 

	Args:
		values (list): list of values to iterate over
		function (_type_): function on which the discrete dynamical system 
		is defined.
		stop_iterations (int): max num of iterations before stop.
		*args and **kwars: parameters of the function.

	Returns:
		dict: dictionary with periods as keys and values with periodic orbit as dictionary values
	"""
	len_dict = {}
	for x in values:
		orbit, period = periodic_orbit(x, function, stop_iterations, *args, **kwargs)

		if period and period in len_dict.keys():
			len_dict[period].append(orbit[0])
		elif period:
			len_dict[period] = [orbit[0]]
	
	return len_dict


class DDS:
	"""
		Class to analyze Discrete dynamical systems
	"""

	def __init__(self, values, function, iterations, stop_iterations, start = 'orbit',*args, **kwargs) -> None:
		"""Constructor for DDS class

		Args:
			values (list): List with the initial values of the DDS
			function (function): function on which the DDS is defined
			iterations (int): Initial number of iterations to calculate
			stop_iterations (int): Max number of iterations before stopping.
			start (str, optional): operation to start with, options are:
									- 'orbit': calculates only the orbits of initial values.
									- 'periods': calculates only the periods of initial values (if stop iterations is not reached).
									- 'orbits_and_periods: calculates orbits and periods of initial values. Defaults to 'orbit'.
		"""
		self.values = values
		self.function = function
		self.iterations = iterations
		self.stop_iterations = stop_iterations
		self.args = args
		self.kwargs = kwargs

		self.orbits = None
		self.periods = None

		if start == 'orbit':
			self.orbits = self.orbit()
		elif start == 'orbits_and_periods':
			self.periods, self.orbits  = self.orbits_and_periods()
		elif start == 'periods':
			self.periods = self.period()
		pass


	def f(self):
		"""Method that iterates all initial values over self.function

		Returns:
			list: list with self.function(x) for each x in self.values
		"""
		f_of_values = [self.function(value, *self.args, **self.kwargs) for value in self.values]
		return f_of_values


	def orbit(self):
		"""Method that calculates the orbit of self.values. It stops at self.iterations.

		Returns:
			dict: dictionary with values as key and orbits as values
		"""
		orbits_values = {}
		for value in self.values:
			orbits_values[value] = orbit(value, self.function, self.iterations, *self.args, **self.kwargs)
		return orbits_values
		
	
	def is_periodic(self):
		"""Method that checks wheter if initial values' orbits are periodic or not.

		Returns:
			dict: dictionary with initial values as keys and values with true if initialvalue is periodic, 
			false otherwise.
		"""
		if not self.orbits:
			self.orbits = self.orbit()

		is_periodic_dict = {}
		for value in self.values:
			is_periodic_dict[value] = is_periodic(self.orbits[value], self.function, *self.args, **self.kwargs)
		return is_periodic_dict

	def periodic_orbit(self):
		"""Method to get the orbit and period of initial values.

		Returns:
			dict: dict with initial value as keys and a tuple of periodic orbit and period as values
		"""
		periodic_orbits = {}
		for value in self.values:
			periodic_orbits[value] = periodic_orbit(value, self.function, self.stop_iterations, *self.args, **self.kwargs)
		return periodic_orbit


	def search_periodic_orbits(self):
		"""Method to look for periodic orbits for initial values. If the orbit is not periodic, the value is not added to result.

		Returns:
			dict: dictionary with initial values as key and orbits as value
		"""
		return search_periodic_orbits(self.values, self.function, self.stop_iterations, *self.args, **self.kwargs)


	def is_fixed(self):
		"""function that checks if initial values are fixed or not

		Returns:
			dict: Dictionary with initial value as keys and values with true if initial value is periodic,
			false otherwise.
		"""
		is_fixed_dict = {}
		for value in self.values:
			is_fixed_dict[value] = is_fixed(value, self.function, *self.args, **self.kwargs)


	def search_fixed_points(self):
		"""Method that searches for fixed points.

		Returns:
			dict: dictionary with values as keys and dict values as follows:
				if fixed point is found, tuple with value and number of iterations is return, 
				tuple with last f^k(x) and None otherwise
		"""
		fixed_dict = {}
		for value in self.values:
			fixed_dict[value] = fixed_point(value, self.function, self.stop_iterations, *self.args, **self.kwargs)
		return fixed_dict


	def plot_f(self, display_mode = 'show', savefig_name = '', title = None, range = (-10,10), num = 100, figsize=(10,8)):
		"""Method to plot the function of DDS in a smooth way

		Args:
			display_mode (str, optional): Way to show the image:
										- 'show' to print the image otherwise stores image on path given
											by savefig_name. Defaults to 'show'.
			savefig_name (str, optional): path and name to store the image. Defaults to ''.
			title (str, optional): Title oft the image. Defaults to ''.
			range (tuple, optional): range of the plot. Defaults to (-10,10).
			num (int, optional): Num of dots to be generated between the range. Defaults to 100.
			figsize (tuple, optional): Size x,y of the image. Defaults to (10,8).
		"""
		
		plot.plot_function(self.function, display_mode, savefig_name = savefig_name, title = title, 
							range = range, num = num, figsize=figsize, *self.args, **self.kwargs)
	
	def plot_dots(self, display_mode = 'show', savefig_name = 'image.png', title = None, range = (-10,10), 
				num = 100, figsize=(10,8), xlim = (-10,10), ylim = (-10,10), *args, **kwargs):
		"""Method to plot dots of the function in DDS

		Args:
			display_mode (str, optional): Way to show the image:
										- 'show' to print the image otherwise stores image on path given
											by savefig_name. Defaults to 'show'.
			savefig_name (str, optional): path and name to store the image. Defaults to ''.
			title (str, optional): Title oft the image. Defaults to ''.
			range (tuple, optional): range of the plot. Defaults to (-10,10).
			num (int, optional): Num of dots to be generated between the range. Defaults to 100.
			figsize (tuple, optional): Size x,y of the image. Defaults to (10,8).
			xlim (tuple, optional): limits of the x axis. Defaults to (-10,10).
			ylim (tuple, optional): limits of the y axis. Defaults to (-10,10).
		"""
		
		plot.plot_dots(self.function, display_mode = display_mode, savefig_name = savefig_name, title = title,
			range = range, num = num, figsize = figsize, xlim = xlim, ylim = ylim, *self.args, **self.kwargs)


	def plot_orbits(self, function_name = 'f', display_mode = 'show', label_data = False, savefig_name = None, 
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
			fontsize (tuple, optional): size of the text in x axis and y axis. Defaults to (8,6).
		"""
		
		orbits_label = ["Orbita de " + "{:.2f}".format(value) for value in self.values]
		ordered_orbits = [self.orbits[value] for value in self.values]
		plot.plot_orbits(ordered_orbits, orbits_label, 
					function_name = function_name, display_mode = display_mode, 
					label_data = label_data, savefig_name = savefig_name, legend = legend, 
					markers = markers, title = title, figsize = figsize)


	def plot_vertical_orbits(self, display_mode = 'show', savefig_name = '', title ='', figsize = (8,6), fontsize = (12,9)):
		"""Method to plot the values in x axis and a dot for each iteration in y axis

		Args:
			display_mode (str, optional): Way to show the image:
										- 'show' to print the image otherwise stores image on path given
											by savefig_name. Defaults to 'show'.
			savefig_name (str, optional): path and name to store the image. Defaults to None.
			title (str, optional): title of the image. Defaults to ''.
			figsize (tuple, optional): size (x,y) of the plot. Defaults to (8,6).
			fontsize (tuple, optional): size of the text in x axis and y axis. Defaults to (12,9).
		"""
		ordered_orbits = [self.orbits[value] for value in self.values]
		plot.plot_vertical_orbits(self.values, ordered_orbits, display_mode = display_mode, 
				savefig_name = savefig_name, title = title, figsize = figsize, fontsize = fontsize)
