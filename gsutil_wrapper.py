import argparse


def run_prog_get_output(prog):
	print(prog)
	return "hello"



if __name__ == '__main__':
	parser = argparse.ArgumentParser(prog='gsutil_wrapper', description='gsutil wrapper')
	parser.add_argument('path_list')

	args = parser.parse_args()

	f_path_list = open(args.path_list)
	path_list = f_path_list.readlines()

	for line in path_list:
		result = run_prog_get_output(line)
		print(result)

