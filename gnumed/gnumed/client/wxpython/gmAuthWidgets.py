"""GNUmed authentication widgets.

This module contains widgets and GUI
functions for authenticating users.
"""
#================================================================
# $Source: /home/ncq/Projekte/cvs2git/vcs-mirror/gnumed/gnumed/client/wxpython/gmAuthWidgets.py,v $
# $Id: gmAuthWidgets.py,v 1.2 2007-12-04 16:14:52 ncq Exp $
__version__ = "$Revision: 1.2 $"
__author__ = "karsten.hilbert@gmx.net, H.Herb, H.Berger, R.Terry"
__license__ = "GPL (details at http://www.gnu.org)"


# stdlib
import sys, os.path, cPickle, zlib


# 3rd party
import wx


# GNUmed
if __name__ == '__main__':
	sys.path.insert(0, '../../')
from Gnumed.pycommon import gmGuiBroker, gmLoginInfo, gmLog, gmI18N, gmPG2, gmBackendListener, gmCfg, gmTools, gmCLI
from Gnumed.business import gmSurgery
from Gnumed.wxpython import gmGuiHelpers


_log = gmLog.gmDefLog
_log.Log(gmLog.lInfo, __version__)
_cfg = gmCfg.gmDefCfgFile

try:
	_('do-not-translate-but-make-epydoc-happy')
except NameError:
	_ = lambda x:x

msg_generic = _("""
GNUmed database version mismatch.

This database version cannot be used with this client:

 version detected: %s
 version needed: %s

Currently connected to database:

 host: %s
 database: %s
 user: %s
""")

msg_insanity = _("""
There is a serious problem with the database settings:

%s
""")

msg_fail = _("""
You must connect to a different database in order
to use the GNUmed client. You may have to contact
your administrator for help.""")

msg_override = _("""
The client will, however, continue to start up because
you are running a development/test version of GNUmed.

There may be schema related errors. Please report and/or
fix them. Do not rely on this database to work properly
in all cases !""")

curr_db = 'gnumed_v8'
#================================================================
# convenience functions
#----------------------------------------------------------------
def connect_to_database(max_attempts=3, expected_version=None, require_version=True):
	"""Display the login dialog and try to log into the backend.

	- up to max_attempts times
	- returns True/False
	"""
	# force programmer to set a valid expected_version
	expected_hash = gmPG2.known_schema_hashes[expected_version]

	attempt = 0

	dlg = cLoginDialog(None, -1)
	dlg.Centre(wx.BOTH)

	while attempt < max_attempts:

		connected = False

		dlg.ShowModal()
		login = dlg.panel.GetLoginInfo()
		if login is None:
			_log.Log(gmLog.lInfo, "user cancelled login dialog")
			break

		# try getting a connection to verify the DSN works
		dsn = gmPG2.make_psycopg2_dsn (
			database = login.database,
			host = login.host,
			port = login.port,
			user = login.user,
			password = login.password
		)
		try:
			conn = gmPG2.get_raw_connection(dsn = dsn, verbose = True)
			connected = True
		except gmPG2.cAuthenticationError, e:
			attempt += 1
			_log.LogException(u"login attempt %s/%s failed" % (attempt, max_attempts), verbose=0)
			if attempt < max_attempts:
				gmGuiHelpers.gm_show_error (_(
						"Unable to connect to database:\n\n"
						"%s\n\n"
						"Please retry or cancel !"
					) % e,
					_('Connecting to backend'),
					gmLog.lErr
				)
			_log.LogException(u"login attempt %s/%s failed, may retry" % (attempt, max_attempts), verbose=0)
			continue
		except StandardError:
			_log.LogException(u"login attempt %s/%s failed, useless to retry" % (attempt+1, max_attempts), verbose=0)
			break

		# connect was successful:
		gmPG2.set_default_login(login = login)
		gmPG2.set_default_client_encoding(encoding = dlg.panel.backend_profile.encoding)

		compatible = gmPG2.database_schema_compatible(version = expected_version)
		if compatible or not require_version:
			dlg.panel.save_state()

		if not compatible:
			connected_db_version = gmPG2.get_schema_version()
			msg = msg_generic % (connected_db_version, expected_version, login.host, login.database, login.user)
			if require_version:
				gmGuiHelpers.gm_show_error(msg + msg_fail, _('Verifying database version'), None)
				continue
			gmGuiHelpers.gm_show_info(msg + msg_override, _('Verifying database version'), None)

		sanity = gmPG2.sanity_check_database_settings()
		if sanity is not True:
			gmGuiHelpers.gm_show_error((msg_insanity % sanity) + msg_fail, _('Verifying database settings'), None)
			continue

		listener = gmBackendListener.gmBackendListener(conn=conn)
		break

	dlg.Destroy()

	return connected
#================================================================
def get_dbowner_connection(procedure=None, dbo_password=None):
	if procedure is None:
		procedure = _('<restricted procedure>')

	# 1) get password for gm-dbo
	if dbo_password is None:
		pwd_gm_dbo = wx.GetPasswordFromUser (
			message = _("""
 [%s]

This is a restricted procedure. We need the
password for the GNUmed database owner.

Please enter the password for <gm-dbo>:""") % procedure,
			caption = procedure
		)
		if pwd_gm_dbo == '':
			return None
	else:
		pwd_gm_dbo = dbo_password

	# 2) connect as gm-dbo
	login = gmPG2.get_default_login()
	dsn = gmPG2.make_psycopg2_dsn(database=login.database, host=login.host, port=login.port, user='gm-dbo', password=pwd_gm_dbo)
	try:
		conn = gmPG2.get_connection(dsn=dsn, readonly=False, verbose=True, pooled=False)
	except:
		_log.LogException('cannot connect')
		gmGuiHelpers.gm_show_error (
			aMessage = _('Cannot connect as the GNUmed database owner <gm-dbo>.'),
			aTitle = procedure,
			aLogLevel = None
		)
		return None

	return conn
#================================================================
class cBackendProfile:
	pass
#================================================================
class cLoginDialog(wx.Dialog):
	"""cLoginDialog - window holding cLoginPanel"""

	icon_serpent='x\xdae\x8f\xb1\x0e\x83 \x10\x86w\x9f\xe2\x92\x1blb\xf2\x07\x96\xeaH:0\xd6\
\xc1\x85\xd5\x98N5\xa5\xef?\xf5N\xd0\x8a\xdcA\xc2\xf7qw\x84\xdb\xfa\xb5\xcd\
\xd4\xda;\xc9\x1a\xc8\xb6\xcd<\xb5\xa0\x85\x1e\xeb\xbc\xbc7b!\xf6\xdeHl\x1c\
\x94\x073\xec<*\xf7\xbe\xf7\x99\x9d\xb21~\xe7.\xf5\x1f\x1c\xd3\xbdVlL\xc2\
\xcf\xf8ye\xd0\x00\x90\x0etH \x84\x80B\xaa\x8a\x88\x85\xc4(U\x9d$\xfeR;\xc5J\
\xa6\x01\xbbt9\xceR\xc8\x81e_$\x98\xb9\x9c\xa9\x8d,y\xa9t\xc8\xcf\x152\xe0x\
\xe9$\xf5\x07\x95\x0cD\x95t:\xb1\x92\xae\x9cI\xa8~\x84\x1f\xe0\xa3ec'

	def __init__(self, parent, id, title=_("Welcome to the")):
		wx.Dialog.__init__(self, parent, id, title)
		self.panel = cLoginPanel(self, -1, isDialog=1)
		self.Fit () # needed for Windoze.
		self.Centre()

		# set window icon
		icon_bmp_data = wx.BitmapFromXPMData(cPickle.loads(zlib.decompress(self.icon_serpent)))
		icon = wx.EmptyIcon()
		icon.CopyFromBitmap(icon_bmp_data)
		self.SetIcon(icon)
#================================================================
class cLoginPanel(wx.Panel):
	"""GUI panel class that interactively gets Postgres login parameters.

		It features combo boxes which "remember" any number of
		previously entered settings.
	"""
	def __init__(self, parent, id,
		pos = wx.DefaultPosition,
		size = wx.DefaultSize,
		style = wx.TAB_TRAVERSAL,
		isDialog = 0
		):
		"""Create login panel.

		isDialog:	if this panel is the main panel of a dialog, the panel will
					resize the dialog automatically to display everything neatly
					if isDialog is set to True
		"""
		wx.Panel.__init__(self, parent, id, pos, size, style)
		self.parent = parent

		self.user_preferences_file = None
		paths = gmTools.gmPaths(app_name = 'gnumed', wx=wx)
		if gmCLI.has_arg('--conf-file'):
			fnames = [gmCLI.arg['--conf-file']]
		else:
			fnames = [
				os.path.join(paths.user_config_dir, 'gnumed.conf'),
				os.path.join(paths.working_dir, 'gnumed.conf')
			]
		for fname in fnames:
			try:
				open(fname, 'r+b')
				self.user_preferences_file = fname
				break
			except IOError:
				continue

		self.gb = gmGuiBroker.GuiBroker()

		#True if dialog was cancelled by user 
		#if the dialog is closed manually, login should be cancelled
		self.cancelled = True

		# True if this panel is displayed within a dialog (will resize the dialog automatically then)
		self.isDialog = isDialog

		self.topsizer = wx.BoxSizer(wx.VERTICAL)

		# find bitmap
		bitmap = os.path.join(paths.system_app_data_dir, 'bitmaps', 'gnumedlogo.png')
		try:
			png = wx.Image(bitmap, wx.BITMAP_TYPE_PNG).ConvertToBitmap()
			bmp = wx.StaticBitmap(self, -1, png, wx.Point(10, 10), wx.Size(png.GetWidth(), png.GetHeight()))
			self.topsizer.Add (
				bmp,
				proportion = 0,
				flag = wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL,
				border = 10
			)
		except:
			self.topsizer.Add (
				wx.StaticText (
					self,
					-1,
					label = _("Cannot find image") + bitmap,
					style = wx.ALIGN_CENTRE
				),
				proportion = 0,
				flag = wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL,
				border = 10
			)

#		if self.gb.has_key('main.slave_mode') and self.gb['main.slave_mode']:
		if gmCLI.has_arg('--slave'):
			paramsbox_caption = _("Slave Login - %s" % gmSurgery.gmCurrentPractice().active_workplace)
		else:
			paramsbox_caption = _("Login - %s" % gmSurgery.gmCurrentPractice().active_workplace)

		# FIXME: why doesn't this align in the centre ?
		self.paramsbox = wx.StaticBox( self, -1, paramsbox_caption, style = wx.ALIGN_CENTRE_HORIZONTAL)
		self.paramsboxsizer = wx.StaticBoxSizer( self.paramsbox, wx.VERTICAL )
		self.paramsbox.SetForegroundColour(wx.Colour(35, 35, 142))
		self.paramsbox.SetFont(wx.Font(
			pointSize = 12,
			family = wx.SWISS,
			style = wx.NORMAL,
			weight = wx.BOLD,
			underline = False
		))
		self.pboxgrid = wx.FlexGridSizer(5, 2, 5, 5)
		self.pboxgrid.AddGrowableCol(1)

		# PROFILE COMBO
		label = wx.StaticText( self, -1, _('Backend'), wx.DefaultPosition, wx.DefaultSize, 0)
		label.SetForegroundColour(wx.Colour(35, 35, 142))
		self.pboxgrid.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
		self.__backend_profiles = self.__get_backend_profiles()
		self._CBOX_profile = wx.ComboBox (
			self,
			-1,
			self.__backend_profiles.keys()[0],
			wx.DefaultPosition,
			size = wx.Size(150,-1),
			choices = self.__backend_profiles.keys(),
			style = wx.CB_READONLY
		)
		self.pboxgrid.Add (self._CBOX_profile, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

		# USER NAME COMBO
		label = wx.StaticText( self, -1, _("Username"), wx.DefaultPosition, wx.DefaultSize, 0 )
		label.SetForegroundColour(wx.Colour(35, 35, 142))
		self.pboxgrid.Add(label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		self.__previously_used_accounts = self.__get_previously_used_accounts()
		self._CBOX_user = wx.ComboBox (
			self,
			-1,
			self.__previously_used_accounts[0],
			wx.DefaultPosition,
			wx.Size(150,-1),
			self.__previously_used_accounts,
			wx.CB_DROPDOWN
		)
		self.pboxgrid.Add( self._CBOX_user, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		#PASSWORD TEXT ENTRY
		label = wx.StaticText( self, -1, _("Password"), wx.DefaultPosition, wx.DefaultSize, 0 )
		label.SetForegroundColour(wx.Colour(35, 35, 142))
		self.pboxgrid.Add( label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		self.pwdentry = wx.TextCtrl( self, 1, '', wx.DefaultPosition, wx.Size(80,-1), wx.TE_PASSWORD )
		# set focus on password entry
		self.pwdentry.SetFocus()
		self.pboxgrid.Add( self.pwdentry, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

		# --debug checkbox
		label = wx.StaticText(self, -1, _('Options'), wx.DefaultPosition, wx.DefaultSize, 0)
		label.SetForegroundColour(wx.Colour(35, 35, 142))
		self.pboxgrid.Add(label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
		self._CHBOX_debug = wx.CheckBox(self, -1, _('debug mode'))
		self._CHBOX_debug.SetToolTipString(_('Check this to run GNUmed client in debugging mode.'))
		self.pboxgrid.Add(self._CHBOX_debug, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

		# --slave checkbox
		label = wx.StaticText(self, -1, '', wx.DefaultPosition, wx.DefaultSize, 0)
		label.SetForegroundColour(wx.Colour(35, 35, 142))
		self.pboxgrid.Add(label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
		self._CHBOX_slave = wx.CheckBox(self, -1, _('enable remote control'))
		self._CHBOX_slave.SetToolTipString(_('Check this to run GNUmed client in slave mode for remote control.'))
		self.pboxgrid.Add(self._CHBOX_slave, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

		#----------------------------------------------------------------------
		#new button code inserted rterry 06Sept02
		#button order re-arraged to make it consistant with usual dialog format
		#in most operating systems ie  btns ok and cancel are standard and 
		#in that order
		#ie Order is now help, ok and cancel
		#The order of creation is the tab order
		#login-ok button automatically is the default when tabbing (or <enter>)
		#from password
		#this eliminates the heavy border when you use the default 
		#?is the default word needed for any other reason?
		#----------------------------------------------------------------------
		self.button_gridsizer = wx.GridSizer(1,3,0,0)
		#---------------------
		#3:create login ok button
		#---------------------
		ID_BUTTON_LOGIN = wx.NewId()
		button_login_ok = wx.Button(self, ID_BUTTON_LOGIN, _("&Ok"), wx.DefaultPosition, wx.DefaultSize, 0 )
		button_login_ok.SetToolTip(wx.ToolTip(_("Proceed with login.")) )
		button_login_ok.SetDefault()

		#---------------------
		#3:create cancel button
		#---------------------
		ID_BUTTON_CANCEL = wx.NewId()
		button_cancel = wx.Button(self, ID_BUTTON_CANCEL, _("&Cancel"), wx.DefaultPosition, wx.DefaultSize, 0 )
		button_cancel.SetToolTip(wx.ToolTip(_("Cancel Login.")) )
		#---------------------
		#2:create Help button
		#---------------------
		ID_BUTTON_HELP = wx.NewId()
		button_help = wx.Button(self, ID_BUTTON_HELP, _("&Help"), wx.DefaultPosition, wx.DefaultSize, 0 )
		button_help.SetToolTip(wx.ToolTip(_("Help for login screen")))
		#----------------------------
		#Add buttons to the gridsizer
		#----------------------------
		self.button_gridsizer.Add (button_help,0,wx.EXPAND|wx.ALL,5)
		self.button_gridsizer.Add (button_login_ok,0,wx.EXPAND|wx.ALL,5)
		self.button_gridsizer.Add (button_cancel,0,wx.EXPAND|wx.ALL,5)
		
		self.paramsboxsizer.Add(self.pboxgrid, 1, wx.GROW|wx.ALL, 10)
		self.topsizer.Add(self.paramsboxsizer, 1, wx.GROW|wx.ALL, 10)
		self.topsizer.Add( self.button_gridsizer, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		self.__load_state()

		self.SetAutoLayout(True)
		self.SetSizer( self.topsizer)
		self.topsizer.Fit( self )
		if self.isDialog:
			self.topsizer.SetSizeHints(parent)

		wx.EVT_BUTTON(self, ID_BUTTON_HELP, self.OnHelp)
		wx.EVT_BUTTON(self, ID_BUTTON_LOGIN, self.__on_login_button_pressed)
		wx.EVT_BUTTON(self, ID_BUTTON_CANCEL, self.OnCancel)

	#----------------------------------------------------------
	# internal helper methods
	#----------------------------------------------------------
	def __get_previously_used_accounts(self):

		accounts = []

		if gmCLI.has_arg('--conf-file'):
			fnames = [gmCLI.arg['--conf-file']]
		else:
			paths = gmTools.gmPaths(app_name = 'gnumed', wx = wx)
			fnames = [
				os.path.join(paths.user_config_dir, 'gnumed.conf'),
				os.path.join(paths.working_dir, 'gnumed.conf')
			]

		for fname in fnames:
			try:
				cfg_file = gmCfg.cCfgFile (
					aFile = fname,
					flags = gmCfg.cfg_IGNORE_CMD_LINE
				)
			except IOError:
				continue

			accounts = gmTools.coalesce (
				cfg_file.get('backend', 'logins'),
				[]
			)

			if len(accounts) > 0:
				return accounts

		if len(accounts) == 0:
			return ['any-doc']

		return accounts
	#----------------------------------------------------
	def __get_backend_profiles(self):
		"""Get server profiles from the configuration files.

		1) from system-wide file
		2) from user file

		Profiles in the user file which have the same name
		as a profile in the system file will override the
		system file.
		"""
		profiles = {}

		if gmCLI.has_arg('--conf-file'):
			fnames = [gmCLI.arg['--conf-file']]
		else:
			paths = gmTools.gmPaths()
			fnames = [
				os.path.join(paths.system_config_dir, 'gnumed-client.conf'),
				os.path.join(paths.user_config_dir, 'gnumed.conf'),
				os.path.join(paths.working_dir, 'gnumed.conf')
			]

		for fname in fnames:
			try:
				cfg_file = gmCfg.cCfgFile (
					aFile = fname,
					flags = gmCfg.cfg_IGNORE_CMD_LINE
				)
			except IOError:
				continue

			profile_names = gmTools.coalesce (
				cfg_file.get('backend', 'profiles'),
				[]
			)

			for profile_name in profile_names:
				profile = cBackendProfile()
				profile.name = profile_name
				profile_section = 'profile %s' % profile_name
				profile.host = gmTools.coalesce(cfg_file.get(profile_section, 'host'), '').strip()
				try:
					profile.port = int (gmTools.coalesce (
						cfg_file.get(profile_section, 'port'),
						5432
					))
					if profile.port < 1024:
						raise ValueError('refusing to use priviledged port (< 1024)')
				except ValueError:
					_log.LogException('invalid port definition: [%s], skipping profile [%s] in [%s]' % (cfg_file.get(profile_section, 'port'), profile_name, fname))
					continue
				profile.database = gmTools.coalesce(cfg_file.get(profile_section, 'database'), '').strip()
				if profile.database == '':
					_log.Log(gmLog.lErr, 'database name not specified, skipping profile [%s] in [%s]' % (profile_name, fname))
					continue
				profile.encoding = gmTools.coalesce (
					cfg_file.get(profile_section, 'encoding'),
					'UTF8'
				)
				profiles[profile_name] = profile

		if len(profiles) == 0:
			host = 'salaam.homeunix.com'
			label = 'public GNUmed database (%s@%s)' % (curr_db, host)
			profiles[label] = cBackendProfile()
			profiles[label].name = label
			profiles[label].host = host
			profiles[label].port = 5432
			profiles[label].database = curr_db
			profiles[label].encoding = 'UTF8'
			
		return profiles
	#----------------------------------------------------------
	def __load_state(self):

		prefs = gmCfg.cCfgFile (
			aFile = self.user_preferences_file,
			flags = gmCfg.cfg_IGNORE_CMD_LINE
		)
		self._CBOX_user.SetValue (
			gmTools.coalesce (
				prefs.get('preferences', 'login'),
				self.__previously_used_accounts[0]
			)
		)

		self._CBOX_profile.SetValue (
			gmTools.coalesce (
				prefs.get('preferences', 'profile'),
				self.__backend_profiles[self.__backend_profiles.keys()[0]].name
			)
		)

		self._CHBOX_debug.SetValue(gmCLI.has_arg('--debug'))
		self._CHBOX_slave.SetValue(gmCLI.has_arg('--slave'))
	#----------------------------------------------------
	def save_state(self):
		"""Save parameter settings to standard configuration file"""

		prefs = gmCfg.cCfgFile (
			aFile = self.user_preferences_file,
			flags = gmCfg.cfg_IGNORE_CMD_LINE
		)
		prefs.set('preferences', 'login', self._CBOX_user.GetValue())
		prefs.set('preferences', 'profile', self._CBOX_profile.GetValue())
		prefs.store()
	#############################################################################
	# Retrieve current settings from user interface widgets
	#############################################################################
	def GetLoginInfo(self):
		"""convenience function for compatibility with gmLoginInfo.LoginInfo"""
		if not self.cancelled:
			# FIXME: do not assume conf file is latin1 !
			profile = self.__backend_profiles[self._CBOX_profile.GetValue().encode('latin1').strip()]
			login = gmLoginInfo.LoginInfo (
				user = self._CBOX_user.GetValue(),
				password = self.pwdentry.GetValue(),
				host = profile.host,
				database = profile.database,
				port = profile.port
			)
			return login

		return None
	#----------------------------
	# event handlers
	#----------------------------
	def OnHelp(self, event):
		tmp = _cfg.get('workplace', 'help desk')
		if tmp is None:
			print _("You need to set the option [workplace] -> <help desk> in the config file !")
			tmp = "http://www.gnumed.org"

		wx.MessageBox(_(
"""GnuMed main login screen

USER:
 name of the GnuMed user
PASSWORD
 password for this user

button OK:
 proceed with login
button OPTIONS:
 set advanced options
button CANCEL:
 abort login and quit GnuMed client
button HELP:
 this help screen

For assistance on using GnuMed please contact:
 %s""") % tmp)

	#----------------------------
	def __on_login_button_pressed(self, event):

		if self._CHBOX_debug.GetValue():
			_log.SetAllLogLevels(gmLog.lData)
			gmCLI._cli_args['--debug'] = True
			_log.Log(gmLog.lInfo, 'debug mode enabled')
		else:
			_log.Log(gmLog.lInfo, 'debug mode disabled')
			gmCLI._cli_args['--debug'] = False
			del gmCLI._cli_args['--debug']
			if gmCLI.has_arg("--quiet"):
				_log.SetAllLogLevels(gmLog.lErr)
			else:
				_log.SetAllLogLevels(gmLog.lInfo)

		if self._CHBOX_slave.GetValue():	
			_log.Log(gmLog.lInfo, 'slave mode enabled')
			self.gb['main.slave_mode'] = True
		else:
			_log.Log(gmLog.lInfo, 'slave mode disabled')
			self.gb['main.slave_mode'] = False

		self.backend_profile = self.__backend_profiles[self._CBOX_profile.GetValue().encode('latin1').strip()]
#		self.user = self._CBOX_user.GetValue().strip()
#		self.password = self.GetPassword()
		self.cancelled = False
		self.parent.Close()
	#----------------------------
	def OnCancel(self, event):
		self.cancelled = True
		self.parent.Close()

#================================================================
# main
#----------------------------------------------------------------
if __name__ == "__main__":
	_log.SetAllLogLevels(gmLog.lData)
	gmI18N.activate_locale()
	gmI18N.install_domain(domain='gnumed')
	#-----------------------------------------------
	#-----------------------------------------------
	def test():
		app = wx.PyWidgetTester(size = (300,400))
		#show the login panel in a main window
#		app.SetWidget(cLoginPanel, -1)
		#and pop the login dialog up modally
		dlg = cLoginDialog(None, -1) #, png_bitmap = 'bitmaps/gnumedlogo.png')
		dlg.ShowModal()
		#demonstration how to access the login dialog values
		lp = dlg.panel.GetLoginInfo()
		if lp is None:
			wx.MessageBox(_("Dialog was cancelled by user"))
		else:
			wx.MessageBox(_("You tried to log in as [%s] with password [%s].\nHost:%s, DB: %s, Port: %s") % (lp.GetUser(),lp.GetPassword(),lp.GetHost(),lp.GetDatabase(),lp.GetPort()))
		dlg.Destroy()
#		app.MainLoop()
	#-----------------------------------------------
	if len(sys.argv) > 1 and sys.argv[1] == 'test':
		print "no regression tests yet"

#================================================================
# $Log: gmAuthWidgets.py,v $
# Revision 1.2  2007-12-04 16:14:52  ncq
# - get_dbowner_connection()
#
# Revision 1.1  2007/12/04 16:03:43  ncq
# - merger of gmLogin and gmLoginDialog
#
#

#----------------------------------------------------------------
# old logs
#----------------------------------------------------------------
# Log: gmLogin.py,v
# Revision 1.37  2007/12/04 15:23:14  ncq
# - reorder connect_to_database()
# - check server settings sanity
#
# Revision 1.36  2007/11/09 14:40:33  ncq
# - gmPG2 dumps schema by itself now on hash mismatch
#
# Revision 1.35  2007/10/23 21:24:39  ncq
# - start backend listener on login
#
# Revision 1.34  2007/06/11 20:25:18  ncq
# - better logging
#
# Revision 1.33  2007/04/27 13:29:31  ncq
# - log schema dump on version conflict
#
# Revision 1.32  2007/03/18 14:10:07  ncq
# - do show schema mismatch warning even if --override-schema-check
#
# Revision 1.31  2007/03/08 11:41:55  ncq
# - set default client encoding from here
# - save state when --override-schema-check == True, too
#
# Revision 1.30  2006/12/15 15:27:01  ncq
# - move database schema version check here
#
# Revision 1.29  2006/10/25 07:46:44  ncq
# - Format() -> strftime() since datetime.datetime does not have .Format()
#
# Revision 1.28  2006/10/25 07:21:57  ncq
# - no more gmPG
#
# Revision 1.27  2006/10/24 13:25:19  ncq
# - Login() -> connect_to_database()
# - make gmPG2 main connection provider, piggyback gmPG onto it for now
#
# Revision 1.26  2006/10/08 11:04:45  ncq
# - simplify wx import
# - piggyback gmPG2 until gmPG is pruned
#
# Revision 1.25  2006/01/03 12:12:03  ncq
# - make epydoc happy re _()
#
# Revision 1.24  2005/09/27 20:44:59  ncq
# - wx.wx* -> wx.*
#
# Revision 1.23  2005/09/26 18:01:51  ncq
# - use proper way to import wx26 vs wx2.4
# - note: THIS WILL BREAK RUNNING THE CLIENT IN SOME PLACES
# - time for fixup
#
# Revision 1.22  2004/09/13 08:54:49  ncq
# - cleanup
# - use gmGuiHelpers
#
# Revision 1.21  2004/07/18 20:30:54  ncq
# - wxPython.true/false -> Python.True/False as Python tells us to do
#
# Revision 1.20  2004/06/20 16:01:05  ncq
# - please epydoc more carefully
#
# Revision 1.19  2004/06/20 06:49:21  ihaywood
# changes required due to Epydoc's OCD
#
# Revision 1.18  2004/03/04 19:47:06  ncq
# - switch to package based import: from Gnumed.foo import bar
#
# Revision 1.17  2003/11/17 10:56:38  sjtan
#
# synced and commiting.
#
# Revision 1.1  2003/10/23 06:02:39  sjtan
#
# manual edit areas modelled after r.terry's specs.
#
# Revision 1.16  2003/06/26 21:40:29  ncq
# - fatal->verbose
#
# Revision 1.15  2003/02/07 14:28:05  ncq
# - cleanup, cvs keywords
#
# @change log:
#	29.10.2001 hherb first draft, untested
#
#----------------------------------------------------------------
# Log: gmLoginDialog.py,v
# Revision 1.90  2007/10/22 12:38:32  ncq
# - default db change
#
# Revision 1.89  2007/10/07 12:32:41  ncq
# - workplace property now on gmSurgery.gmCurrentPractice() borg
#
# Revision 1.88  2007/09/20 19:07:38  ncq
# - port 5432 on salaam again
#
# Revision 1.87  2007/09/04 23:30:28  ncq
# - support --slave and slave mode checkbox
#
# Revision 1.86  2007/08/07 21:42:40  ncq
# - cPaths -> gmPaths
#
# Revision 1.85  2007/06/14 21:55:49  ncq
# - try to fix wx2.8 problem with size
#
# Revision 1.84  2007/06/11 20:25:55  ncq
# - bump database version
#
# Revision 1.83  2007/06/10 10:17:54  ncq
# - fix when no --debug
#
# Revision 1.82  2007/05/22 13:35:11  ncq
# - default port 5433 now on salaam
#
# Revision 1.81  2007/05/08 11:16:10  ncq
# - set debugging flag based on user checkbox selection
#
# Revision 1.80  2007/05/07 12:33:31  ncq
# - use gmTools.cPaths
# - support debug mode checkbox
#
# Revision 1.79  2007/04/11 20:45:01  ncq
# - no more 'resource dir'
#
# Revision 1.78  2007/04/02 15:15:19  ncq
# - v5 -> v6
#
# Revision 1.77  2007/03/08 16:20:50  ncq
# - need to reference proper cfg file
#
# Revision 1.76  2007/03/08 11:46:23  ncq
# - restructured
#   - cleanup
#   - no more cLoginParamChoices
#   - no more loginparams keyword
#   - properly set user preferences file
#   - backend profile now can contain per-profile default encoding
#   - support system-wide profile pre-defs in /etc/gnumed/gnumed-client.conf
#
# Revision 1.75  2007/02/17 14:13:11  ncq
# - gmPerson.gmCurrentProvider().workplace now property
#
# Revision 1.74  2007/01/30 17:40:22  ncq
# - cleanup, get rid of wxMAC IFDEF
# - use user preferences file for storing login preferences
#
# Revision 1.73  2006/12/21 16:54:32  ncq
# - inage handlers already inited
#
# Revision 1.72  2006/12/15 15:27:28  ncq
# - cleanup
#
# Revision 1.71  2006/10/25 07:21:57  ncq
# - no more gmPG
#
# Revision 1.70  2006/09/01 14:45:03  ncq
# - assume conf file is latin1 ... FIX later !
#
# Revision 1.69  2006/07/30 17:50:03  ncq
# - properly load bitmaps
#
# Revision 1.68  2006/05/15 07:05:07  ncq
# - must import gmPerson now
#
# Revision 1.67  2006/05/14 21:44:22  ncq
# - add get_workplace() to gmPerson.gmCurrentProvider and make use thereof
# - remove use of gmWhoAmI.py
#
# Revision 1.66  2006/05/12 12:18:11  ncq
# - whoami -> whereami cleanup
# - use gmCurrentProvider()
#
# Revision 1.65  2005/09/28 21:27:30  ncq
# - a lot of wx2.6-ification
#
# Revision 1.64  2005/09/27 20:44:59  ncq
# - wx.wx* -> wx.*
#
# Revision 1.63  2005/09/26 18:01:51  ncq
# - use proper way to import wx26 vs wx2.4
# - note: THIS WILL BREAK RUNNING THE CLIENT IN SOME PLACES
# - time for fixup
#
# Revision 1.62  2005/09/24 09:17:29  ncq
# - some wx2.6 compatibility fixes
#
# Revision 1.61  2005/08/15 15:15:25  ncq
# - improved error message
#
# Revision 1.60  2005/08/14 15:22:04  ncq
# - need to import gmNull
#
# Revision 1.59  2005/08/14 14:31:53  ncq
# - better handling of missing/malformed config file
#
# Revision 1.58  2005/06/10 16:09:36  shilbert
# foo.AddSizer()-> foo.Add() such that wx2.5 works
#
# Revision 1.57  2005/03/06 14:54:19  ncq
# - szr.AddWindow() -> Add() such that wx2.5 works
# - 'demographic record' -> get_identity()
#
# Revision 1.56  2005/01/22 22:26:06  ncq
# - a bunch of cleanups
# - i18n
#
# Revision 1.55  2005/01/20 21:37:40  hinnef
# - added error dialog when no profiles specified
#
# Revision 1.54  2004/11/24 21:16:33  hinnef
# - fixed issue with missing profiles when writing to empty gnumed.conf.
# This lead to a crash when trying to load the invalid gnumed.conf.
# Now we just ignore this and fall back to defaults.
#
# Revision 1.53  2004/11/22 19:32:36  hinnef
# new login dialog with profiles
#
# Revision 1.52  2004/09/13 08:57:33  ncq
# - losts of cleanup
# - opt/tty not used in DSN anymore
# - --slave -> gb['main.slave_mode']
#
# Revision 1.51  2004/07/18 20:30:54  ncq
# - wxPython.true/false -> Python.True/False as Python tells us to do
#
# Revision 1.50  2004/07/18 18:44:27  ncq
# - use Python True, not wxPython true
#
# Revision 1.49  2004/06/20 16:01:05  ncq
# - please epydoc more carefully
#
# Revision 1.48  2004/06/20 06:49:21  ihaywood
# changes required due to Epydoc's OCD
#
# Revision 1.47  2004/05/28 13:06:41  ncq
# - improve faceName/Mac OSX fix
#
# Revision 1.46  2004/05/28 09:09:34  shilbert
# - remove faceName option from wx.Font on wxMac or else no go
#
# Revision 1.45  2004/05/26 20:35:23  ncq
# - don't inherit from LoginDialog in OptionWindow, it barks on MacOSX
#
# Revision 1.44  2004/04/24 12:46:35  ncq
# - logininfo() needs host=
#
# Revision 1.43  2004/03/04 19:47:06  ncq
# - switch to package based import: from Gnumed.foo import bar
#
# Revision 1.42  2003/12/29 16:58:52  uid66147
# - use whoami
#
# Revision 1.41  2003/11/17 10:56:38  sjtan
#
# synced and commiting.
#
# Revision 1.1  2003/10/23 06:02:39  sjtan
#
# manual edit areas modelled after r.terry's specs.
#
# Revision 1.40  2003/06/17 19:27:44  ncq
# - cleanup
# - only use cfg file login params if not empty list
#
# Revision 1.39  2003/05/17 17:30:36  ncq
# - just some cleanup
#
# Revision 1.38  2003/05/12 09:01:45  ncq
# - 1) type(tmp) is types.ListType implies tmp != None
# - 2) check for ListType, not StringType
#
# Revision 1.37  2003/05/10 18:48:09  hinnef
# - added stricter type checks when reading from cfg-file
#
# Revision 1.36  2003/04/05 00:37:46  ncq
# - renamed a few variables to reflect reality
#
# Revision 1.35  2003/03/31 00:18:34  ncq
# - or so I thought
#
# Revision 1.34  2003/03/31 00:17:43  ncq
# - started cleanup/clarification
# - made saving of values work again
#
# Revision 1.33  2003/02/09 18:55:47  ncq
# - make comment less angry
#
# Revision 1.32  2003/02/08 00:32:30  ncq
# - fixed failure to detect config file
#
# Revision 1.31  2003/02/08 00:15:17  ncq
# - cvs metadata keywords
#
# Revision 1.30  2003/02/07 21:06:02  sjtan
#
# refactored edit_area_gen_handler to handler_generator and handler_gen_editarea. New handler for gmSelectPerson
#
# Revision 1.29  2003/02/02 07:38:29  michaelb
# set serpent as window icon - login dialog & option dialog
#
# Revision 1.28  2003/01/16 09:22:28  ncq
# - changed default workplace name to "__default__" to play better with the database
#
# Revision 1.27  2003/01/07 10:22:52  ncq
# - fixed font definition
#
# Revision 1.26  2002/09/21 14:49:22  ncq
# - cleanup related to gmi18n
#
# Revision 1.25  2002/09/12 23:19:27  ncq
# - cleanup in preparation of cleansing
#
# Revision 1.24  2002/09/10 08:54:35  ncq
# - remember workplace name once loaded
#
# Revision 1.23  2002/09/09 01:05:16  ncq
# - fixed i18n glitch
# - added note that _("") is invalid !!
#
# @change log:
#	10.10.2001 hherb initial implementation, untested
#	24.10.2001 hherb comments added
#	24.10.2001 hherb LoginDialog class added,
#	24.10.2001 hherb persistent changes across multiple processes enabled
#	25.10.2001 hherb more flexible configuration options, more commenting
#	07.02.2002 hherb saved parameters now showing corectly in combo boxes
#   	05.09.2002 hberger moved options to own dialog
#       06.09.2002 rterry simplified gui
#                  -duplication and visual clutter removed
#                   removed duplication of information in display
#                   login gone from title bar , occurs once only now
#                   visually highlighted in dark blue
#                   login button title now 'ok' to conform to usual defaults of 
#                   ok, cancel in most operating systems
#                   reference to help removed (have help button for that)
#                   date removed - can't see use of this in login - clutters
#   	06.09.2002 hberger removed old code, fixed "login on close window" bug
#       07.09.2002 rterry removed duplicated heading in advanced login options