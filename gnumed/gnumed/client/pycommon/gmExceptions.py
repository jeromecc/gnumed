############################################################################
#
# gmExceptions - classes for exceptions gnumed modules may throw
# --------------------------------------------------------------------------
#
# @author: Dr. Horst Herb
# @copyright: author
# @license: GPL v2 or later (details at http://www.gnu.org)
# @dependencies: nil
# @change log:
#	07.02.2002 hherb first draft, untested
############################################################################

class AccessDenied(Exception):
	def __init__(self, msg, source=None, code=None, details=None):
		self.errmsg = msg
		self.source = source
		self.code = code
		self.details = details
	#----------------------------------
	def __str__(self):
		txt = self.errmsg
		if self.source is not None:
			txt += u'\nSource: %s' % self.source
		if self.code is not None:
			txt += u'\nCode: %s' % self.code
		if self.details is not None:
			txt += u'\n%s' % self.details
		return txt
	#----------------------------------
	def __repr__(self):
		txt = self.errmsg
		if self.source is not None:
			txt += u'\nSource: %s' % source
		if self.code is not None:
			txt += u'\nCode: %s' % self.code
		if self.details is not None:
			txt += u'\n%s' % self.details
		return txt

#------------------------------------------------------------
class DatabaseObjectInUseError(Exception):
	def __init__(self, msg):
		self.errmsg = msg

	def __str__(self):
		return self.errmsg


class ConnectionError(Exception):
	#raised whenever the database backend connection fails
	def __init__(self, errmsg):
		self.errmsg=errmsg

	def __str__(self):
		return self.errmsg

class ConfigError(Exception):
	#raised whenever a configuration error occurs
	def __init__(self, errmsg):
		self.errmsg=errmsg

	def __str__(self):
		return self.errmsg



class NoGuiError(Exception):
	def __init__(self, errmsg):
		self.errmsg=errmsg

	def __str__(self):
		return self.errmsg


class PureVirtualFunction(Exception):
	#raised whenever the database backend connection fails
	def __init__(self, errmsg=None):
		if errmsg is not None:
			self.errmsg=errmsg
		else:
			self.errmsg="Attempt to call a pure virtual function!"

	def __str__(self):
		return self.errmsg

#------------------------------------------------------------
# constructor errors
class ConstructorError(Exception):
	"""Raised when a constructor fails."""
	def __init__(self, errmsg = None):
		if errmsg is None:
			self.errmsg = "%s.__init__() failed" % self.__class__.__name__
		else:
			self.errmsg = errmsg
	def __str__(self):
		return self.errmsg

# business DB-object exceptions
class NoSuchBusinessObjectError(ConstructorError):
	"""Raised when a business db-object can not be found."""
	def __init__(self, errmsg = None):
		if errmsg is None:
			self.errmsg = "no such business DB-object found"
		else:
			self.errmsg = errmsg
	def __str__(self):
		return self.errmsg

#------------------------------------------------------------
class InvalidInputError(Exception):
	"""Raised by business layers when an attempt is made to input
	invalid data"""
	def __init__(self, errmsg = None):
		if errmsg is None:
			self.errmsg = "%s.__init__() failed" % self.__class__.__name__
		else:
			self.errmsg = errmsg

	def __str__(self):
		return self.errmsg

#=====================================================================
