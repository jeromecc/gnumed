# -*- coding: utf-8 -*-
#======================================================================
# GNUmed patient overview plugin
# ------------------------------
#
# @copyright: author
#======================================================================
__author__ = "Carlos Moro, Karsten Hilbert"
__license__ = 'GPL v2 or later (details at http://www.gnu.org)'

import logging


if __name__ == '__main__':
	# stdlib
	import sys
	sys.path.insert(0, '../../../')

	from Gnumed.pycommon import gmI18N
	gmI18N.activate_locale()
	gmI18N.install_domain()

# GNUmed
from Gnumed.wxpython import gmPlugin, gmPatOverviewWidgets
from Gnumed.wxpython import gmAccessPermissionWidgets


_log = logging.getLogger('gm.ui')
#======================================================================
class gmPatientOverviewPlugin(gmPlugin.cNotebookPlugin):

	tab_name = _('Overview')
	required_minimum_role = 'full clinical access'

	@gmAccessPermissionWidgets.verify_minimum_required_role (
		required_minimum_role,
		activity = _('loading plugin <%s>') % tab_name,
		return_value_on_failure = False,
		fail_silently = False
	)
	def register(self):
		gmPlugin.cNotebookPlugin.register(self)
	#-------------------------------------------------
	def name (self):
		return gmPatientOverviewPlugin.tab_name

	def GetWidget (self, parent):
		self._widget = gmPatOverviewWidgets.cPatientOverviewPnl(parent, -1)
		return self._widget

	def MenuInfo (self):
		return ('emr', _('&Overview'))

	def can_receive_focus(self):
		# need patient
		if not self._verify_patient_avail():
			return None
		return True
#======================================================================
# main
#----------------------------------------------------------------------
if __name__ == "__main__":

	# 3rd party
	import wx

	# GNUmed
	from Gnumed.business import gmPersonSearch
	from Gnumed.wxpython import gmSOAPWidgets

	_log.info("starting Notebooked progress notes input plugin...")

	try:
		# obtain patient
		patient = gmPersonSearch.ask_for_patient()
		if patient is None:
			print "None patient. Exiting gracefully..."
			sys.exit(0)
		gmPatSearchWidgets.set_active_patient(patient=patient)

		# display standalone multisash progress notes input
		application = wx.wx.PyWidgetTester(size = (800,600))
		multisash_notes = gmSOAPWidgets.cNotebookedProgressNoteInputPanel(application.frame, -1)

		application.frame.Show(True)
		application.MainLoop()

		# clean up
		if patient is not None:
			try:
				patient.cleanup()
			except:
				print "error cleaning up patient"
	except Exception:
		_log.exception("unhandled exception caught !")
		# but re-raise them
		raise

	_log.info("closing Notebooked progress notes input plugin...")
#======================================================================
