from collatz import functions
from itertools import groupby
from operator import itemgetter

def fixed_points(n):
	if n % 2 == 0:
		return ((5/2) * n * n + (7 / 2) * n) / ((5 / 2) * n + 3)
	else:
		return (((5/2) * n * n + (7 / 2) * n + 1) / ((5 / 2) * n + (3 / 2)))


def orbit(n):
	orbit = []
	orbit.append(n)

	n0 = n
	while(n0 != 1):
		n0 = functions.collatz_function(n0)
		orbit.append(n0)

	return orbit

def orbit_and_period(n):
	orbita = []
	orbita.append(n)

	n0 = n
	i = 1
	while(n0 != 1):
		n0 = functions.collatz_function(n0)
		orbita.append(n0)
		i += 1

	return i, orbita


def same_orbit_length_range(begin, end):
	if end <= begin:
		end = begin + 1
	 
	len_dict = {}
	for i in range(begin, end):
		len, orbit = orbit_and_period(i)
		
		try:
			len_dict[len].append(i)
		except:
			len_dict[len] = [i]
	
	return len_dict


def same_orbit_length(lengths, begin = 1, end = 1000):
	if type(lengths) != type([]):
		lengths = [lengths]

	same_len_range = same_orbit_length_range(begin, end)
	same_len = {}
	
	for key in lengths:
		try:
			numbers = same_len_range[key]

		except:
			numbers = []

		same_len[key] = numbers

	return same_len


def consecutive_orbits_length(begin, end):
	same_len = same_orbit_length_range(begin, end)
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
