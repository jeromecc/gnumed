#===========================================================================
# THIS NEEDS TO BE IMPORTED FIRST IN YOUR MODULES !
#===========================================================================

"""GNUmed client internationalization/localization.

All i18n/l10n issues should be handled through this modules.

Theory of operation:

By importing this module a textdomain providing translations is
automatically installed. The translating method gettext.gettext()
is installed into the global (!) namespace as _(). Your own modules thus
need not do _anything_ (not even import gmI18N) to have _() available
to them for translating strings. You need to make sure, however, that
gmI18N is imported in your main module before any of the modules using
it. In order to resolve circular references involving modules that
absolutely _have_ to be imported before this module you can explicitely
import gmI18N into them at the very beginning.

The text domain (i.e. the name of the message catalog file) is derived
from the name of the main executing script unless explicitely given on
the command line like this:
 --text-domain=<your text domain>

This module searches for message catalog files in 3 main locations:
 - in standard POSIX places (/usr/share/locale/ ...)
 - below $GNUMED_DIR/locale/
 - below (one level above binary directory)/locale/

For DOS/Windows I don't know of standard places so only the last
option will work unless you have CygWin installed. I don't know a
thing about classic Mac behaviour. New Mac's are POSIX, of course.

The language you want to see is derived from the following locale
related environment variables (in this order):
 - LANGUAGE
 - LC_ALL
 - LC_MESSAGES
 - LANG

@license: GPL (details at http://www.gnu.org)
@copyright: author
"""
#---------------------------------------------------------------------------
# $Source: /home/ncq/Projekte/cvs2git/vcs-mirror/gnumed/gnumed/client/python-common/Attic/gmI18N.py,v $
__version__ = "$Revision: 1.25 $"
__author__ = "H. Herb <hherb@gnumed.net>, I. Haywood <i.haywood@ugrad.unimelb.edu.au>, K. Hilbert <Karsten.Hilbert@gmx.net>"
############################################################################

import gettext, sys, os.path, string, os
import gmLog, gmCLI
_log = gmLog.gmDefLog

system_locale = None
system_locale_level = {}
#---------------------------------------------------------------------------
def install_domain():
	"""Install a text domain suitable for the main script.
	"""
	text_domain = ""
	# text domain given on command line ?
	if gmCLI.has_arg('--text-domain'):
		text_domain = gmCLI.arg['--text-domain']
	# else get text domain from name of script 
	else:
		text_domain = os.path.splitext(os.path.basename(sys.argv[0]))[0]

	_log.Log(gmLog.lInfo, 'text domain is "%s"' % text_domain)

	# explicitely probe user locale settings
	global system_locale
	global system_locale_level
	env_key = 'LANGUAGE'
	if os.environ.has_key(env_key):
		system_locale = os.environ[env_key]
		_log.Log(gmLog.lData, '$(%s) is set to "%s"' % (env_key, system_locale))
	else:
		_log.Log(gmLog.lData, '$(%s) is not set' % (env_key))

	env_key = 'LC_ALL'
	if os.environ.has_key(env_key):
		system_locale = os.environ[env_key]
		_log.Log(gmLog.lData, '$(%s) is set to "%s"' % (env_key, system_locale))
	else:
		_log.Log(gmLog.lData, '$(%s) is not set' % (env_key))

	env_key = 'LC_MESSAGES'
	if os.environ.has_key(env_key):
		system_locale = os.environ[env_key]
		_log.Log(gmLog.lData, '$(%s) is set to "%s"' % (env_key, system_locale))
	else:
		_log.Log(gmLog.lData, '$(%s) is not set' % (env_key))

	env_key = 'LANG'
	if os.environ.has_key(env_key):
		system_locale = os.environ[env_key]
		_log.Log(gmLog.lData, '$(%s) is set to "%s"' % (env_key, system_locale))
	else:
		_log.Log(gmLog.lData, '$(%s) is not set' % (env_key))

	# generate system locale levels
	system_locale_level['full'] = system_locale
	# trim '@<variant>' part
	# FIXME: may be a different deliminator on other systems
	system_locale_level['country'] = system_locale.split('@', 1)[0]
	# trim '_<COUNTRY>@<variant>' part
	system_locale_level['language'] = system_locale.split('_', 1)[0]

	# search for message catalog
	_log.Log(gmLog.lData, 'Searching message catalog file for system locale [%s].' % system_locale)

	# now we can install this text domain
	# 1) try standard places first
	if os.name == 'posix':
		_log.Log(gmLog.lData, 'Looking in standard POSIX locations (see Python Manual).')
		try:
			gettext.install(text_domain)
			_log.Log(gmLog.lData, 'Found message catalog.')
			return 1
		except IOError:
			# most likely we didn't have a .mo file
			_log.LogException('Cannot install textdomain from standard POSIX locations.', sys.exc_info(), fatal=0)
	else:
		_log.Log(gmLog.lData, 'No use looking in standard POSIX locations - not a POSIX system.')

	# 2) $(<script-name>_DIR)/
	env_key = "%s_DIR" % string.upper(os.path.splitext(os.path.basename(sys.argv[0]))[0])
	_log.Log(gmLog.lData, 'Looking behind environment variable $(%s).' % env_key)
	if os.environ.has_key(env_key):
		loc_dir = os.path.abspath(os.path.join(os.environ[env_key], "locale"))
		_log.Log(gmLog.lData, '$(%s) = "%s" -> [%s]' % (env_key, os.environ[env_key], loc_dir))
		if os.path.exists(loc_dir):
			try:
				gettext.install(text_domain, loc_dir)
				_log.Log(gmLog.lData, 'Found message catalog.')
				return 1
			except IOError:
				# most likely we didn't have a .mo file
				_log.LogException('Cannot install textdomain from custom location [%s].' % (loc_dir), sys.exc_info())
		else:
			_log.Log(gmLog.lWarn, 'Custom location [%s] does not exist. Cannot install textdomain from there.' % (loc_dir))
	else:
		_log.Log(gmLog.lInfo, "Environment variable %s is not set." % env_key)

	# 3) one level below path to binary
	#    last resort for inferior operating systems such as DOS/Windows
	#    strip one directory level
	#    this is a rather neat trick :-)
	loc_dir = os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), '..', 'locale'))
	_log.Log(gmLog.lData, 'Looking in application level directory [%s].' % loc_dir)
	#    sanity check (paranoia rulez)
	if os.path.exists(loc_dir):
		try:
			gettext.install(text_domain, loc_dir)
			_log.Log(gmLog.lData, 'Found message catalog.')
			return 1
		except IOError:
			# most likely we didn't have a .mo file
			_log.LogException('Cannot install textdomain from one level above binary location [%s].' % (loc_dir), sys.exc_info(), 0)
	else:
		_log.Log(gmLog.lWarn, "The application level locale directory [%s] does not exist. Cannot install textdomain from there." % (loc_dir))

	# 4) in path to binary
	loc_dir = os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), 'locale' ))
	_log.Log(gmLog.lData, 'Looking in application level directory [%s].' % loc_dir)
	#    sanity check (paranoia rulez)
	if os.path.exists(loc_dir):
		try:
			gettext.install(text_domain, loc_dir)
			_log.Log(gmLog.lData, 'Found message catalog.')
			return 1
		except IOError:
			# most likely we didn't have a .mo file
			_log.LogException('Cannot install textdomain from within path to binary [%s].' % (loc_dir), sys.exc_info(), 0)
	else:
		_log.Log(gmLog.lWarn, "The application level locale directory [%s] does not exist. Cannot install textdomain from there." % (loc_dir))

	# 5) install a dummy translation class
	_log.Log(gmLog.lWarn, "Giving up and falling back to NullTranslations() class in despair.")
	# this shouldn't fail
	dummy = gettext.NullTranslations()
	dummy.install()
#---------------------------------------------------------------------------
# Main
#---------------------------------------------------------------------------
if __name__ == "__main__":
	_log.SetAllLogLevels(gmLog.lData)
	print "======================================================================"
	print __doc__
	print "======================================================================"

_log.Log(gmLog.lData, __version__)

install_domain()

if __name__ == "__main__":
	print "system locale: [%s]" % system_locale
	print "levels:", system_locale_level

# we can now safely set up a bunch of variables

# gmTimeFormat is used to define a standard way of
# displaying a date as a string,
# this is marked for translation by _(),
# this way this variable can be used as a crude
# means of date formatting localization
gmTimeformat = _("%Y-%m-%d  %H:%M:%S")

_log.Log(gmLog.lData, 'local time format set to "%s"' % gmTimeformat)

#=====================================================================
# $Log: gmI18N.py,v $
# Revision 1.25  2003-03-24 16:52:27  ncq
# - calculate system locale levels at startup
#
# Revision 1.24  2003/02/05 21:27:05  ncq
# - more aptly names a variable
#
# Revision 1.23  2003/02/01 02:42:46  ncq
# - log -> _log to prevent namespace pollution on import
#
# Revision 1.22  2003/02/01 02:39:53  ncq
# - get and remember user's locale
#
# Revision 1.21  2002/12/09 23:39:50  ncq
# - only try standard message catalog locations on true POSIX systems
#   as windows will choke on it
#
# Revision 1.20  2002/11/18 09:41:25  ncq
# - removed magic #! interpreter incantation line to make Debian happy
#
# Revision 1.19  2002/11/17 20:09:10  ncq
# - always display __doc__ when called standalone
#
# Revision 1.18  2002/09/26 13:16:52  ncq
# - log version
#
# Revision 1.17  2002/09/23 02:23:16  ncq
# - comment on why it fails on some version of Windows
#
# Revision 1.16  2002/09/22 18:38:58  ncq
# - added big comment on gmTimeFormat
#
# Revision 1.15  2002/09/10 07:52:29  ncq
# - increased log level of gmTimeFormat
#
# Revision 1.14  2002/09/08 15:57:42  ncq
# - added log cvs keyword
#
