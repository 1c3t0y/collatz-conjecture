import matplotlib.pyplot as plt

def plot_collatz_lines(a, b, n = 1000):
	x = np.arange(start = a, stop = b, step = 1 / n)
	y = list(map(collatz_lines, x))

	x_int = range(a, b + 1, 1)
	y_int = list(map(collatz_function, x_int))

	fix_pts = list(map(fixed_points, x_int))

	x_par = list(map(lambda x: x/2, x_int))
	x_impar = list(map(lambda x: 3*x + 1, x_int))

	plt.plot(x, y)

	plt.plot(x, x)

	plt.plot(x_int, x_par)
	plt.plot(x_int, x_impar)

	plt.scatter(fix_pts, fix_pts)