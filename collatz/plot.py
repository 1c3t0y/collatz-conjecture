from matplotlib import markers
import matplotlib.pyplot as plt
plt.rcParams['text.usetex'] = True

def plot_orbit(orbit_list, function_name = 'f', display_mode = 'show', label_data = False, savefig_name = '', title = None, marker = 'o'):
	if title is None:
		title = 'Orbit of $x_0$ ' + str(orbit_list[0])+' under ' + function_name

	x = range(0, len(orbit_list))
	plt.title(title)
	plt.plot(x, orbit_list, marker = marker)
	plt.ylabel(r"$f^{k}(x)$")
	plt.xlabel("Iterations")

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
				label_data = False, savefig_name = '', legend = True, markers = None, title = None):
	
	if title is None:
		title = 'Orbits under ' + function_name
	
	plt.title(title)

	if markers is None:
		markers = ['o' for i in range(len(orbits_list))]

	for i, orbit_list in enumerate(orbits_list):
		x = range(0, len(orbit_list))
		plt.plot(x, orbit_list, label = orbits_label[i], marker = markers[i])
		plt.ylabel(r"$f^{k}(x)$")
		plt.xlabel("Iterations")

		if label_data:
			for x, y in zip(x,orbit_list):
				plt.annotate(y, # this is the text
							(x,y), # these are the coordinates to position the label
							textcoords="offset points", # how to position the text
							xytext=(0,5), # distance from text to points (x,y)
							ha='center') # horizontal alignment can be left, right or center

	if legend:
		plt.legend()

	if display_mode == 'show':
		plt.show()
	else:
		plt.savefig(savefig_name)