import matplotlib.pyplot as plt
import numpy as np
import networkx as nx

from networkx.drawing.nx_pydot import graphviz_layout
from matplotlib import markers

plt.rcParams['text.usetex'] = True


def plot_dots(func, 
				display_mode = 'show', 
				savefig_name = 'image.png', 
				title = None, 
				range = (-10,10), 
				num = 100, 
				figsize=(10,8),
				xlim = (-10,10),
				ylim = (-10,10), 
				*args, **kwargs):
	if title is None:
		title = 'Plot of $f(x)$'
	
	# linearly spaced numbers
	x = np.linspace(range[0], range[1], num)
	y = [func(value, *args, **kwargs) for value in x]

	fig = plt.figure(figsize=figsize)
	ax = fig.add_subplot(1, 1, 1)
	ax.set_title(title, fontsize = figsize[0]*2)
	ax.spines['left'].set_position('zero')
	ax.spines['bottom'].set_position('zero')
	ax.spines['right'].set_color('none')
	ax.spines['top'].set_color('none')
	ax.xaxis.set_ticks_position('bottom')
	ax.yaxis.set_ticks_position('left')
	ax.grid()

	# plot the function
	plt.xlim(xlim)
	plt.ylim(ylim)
	plt.scatter(x,y)

	
	if display_mode == 'show':
		plt.show()
	else:
		plt.savefig(savefig_name)
	


def plot_function(func, display_mode = 'show', 
					savefig_name = 'image.png', 
					title = None, range = (-10,10), 
					num = 100, 
					figsize=(10,8),
					xlim = (-10,10),
					ylim = (-10,10),
					 *args, **kwargs):
	if title is None:
		title = 'Plot of $f(x)$'


	# linearly spaced numbers
	x = np.linspace(range[0], range[1], num)
	y = [func(value, *args, **kwargs) for value in x]
	
	fig = plt.figure(figsize=figsize)
	ax = fig.add_subplot(1, 1, 1)
	ax.set_title(title, fontsize = figsize[0]*2)
	ax.spines['left'].set_position('center')
	ax.spines['bottom'].set_position('zero')
	ax.spines['right'].set_color('none')
	ax.spines['top'].set_color('none')
	ax.xaxis.set_ticks_position('bottom')
	ax.yaxis.set_ticks_position('left')
	ax.grid()

	# plot the function
	plt.xlim(xlim)
	plt.ylim(ylim)
	plt.plot(x, y, 'r')

	if display_mode == 'show':
		plt.show()
	else:
		plt.savefig(savefig_name)


def plot_function_dots(func,
				dots,
				constant = None,
				display_mode = 'show', 
				savefig_name = 'image.png', 
				title = None, 
				range = (-10,10), 
				num = 100, 
				figsize=(10,8),
				xlim = (-10,10),
				ylim = (-10,10), 
				*args, **kwargs):

	# linearly spaced numbers
	x = np.linspace(range[0], range[1], num)
	y = [func(value, *args, **kwargs) for value in x]
	y_dots = [func(value, *args, **kwargs) for value in dots]

	fig = plt.figure(figsize=figsize)
	ax = fig.add_subplot(1, 1, 1)
	ax.set_title(title, fontsize = figsize[0]*3)
	ax.spines['left'].set_position('zero')
	ax.spines['bottom'].set_position('zero')
	ax.spines['right'].set_color('none')
	ax.spines['top'].set_color('none')
	ax.xaxis.set_ticks_position('bottom')
	ax.yaxis.set_ticks_position('left')
	ax.grid()

	# plot the function
	plt.xlim(xlim)
	plt.ylim(ylim)
	if constant:
		plt.plot(x, [constant]*len(x), 'gray')
		plt.plot(x, [constant*-1]*len(x), 'gray')
	plt.plot(x, y, 'r')
	plt.scatter(dots, y_dots, color = 'b')

	if display_mode == 'show':
		plt.show()
	else:
		plt.savefig(savefig_name)


def plot_fixed(func,
				fixed,
				identity = True,
				display_mode = 'show', 
				savefig_name = 'image.png', 
				title = None, 
				range = (-10,10), 
				num = 100, 
				figsize=(10,8),
				xlim = (-10,10),
				ylim = (-10,10), 
				*args, **kwargs):

	# linearly spaced numbers
	x = np.linspace(range[0], range[1], num)
	y = [func(value, *args, **kwargs) for value in x]

	fig = plt.figure(figsize=figsize)
	ax = fig.add_subplot(1, 1, 1)
	ax.set_title(title, fontsize = figsize[0]*3)
	ax.spines['left'].set_position('zero')
	ax.spines['bottom'].set_position('zero')
	ax.spines['right'].set_color('none')
	ax.spines['top'].set_color('none')
	ax.xaxis.set_ticks_position('bottom')
	ax.yaxis.set_ticks_position('left')
	ax.grid()

	# plot the function
	plt.xlim(xlim)
	plt.ylim(ylim)
	if identity:
		plt.plot(x, x, 'gray')
	plt.plot(x, y, 'r')
	plt.scatter(fixed, fixed, color = 'b')

	if display_mode == 'show':
		plt.show()
	else:
		plt.savefig(savefig_name)


def plot_orbit(orbit_list, function_name = 'f', display_mode = 'show', 
				label_data = False, savefig_name = 'image.png', title = None, 
				marker = 'o', figsize = (10,8)):
	if title is None:
		title = 'Orbit of $x_0=$ ' + str(orbit_list[0])+' under ' + function_name

	x = range(0, len(orbit_list))
	fig = plt.figure(figsize=figsize)
	ax = fig.add_subplot(1, 1, 1)
	ax.set_title(title, fontsize = figsize[0]*2)
	ax.grid()

	plt.plot(x, orbit_list, marker = marker)
	plt.ylabel(r"$" + function_name + r"^{k}(x)$", fontsize = figsize[0]*1.5)
	plt.xlabel("mandelbrot_set", fontsize = figsize[1]*1.5)
	plt.xticks(fontsize = figsize[0]*1.5)
	plt.yticks(fontsize = figsize[1]*1.5)

	if label_data:
		for x, y in zip(x,orbit_list):
			plt.annotate(y, # this is the text
						(x,y), # these are the coordinates to position the label
						textcoords="offset points", # how to position the text
						xytext=(0,5), # distance from text to points (x,y)
						ha='center') # horizontal alignment can be left, right or center

	if display_mode == 'show':
		plt.show()
	else:
		plt.savefig(savefig_name)
		

def plot_orbits(orbits_list, orbits_label, function_name = 'f', display_mode = 'show', 
				label_data = False, savefig_name = 'image.png', legend = True, markers = None, 
				title = '', figsize = (8,6), fontsize = (12,9)):
	
	if title is None:
		title = r'Orbits under ' + function_name

	if markers is None:
		markers = ['o' for i in range(len(orbits_list))]

	fig = plt.figure(figsize=figsize)
	ax = fig.add_subplot(1, 1, 1)
	#ax.set_title(title, fontsize = figsize[0]*2)
	ax.grid()

	for i, orbit_list in enumerate(orbits_list):
		x = range(0, len(orbit_list))
		ax.plot(x, orbit_list, label = orbits_label[i], marker = markers[i])
		
		if label_data:
			for x, y in zip(x,orbit_list):
				plt.annotate("{:.2f}".format(y), # this is the text
							(x,y), # these are the coordinates to position the label
							textcoords="offset points", # how to position the text
							xytext=(0,5), # distance from text to points (x,y)
							ha='center') # horizontal alignment can be left, right or center

	plt.ylabel("$"+ function_name + r"^{k}(x)$", fontsize = fontsize[1])
	plt.xlabel("Iteraciones", fontsize = fontsize[0])
	plt.xticks(fontsize = fontsize[0])
	plt.yticks(fontsize = fontsize[1])
	if legend:
		plt.legend(loc='upper right')

	if display_mode == 'show':
		plt.show()
	else:
		plt.savefig(savefig_name)


def plot_vertical_orbits(values, orbits_list, display_mode = 'show', savefig_name = 'image.png', 
						title ='', figsize = (8,6), fontsize = (12,9)):
	
	if title is None:
		title = 'Orbits under f' 

	fig = plt.figure(figsize=figsize)
	ax = fig.add_subplot(1, 1, 1)
	ax.set_title(title, fontsize = figsize[0]*2)
	ax.grid()
	
	for value, orbit in zip(values, orbits_list):
		x = [value]*len(orbit)
		ax.scatter(x, orbit)
	
	plt.ylabel(r"orbita de $f(x)$", fontsize = figsize[1]*1.5)
	plt.xlabel("Iteraciones", fontsize = fontsize[0])
	plt.xticks(fontsize = fontsize[0])
	plt.yticks(fontsize = fontsize[1])
	
	if display_mode == 'show':
		plt.show()
	else:
		plt.savefig(savefig_name)


def plot_directed_orbit(orbit_list, prog = 'neato', value_format = "{:.2f}", figsize = (10,8), connectionstyle = 'arc3, rad = 0', display_mode = 'show', savefig_name = 'image.png',
						node_size = 500, font_size = 12, node_color = 'white', edgecolors = 'black', width = 2):

	orbit_tuples = list(set(
					[(" " + value_format.format(orbit_list[i]), " " + value_format.format(orbit_list[i+1])) 
					for i in range(len(orbit_list) - 1)]
					))
					
	G = nx.MultiDiGraph()
	G.add_edges_from(orbit_tuples)

	plt.figure(figsize=figsize)

	pos = graphviz_layout(G, prog = prog)
	nx.draw(G, pos = pos, with_labels = True, node_size = node_size, edgecolors = edgecolors, font_size = font_size, 
					width = width, node_color = node_color, connectionstyle = connectionstyle)


	if display_mode == 'show':
		plt.show()
	else:
		plt.savefig(savefig_name)


def plot_directed_orbits(orbits_list, prog  = 'dot', value_format = "{:.2f}", figsize = (10,8), 
						connectionstyle = 'arc3, rad = 0', display_mode = 'show', 
						savefig_name = 'image.png', node_size = 500, font_size = 12, 
						node_color = 'white', edgecolors = 'black', width = 2):

	orbit_tuples = list(set([(" " + value_format.format(orbits_list[i][j]), " " + value_format.format(orbits_list[i][j+1])) 
						for i in range(len(orbits_list)) for j in range(len(orbits_list[i]) - 1)]))
	
	G = nx.MultiDiGraph()
	G.add_edges_from(orbit_tuples)

	plt.figure(figsize=figsize)

	pos = graphviz_layout(G, prog = prog)
	nx.draw(G, pos = pos, with_labels = True, node_size = node_size, edgecolors = edgecolors, font_size = font_size, 
					width = width, node_color = node_color, connectionstyle = connectionstyle)


	if display_mode == 'show':
		plt.show()
	else:
		plt.savefig(savefig_name)


def plot_mandelbrot_set(initial_values, periods_list, display_mode = 'Show', savefig_name = 'image.png',figsize = (10,8), *args, **kwargs):
	
	plt.figure(figsize=figsize)
	plt.scatter(initial_values, periods_list, *args, **kwargs)

	if display_mode == 'show':
		plt.show()
	else:
		plt.savefig(savefig_name)


def plot_fractal(mandelbrot_set, xrange, yrange, display_mode = 'show', savefig_name = 'image.png', figsize = (50,10), 
		cmap = 'inferno', labels_size = (20, 20), ticks_size = (20, 20)):
	
	plt.rcParams["figure.figsize"] = figsize
	# Objects for color bar
	fig = plt.figure()
	ax = plt.axes() 

	im = plt.imshow(mandelbrot_set, cmap=cmap, interpolation = 'spline16', 
			extent = (xrange[0], xrange[1], yrange[0], yrange[1]), origin = 'lower')

	#axes labels
	plt.xlabel('Re(z)', fontsize = labels_size[0])
	plt.ylabel('Im(z)', fontsize = labels_size[0])

	#ticks fontsize
	plt.xticks(fontsize=ticks_size[0])
	plt.yticks(fontsize=ticks_size[1])   

	if mandelbrot_set.shape[0] < mandelbrot_set.shape[1]:
		# sets color bar horizontal
		cax = fig.add_axes([ax.get_position().x0,
					ax.get_position().y0-0.2,
					ax.get_position().width,
					0.02])
		orientation = 'horizontal'
		tickssize = ticks_size[0]
		labelsize = labels_size[0]
	else:
		# sets color bar vertical
		cax = fig.add_axes([ax.get_position().x1+0.01,
					ax.get_position().y0,
					0.02,
					ax.get_position().height])
		orientation = 'vertical'
		tickssize = ticks_size[1]
		labelsize = labels_size[1]
		
	cbar = plt.colorbar(im, cax = cax, orientation = orientation)
	cbar.ax.tick_params(labelsize=tickssize)
	cbar.set_label(label='Iteraciones',size=labelsize)

	if display_mode == 'show':
		plt.show()
	else:
		plt.savefig(savefig_name)