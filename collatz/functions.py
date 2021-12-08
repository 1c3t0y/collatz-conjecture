import numpy as np

def collatz_function(n):
	if(n % 2 == 0):
		return n // 2
	else:
		return 3*n + 1

def collatz_lines(x):
	n = math.floor(x)
	if(n % 2 == 0):
		return (((5 / 2) * n + 4) * (x - n) + (n / 2))
	else:
		return (-(5 / 2) * n - (1 / 2)) * (x - n) + 3*n + 1

def collatz_extension(x):
    return x + 0.25 - ((2*x + 1) / 2) * np.cos(np.pi * x)

def generate_collatz_data(num_files = 0):
	last_begin_end = load_last_begin_end()
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
			period, orbit = orbit_and_period(num)
			collatz[num] = {"period" : period , "orbit" : orbit}

		save_collatz_orbit_and_period(begin, end, collatz)
		save_last_begin_end(begin, end)
		print("Saved orbits and periods from " + str(begin) + " to " + str(end))

		files_created += 1