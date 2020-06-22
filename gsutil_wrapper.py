import argparse
import subprocess
import logging
import time

opt_MAX_PROCESSES = 20
opt_MAX_TEMP_STORAGE = 10
log = logging.getLogger("gsutil_wrapper")
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
log.addHandler(handler)
log.setLevel(logging.DEBUG)

def run_prog_get_output(prog):
	p = subprocess.Popen(prog, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	return p.stdout.readlines()

def run_gsutil(list):
	log.info("MAX_PROCESSES: {}".format(opt_MAX_PROCESSES))
	log.info("MAX_TEMP_STORAGE: {}GB".format(opt_MAX_TEMP_STORAGE))
	log.info("Total files {}".format(len(list)))
	processes = []
	temp_storage = 0
	max_temp_storage = opt_MAX_TEMP_STORAGE * 1024 * 1024 * 1024
	completed = 0
	for entry in list:
		size, source, dest = entry
		log.debug("entry {}, {}, {}".format(size, source, dest))
		paths = source.split('/')
		fn = paths[len(paths) - 1]
		p = subprocess.Popen("gsutil cp {} . && gsutil mv {} {}".format(source, fn, dest), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		temp_storage = temp_storage + int(size)
		processes.append([p, size, source])
		log.info("Started copying {} to {} - {}/{} - {} procs {}GB".format(source, dest, completed, len(list), len(processes), temp_storage/1024/1024/1024))
		while len(processes) >= opt_MAX_PROCESSES or temp_storage >= max_temp_storage:
			new_processes = []
			for proc in processes:
				p, size, source = proc
				if p.poll() == None:
					new_processes.append([p, size, source])
				else:
					temp_storage = temp_storage - int(size)
					completed = completed + 1
					log.info("Completed copying {} - {}/{}".format(source, completed, len(list)))
			processes = new_processes
			time.sleep(0.1)
	for proc in processes:
		p, size, source = proc
		p.wait()
		temp_storage = temp_storage - int(size)
		completed = completed + 1
		log.info("Completed copying {} - {}/{}".format(source, completed, len(list)))

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
			log.debug(source)
			log.debug(dest)
			log.debug(opt)

			s_list = run_prog_get_output("gsutil du " + source)
			
			for s in s_list:
				s_list_all.append(s.rstrip().split() + [dest])
	
	run_gsutil(s_list_all)

