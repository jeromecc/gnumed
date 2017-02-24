"""GNUmed logging framework setup.

All error logging, user notification and otherwise unhandled 
exception handling should go through classes or functions of 
this module.

Theory of operation:

This module tailors the standard logging framework to
the needs of GNUmed.

By importing gmLog2 into your code you'll get the root
logger send to a unicode file with messages in a format useful
for debugging. The filename is either taken from the
command line (--log-file=...) or derived from the name
of the main application.

The log file will be found in one of the following standard
locations:

1) given on the command line as "--log-file=LOGFILE"
2) ~/.<base_name>/<base_name>.log
3) /dir/of/binary/<base_name>.log		(mainly for DOS/Windows)

where <base_name> is derived from the name
of the main application.

If you want to specify just a directory for the log file you
must end the --log-file definition with a slash.

By importing "logging" and getting a logger your modules
never need to worry about the real message destination or whether
at any given time there's a valid logger available.

Your MAIN module simply imports gmLog2 and all other modules
will merrily and automagically start logging away.
"""
# TODO:
# - exception()
# - ascii_ctrl2mnemonic()
#========================================================================
__author__  = "K. Hilbert <Karsten.Hilbert@gmx.net>"
__license__ = "GPL v2 or later (details at http://www.gnu.org)"


# stdlib
import logging
import sys
import os
import io
import codecs
import locale
import datetime as pydt


_logfile_name = None
_logfile = None

_string_encoding = None

# table used for cooking non-printables
AsciiName = ['<#0-0x00-nul>',
			 '<#1-0x01-soh>',
			 '<#2-0x02-stx>',
			 '<#3-0x03-etx>',
			 '<#4-0x04-eot>',
			 '<#5-0x05-enq>',
			 '<#6-0x06-ack>',
			 '<#7-0x07-bel>',
			 '<#8-0x08-bs>',
			 '<#9-0x09-ht>',
			 '<#10-0x0A-lf>',
			 '<#11-0x0B-vt>',
			 '<#12-0x0C-ff>',
			 '<#13-0x0D-cr>',
			 '<#14-0x0E-so>',
			 '<#15-0x0F-si>',
			 '<#16-0x10-dle>',
			 '<#17-0x11-dc1/xon>',
			 '<#18-0x12-dc2>',
			 '<#19-0x13-dc3/xoff>',
			 '<#20-0x14-dc4>',
			 '<#21-0x15-nak>',
			 '<#22-0x16-syn>',
			 '<#23-0x17-etb>',
			 '<#24-0x18-can>',
			 '<#25-0x19-em>',
			 '<#26-0x1A-sub>',
			 '<#27-0x1B-esc>',
			 '<#28-0x1C-fs>',
			 '<#29-0x1D-gs>',
			 '<#30-0x1E-rs>',
			 '<#31-0x1F-us>'
			]

# msg = reduce(lambda x, y: x+y, (map(self.__char2AsciiName, list(tmp))), '')
#
#	def __char2AsciiName(self, aChar):
#		try:
#			return AsciiName[ord(aChar)]
#		except IndexError:
#			return aChar
#
#	def __tracestack(self):
#		"""extract data from the current execution stack
#
#		this is rather fragile, I guess
#		"""
#		stack = traceback.extract_stack()
#		self.__modulename = stack[-4][0]
#		self.__linenumber = stack[-4][1]
#		self.__functionname = stack[-4][2]
#		if (self.__functionname == "?"):
#			self.__functionname = "Main"

#===============================================================
# external API
#===============================================================
def flush():
	logger = logging.getLogger('gm.logging')
	logger.critical(u'-------- synced log file -------------------------------')
	root_logger = logging.getLogger()
	for handler in root_logger.handlers:
		handler.flush()

#===============================================================
#def log_exception_details():
#
#	t, v, tb = sys.exc_info()
#	if t is None:
#		logger.debug('no exception to detail')
#		return
#
#	logger = logging.getLogger('gm.logging')
#	logger.debug('exception: %s', v)
#	logger.debug('type: %s', t)
#	logger.debug('list of attributes:')
#	for attr in [ a for a in dir(v) if not a.startswith('__') ]:
#		logger.debug('  %s: %s', attr, getattr(v, attr))

#===============================================================
def log_stack_trace(message=None, t=None, v=None, tb=None):

	logger = logging.getLogger('gm.logging')

	if t is None:
		t = sys.exc_info()[0]
	if v is None:
		v = sys.exc_info()[1]
	if tb is None:
		tb = sys.exc_info()[2]
	if tb is None:
		logger.debug(u'sys.exc_info() did not return a traceback object, trying sys.last_traceback')
		try:
			tb = sys.last_traceback
		except AttributeError:
			logger.debug(u'no stack to trace (no exception information available)')
			return

	# log exception details
	logger.debug(u'exception: %s', v)
	logger.debug(u'type: %s', t)
	logger.debug(u'list of attributes:')
	for attr in [ a for a in dir(v) if not a.startswith(u'__') ]:
		logger.debug(u'  %s: %s', attr, getattr(v, attr))

	# make sure we don't leave behind a bind
	# to the traceback as warned against in
	# sys.exc_info() documentation
	try:
		# recurse back to root caller
		while 1:
			if not tb.tb_next:
				break
			tb = tb.tb_next
		# put the frames on a stack
		stack_of_frames = []
		frame = tb.tb_frame
		while frame:
			stack_of_frames.append(frame)
			frame = frame.f_back
	finally:
		del tb
	stack_of_frames.reverse()

	if message is not None:
		logger.debug(message)
	logger.debug(u'stack trace follows:')
	logger.debug(u'(locals by frame, outmost frame first)')
	for frame in stack_of_frames:
		logger.debug (
			u'>>> execution frame [%s] in [%s] at line %s <<<',
			frame.f_code.co_name,
			frame.f_code.co_filename,
			frame.f_lineno
		)
		for varname, value in frame.f_locals.items():
			if varname == u'__doc__':
				continue

			try:
				value = unicode(value, encoding = _string_encoding, errors = 'replace')
			except TypeError:
				try:
					value = unicode(value)
				except (UnicodeDecodeError, TypeError):
					value = '%s' % str(value)
					value = value.decode(_string_encoding, 'replace')

			logger.debug(u'%20s = %s', varname, value)

#===============================================================
def set_string_encoding(encoding=None):

	logger = logging.getLogger('gm.logging')

	global _string_encoding

	if encoding is not None:
		codecs.lookup(encoding)
		_string_encoding = encoding
		logger.info(u'setting python.str -> python.unicode encoding to <%s> (explicit)', _string_encoding)
		return True

	enc = sys.getdefaultencoding()
	if enc != 'ascii':
		_string_encoding = enc
		logger.info(u'setting python.str -> python.unicode encoding to <%s> (sys.getdefaultencoding)', _string_encoding)
		return True

	enc = locale.getlocale()[1]
	if enc is not None:
		_string_encoding = enc
		logger.info(u'setting python.str -> python.unicode encoding to <%s> (locale.getlocale)', _string_encoding)
		return True

	# FIXME: or rather use utf8 ?
	_string_encoding = locale.getpreferredencoding(do_setlocale=False)
	logger.info(u'setting python.str -> python.unicode encoding to <%s> (locale.getpreferredencoding)', _string_encoding)
	return True

#===============================================================
# internal API
#===============================================================
def __setup_logging():

	set_string_encoding()

	global _logfile
	if _logfile is not None:
		return True

	if not __get_logfile_name():
		return False

	if sys.version[:3] < '2.5':
		fmt = u'%(asctime)s  %(levelname)-8s  %(name)s (%(pathname)s @ #%(lineno)d): %(message)s'
	else:
		fmt = u'%(asctime)s  %(levelname)-8s  %(name)s (%(pathname)s::%(funcName)s() #%(lineno)d): %(message)s'

	_logfile = io.open(_logfile_name, mode = 'wt', encoding = 'utf8', errors = 'replace')

	logging.basicConfig (
		format = fmt,
		datefmt = '%Y-%m-%d %H:%M:%S',
		level = logging.DEBUG,
		stream = _logfile
	)

	logger = logging.getLogger('gm.logging')
	logger.critical(u'-------- start of logging ------------------------------')
	logger.info(u'log file is <%s>', _logfile_name)
	logger.info(u'log level is [%s]', logging.getLevelName(logger.getEffectiveLevel()))
	logger.info(u'log file encoding is <utf8>')
	logger.info(u'initial python.str -> python.unicode encoding is <%s>', _string_encoding)
#---------------------------------------------------------------
def __get_logfile_name():

	global _logfile_name
	if _logfile_name is not None:
		return _logfile_name

	def_log_basename = os.path.splitext(os.path.basename(sys.argv[0]))[0]
	default_logfile_name = '%s-%s-%s.log' % (
		def_log_basename,
		pydt.datetime.now().strftime('%Y_%m_%d-%H_%M_%S'),
		os.getpid()
	)

	# given on command line ?
	for option in sys.argv[1:]:
		if option.startswith(u'--log-file='):
			(opt_name, value) = option.split(u'=')
			(dir_name, file_name) = os.path.split(value)
			if dir_name == u'':
				dir_name = u'.'
			if file_name == '':
				file_name = default_logfile_name
			_logfile_name = os.path.abspath(os.path.expanduser(os.path.join(dir_name, file_name)))
			return True

	# else store it in ~/.gnumed/logs/def_log_basename/default_logfile_name
	dir_name = os.path.expanduser(os.path.join('~', '.gnumed', 'logs', def_log_basename))
	try:
		os.makedirs(dir_name)
	except OSError as e:
		if (e.errno == 17) and not os.path.isdir(dir_name):
			raise

	_logfile_name = os.path.join(dir_name, default_logfile_name)

	return True

#===============================================================
# main
#---------------------------------------------------------------
__setup_logging()

if __name__ == '__main__':

	#-----------------------------------------------------------
	def test():
		logger = logging.getLogger('gmLog2.test')
		logger.error("I expected to see %s::test()" % __file__)
		try:
			int(None)
		except:
			logger.exception(u'unhandled exception')
			log_stack_trace()
		flush()
	#-----------------------------------------------------------
	if len(sys.argv) > 1 and sys.argv[1] == u'test':
		test()
#===============================================================
