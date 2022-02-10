from tkinter import font
from matplotlib import markers
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['text.usetex'] = True

def plot_function(func, display_mode = 'show', savefig_name = '', title = None, range = (-10,10), num = 100, figsize=(10,8), *args, **kwargs):
	if title is None:
		title = 'Plot of $f(x)$'


	# 100 linearly spaced numbers
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
	plt.plot(x, y, 'r')

	if display_mode == 'show':
		plt.show()
	else:
		plt.savefig(savefig_name)


def plot_orbit(orbit_list, function_name = 'f', display_mode = 'show', label_data = False, savefig_name = '', title = None, marker = 'o', figsize = (10,8)):
	if title is None:
		title = 'Orbit of $x_0$ ' + str(orbit_list[0])+' under ' + function_name

	x = range(0, len(orbit_list))
	fig = plt.figure(figsize=figsize)
	ax = fig.add_subplot(1, 1, 1)
	ax.set_title(title, fontsize = figsize[0]*2)
	ax.grid()

	plt.plot(x, orbit_list, marker = marker)
	plt.ylabel(r"$f^{k}(x)$", fontsize = figsize[0]*1.5)
	plt.xlabel("Iterations", fontsize = figsize[1]*1.5)
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
				label_data = False, savefig_name = '', legend = True, markers = None, title ='', figsize = (8,6)):
	
	if title is None:
		title = 'Orbits under ' + function_name

	if markers is None:
		markers = ['o' for i in range(len(orbits_list))]

	fig = plt.figure(figsize=figsize)
	ax = fig.add_subplot(1, 1, 1)
	ax.set_title(title, fontsize = figsize[0]*2)
	ax.grid()

	for i, orbit_list in enumerate(orbits_list):
		x = range(0, len(orbit_list))
		ax.plot(x, orbit_list, label = orbits_label[i], marker = markers[i])
		
		if label_data:
			for x, y in zip(x,orbit_list):
				plt.annotate(y, # this is the text
							(x,y), # these are the coordinates to position the label
							textcoords="offset points", # how to position the text
							xytext=(0,5), # distance from text to points (x,y)
							ha='center') # horizontal alignment can be left, right or center

	plt.ylabel(r"$f^{k}(x)$", fontsize = figsize[1]*1.5)
	plt.xlabel("Iterations", fontsize = figsize[0]*1.5)
	plt.xticks(fontsize = figsize[0]*1.5)
	plt.yticks(fontsize = figsize[1]*1.5)
	if legend:
		plt.legend()

	if display_mode == 'show':
		plt.show()
	else:
		plt.savefig(savefig_name)


def plot_horizontal_orbits(values, orbits_list, display_mode = 'show', 
				savefig_name = '', title ='', figsize = (8,6)):
	
	if title is None:
		title = 'Orbits under f' 

	fig = plt.figure(figsize=figsize)
	ax = fig.add_subplot(1, 1, 1)
	ax.set_title(title, fontsize = figsize[0]*2)

	for value, orbit in zip(values, orbits_list):
		x = [value]*len(orbit)
		ax.scatter(x, orbit)
	
	plt.ylabel(r"orbita de $f(x)$", fontsize = figsize[1]*1.5)
	plt.xlabel("x (values)", fontsize = figsize[0]*1.5)
	#plt.xticks(fontsize = figsize[0]*1.5)
	#plt.yticks(fontsize = figsize[1]*1.5)
	
	if display_mode == 'show':
		plt.show()
	else:
		plt.savefig(savefig_name)