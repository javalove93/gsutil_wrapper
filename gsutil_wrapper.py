import argparse
import subprocess
import logging
import time
import uuid

opt_MAX_PROCESSES = 20
opt_MAX_TEMP_STORAGE = 10
log = logging.getLogger("gsutil_wrapper")
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
log.addHandler(handler)
log.setLevel(logging.DEBUG)

def run_prog_get_output(prog):
	p = subprocess.Popen(prog, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='utf-8')
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
		recursive = False
		if size.startswith("r"):
			size = size[1:]
			recursive = True
		paths = source.split('/')
		fn = paths[len(paths) - 1]
		if not dest.endswith('/'):
			dest = dest + '/'
		temp_fn = fn + '_' + str(uuid.uuid1())
		temp_storage = temp_storage + int(size)
		while len(processes)+1 >= opt_MAX_PROCESSES or temp_storage >= max_temp_storage:
			new_processes = []
			for proc in processes:
				p, psize, psource = proc
				if p.poll() == None:
					new_processes.append([p, psize, psource])
				else:
					temp_storage = temp_storage - int(psize)
					completed = completed + 1
					log.info("Completed copying {} - {}/{}".format(psource, completed, len(list)))
			processes = new_processes
			time.sleep(0.1)
		if recursive:
			p = subprocess.Popen("aws s3 sync {} {} && cd {} && gsutil -o 'GSUtil:parallel_process_count={}' -m mv . {} && cd .. && rmdir {}".format(source, temp_fn, temp_fn, opt_MAX_PROCESSES, dest, temp_fn), shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
		else:
			p = subprocess.Popen("gsutil cp {} {} && gsutil mv {} {}".format(source, temp_fn, temp_fn, dest + fn), shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
		processes.append([p, size, source])
		log.info("Started copying {} to {} - {}/{} - {} procs {}GB".format(source, dest, completed, len(list), len(processes), temp_storage/1024/1024/1024))

	while len(processes) > 0:
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

if __name__ == '__main__':
	parser = argparse.ArgumentParser(prog='gsutil_wrapper', description='gsutil wrapper')
	parser.add_argument('path_list')

	args = parser.parse_args()

	f_path_list = open(args.path_list)
	path_list = f_path_list.readlines()

	s_list_all = []

	for line in path_list:
		line = line.rstrip()
		log.debug(line)
		if line.startswith('#'):
			if line[1:].strip().startswith('MAX_TEMP_STORAGE'):
				opt, value = line[1:].strip().split()
				opt_MAX_TEMP_STORAGE = int(value)
			elif line[1:].strip().startswith('MAX_PROCESSES'):
				opt, value = line[1:].strip().split()
				opt_MAX_PROCESSES = int(value)
		elif line.strip() != "":
			entry = line.rstrip().split()
			opt = None
			if len(entry) == 3:
				source, dest, opt = entry
				if source.find('*') >= 0 or source.find('?') >0:
					log.error("Wildcard can't be used with -r option")
					log.error(line)
					exit(1)
				
				if opt.strip() == "-r":
					s_list = run_prog_get_output("gsutil du -s " + source)
					size = int(s_list[0].rstrip().split()[0])
					s_list_all.append(["r{}".format(size), source, dest])
				else:
					log.error("-r option is only allowed")
					exit(1)
			else:
				source, dest = entry
				s_list = run_prog_get_output("gsutil du " + source)
				subdirs = []
				for s in s_list:
					if s.strip().endswith('/'):
						subdirs.append(s.split()[1].strip())
				for s in s_list:
					size, source = s.rstrip().split()
					subdir = False
					for d in subdirs:
						if source.startswith(d):
							subdir = True
					if not subdir:
						s_list_all.append([size, source, dest])
	
	run_gsutil(s_list_all)

