import numpy as np

from collatz import plot
from scipy.optimize import newton, bisect

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
			periodic_orbits[value] = orbit_list
			
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
		if is_fixed(x, function, *args, **kwargs):
			return x
		x = function(x, *args, **kwargs)
	return None


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


def mandelbrot_set(function, xrange, yrange, stop_iterations, threshold = 1, diverge_method = 'abs', julia = False, *args, **kwargs):
	"""Function to calculate the number of iterations of a mandelbrot (or julia) set. 

	Args:
		f (callable (numpy vectorized)): Function or callable of the set.
		xrange (iterable): Iterable with the limits of the real part in the following order: 
							(left limit for the x axis (real part),
							right limit for the x axis (real part),
							number of values to generate in the range of the two limits above).
		yrange (iterable): Iterable with the limits of the imaginary part in the following order: 
							(lower limit for the y axis (imaginary part),
							upper limit for the y axis (imaginary part),
							number of values to generate in the range of the two limits above)
		 
		stop_iterations (int): Max number of iterations.
		threshold (int, optional): Threshold that represents when the complex number is diverging . Defaults to 1.
		diverge_method (str, optional): Type of divergence method.
										'abs' for  abs(z) > threshold 
										'real_and_imag' for abs(Re(z)) > threshold) and (abs(Im(z)) > threshold 
										'real_or_imag' for abs(Re(z)) > threshold) or (abs(Im(z)) > threshold
										'real' for abs(Re(z)) > threshold
										'imag' for abs(Im(z)) > threshold

		julia (bool, optional): If True, returns the iterations over f(z), if false it calculates the initial constants c
		and iterates over f(z) + c. Defaults to False.

	Returns:
		array: Numpy array with the number of iterations that f took to diverge, array has the shapes determined by 
		third element of xrange and yrange
	"""
	# Grid with the values to iterate over lower limit : upper limit : number of values
	x, y = np.ogrid[xrange[0]: xrange[1]: xrange[2]*1j, yrange[0]: yrange[1]: yrange[2]*1j]

	# Creation of the matrix with numbers to iterate 
	z = np.transpose(x + y*1j)

	if julia:
		c = np.zeros(z.shape, dtype = z.dtype)
	else:
		c = z 

	# If number is never reached, then divergence is assumed
	iterations = stop_iterations + np.zeros(z.shape, dtype=np.dtype(int))
	not_diverged = np.full(z.shape, True) # Auxiliar for numbers that haven't diverged yet
	diverged = np.full(z.shape, False) # Auxiliar for numers that diverged.

	for i in range(stop_iterations):
		z = function(z, *args, **kwargs) + c #f^i(z) + c
		if diverge_method == 'abs':
			diverging = abs(z) > threshold
		elif diverge_method == 'real_or_imag':
			diverging = (abs(np.real(z)) > threshold) | (abs(np.imag(z)) > threshold)
		elif diverge_method == 'real_part':
			diverging = abs(np.real(z)) > threshold
		elif diverge_method == 'imag_part':
			diverging = abs(np.imag(z)) > threshold
		elif diverge_method == 'real_and_imag':
			diverging = (abs(np.real(z)) > threshold) & (abs(np.imag(z)) > threshold)
			
		new_diverging = diverging & not_diverged
		iterations[new_diverging] = i
		not_diverged = np.invert(new_diverging) & not_diverged
		
		# prevent overflow for diverging numbers
		diverged = diverged | new_diverging
		z[diverged] = np.inf
	return iterations



class DDS:
	"""
		Class to analyze Discrete dynamical systems
	"""

	def __init__(self, values, function, iterations, stop_iterations, fprime = None, start = 'orbit',*args, **kwargs) -> None:
		"""Constructor for DDS class

		Args:
			values (list): List with the initial values of the DDS
			function (function): function on which the DDS is defined
			fprime (function): Derivative of the function on which the DDS is defined
			iterations (int): Initial number of iterations to calculate
			stop_iterations (int): Max number of iterations before stopping.
			start (str, optional): operation to start with, options are:
									- 'orbit': calculates only the orbits of initial values.
									- 'periods': calculates only the periods of initial values (if stop iterations is not reached).
									- 'orbits_and_periods: calculates orbits and periods of initial values. Defaults to 'orbit'.
		"""
		self.values = values
		self.function = function
		self.fprime = fprime
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
		return is_fixed_dict


	def search_fixed_points(self, method = None, tol = 1.48e-08, sec_epsilon = 0.01, bisect_values = [(-5, -4),(-4,-3)]):
		"""Method that searches for fixed points.
		Args:
			method (string, optional): Method to use to calculate fixed points:
							if 'newton' then uses SciPy's newthon-raphson method with 
							self.values as initial values. self.fprime must be set.
							
							Uses Fixed point method otherwise.
		Returns:
			dict: dictionary with values as keys and dict values as follows:
				if fixed point is found, tuple with value and number of iterations is return, 
				tuple with last f^k(x) and None otherwise
		"""
		aux_roots = lambda x: self.function(x, *self.args, **self.kwargs) - x
		aux_roots_prime = lambda x: self.fprime(x, *self.args, **self.kwargs) - 1

		if method == 'newton':
			fixed_dict = {value : newton(aux_roots, value, fprime = aux_roots_prime, tol = tol, maxiter = self.stop_iterations, 
							disp = False)
							for value in self.values}

		elif method == 'secant':
			fixed_dict = {value : newton(aux_roots, x0 = value - sec_epsilon, x1 = value + sec_epsilon, tol = tol, 
							maxiter = self.stop_iterations, disp = False)
							for value in self.values}

		elif method == 'bisect':
			fixed_dict = {values : bisect(aux_roots, values[0], values[1], xtol=tol, maxiter=self.stop_iterations, disp=False)
							for values in bisect_values}

		else:
			fixed_dict = {value : fixed_point(value, self.function, self.stop_iterations, *self.args, **self.kwargs)
							for value in self.values}
		return fixed_dict

	
	def mandelbrot_set(self, xrange, yrange, threshold = 1, diverge_method = 'abs', julia = False):
		"""Function to calculate the number of iterations of a mandelbrot (or julia) set. 

	Args:
		xrange (iterable): Iterable with the limits of the real part in the following order: 
							(left limit for the x axis (real part),
							right limit for the x axis (real part),
							number of values to generate in the range of the two limits above).
		yrange (iterable): Iterable with the limits of the imaginary part in the following order: 
							(lower limit for the y axis (imaginary part),
							upper limit for the y axis (imaginary part),
							number of values to generate in the range of the two limits above)
		 
		threshold (int, optional): Threshold that represents when the complex number is diverging . Defaults to 1.
		diverge_method (str, optional): Type of divergence method.
										'abs' for  abs(z) > threshold 
										'real_and_imag' for abs(Re(z)) > threshold) and (abs(Im(z)) > threshold 
										'real_or_imag' for abs(Re(z)) > threshold) or (abs(Im(z)) > threshold
										'real' for abs(Re(z)) > threshold
										'imag' for abs(Im(z)) > threshold

		julia (bool, optional): If True, returns the iterations over f(z), if false it calculates the initial constants c
		and iterates over f(z) + c. Defaults to False.

	Returns:
		array: Numpy array with the number of iterations that f took to diverge, array has the shapes determined by 
		third element of xrange and yrange
	"""

		#vfunction = np.vectorize(self.function)

		return mandelbrot_set(self.function, xrange, yrange, self.stop_iterations, threshold, diverge_method,
			julia, *self.args, **self.kwargs)



	def plot_f(self, display_mode = 'show', savefig_name = 'image.png', title = None, range = (-10,10), num = 100, 
					figsize=(10,8),xlim = (-10,10),ylim = (-10,10)):
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
							range = range, num = num, figsize=figsize, xlim = xlim, ylim = ylim, *self.args, **self.kwargs)

	
	def plot_dots(self, display_mode = 'show', savefig_name = 'image.png', title = None, range = (-10,10), 
				num = 100, figsize=(10,8), xlim = (-10,10), ylim = (-10,10)):
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


	def plot_function_dots(self, dots, constant = None, display_mode = 'show', savefig_name = 'image.png', title = None, 
							range = (-10,10), num = 100, figsize=(10,8), xlim = (-10,10), ylim = (-10,10), *args, **kwargs):
		"""Method to plot the points (x, f(x)) and the function in DDS

		Args:
			dots (list, optional): List with the x values to plot (x, f(x)).
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
		plot.plot_function_dots(self.function, dots = dots, constant = constant, display_mode = display_mode,  savefig_name = savefig_name,  
								title = title, range = range,  num = num,  figsize=figsize, 
								xlim = xlim, ylim = ylim,  *args, **kwargs)

	def plot_fixed(self, fixed = None,  identity = True, display_mode = 'show', savefig_name = 'image.png', title = None, 
				range = (-10,10), num = 100, figsize=(10,8), xlim = (-10,10), ylim = (-10,10)):
		"""Method to plot the identity function, fixed points and the function in DDS

		Args:
			fixed (list, optional): List with the fixed points of the DDS if None, fixed points are calculated by newton method.
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
		
		if not fixed:
			fixed = self.search_fixed_points(method = 'newton').values()
			fixed = sorted(list(set([value for value in fixed])))
			fixed = [fixed[i] for i in range(0, len(fixed)-1) if abs(fixed[i+1] - fixed[i]) > 1e-06]

		plot.plot_fixed(self.function, fixed, identity = identity, display_mode = display_mode, savefig_name = savefig_name, title = title,
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

	def plot_fractal(self, set, xrange, yrange, display_mode = 'show', savefig_name = 'image.png', figsize = (50,10), 
		cmap = 'inferno', labels_size = (20, 20), ticks_size = (20, 20)):

		plot.plot_fractal(set, xrange, yrange, display_mode, savefig_name, figsize, cmap, labels_size, ticks_size)
