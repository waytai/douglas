# vim: tabstop=4 shiftwidth=4
"""
Walks through your blog root figuring out all the available monthly archives in
your blogs.  It generates html with this information and stores it in the
$archivelinks variable which you can use in your head or foot templates.

Additionally, you can specify the flavour for the link by creating an entry in
the config.py file or the ini file with the name "archive_flavour" and the
value of the flavour you want to use.

ini-file example (in the pyblosxom section):

   archive_flavour = index

config.py example:

   py["archive_flavour"] = "index"
"""
__author__ = "Wari Wahab - wari at wari dot per dot sg"
__version__ = "$Id$"

from libs import tools
import time, os

class PyblArchives:
	def __init__(self, py):
		self._py = py
		self._archives = None

	def __str__(self):
		if self._archives == None:
			self.genLinearArchive()
		return self._archives

	def genLinearArchive(self):
		root = self._py["datadir"]
		baseurl = self._py.get("base_url", "")
		
		if self._py.get("archive_flavour", ""):
			self._flavour = "?flav=" + self._py["archive_flavour"]
		else:
			self._flavour = ""
			
		archives = {}
		archiveList = tools.Walk(root)
		for file in archiveList:
			mtime = tools.filestat(file)[8]
			timetuple = time.localtime(mtime)
			mo = time.strftime('%b',timetuple)
			mo_num = time.strftime('%m',timetuple)
			da = time.strftime('%d',timetuple)
			yr = time.strftime('%Y',timetuple)
			if not archives.has_key(yr + mo_num):
				archives[yr + mo_num] = ('<a href="%s/%s/%s%s">%s-%s</a><br />' % 
										(baseurl, yr, mo, self._flavour, yr, mo))
		arcKeys = archives.keys()
		arcKeys.sort()
		arcKeys.reverse()
		result = []
		for key in arcKeys:
			result.append(archives[key])
		self._archives = '\n'.join(result)

def load(py, entryList, renderer):
	py["archivelinks"] = PyblArchives(py)

if __name__ == '__main__':
	# print genLinearArchive('../../../blosxom', 'http://roughingit.subtlehints.net/p')
	pass