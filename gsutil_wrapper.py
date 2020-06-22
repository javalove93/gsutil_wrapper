import argparse
import subprocess

def run_prog_get_output(prog):
	p = subprocess.Popen(prog, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	return p.stdout.readlines()



if __name__ == '__main__':
	parser = argparse.ArgumentParser(prog='gsutil_wrapper', description='gsutil wrapper')
	parser.add_argument('path_list')

	args = parser.parse_args()

	f_path_list = open(args.path_list)
	path_list = f_path_list.readlines()

	s_list_all = []

	for line in path_list:
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
			s_list_all.append([s.rstrip(), dest])
	
	print(s_list_all)

