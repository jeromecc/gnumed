"""GnuMed configuration handling.

Two sources of configuration information are supported:

 - INI-style configuration files
 - database tables

Just import this module to have access to a default config file.

Theory of operation:

Upon importing this module a basic config file will be parsed. This
file is registered at the default source for configuration information.

The module will look for the config file in the following standard
places:

1) programmer supplied arguments
2) user supplied command line (getopt style):	--conf-file=<a file name>
3) user supplied $aName_DIR environment variable (all uppercase)
4) ~/.<aDir>/<aName>.conf
5) ~/.<aName>.conf
6) /etc/<aDir>/<aName>.conf
7) /etc/<aName>.conf
8) ./<aName>.conf		- last resort for DOS/Win

<aDir> and <aName> will be derived automatically from the name of
the main script.

It is helpful to have a solid log target set up before importing this
module in your code. This way you will be able to see even those log
messages generated during module import.

It is also possible to instantiate objects for other config files
later on.

Once your software has established database connectivity you can
set up a config source from the database. You can limit the option
applicability by the constraints "machine", "user", and "cookie".

The basic API for handling items is get()/set() which works for both
database and INI file access. Both sources cache data. The database
config objects auto-syncs with the backend. To make INI file changes
permanent you need to call store() on the file object.

@copyright: GPL
"""
# TODO:
# - optional arg for set -> type
#==================================================================
# $Source: /home/ncq/Projekte/cvs2git/vcs-mirror/gnumed/gnumed/client/python-common/Attic/gmCfg.py,v $
__version__ = "$Revision: 1.57 $"
__author__ = "Karsten Hilbert <Karsten.Hilbert@gmx.net>"

# standard modules
import os.path, fileinput, string, sys, shutil
from types import *

# gnumed modules
import gmLog, gmCLI, gmPG

_log = gmLog.gmDefLog

# flags for __get_conf_name
cfg_SEARCH_STD_DIRS = 1
cfg_IGNORE_CMD_LINE = 2

# don't change this without knowing what you do as
# it will already be in many databases
cfg_DEFAULT = "__default__"
#================================
class cCfgBase:
	def __init__(self):
		pass

	def get(machine = None, user = None, cookie = None, option = None):
		pass

	def set(machine = None, user = None, cookie = None, option = None, value = None):
		pass
#================================
# FIXME: notify/listen on set() to ensure cache coherency across clients
class cCfgSQL:
	def __init__(self, aConn = None, aDBAPI = None):
		if aConn is None:
			_log.Log(gmLog.lErr, "Cannot init database config object without database connection.")
			raise AssertionError, "Cannot init database config object without database connection."

		self.dbapi = aDBAPI
		self.conn = aConn
		self.cache = {}
	#----------------------------
	def __del__(self):
		pass
	#----------------------------
	def get(self, machine = cfg_DEFAULT, user = None, cookie = cfg_DEFAULT, option = None):
		"""Get config value from database.

		- works for
			- strings
			- ints/floats
			- (string) lists
		- string lists currently only work with pyPgSQL >= 2.3
		  due to the need for a PgArray data type
		- also string lists will work with PostgreSQL only
		- caches items for faster repeat retrieval
		"""
		# fastpath
		cache_key = self.__make_key(machine, user, cookie, option)
		if self.cache.has_key(cache_key):
			return self.cache[cache_key]

		# sanity checks
		if option is None:
			_log.Log(gmLog.lErr, "Need to know which option to retrieve.")
			return None
		where_option = "cfg_template.name like '%s'" % option

		# if no machine given: any machine
		where_machine = " and cfg_item.machine like '%s'" % machine

		# if no cookie given: standard cookie
		where_cookie = " and cfg_item.cookie like '%s'" % cookie

		# if no user given: current db user
		# but check for "_user", too, due to ro/rw conn interaction
		if user is None:
			where_user = " and (cfg_item.owner like CURRENT_USER or cfg_item.owner like '_' || CURRENT_USER)"
		else:
			where_user = " and cfg_item.owner like '%s'" % user

		curs = self.conn.cursor()

		# retrieve option definition
		if gmPG.run_query(curs, "select cfg_item.id, cfg_template.type from cfg_item, cfg_template where %s%s%s%s and cfg_template.id = cfg_item.id_template limit 1;" % (where_option, where_user, where_machine, where_cookie)) is None:
			curs.close()
			return None

		result = curs.fetchone()
		if result is None:
			curs.close()
			_log.Log(gmLog.lWarn, 'option [%s] not in config database' % cache_key)
			return None
		(item_id, value_type) = result

		# retrieve values from appropriate table
		cmd = "select value from cfg_%s where id_item=%%s limit 1;" % value_type
		if gmPG.run_query(curs, cmd, item_id) is None:
			curs.close()
			return None
		result = curs.fetchone()
		curs.close()

		if result is None:
			_log.Log(gmLog.lWarn, 'option [%s] not in config database' % cache_key)
			return None
		else:
			self.cache[cache_key] = result[0]

		return result[0]
	#----------------------------
	def getID(self, machine = cfg_DEFAULT, user = None, cookie = cfg_DEFAULT, option = None):
		# sanity checks
		if option is None:
			_log.Log(gmLog.lErr, "Need to know which option to retrieve the ID for.")
			return None
		where_option = "cfg_template.name like '%s'" % option

		# if no machine given: any machine
		where_machine = " and cfg_item.machine like '%s'" % machine

		# if no user given: current db user
		if user is None:
			where_user = " and (cfg_item.owner like CURRENT_USER or cfg_item.owner like '_' || CURRENT_USER)"
		else:
			where_user = " and cfg_item.owner like '%s'" % user

		# if no cookie given: standard cookie
		where_cookie = " and cfg_item.cookie like '%s'" % cookie

		curs = self.conn.cursor()
		# retrieve option definition
		if gmPG.run_query(curs, "select cfg_item.id from cfg_item, cfg_template where %s%s%s%s and cfg_template.id = cfg_item.id_template limit 1;" % (where_option, where_user, where_machine, where_cookie)) is None:
			curs.close()
			return None
		result = curs.fetchone()
		if result is None:
			cache_key = self.__make_key(machine, user, cookie, option)
			_log.Log(gmLog.lWarn, 'option [%s] not in config database' % cache_key)
			curs.close()
			return None

		return result[0]
	#----------------------------
	def set(self, machine = None, user = None, cookie = None, option = None, value = None, aRWConn = None):
		"""Set the value of a config option.

		- inserts or updates value in the database
		"""

		# sanity checks
		if option is None:
			_log.Log(gmLog.lErr, "Need to know which option to store.")
			return None
		if value is None:
			_log.Log(gmLog.lErr, "Need to know the value to store.")
			return None
		if aRWConn is None:
			_log.Log(gmLog.lErr, "Need rw connection to database to store the value.")
			return None

		cache_key = self.__make_key(machine, user, cookie, option)
		data_value = value
		if type(value) is StringType:
			data_type = 'string'
		elif type(value) in [FloatType, IntType, LongType]:
			data_type = 'numeric'
		elif type(value) is ListType:
			data_type = 'str_array'
			try:
				data_value = self.dbapi.PgArray(value)
			except AttributeError:
				_log.LogException('this dbapi does not support PgArray', sys.exc_info())
				print "This Python DB-API module does not support the PgArray data type."
				print "It is recommended to install at least version 2.3 of pyPgSQL from"
				print "<http://pypgsql.sourceforge.net>."
				return None
		elif isinstance(value, self.dbapi.PgArray):
			data_type = 'str_array'
			data_value = value
		# FIXME: UnicodeType ?
		else:
			_log.Log(gmLog.lErr, "Don't know how to store option of type [%s] (%s -> %s)." % (type(value), cache_key, data_value))
			return None

		# set up field/value pairs
		if user is None:
			owner_field = ""
			owner_value = ""
			owner_where = ""
		else:
			owner_field = ", owner"
			owner_value = ", '%s'" % user
			owner_where = " and owner='%s'" % user

		if machine is None:
			machine_field = ""
			machine_value = ""
			machine_where = ""
		else:
			machine_field = ", machine"
			machine_value = ", '%s'" % machine
			machine_where = " and machine='%s'" % machine

		if cookie is None:
			cookie_field = ""
			cookie_value = ""
			cookie_where = ""
		else:
			cookie_field = ", cookie"
			cookie_value = ", '%s'" % cookie
			cookie_where = " and cookie='%s'" % cookie

		# get id of option template
		curs = aRWConn.cursor()
		cmd = "select id from cfg_template where name like %s and type like %s limit 1;"
		if gmPG.run_query(curs, cmd, option, data_type) is None:
			curs.close()
			return None
		# if not in database insert new option template
		result = curs.fetchone()
		if result is None:
			# insert new template
			cmd = "insert into cfg_template (name, type) values ( %s , %s );"
			if gmPG.run_query(curs, cmd, option, data_type) is None:
				curs.close()
				return None
			cmd = "select id from cfg_template where name like %s and type like %s limit 1;"
			if gmPG.run_query(curs, cmd, option, data_type) is None:
				curs.close()
				return None
			result = curs.fetchone()
		template_id = result[0]

		# do we need to insert a new option or update an existing one ?
		if self.get(machine, user, cookie, option) is None:
			# insert new option
			# insert option instance
			if gmPG.run_query(curs, "insert into cfg_item (id_template %s%s%s) values (%s%s%s%s)" % (owner_field, machine_field, cookie_field, template_id, owner_value, machine_value, cookie_value)) is None:
				curs.close()
				return None
			# insert option value
			cmd = "insert into cfg_%s (id_item, value)" % data_type + " values (currval('cfg_item_id_seq'), %s);"
			if gmPG.run_query(curs, cmd, data_value) is None:
				curs.close()
				return None
		else:
			# update existing option
			# get item id
			item_id = self.getID(machine, user, cookie, option)
			if item_id is None:
				curs.close()
				return None
			# update option instance
			cmd = "update cfg_%s" % data_type + " set value=%s" + " where id_item='%s';" % (item_id)
			if gmPG.run_query(curs, cmd, data_value ) is None:
				curs.close()
				return None

		# actually commit our stuff
		aRWConn.commit()
		curs.close()

		# don't update the cache BEFORE successfully committing to the
		# database because that would make the get() fastpath valid
		# without knowing whether the option is stored in the database
		self.cache[cache_key] = value

		return 1
	#-------------------------------------------
	def getAllParams(self, user = None, machine = cfg_DEFAULT):
		"""Get names of all stored parameters for a given machine/(user)/cookie-key.
		This will be used by the ConfigEditor object to create a parameter tree.
		"""
		where_args = []
		# if no machine given: any machine (= cfg_DEFAULT)
		where_machine = "cfg_item.machine like %s"
		where_args.append(machine)

		# if no user given: current db user
		# but check for "_user", too, due to ro/rw conn interaction
		if user is None:
			where_user = "(cfg_item.owner like CURRENT_USER or cfg_item.owner like '_' || CURRENT_USER)"
		else:
			where_user = "cfg_item.owner like %s"
			where_args.append(user)

		cmd =	("select name, cookie, owner, type, description "
				"from cfg_template, cfg_item "
				"where cfg_template.id = cfg_item.id_template and %s and %s" % (where_machine, where_user))

		curs = self.conn.cursor()
        # retrieve option definition
		if gmPG.run_query(curs, cmd, where_args) is None:
			curs.close()
			return None

		# result should contain a list of strings
		result = curs.fetchall()
		curs.close()
#<DEBUG>
		_log.Log(gmLog.lData, 'options [%s@%s]: %s' % (user, machine, result))
#</DEBUG>
		if result is None:
			_log.Log(gmLog.lWarn, 'no parameters stored for [%s@%s] in config database' % (user, machine))
			return None

		return result
	#----------------------------
	def __make_key(self, machine, user, cookie, option):
		return '%s-%s-%s-%s' % (machine, user, cookie, option)
	#----------------------------
#	def __run_query(self, aCursor, aQuery, *args):
#		try:
#			if len(args) == 0:
#				aCursor.execute(aQuery)
#			else:
#				aCursor.execute(aQuery, args)
#		except:
#			if len(args) == 0:
#				_log.LogException("query >>>%s<<< failed" % aQuery, sys.exc_info(), verbose=0)
#			else:
#				_log.LogException("query >>>%s<<< (args: %s) failed" % (aQuery, args), sys.exc_info(), verbose=0)
#			return None
#		return 1
#================================
class cCfgFile:
	"""Handle common INI-style config files.

	The INI file structure follows the common rules. Option values
	can be strings or lists of strings. Lists are handled transparently.
	The list format is as follows:

	listname = $listname$ # comment
	item 1
	item 2
	item 3
	$listname$

	Config data is cached in the following layout:

	self._cfg_data	= {dict}
	|
	|-> 'comment'	= [list of strings]
	`-> 'groups'	= {dict}
	 |
	 |-> group 1	= {dict}
	 | ...
	 `-> group n
	  |
	  |-> 'comment' = [list of strings]
	  `-> 'options'	= {dict}
	   |
	   |-> option 1	= {dict}
	   | ...
	   `-> option n
		|
		|-> 'comment' [list of strings]
		`-> 'value'
	"""

	_modified = None
	#----------------------------
	def __init__(self, aPath = None, aFile = None, flags = 0):
		"""Init ConfigFile object. For valid combinations of these
		parameters see above. Raises a ConfigError exception if
		no config file could be found. 
		"""
		self._cfg_data = {}
		# get conf file name
		if not self.__get_conf_name(aPath, aFile, flags):
			raise IOError, "cannot find config file"
		# load config file
		if not self.__parse_conf_file():
			raise SyntaxError, "cannot parse config file"
	#----------------------------
	# API - access config data
	#----------------------------
	def getCfg(self):
		"""Return handle to entire config dict."""
		return self._cfg_data
	#----------------------------
	def getGroups(self):
		"""Return list of all groups in config dict."""
		return self._cfg_data['groups'].keys()
	#----------------------------
	def getOptions(self, aGroup = None):
		"""Return list of all options in a group."""
		if not self._cfg_data['groups'].has_key(aGroup):
			_log.Log(gmLog.lWarn, "Cannot return options for [%s]. No such group." % aGroup)
			return None

		return self._cfg_data['groups'][aGroup]['options'].keys()
	#----------------------------
	def get(self, aGroup = None, anOption = None):
		if not self._cfg_data['groups'].has_key(aGroup):
			_log.Log(gmLog.lWarn, 'group [%s] not found' % aGroup)
			return None

		group = self._cfg_data['groups'][aGroup]

		if not group['options'].has_key(anOption):
			_log.Log(gmLog.lWarn, 'option <%s> not found in group [%s]' % (anOption, aGroup))
			return None

		return group['options'][anOption]['value']
	#----------------------------
	def getComment(self, aGroup = None, anOption = None):
		# file level
		if aGroup is None:
			# return file level comment if available
			if self._cfg_data.has_key('comment'):
				return self._cfg_data['comment']
			else:
				_log.Log(gmLog.lWarn, 'file [%s] has no comment' % self.cfgName)
				return None

		# group or option level
		if self._cfg_data['groups'].has_key(aGroup):
			if anOption is None:
				if self._cfg_data['groups'][aGroup].has_key('comment'):
					return self._cfg_data['groups'][aGroup]['comment']
				else:
					_log.Log(gmLog.lWarn, 'group [%s] (in [%s]) has no comment' % (aGroup, self.cfgName))
					return None
			else:
				if self._cfg_data['groups'][aGroup]['options'].has_key(anOption):
					if self._cfg_data['groups'][aGroup]['options'][anOption].has_key('comment'):
						return self._cfg_data['groups'][aGroup]['options'][anOption]['comment']
					else:
						_log.Log(gmLog.lWarn, 'option [%s] in group [%s] (in [%s]) has no comment' % (anOption, aGroup, self.cfgName))
						return None
				else:
					_log.Log(gmLog.lErr, 'option [%s] not in group [%s] in file [%s]' % (anOption, aGroup, self.cfgName))
					return None
		else:
			_log.Log(gmLog.lErr, 'group [%s] not in file [%s]' % (aGroup, self.cfgName))
			return None
	#----------------------------
	# API - setting config items
	#----------------------------
	def set(self, aGroup = None, anOption = None, aValue = None, aComment = None):
		"""Set an option to an arbitrary type.

		This does not write the changed configuration to a file !
		"""
		# setting file level comment ?
		if aGroup is None:
			if aComment is None:
				_log.Log(gmLog.lErr, "don't know what to do with (aGroup = %s, anOption = %s, aValue = %s, aComment = %s)" % (aGroup, anOption, aValue, aComment))
				return None
			self._cfg_data['comment'] = [str(aComment)]
			self._modified = 1
			return 1

		# make sure group is there
		if not self._cfg_data['groups'].has_key(aGroup):
			self._cfg_data['groups'][aGroup] = {'options': {}}

		# setting group level comment ?
		if anOption is None:
			if aComment is None:
				_log.Log(gmLog.lErr, "don't know what to do with (aGroup = %s, anOption = %s, aValue = %s, aComment = %s)" % (aGroup, anOption, aValue, aComment))
				return None
			self._cfg_data['groups'][aGroup]['comment'] = aComment
			self._modified = 1
			return 1

		# setting option
		if aValue is None:
			_log.Log(gmLog.lErr, "don't know what to do with (aGroup = %s, anOption = %s, aValue = %s, aComment = %s)" % (aGroup, anOption, aValue, aComment))
			return None
		# make sure option is there
		if not self._cfg_data['groups'][aGroup]['options'].has_key(anOption):
			self._cfg_data['groups'][aGroup]['options'][anOption] = {}
		# set value
		self._cfg_data['groups'][aGroup]['options'][anOption]['value'] = aValue
		# set comment
		if not aComment is None:
			self._cfg_data['groups'][aGroup]['options'][anOption]['comment'] = aComment
		self._modified = 1
		return 1
	#----------------------------
	def store(self):
		"""Store changed configuration in config file.

		- first backup old config file in case we want to take
		  back changes of content
		- then create the new config file with a separate name
		- only copy the new file to the old name if writing the
		  new file succeeds
		# FIXME: actually we need to reread the config file here before writing
		"""
		if not self._modified:
			_log.Log(gmLog.lInfo, "No changed items: nothing to be stored.")
			return 1

		bak_name = "%s.gmCfg.bak" % self.cfgName
		try:
			os.remove(bak_name)
		except:
			_log.LogException("Problem backing up config file !", sys.exc_info(), verbose=0)

		try:
			shutil.copyfile(self.cfgName, bak_name)
		except:
			_log.LogException("Problem backing up config file !", sys.exc_info(), verbose=0)

		# open new file for writing
		new_name = "%s.gmCfg.new" % self.cfgName
		new_file = open(new_name, "wb")

		# file level comment
		if self._cfg_data.has_key('comment'):
			if not self._cfg_data['comment'] == []:
				for line in self._cfg_data['comment']:
					new_file.write("# %s\n" % line)
				new_file.write("\n")
		# loop over groups
		for group in self._cfg_data['groups'].keys():
			gdata = self._cfg_data['groups'][group]
			# group level comment
			if gdata.has_key('comment'):
				if not gdata['comment'] == []:
					for line in gdata['comment']:
						new_file.write("# %s\n" % line)
			new_file.write("[%s]\n" % group)
			# loop over options for group
			for opt in gdata['options'].keys():
				odata = gdata['options'][opt]
				# option level comment
				if odata.has_key('comment'):
					for line in odata['comment']:
						new_file.write("# %s\n" % line)
				if type(odata['value']) == type([]):
					new_file.write("%s = $%s$\n" % (opt, opt))
					for line in odata['value']:
						new_file.write("%s\n" % line)
					new_file.write("$%s$\n" % opt)
				else:
					new_file.write("%s = %s\n" % (opt, odata['value']))
			new_file.write("\n\n")

		new_file.close()
		# copy new file to old file
		try:
			shutil.copyfile(new_name, self.cfgName)
		except StandardError:
			_log.LogException('cannot move modified options into config file', verbose=0)

		os.remove(new_name)
		return 1
	#----------------------------
	# internal methods
	#----------------------------
	def __get_conf_name(self, aDir = None, aName = None, flags = 0):
		"""Try to construct a valid config file name.

		- None: no valid name found
		- true(1): valid name found
		"""
		_log.Log(gmLog.lData, '(<aDir=%s>, <aName=%s>)' % (aDir, aName))

		# did the user manually supply a config file on the command line ?
		if not (flags & cfg_IGNORE_CMD_LINE):
			if gmCLI.has_arg('--conf-file'):
				self.cfgName = gmCLI.arg['--conf-file']
				# file valid ?
				if os.path.isfile(self.cfgName):
					_log.Log(gmLog.lData, 'found config file [--conf-file=%s]' % self.cfgName)
					return 1
				else:
					_log.Log(gmLog.lErr, "config file [--conf-file=%s] not found, aborting" % self.cfgName)
					return None
			else:
				_log.Log(gmLog.lData, "No config file given on command line. Format: --conf-file=<config file>")
		else:
			if gmCLI.has_arg('--conf-file'):
				_log.Log(gmLog.lInfo, 'ignoring command line per cfg_IGNORE_CMD_LINE')

		candidate_files = []

		# now make base path components
		# 1) get base name:
		if aName is None:
			# - from name of script if no file name given
			base_name = os.path.splitext(os.path.basename(sys.argv[0]))[0] + ".conf"
		else:
			# - from given file name/dir
			# don't try to expand give file name if
			# explicitely asked to search in standard dirs
			if (flags & cfg_SEARCH_STD_DIRS):
				base_name = aName
			# else do try to expand
			else:
				if aDir is None:
					absName = os.path.abspath(aName)
				else :
					absName = os.path.abspath(os.path.join(aDir, aName))
				# this candidate will stay the only one
				candidate_files.append(absName)
		# 2) get base dir
		if aDir is None:
			# from name of script
			base_dir = os.path.splitext(os.path.basename(sys.argv[0]))[0]
		else:
			# or from path in arguments
			base_dir = aDir

		# if we don't have a filename given we explicitly want
		# to search various locations -> create location list
		# huh ??
		if (flags & cfg_SEARCH_STD_DIRS) or aDir is None:
			# create list of standard config file locations
			std_dirs = []
			# - $(<script-name>_DIR)/etc/
			env_key = "%s_DIR" % string.upper(os.path.splitext(os.path.basename(sys.argv[0]))[0])
			if os.environ.has_key(env_key):
				env_key_val = os.environ[env_key]
				a_dir = os.path.abspath(os.path.expanduser(os.path.join(env_key_val, 'etc')))
				std_dirs.append(a_dir)
			else:
				_log.Log(gmLog.lInfo, "$%s not set" % env_key)

			# - ~/.base_dir/
			a_dir = os.path.expanduser(os.path.join('~', '.' + base_dir))
			std_dirs.append(a_dir)	

			# - /etc/base_dir/
			a_dir = os.path.join('/etc', base_dir)
			std_dirs.append(a_dir)

			# - /etc/
			std_dirs.append('/etc')

			# 8) ./
			# last resort for inferior operating systems such as DOS/Windows
			a_dir = os.path.abspath(os.path.split(sys.argv[0])[0])
			std_dirs.append(a_dir)

			# compile candidate file names from
			# standard dirs and base name
			for a_dir in std_dirs:
				candidate_files.append(os.path.join(a_dir, base_name))

			# eventually add hidden file:
			# - ~/.base_name
			cfgNameHidden = os.path.expanduser(os.path.join('~', '.' + base_name))
			candidate_files.insert(1, cfgNameHidden)

		#<DEBUG>
		_log.Log(gmLog.lInfo, "config file search order: %s" % str(candidate_files))
		#</DEBUG>

		# eventually loop through all candidates
		for candidate in (candidate_files):
			if not os.path.isfile(candidate):
				_log.Log(gmLog.lWarn, "config file [%s] not found" % candidate)
			else:
				_log.Log(gmLog.lData, 'found config file [%s]' % candidate)
				self.cfgName = candidate
				return 1

		# still don't have a valid config file name ?!?
		# we can't help it
		_log.Log(gmLog.lErr, "cannot find config file in any of the standard paths")
		return None
	#----------------------------
	def __parse_conf_file(self):
		if not os.path.exists(self.cfgName):
			_log.Log(gmLog.lWarn, "config file [%s] not found" % self.cfgName)

		_log.Log(gmLog.lData, "parsing config file [%s]" % self.cfgName)

		self._cfg_data['groups'] = {}

		curr_group = None
		curr_opt = None
		in_list = None
		comment_buf = []
		file_comment_buf = []
		for line in fileinput.input(self.cfgName):
			# remove trailing CR and/or LF
			line = string.replace(line,'\015','')
			line = string.replace(line,'\012','')
			# remove leading/trailing whitespace
			line = string.strip(line)

			#-----------------------
			# are we inside a list ?
			if in_list:
				# end of list ?
				if line == ("$%s$" % curr_opt):
					in_list = None
					continue
				# else keep unmodified line as list item
				self._cfg_data['groups'][curr_group]['options'][curr_opt]['value'].append(line)
				continue

			#-----------------------
			# ignore empty lines
			if line == "":
				# if before first group
				if curr_group is None:
					if self._cfg_data.has_key('comment'):
						self._cfg_data['comment'].append(comment_buf)
					else:
						self._cfg_data['comment'] = comment_buf
					comment_buf = []
				continue

			#----------
			# comment ?
			if line.startswith('#') or line.startswith(';'):
				comment = string.strip(line[1:])
				if not comment == "":
					comment_buf.append(comment)
				continue

			#----------
			# [group] ?
			if line.startswith('['):
				try:
					tmp, comment = line.split(']', 1)
				except:
					_log.Log(gmLog.lErr, 'parse error in line #%s of config file [%s]' % (fileinput.filelineno(), fileinput.filename()))
					raise
				if tmp == "[":
					_log.Log(gmLog.lErr, 'empty group definition "[]" not allowed')
					continue

				comment = string.strip(comment)
				if not comment == "":
					comment_buf.append(comment)

				curr_group = tmp[1:]
				if self._cfg_data['groups'].has_key(curr_group):
					_log.Log(gmLog.lWarn, 'duplicate group [%s] (file [%s]) - overriding options' % (curr_group, self.cfgName))
				else:
					self._cfg_data['groups'][curr_group] = {'options': {}}

				self._cfg_data['groups'][curr_group]['comment'] = comment_buf
				comment_buf = []
				continue

			#----------
			# option= ?
			if not curr_group:
				_log.Log(gmLog.lErr, 'option found before first group statement')
				continue

			#  normalize
			colon_pos = line.find(":")
			equal_pos = line.find("=")
			if colon_pos == -1 and equal_pos == -1:
				_log.Log(gmLog.lErr, 'option [%s] does not contain a separator ("=" or ":")' % line)
				continue
			if colon_pos < equal_pos:
				line = line.replace(':', '=', 1)

			#  separate <opt_name> = <opt_val # opt_comment>
			name, tmp = line.split('=', 1)
			name = string.strip(name)
			if name == "":
				_log.Log(gmLog.lErr, 'option name must not be empty')
				continue
			curr_opt = name
			if self._cfg_data['groups'][curr_group]['options'].has_key(curr_opt):
				_log.Log(gmLog.lWarn, 'duplicate option [%s] (group [%s], file [%s]) - overriding value' % (curr_opt, curr_group, self.cfgName))
			else:
				self._cfg_data['groups'][curr_group]['options'][curr_opt] = {}

			#  normalize again
			tmp = string.replace(tmp, ';', '#', 1)
			if tmp.find("#") == -1:
				val = tmp
				comment = ""
			else:
				#  separate <opt_val> # <opt_comment>
				val, comment = tmp.split('#', 1)
				comment = string.strip(comment)
			val = string.strip(val)
			if comment != "":
				comment_buf.append(comment)

			self._cfg_data['groups'][curr_group]['options'][curr_opt]['comment'] = comment_buf
			comment_buf = []

			# start of list ?
			if val == ("$%s$" % curr_opt):
				in_list = 1
				self._cfg_data['groups'][curr_group]['options'][curr_opt]['value'] = []
			else:
				self._cfg_data['groups'][curr_group]['options'][curr_opt]['value'] = val

		return 1
#=============================================================
def create_default_cfg_file():
	# get base dir from name of script
	base_dir = os.path.splitext(os.path.basename(sys.argv[0]))[0]

	# make sure base directory is there
	# FIXME: this isn't portable very well
	# - should we rather use the current dir ?
	# - but no, this may not be writeable
	tmp = os.path.expanduser(os.path.join('~', "." + base_dir))
	if not os.path.exists(tmp):
		os.mkdir(tmp)

	base_dir = tmp

	# get base name from name of script
	base_name = os.path.splitext(os.path.basename(sys.argv[0]))[0]
	conf_name = base_name + ".conf"

	# - now the path exists but we still need to
	#   make sure the file itself exists
	tmp = os.path.join(base_dir, conf_name)
	if not os.path.exists(tmp):
		try:
			f = open(tmp, "wb")
			f.write('# [%s]: empty default config file\n' % base_name)
			f.write('# -------------------------------------------------------------\n')
			f.write('# created by gmCfg because no other config file could be found,\n')
			f.write('# please check the docs that came with the software\n')
			f.write('# to find out what options you can set in here\n')
			f.write('\n')
			f.close()
		except StandardError:
			_log.LogException("Cannot create empty default config file [%s]." % tmp, sys.exc_info(), verbose=0)
			return None

	_log.Log(gmLog.lErr, 'Created empty config file [%s].' % tmp)
	print "Had to create empty (default) config file [%s].\nPlease check the docs for possible settings." % tmp
	return 1
#=============================================================
# main
#=============================================================
if __name__ == '__main__':
	_log.SetAllLogLevels(gmLog.lData)

_log.Log(gmLog.lData, __version__)

if __name__ == "__main__":
	if len(sys.argv) > 1:
		try:
			myCfg = cCfgFile(aFile = sys.argv[1])
#			myCfg = cCfgFile(aFile = sys.argv[1],flags=cfg_SEARCH_STD_DIRS)
		except:
			exc = sys.exc_info()
			_log.LogException('unhandled exception', exc, verbose=1)
			raise

		print myCfg

		# display file level data
		print "file: %s" % myCfg.cfgName
		tmp = myCfg.getComment()
		if not tmp is None:
			print "comment:", tmp

		# display group level data
		groups = myCfg.getGroups()
		print "groups:", str(groups)

		# recurse groups
		for group in groups:
			print "GROUP [%s]" % group

			tmp = myCfg.getComment(aGroup = group)
			if not tmp is None:
				print " ", tmp

			# recurse options
			options = myCfg.getOptions(group)
			for option in options:
				tmp = myCfg.get(group, option)
				if not tmp is None:
					print "OPTION <%s> = >>>%s<<<" % (option, tmp)
				tmp = myCfg.getComment(group, option)
				if not tmp is None:
					print "  %s" % tmp

		myCfg.set("date", "modified", "right now", ["should always be rather current"])
		myCfg.store()

	else:
		print "======================================================================"
		print __doc__
		print "======================================================================"
		raw_input()

		print "testing database config"
		print "======================="
		from pyPgSQL import PgSQL
		dsn = "%s:%s:%s:%s:%s:%s:%s" % ('localhost', '5432', 'test', 'postgres', '', '', '')
		conn = PgSQL.connect(dsn)
		myDBCfg = cCfgSQL(aConn = conn, aDBAPI=PgSQL)

		font = myDBCfg.get(option = 'font name')
		print "font is currently:", font

		new_font = "huh ?"
		if font == "Times New Roman":
			new_font = "Courier"
		if font == "Courier":
			new_font = "Times New Roman"
		myDBCfg.set(option='font name', value=new_font, aRWConn=conn)

		font = myDBCfg.get(option = 'font name')
		print "font is now:", font

		import random
		random.seed()
		new_opt = str(random.random())
		print "setting new option", new_opt
		myDBCfg.set(option=new_opt, value = "I do not know.", aRWConn=conn)
		print "new option is now:", myDBCfg.get(option = new_opt)

		print "setting array option"
		aList = []
		aList.append("val 1")
		aList.append("val 2")
		new_opt = str(random.random())
		myDBCfg.set(option=new_opt, value = aList, aRWConn=conn)
		aList = []
		aList.append("val 2")
		aList.append("val 1")
		myDBCfg.set(option=new_opt, value = aList, aRWConn=conn)

		conn.close()
else:
	# - we are being imported

	# have a sane pointer even if we fail
	gmDefCfgFile = None

	# - if we don't find any config file we return None
	# - IF the caller really knows what she does she can handle
	#   that exception in her own code
	try:
		gmDefCfgFile = cCfgFile()
	except:
		_log.LogException('unhandled exception', sys.exc_info(), verbose=0)

#=============================================================
# $Log: gmCfg.py,v $
# Revision 1.57  2003-08-10 00:53:09  ncq
# - cleanup to Hilmars nice additions
#
# Revision 1.56  2003/08/07 23:31:04  hinnef
# changed CfgFile.__get_conf_name so that files can be searched in more than one location
#
# Revision 1.55  2003/07/21 20:53:50  ncq
# - fix string screwup
#
# Revision 1.54  2003/07/21 19:18:06  ncq
# - use gmPG.run_query(), not home-brew
# - kill gmPG.esc() use
# - cleanup/comments
#
# Revision 1.53  2003/06/26 21:29:58  ncq
# - (cmd, arg) style, fatal->verbose
#
# Revision 1.52  2003/06/26 04:18:40  ihaywood
# Fixes to gmCfg for commas
#
# Revision 1.51  2003/06/21 10:44:09  ncq
# - handle read-only media better when modifying config file
#
# Revision 1.50  2003/06/17 22:21:53  ncq
# - improve __get_conf_name()
#
# Revision 1.49  2003/06/03 21:52:23  hinnef
# - fixed a bug in cfgSQL.set() when updating a value
#
# Revision 1.48  2003/05/12 09:12:48  ncq
# - minor cleanups
#
# Revision 1.47  2003/05/10 18:45:52  hinnef
# - added getAllParams for use in gmConfigRegistry
#
# Revision 1.46  2003/04/14 07:45:47  ncq
# - better temp names in cfgFile.store()
#
# Revision 1.45  2003/03/31 00:26:46  ncq
# - forgot "\n"
#
# Revision 1.44  2003/03/30 21:38:28  ncq
# - put some blurb in new, empty config files
#
# Revision 1.43  2003/03/27 21:10:12  ncq
# - move '__default__' to cfg_DEFAULT constant
#
# Revision 1.42  2003/03/23 10:32:50  ncq
# - improve console messages a bit
#
# Revision 1.41  2003/02/21 08:58:51  ncq
# - improve PgArray detection even more
#
# Revision 1.40  2003/02/21 08:51:57  ncq
# - catch exception on missing PgArray
#
# Revision 1.39  2003/02/15 08:51:05  ncq
# - don't remove empty lines in lists
#
# Revision 1.38  2003/02/11 16:52:36  ncq
# - log one more failing corner case
#
# Revision 1.37  2003/02/09 09:48:28  ncq
# - revert breakage created by sjtan
#
# Revision 1.36  2003/02/09 02:02:30  sjtan
#
# allows first time run of gmGuiMain without a conf file. A Default conf file called gnumed.conf is created.
#
# Revision 1.35  2003/01/28 10:53:09  ncq
# - clarification to test code
#
# Revision 1.34  2003/01/12 11:53:58  ncq
# - fixed subtle bug resulting from ro/rw connections:
#  - set() would request a rw conn thus CURRENT_USER = "_user"
#  - get() would use a ro conn, thus CURRENT_USER == "user"
#  - there'd never be a match and the items would keep proliferating
#
# Revision 1.33  2003/01/05 09:56:58  ncq
# - ironed out some bugs in the array handling
# - streamlined code
# - have cfg.set() explicitely use rw conn to DB only when needed
#
# Revision 1.32  2003/01/04 12:19:04  ncq
# - better comment
#
# Revision 1.31  2003/01/04 12:17:05  ncq
# - backup old config file before overwriting
#
# Revision 1.30  2002/12/26 15:49:10  ncq
# - better comments
#
# Revision 1.29  2002/12/26 15:21:18  ncq
# - database config now works even with string lists
#
# Revision 1.28  2002/12/01 01:11:42  ncq
# - log config file line number on parse errors
#
# Revision 1.27  2002/11/28 11:40:12  ncq
# - added database config
# - reorganized self test
#
# Revision 1.26  2002/11/18 09:41:25  ncq
# - removed magic #! interpreter incantation line to make Debian happy
#
# Revision 1.25  2002/11/17 20:09:10  ncq
# - always display __doc__ when called standalone
#
# Revision 1.24  2002/11/05 18:15:03  ncq
# - new helper getOptions()
# - modified example code to show real use
#
# Revision 1.23  2002/11/04 15:38:28  ncq
# - moved empty config file creation to helper function
#
# Revision 1.22  2002/11/03 14:11:19  ncq
# - autocreate log file on failing to find one
#
# Revision 1.21  2002/11/03 13:21:05  ncq
# - phase 1: error levels more suitable
#
# Revision 1.20  2002/10/22 21:11:44  ncq
# - throwing exception ImportError on failing to load the
#   default config file wasn't such a good idea after all
#   since we might _actually_ only be interested in a different
#   file ...
#
# Revision 1.19  2002/10/22 15:30:16  ncq
# - added getGroups()
#
# Revision 1.18  2002/10/19 19:30:13  ncq
# - on being imported always raise ImportError on failing to use default config file
#
# Revision 1.17  2002/10/19 19:24:37  ncq
# - fixed some whitespace breakage
# - raise error on failing to parse default config file, if you really want
#   to override this you should handle that exception in your own code
#
# Revision 1.16  2002/10/18 19:57:09  hinnef
# fixed problems when a invalid filename is given, static class variables and
# changed the initialization of gmDefCfgFile so that it can be imported from
# standalone modules
#
# Revision 1.15  2002/09/30 10:58:27  ncq
# - consistently spell GnuMed
#
# Revision 1.14  2002/09/26 13:21:37  ncq
# - log version
#
# Revision 1.13  2002/09/12 23:11:14  ncq
# - fixed one nasty overwriting bug in store()
#
# Revision 1.12  2002/09/12 10:07:29  ncq
# - properly normalize : -> =
#
# Revision 1.11  2002/09/12 09:17:11  ncq
# - windows unsucked
#
# Revision 1.10  2002/09/10 18:43:02  ncq
# - windows sucks !
#
# Revision 1.9  2002/09/10 18:31:45  ncq
# - windows is strange: os.rename -> shutil.copyfile + os.remove
#
# Revision 1.8  2002/09/10 18:15:28  ncq
# - os.rename() over existing files fails on non-UNIX
#
# Revision 1.7  2002/09/10 17:51:33  ncq
# - more sensible log levels for some data
#
# Revision 1.6  2002/09/08 15:55:47  ncq
# - added log cvs keyword
#
