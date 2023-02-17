from collatz import utils
import numpy as np
import math

def collatz_function(n):
	if(n % 2 == 0):
		return n // 2
	else:
		return 3*n + 1


def collatz_function_short(n):
	if(n % 2 == 0):
		return n // 2
	else:
		return (3*n + 1) // 2


def collatz_lines(x):
	n = math.floor(x)
	if(n % 2 == 0):
		return 0.5*x*(5*n + 8) - 0.5*n*(5*n + 7)
	else:
		return -0.5*x*(5*n+1) + 0.5*n*(5*n + 7) + 1


def lines_fixed_points(n):
	if n % 2 == 0:
		return ((5/2) * n * n + (7 / 2) * n) / ((5 / 2) * n + 3)
	else:
		return (((5/2) * n * n + (7 / 2) * n + 1) / ((5 / 2) * n + (3 / 2)))


def collatz_extension(x):
    return 1.75*x + 0.5 - (1.25*x + 0.5)*np.cos(np.pi*x)


def generate_collatz_data(num_files = 0):
	last_begin_end = utils.load_last_begin_end()
	begin = last_begin_end["begin"]
	end = last_begin_end["end"]

	interval = 10000
	files_created = 0

	while(files_created < num_files):
		collatz = {}
		begin = end + 1
		end = end + interval

		for i in range(end - begin + 1):
			num = i + begin
			period, orbit = utils.orbit_and_period(num)
			collatz[num] = {"period" : period , "orbit" : orbit}

		utils.save_collatz_orbit_and_period(begin, end, collatz)
		utils.save_last_begin_end(begin, end)
		print("Saved orbits and periods from " + str(begin) + " to " + str(end))

		files_created += 1