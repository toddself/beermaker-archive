import os
import cPickle
import shutil

from gzip import GzipFile


backup_levels = 10

def do_backup(filename):
	for i in range(1, backup_levels)[::-1]:
		if os.path.exists(filename):
			if i == 9:				
				pass
			elif i == 1:
				pass
			else:
				pass

def save_data(filename, dataset):
	if os.path.exists(filename):
		do_backup(filename)
	FILE = GzipFile(filename,'w')
	cPickle.dump(dataset,FILE)
	close(FILE)
	
def load_data(filename):
	FILE = GzipFile(filename,'r')
	dataset = cPickle.load(FILE)
	close(FILE)
	return dataset
	
def export_beerXML(recipe):
	pass
	
def import_beerXML(filename):
	pass