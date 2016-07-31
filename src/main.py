"""
MedCrawler

Main interface to all functionalities

Andreas Helfenstein 2016
"""

import sys, os
from datetime import datetime

#import mc_scraper
import mc_indexer
#import mc_grapher

#reload(mc_grapher)





def _get_index(posts):
	"""Get relevant terms from posts"""

	term_list = mc_indexer.main(posts)
	return term_list

def _save(project, term_list, comment=False):
	"""Save terms to file in project dir"""

	f_name = "../projects/%s/terms.txt" % project
	timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	#f_counter = 1
	#while os.path.isfile(f_name):
	#	f_name = "../projects/%s/terms-%s.txt" % (project, f_counter)
	#	f_counter += 1
	with open(f_name, 'a') as f:
		f.write('# Automated saving %s \n' % timestamp)
		if comment:
			f.write('# Comment: %s \n' % comment)
		for items in term_list:
			f.write("|".join(items))
			f.write("\n")

def _plot(project, categories=[], minweight=1, highlight=False, exclude=[]):
	"""Create plots"""

	keywords = {"project": project, "categories": categories,
		"minweight": minweight, "highlight": highlight, "exclude": exclude}
	mc_grapher.main(**keywords)

def _deploy_crawler(sysargs):
	"""Analyze sysargs and send them to the crawler"""

	i = 2
	n = len(sysargs)
	size = 0
	tags = []
	to = '.'
	fname = 'results'
	plugins = []
	while i < n:
		arg = sys.argv[i]
		if arg.startswith('-'):
			if arg in ('-h', '--help'):
				showhelp()
				break
			if arg in ('-pr', '--project'):
				i += 1
				to = sys.argv[i]
			if arg in ('-p', '--plugins'):
				i += 1
				plugins = sys.argv[i].split(',')
		elif arg.isdigit():
			size = int(arg)
		elif type(arg) == str:
			tags.append(arg)
		i += 1

	if len(tags) <= 0:
		print("You must specify at least one tag.")
		sys.exit(0)
	if size <= 0:
		print("Size must be larger than zero.")
		sys.exit()
	project_dir = "../projects/%s/" % to
	if not os.path.exists(project_dir):
		os.makedirs(project_dir)
	for indexed_list in mc_indexer.main(tags, size, plugins=plugins):
		_save(project_dir, indexed_list)
	sys.exit(0)

def _deploy_plotter(sysargs):
	"""Analyze sysargs and send them to the crawler"""

	i = 2
	n = len(sysargs)
	project = '.'
	categories = []
	minweight = 10
	highlight = False
	exclude = []

	while i < n:
		arg = sys.argv[i]
		if arg.startswith('-'):
			if arg in ('-h', '--help'):
				showhelp()
				break
			if arg in ('-pr', '--project'):
				i += 1
				project = sys.argv[i]
			if arg in ('-hl', '--highlight'):
				i += 1
				highlight = sys.argv[i]
			if arg in ('-mw', '--minweight'):
				i += 1
				minweight = int(sys.argv[i])
		elif arg.startswith('/'):
			exclude.append(sys.argv[i][1:])
		else:
			categories.append(arg)
		i += 1
	_plot(project, categories=categories, minweight=minweight,
		highlight=highlight, exclude=exclude)

def showhelp():
	"""Display help and usage"""

	print("This is the help")
	return True

if __name__ == '__main__':
	n = len(sys.argv)
	if n < 1:
		showhelp()
		sys.exit(0)
	job = sys.argv[1]
	if job.lower() in ("c", "crawl"):
		_deploy_crawler(sys.argv)
	elif job.lower() in ("p", "plot"):
		_deploy_plotter(sys.argv)
	else:
		print("Unknown command '%s'\n" % job)
		showhelp()
		sys.exit(0)
