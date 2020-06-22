import argparse
import subprocess

opt_MAX_PROCESSES = 20
opt_MAX_TEMP_STORAGE = 10

def run_prog_get_output(prog):
	p = subprocess.Popen(prog, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	return p.stdout.readlines()

def run_gsutil(list):
	for entry in list:
		size, source, dest = entry
		print(size, source, dest)


if __name__ == '__main__':
	parser = argparse.ArgumentParser(prog='gsutil_wrapper', description='gsutil wrapper')
	parser.add_argument('path_list')

	args = parser.parse_args()

	f_path_list = open(args.path_list)
	path_list = f_path_list.readlines()

	s_list_all = []

	for line in path_list:
		if line.startswith('#'):
			opt, value = line[1:].strip().split()
			if opt == 'MAX_TEMP_STORAGE':
				opt_MAX_TEMP_STORAGE = int(value)
			elif opt == 'MAX_PROCESSES':
				opt_MAX_PROCESSES = int(value)
		else:
			entry = line.rstrip().split()
			opt = None
			if len(entry) == 3:
				source, dest, opt = entry
			else:
				source, dest = entry
			print(source)
			print(dest)
			print(opt)

			s_list = run_prog_get_output("gsutil du " + source)
			
			for s in s_list:
				s_list_all.append(s.rstrip().split() + [dest])
	
	run_gsutil(s_list_all)

