"""gmRegetMixin - GnuMed data change callback mixin.

Widget code can mix in this class as a base class and
thus gain the infrastructure to update it's display
when data changes. If the widget is not visible it will
only schedule refetching data from the business layer.
If it *is* visible it will immediately fetch and redisplay.

You must call cRegetOnPaintMixin.__init__() in your own
__init__() after calling __init__() on the appropriate
wxWidgets class your widget inherits from.

You must then make sure to call _schedule_data_reget()
whenever you learn of backend data changes. This will
in most cases happen after you receive a gmDispatcher
signal indicating a change in the backend.

@copyright: authors
"""
#===========================================================================
# $Source: /home/ncq/Projekte/cvs2git/vcs-mirror/gnumed/gnumed/client/wxpython/gmRegetMixin.py,v $
# $Id: gmRegetMixin.py,v 1.1 2004-07-28 15:27:31 ncq Exp $
__version__ = "$Revision: 1.1 $"
__author__ = "K.Hilbert <Karsten.Hilbert@gmx.net>"
__license__ = 'GPL (details at http://www.gnu.org)'


from wxPython import wx

#===========================================================================
class cRegetOnPaintMixin:
	"""Mixin to add redisplay_data-on-EVT_PAINT aspect.

	Any code mixing in this class will gain the mechanism
	to reget data on wxPaint events. The code must be an
	instance of a wxWindow and must implement a
	_populate_with_data() method. It must also call
	_schedule_data_reget() at appropriate times.
	"""
	def __init__(self):
		self._data_stale = True
		try:
			wx.EVT_PAINT(self, self._on_paint_event)
		except:
			_log.Log(gmLog.lErr, 'you likely need to call "cRegetOnPaintMixin.__init__()" later in your __init__()')
			raise
	#-----------------------------------------------------
	def _on_paint_event(self, event):
		"""Repopulate UI if data is stale."""
		if self._data_stale:
			print "%s._on_paint_event(): stale data, repopulating" % self.__class__.__name__
			self.__populate_with_data()
		event.Skip()
	#-----------------------------------------------------
	def __populate_with_data(self):
		if self._populate_with_data():
			self._data_stale = False
		else:
			self._data_stale = True
	#-----------------------------------------------------
	def _populate_with_data(self):
		"""Override in includers !"""
		print "%s._populate_with_data() not implemented" % self.__class__.__name__
		_log.Log(gmLog.lErr, 'not implemented for %s' % self.__class__.__name__)
		return False
	#-----------------------------------------------------
	def _schedule_data_reget(self):
		"""Flag data as stale and redisplay if needed.

		- if not visible schedule reget only
		- if visible redisplay immediately
		"""
		if self.GetUpdateRegion().IsEmpty() == 1:
			print "%s._schedule_data_reget(): scheduling update" % self.__class__.__name__
			self._data_stale = True
		else:
			print "%s._schedule_data_reget(): updating now" % self.__class__.__name__
			self.__populate_with_data()
			self.Refresh()

#===========================================================================
# main
#---------------------------------------------------------------------------
if __name__ == '__main__':
	print "no unit test available"

#===========================================================================
# $Log: gmRegetMixin.py,v $
# Revision 1.1  2004-07-28 15:27:31  ncq
# - first checkin, used in gmVaccWidget
#
#
