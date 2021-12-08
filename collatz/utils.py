import os
import json
import matplotlib.pyplot as plt
import numpy as np
import math
import random
from itertools import groupby
from operator import itemgetter

def save_dict_json(dictionary, path, filename):
	with open(os.path.join(path, filename), 'w') as f:
		json.dump(dictionary, f)
		print("File " + filename + " created")

def load_dict_json(path, filename):
	with open(os.path.join(path, filename), 'r') as f:
		dictionary = json.load(f)
		print("File " + filename + " loaded")

	return dictionary

def make_dict_filename(begin, end):
	return "collatz_"+ str(begin)+"_"+str(end)+".json"

def make_path(dir_name):
	home = os.path.expanduser("~")
	path = os.path.join(home, dir_name)

	if not os.path.exists(path):
		os.mkdir(path)
		print("Directory " + path + " created.")

	return path

def save_collatz_orbit_and_period(begin, end, dictionary):
	dir_name = "Documentos/MAC/Tesis/software/collatz_data/orbits_and_periods"
	path = make_path(dir_name)
	filename = make_dict_filename(begin,end)
	save_dict_json(dictionary, path, filename)

def load_single_collatz_orbit_and_period(begin, end):
	dir_name = "Documentos/MAC/Tesis/software/collatz_data/orbits_and_periods"
	path = make_path(dir_name)
	filename = make_dict_filename(begin,end)
	dictionary = load_dict_json(path, filename)

	return dictionary

def load_all_collatz_orbit_and_period():
	dir_name = "Documentos/MAC/Tesis/software/collatz_data/orbits_and_periods"
	path = make_path(dir_name)
	dictionary = {}
	_, _, filenames = next(os.walk(path))
	for filename in filenames:
		dictionary.update(load_dict_json(path, filename))

	return dictionary

def load_collatz_orbit_and_period(num_files):
	dir_name = "Documentos/MAC/Tesis/software/collatz_data/orbits_and_periods"
	path = make_path(dir_name)
	dictionary = {}
	_, _, filenames = next(os.walk(path))
	for i in range(num_files):
		dictionary.update(load_dict_json(path, filenames[i]))

	return dictionary

def save_last_begin_end(begin, end):
	dictionary = {"begin": begin, "end": end}
	dir_name = "Documentos/MAC/Tesis/software/collatz_data"
	path = make_path(dir_name)
	filename = "last_begin_end_saved.json"
	save_dict_json(dictionary, path, filename)

def load_last_begin_end():
	dir_name = "Documentos/MAC/Tesis/software/collatz_data/"
	path = make_path(dir_name)
	filename = "last_begin_end_saved.json"
	dictionary = load_dict_json(path, filename)

	return dictionary