"""GNUmed EMR structure editors

	This module contains widgets to create and edit EMR structural
	elements (issues, enconters, episodes).

	This is based on initial work and ideas by Syan <kittylitter@swiftdsl.com.au>
	and Karsten <Karsten.Hilbert@gmx.net>.
"""
#================================================================
__author__ = "cfmoro1976@yahoo.es, karsten.hilbert@gmx.net"
__license__ = "GPL v2 or later"

# stdlib
import sys
import time
import logging
import datetime as pydt


# 3rd party
import wx


# GNUmed
if __name__ == '__main__':
	sys.path.insert(0, '../../')

from Gnumed.pycommon import gmI18N
from Gnumed.pycommon import gmDateTime

if __name__ == '__main__':
	gmI18N.activate_locale()
	gmI18N.install_domain()
	gmDateTime.init()

from Gnumed.pycommon import gmExceptions
from Gnumed.pycommon import gmCfg
from Gnumed.pycommon import gmTools
from Gnumed.pycommon import gmDispatcher
from Gnumed.pycommon import gmMatchProvider

from Gnumed.business import gmEMRStructItems
from Gnumed.business import gmPraxis
from Gnumed.business import gmPerson

from Gnumed.wxpython import gmPhraseWheel
from Gnumed.wxpython import gmGuiHelpers
from Gnumed.wxpython import gmListWidgets
from Gnumed.wxpython import gmEditArea
from Gnumed.wxpython import gmOrganizationWidgets


_log = logging.getLogger('gm.ui')

#================================================================
# EMR access helper functions
#----------------------------------------------------------------
def emr_access_spinner(time2spin=0):
	"""Spin time in seconds but let wx go on."""
	if time2spin == 0:
		return
	sleep_time = 0.1			# 100ms
	total_rounds = int(time2spin / sleep_time)
	if total_rounds < 1:
		wx.Yield()
		time.sleep(sleep_time)
		return
	rounds = 0
	while rounds < total_rounds:
		wx.Yield()
		time.sleep(sleep_time)
		rounds += 1

#================================================================
# performed procedure related widgets/functions
#----------------------------------------------------------------
def manage_performed_procedures(parent=None):

	pat = gmPerson.gmCurrentPatient()
	emr = pat.get_emr()

	if parent is None:
		parent = wx.GetApp().GetTopWindow()

	#-----------------------------------------
	def get_tooltip(procedure=None):
		if procedure is None:
			return None
		return procedure.format (
			left_margin = 1,
			include_episode = False,
			include_codes = False,
			include_address = True,
			include_comm = True
		)

	#-----------------------------------------
	def edit(procedure=None):
		return edit_procedure(parent = parent, procedure = procedure)

	#-----------------------------------------
	def delete(procedure=None):
		if gmEMRStructItems.delete_performed_procedure(procedure = procedure['pk_procedure']):
			return True

		gmDispatcher.send (
			signal = u'statustext',
			msg = _('Cannot delete performed procedure.'),
			beep = True
		)
		return False

	#-----------------------------------------
	def refresh(lctrl):
		procs = emr.get_performed_procedures()
		items = [
			[
				u'%s%s' % (
					p['clin_when'].strftime('%Y-%m-%d'),
					gmTools.bool2subst (
						p['is_ongoing'],
						_(' (ongoing)'),
						gmTools.coalesce (
							initial = p['clin_end'],
							instead = u'',
							template_initial = u' - %s',
							function_initial = ('strftime', u'%Y-%m-%d')
						)
					)
				),
				p['performed_procedure'],
				u'%s @ %s' % (p['unit'], p['organization']),
				p['episode']
			] for p in procs
		]
		lctrl.set_string_items(items = items)
		lctrl.set_data(data = procs)

	#-----------------------------------------
	gmListWidgets.get_choices_from_list (
		parent = parent,
		msg = _('\nSelect the procedure you want to edit !\n'),
		caption = _('Editing performed procedures ...'),
		columns = [_('When'), _('Procedure'), _('Where'), _('Episode')],
		single_selection = True,
		edit_callback = edit,
		new_callback = edit,
		delete_callback = delete,
		refresh_callback = refresh,
		list_tooltip_callback = get_tooltip
	)

#----------------------------------------------------------------
def edit_procedure(parent=None, procedure=None):
	ea = cProcedureEAPnl(parent = parent, id = -1)
	ea.data = procedure
	ea.mode = gmTools.coalesce(procedure, 'new', 'edit')
	dlg = gmEditArea.cGenericEditAreaDlg2(parent = parent, id = -1, edit_area = ea, single_entry = True)
	dlg.SetTitle(gmTools.coalesce(procedure, _('Adding a procedure'), _('Editing a procedure')))
	if dlg.ShowModal() == wx.ID_OK:
		dlg.Destroy()
		return True
	dlg.Destroy()
	return False

#----------------------------------------------------------------
from Gnumed.wxGladeWidgets import wxgProcedureEAPnl

class cProcedureEAPnl(wxgProcedureEAPnl.wxgProcedureEAPnl, gmEditArea.cGenericEditAreaMixin):

	def __init__(self, *args, **kwargs):
		wxgProcedureEAPnl.wxgProcedureEAPnl.__init__(self, *args, **kwargs)
		gmEditArea.cGenericEditAreaMixin.__init__(self)

		self.mode = 'new'
		self.data = None

		self.__init_ui()
	#----------------------------------------------------------------
	def __init_ui(self):
		self._PRW_hospital_stay.add_callback_on_lose_focus(callback = self._on_hospital_stay_lost_focus)
		self._PRW_hospital_stay.set_context(context = 'pat', val = gmPerson.gmCurrentPatient().ID)
		self._PRW_location.add_callback_on_lose_focus(callback = self._on_location_lost_focus)
		self._DPRW_date.add_callback_on_lose_focus(callback = self._on_start_lost_focus)
		self._DPRW_end.add_callback_on_lose_focus(callback = self._on_end_lost_focus)

		# procedure
		mp = gmMatchProvider.cMatchProvider_SQL2 (
			queries = [
u"""
select distinct on (narrative) narrative, narrative
from clin.procedure
where narrative %(fragment_condition)s
order by narrative
limit 25
"""			]
		)
		mp.setThresholds(2, 4, 6)
		self._PRW_procedure.matcher = mp
	#----------------------------------------------------------------
	def _on_hospital_stay_lost_focus(self):
		stay = self._PRW_hospital_stay.GetData()
		if stay is None:
			self._PRW_hospital_stay.SetText()
			self._PRW_location.Enable(True)
			self._PRW_episode.Enable(True)
			self._LBL_hospital_details.SetLabel(u'')
		else:
			self._PRW_location.SetText()
			self._PRW_location.Enable(False)
			self._PRW_episode.SetText()
			self._PRW_episode.Enable(False)
			self._LBL_hospital_details.SetLabel(gmEMRStructItems.cHospitalStay(aPK_obj = stay).format())
	#----------------------------------------------------------------
	def _on_location_lost_focus(self):
		loc = self._PRW_location.GetData()
		if loc is None:
			self._PRW_hospital_stay.Enable(True)
			self._PRW_episode.Enable(False)
		else:
			self._PRW_hospital_stay.SetText()
			self._PRW_hospital_stay.Enable(False)
			self._PRW_episode.Enable(True)
	#----------------------------------------------------------------
	def _on_start_lost_focus(self):
		if not self._DPRW_date.is_valid_timestamp():
			return
		end = self._DPRW_end.GetData()
		if end is None:
			return
		end = end.get_pydt()
		start = self._DPRW_date.GetData().get_pydt()
		if start < end:
			return
		self._DPRW_date.display_as_valid(False)
	#----------------------------------------------------------------
	def _on_end_lost_focus(self):
		end = self._DPRW_end.GetData()
		if end is None:
			self._CHBOX_ongoing.Enable(True)
			self._DPRW_end.display_as_valid(True)
		else:
			self._CHBOX_ongoing.Enable(False)
			end = end.get_pydt()
			now = gmDateTime.pydt_now_here()
			if end > now:
				self._CHBOX_ongoing.SetValue(True)
			else:
				self._CHBOX_ongoing.SetValue(False)
			start = self._DPRW_date.GetData()
			if start is None:
				self._DPRW_end.display_as_valid(True)
			else:
				start = start.get_pydt()
				if end > start:
					self._DPRW_end.display_as_valid(True)
				else:
					self._DPRW_end.display_as_valid(False)
	#----------------------------------------------------------------
	# generic Edit Area mixin API
	#----------------------------------------------------------------
	def _valid_for_save(self):

		has_errors = False

		if not self._DPRW_date.is_valid_timestamp():
			self._DPRW_date.display_as_valid(False)
			has_errors = True
		else:
			self._DPRW_date.display_as_valid(True)

		start = self._DPRW_date.GetData()
		end = self._DPRW_end.GetData()
		self._DPRW_end.display_as_valid(True)
		if end is not None:
			end = end.get_pydt()
			if start is not None:
				start = start.get_pydt()
				if end < start:
					has_errors = True
					self._DPRW_end.display_as_valid(False)
			if self._CHBOX_ongoing.IsChecked():
				now = gmDateTime.pydt_now_here()
				if end < now:
					has_errors = True
					self._DPRW_end.display_as_valid(False)

		if self._PRW_hospital_stay.GetData() is None:
			if self._PRW_episode.GetValue().strip() == u'':
				self._PRW_episode.display_as_valid(False)
				has_errors = True
			else:
				self._PRW_episode.display_as_valid(True)
		else:
			self._PRW_episode.display_as_valid(True)

		if (self._PRW_procedure.GetValue() is None) or (self._PRW_procedure.GetValue().strip() == u''):
			self._PRW_procedure.display_as_valid(False)
			has_errors = True
		else:
			self._PRW_procedure.display_as_valid(True)

		invalid_location = (
			(self._PRW_hospital_stay.GetData() is None) and (self._PRW_location.GetData() is None)
				or
			(self._PRW_hospital_stay.GetData() is not None) and (self._PRW_location.GetData() is not None)
		)
		if invalid_location:
			self._PRW_hospital_stay.display_as_valid(False)
			self._PRW_location.display_as_valid(False)
			has_errors = True
		else:
			self._PRW_hospital_stay.display_as_valid(True)
			self._PRW_location.display_as_valid(True)

		gmDispatcher.send(signal = 'statustext', msg = _('Cannot save procedure.'), beep = True)

		return (has_errors is False)
	#----------------------------------------------------------------
	def _save_as_new(self):

		pat = gmPerson.gmCurrentPatient()
		emr = pat.get_emr()

		stay = self._PRW_hospital_stay.GetData()
		if stay is None:
			epi = self._PRW_episode.GetData(can_create = True)
		else:
			epi = gmEMRStructItems.cHospitalStay(aPK_obj = stay)['pk_episode']

		proc = emr.add_performed_procedure (
			episode = epi,
			location = self._PRW_location.GetData(),
			hospital_stay = stay,
			procedure = self._PRW_procedure.GetValue().strip()
		)

		proc['clin_when'] = self._DPRW_date.GetData().get_pydt()
		if self._DPRW_end.GetData() is None:
			proc['clin_end'] = None
		else:
			proc['clin_end'] = self._DPRW_end.GetData().get_pydt()
		proc['is_ongoing'] = self._CHBOX_ongoing.IsChecked()
		proc.save()

		proc.generic_codes = [ c['data'] for c in self._PRW_codes.GetData() ]

		self.data = proc

		return True
	#----------------------------------------------------------------
	def _save_as_update(self):
		self.data['clin_when'] = self._DPRW_date.GetData().get_pydt()
		self.data['is_ongoing'] = self._CHBOX_ongoing.IsChecked()
		self.data['pk_org_unit'] = self._PRW_location.GetData()
		self.data['pk_hospital_stay'] = self._PRW_hospital_stay.GetData()
		self.data['performed_procedure'] = self._PRW_procedure.GetValue().strip()
		if self._DPRW_end.GetData() is None:
			self.data['clin_end'] = None
		else:
			self.data['clin_end'] = self._DPRW_end.GetData().get_pydt()
		if self.data['pk_hospital_stay'] is None:
			self.data['pk_episode'] = self._PRW_episode.GetData()
		else:
			self.data['pk_episode'] = gmEMRStructItems.cHospitalStay(aPK_obj = self._PRW_hospital_stay.GetData())['pk_episode']
		self.data.save()

		self.data.generic_codes = [ c['data'] for c in self._PRW_codes.GetData() ]

		return True
	#----------------------------------------------------------------
	def _refresh_as_new(self):
		self._DPRW_date.SetText()
		self._DPRW_end.SetText()
		self._CHBOX_ongoing.SetValue(False)
		self._CHBOX_ongoing.Enable(True)
		self._PRW_hospital_stay.SetText()
		self._LBL_hospital_details.SetLabel(u'')
		self._PRW_location.SetText()
		self._PRW_episode.SetText()
		self._PRW_procedure.SetText()
		self._PRW_codes.SetText()

		self._PRW_procedure.SetFocus()
	#----------------------------------------------------------------
	def _refresh_from_existing(self):
		self._DPRW_date.SetData(data = self.data['clin_when'])
		if self.data['clin_end'] is None:
			self._DPRW_end.SetText()
			self._CHBOX_ongoing.Enable(True)
			self._CHBOX_ongoing.SetValue(self.data['is_ongoing'])
		else:
			self._DPRW_end.SetData(data = self.data['clin_end'])
			self._CHBOX_ongoing.Enable(False)
			now = gmDateTime.pydt_now_here()
			if self.data['clin_end'] > now:
				self._CHBOX_ongoing.SetValue(True)
			else:
				self._CHBOX_ongoing.SetValue(False)
		self._PRW_episode.SetText(value = self.data['episode'], data = self.data['pk_episode'])
		self._PRW_procedure.SetText(value = self.data['performed_procedure'], data = self.data['performed_procedure'])

		if self.data['pk_hospital_stay'] is None:
			self._PRW_hospital_stay.SetText()
			self._PRW_hospital_stay.Enable(False)
			self._LBL_hospital_details.SetLabel(u'')
			self._PRW_location.SetText(value = u'%s @ %s' % (self.data['unit'], self.data['organization']), data = self.data['pk_org_unit'])
			self._PRW_location.Enable(True)
			self._PRW_episode.Enable(True)
		else:
			self._PRW_hospital_stay.SetText(value = u'%s @ %s' % (self.data['unit'], self.data['organization']), data = self.data['pk_hospital_stay'])
			self._PRW_hospital_stay.Enable(True)
			self._LBL_hospital_details.SetLabel(gmEMRStructItems.cHospitalStay(aPK_obj = self.data['pk_hospital_stay']).format())
			self._PRW_location.SetText()
			self._PRW_location.Enable(False)
			self._PRW_episode.Enable(False)

		val, data = self._PRW_codes.generic_linked_codes2item_dict(self.data.generic_codes)
		self._PRW_codes.SetText(val, data)

		self._PRW_procedure.SetFocus()
	#----------------------------------------------------------------
	def _refresh_as_new_from_existing(self):
		self._refresh_as_new()

		self._PRW_episode.SetText(value = self.data['episode'], data = self.data['pk_episode'])

		if self.data['pk_hospital_stay'] is None:
			self._PRW_hospital_stay.SetText()
			self._PRW_hospital_stay.Enable(False)
			self._LBL_hospital_details.SetLabel(u'')
			self._PRW_location.SetText(value = u'%s @ %s' % (self.data['unit'], self.data['organization']), data = self.data['pk_org_unit'])
			self._PRW_location.Enable(True)
			self._PRW_episode.Enable(True)
		else:
			self._PRW_hospital_stay.SetText(value = u'%s @ %s' % (self.data['unit'], self.data['organization']), data = self.data['pk_hospital_stay'])
			self._PRW_hospital_stay.Enable(True)
			self._LBL_hospital_details.SetLabel(gmEMRStructItems.cHospitalStay(aPK_obj = self.data['pk_hospital_stay']).format())
			self._PRW_location.SetText()
			self._PRW_location.Enable(False)
			self._PRW_episode.Enable(False)

		self._PRW_procedure.SetFocus()
	#----------------------------------------------------------------
	# event handlers
	#----------------------------------------------------------------
	def _on_add_hospital_stay_button_pressed(self, evt):
		# FIXME: this would benefit from setting the created stay
		edit_hospital_stay(parent = self.GetParent())
		evt.Skip()
	#----------------------------------------------------------------
	def _on_add_location_button_pressed(self, event):
		gmOrganizationWidgets.manage_orgs(parent = self)	#self.GetParent())
		event.Skip()
	#----------------------------------------------------------------
	def _on_ongoing_checkbox_checked(self, event):
		if self._CHBOX_ongoing.IsChecked():
			end = self._DPRW_end.GetData()
			if end is None:
				self._DPRW_end.display_as_valid(True)
			else:
				end = end.get_pydt()
				now = gmDateTime.pydt_now_here()
				if end > now:
					self._DPRW_end.display_as_valid(True)
				else:
					self._DPRW_end.display_as_valid(False)
		else:
			self._DPRW_end.is_valid_timestamp()
		event.Skip()

#================================================================
# hospitalizations related widgets/functions
#----------------------------------------------------------------
def manage_hospital_stays(parent=None):

	pat = gmPerson.gmCurrentPatient()
	emr = pat.get_emr()

	if parent is None:
		parent = wx.GetApp().GetTopWindow()
	#-----------------------------------------
	def get_tooltip(stay=None):
		if stay is None:
			return None
		return stay.format (
			include_procedures = True,
			include_docs = True
		)
	#-----------------------------------------
	def edit(stay=None):
		return edit_hospital_stay(parent = parent, hospital_stay = stay)
	#-----------------------------------------
	def delete(stay=None):
		if gmEMRStructItems.delete_hospital_stay(stay = stay['pk_hospital_stay']):
			return True
		gmDispatcher.send (
			signal = u'statustext',
			msg = _('Cannot delete hospitalization.'),
			beep = True
		)
		return False
	#-----------------------------------------
	def refresh(lctrl):
		stays = emr.get_hospital_stays()
		items = [
			[
				s['admission'].strftime('%Y-%m-%d'),
				gmTools.coalesce(s['discharge'], u'', function_initial = ('strftime', '%Y-%m-%d')),
				s['episode'],
				u'%s @ %s' % (s['ward'], s['hospital'])
			] for s in stays
		]
		lctrl.set_string_items(items = items)
		lctrl.set_data(data = stays)
	#-----------------------------------------
	gmListWidgets.get_choices_from_list (
		parent = parent,
		msg = _("The patient's hospitalizations:\n"),
		caption = _('Editing hospitalizations ...'),
		columns = [_('Admission'), _('Discharge'), _('Reason'), _('Hospital')],
		single_selection = True,
		edit_callback = edit,
		new_callback = edit,
		delete_callback = delete,
		refresh_callback = refresh,
		list_tooltip_callback = get_tooltip
	)

#----------------------------------------------------------------
def edit_hospital_stay(parent=None, hospital_stay=None):
	ea = cHospitalStayEditAreaPnl(parent = parent, id = -1)
	ea.data = hospital_stay
	ea.mode = gmTools.coalesce(hospital_stay, 'new', 'edit')
	dlg = gmEditArea.cGenericEditAreaDlg2(parent = parent, id = -1, edit_area = ea, single_entry = True)
	dlg.SetTitle(gmTools.coalesce(hospital_stay, _('Adding a hospitalization'), _('Editing a hospitalization')))
	if dlg.ShowModal() == wx.ID_OK:
		dlg.Destroy()
		return True
	dlg.Destroy()
	return False

#----------------------------------------------------------------
class cHospitalWardPhraseWheel(gmPhraseWheel.cPhraseWheel):
	"""Phrasewheel to allow selection of a hospitalization."""
	def __init__(self, *args, **kwargs):

		gmPhraseWheel.cPhraseWheel.__init__ (self, *args, **kwargs)

		query = u"""
		SELECT data, list_label, field_label FROM (
			SELECT DISTINCT ON (data) * FROM ((

				-- already-used org_units
				SELECT
					pk_org_unit
						AS data,
					ward || ' @ ' || hospital
						AS list_label,
					ward || ' @ ' || hospital
						AS field_label,
					1
						AS rank
				FROM
					clin.v_hospital_stays
				WHERE
					ward %(fragment_condition)s
						OR
					hospital %(fragment_condition)s

				) UNION ALL (
				-- wards
				SELECT
					pk_org_unit
						AS data,
					unit || ' (' || l10n_unit_category || ') @ ' || organization
						AS list_label,
					unit || ' @ ' || organization
						AS field_label,
					2
						AS rank
				FROM
					dem.v_org_units
				WHERE
					unit_category = 'Ward'
						AND
					unit %(fragment_condition)s
						AND
					NOT EXISTS (
						SELECT 1 FROM clin.v_hospital_stays WHERE clin.v_hospital_stays.pk_org_unit = dem.v_org_units.pk_org_unit
					)

				) UNION ALL (
				-- hospital units
				SELECT
					pk_org_unit
						AS data,
					unit || coalesce(' (' || l10n_unit_category || ')', '') || ' @ ' || organization || ' (' || l10n_organization_category || ')'
						AS list_label,
					unit || ' @ ' || organization
						AS field_label,
					3
						AS rank
				FROM
					dem.v_org_units
				WHERE
					unit_category <> 'Ward'
						AND
					organization_category = 'Hospital'
						AND
					unit %(fragment_condition)s
						AND
					NOT EXISTS (
						SELECT 1 FROM clin.v_hospital_stays WHERE clin.v_hospital_stays.pk_org_unit = dem.v_org_units.pk_org_unit
					)

				) UNION ALL (
				-- any other units
				SELECT
					pk_org_unit
						AS data,
					unit || coalesce(' (' || l10n_unit_category || ')', '') || ' @ ' || organization || ' (' || l10n_organization_category || ')'
						AS list_label,
					unit || ' @ ' || organization
						AS field_label,
					3
						AS rank
				FROM
					dem.v_org_units
				WHERE
					unit_category <> 'Ward'
						AND
					organization_category <> 'Hospital'
						AND
					unit %(fragment_condition)s
						AND
					NOT EXISTS (
						SELECT 1 FROM clin.v_hospital_stays WHERE clin.v_hospital_stays.pk_org_unit = dem.v_org_units.pk_org_unit
					)
			)) AS all_matches
			ORDER BY data, rank
		) AS distinct_matches
		ORDER BY rank, list_label
		LIMIT 50
		"""

		mp = gmMatchProvider.cMatchProvider_SQL2(queries = [query])
		mp.setThresholds(2, 4, 6)
		self.matcher = mp
		self.selection_only = True

#----------------------------------------------------------------
class cHospitalStayPhraseWheel(gmPhraseWheel.cPhraseWheel):
	"""Phrasewheel to allow selection of a hospital-type org_unit."""
	def __init__(self, *args, **kwargs):

		gmPhraseWheel.cPhraseWheel.__init__ (self, *args, **kwargs)

		ctxt = {'ctxt_pat': {'where_part': u'(pk_patient = %(pat)s) AND', 'placeholder': u'pat'}}

		mp = gmMatchProvider.cMatchProvider_SQL2 (
			queries = [
u"""
SELECT
	pk_hospital_stay,
	descr
FROM (
	SELECT DISTINCT ON (pk_hospital_stay)
		pk_hospital_stay,
		descr
	FROM
		(SELECT
			pk_hospital_stay,
			(
				to_char(admission, 'YYYY-Mon-DD')
				|| ' (' || ward || ' @ ' || hospital || '):'
				|| episode
				|| coalesce((' (' || health_issue || ')'), '')
			) AS descr
		 FROM
		 	clin.v_hospital_stays
		 WHERE
			%(ctxt_pat)s (
				hospital %(fragment_condition)s
					OR
				ward %(fragment_condition)s
					OR
				episode %(fragment_condition)s
					OR
				health_issue %(fragment_condition)s
			)
		) AS the_stays
) AS distinct_stays
ORDER BY descr
LIMIT 25
"""			],
			context = ctxt
		)
		mp.setThresholds(3, 4, 6)
		mp.set_context('pat', gmPerson.gmCurrentPatient().ID)

		self.matcher = mp
		self.selection_only = True

#----------------------------------------------------------------
from Gnumed.wxGladeWidgets import wxgHospitalStayEditAreaPnl

class cHospitalStayEditAreaPnl(wxgHospitalStayEditAreaPnl.wxgHospitalStayEditAreaPnl, gmEditArea.cGenericEditAreaMixin):

	def __init__(self, *args, **kwargs):
		wxgHospitalStayEditAreaPnl.wxgHospitalStayEditAreaPnl.__init__(self, *args, **kwargs)
		gmEditArea.cGenericEditAreaMixin.__init__(self)
	#----------------------------------------------------------------
	# generic Edit Area mixin API
	#----------------------------------------------------------------
	def _valid_for_save(self):

		valid = True

		if self._PRW_episode.GetValue().strip() == u'':
			valid = False
			self._PRW_episode.display_as_valid(False)
			gmDispatcher.send(signal = 'statustext', msg = _('Must select an episode or enter a name for a new one. Cannot save hospitalization.'), beep = True)
			self._PRW_episode.SetFocus()

		if not self._PRW_admission.is_valid_timestamp(allow_empty = False):
			valid = False
			gmDispatcher.send(signal = 'statustext', msg = _('Missing admission data. Cannot save hospitalization.'), beep = True)
			self._PRW_admission.SetFocus()

		if self._PRW_discharge.is_valid_timestamp(allow_empty = True):
			if self._PRW_discharge.date is not None:
				adm = self._PRW_admission.date
				discharge = self._PRW_discharge.date
				# normalize for comparison
				discharge = discharge.replace (
					hour = adm.hour,
					minute = adm.minute,
					second = adm.second,
					microsecond = adm.microsecond
				)
				if adm is not None:
					if discharge == adm:
						self._PRW_discharge.SetData(discharge + pydt.timedelta(seconds = 1))
					elif not self._PRW_discharge.date > self._PRW_admission.date:
						valid = False
						self._PRW_discharge.display_as_valid(False)
						gmDispatcher.send(signal = 'statustext', msg = _('Discharge date must be empty or later than admission. Cannot save hospitalization.'), beep = True)
						self._PRW_discharge.SetFocus()

		if self._PRW_hospital.GetData() is None:
			self._PRW_hospital.display_as_valid(False)
			self.status_message = _('Must select a hospital. Cannot save hospitalization.')
			self._PRW_hospital.SetFocus()
		else:
			self._PRW_hospital.display_as_valid(True)

		return (valid is True)
	#----------------------------------------------------------------
	def _save_as_new(self):

		pat = gmPerson.gmCurrentPatient()
		emr = pat.get_emr()
		stay = emr.add_hospital_stay(episode = self._PRW_episode.GetData(can_create = True), fk_org_unit = self._PRW_hospital.GetData())
		stay['comment'] = self._TCTRL_comment.GetValue().strip()
		stay['admission'] = self._PRW_admission.GetData()
		stay['discharge'] = self._PRW_discharge.GetData()
		stay['comment'] = self._TCTRL_comment.GetValue()
		stay.save_payload()

		self.data = stay
		return True
	#----------------------------------------------------------------
	def _save_as_update(self):

		self.data['pk_episode'] = self._PRW_episode.GetData(can_create = True)
		self.data['pk_org_unit'] = self._PRW_hospital.GetData()
		self.data['admission'] = self._PRW_admission.GetData()
		self.data['discharge'] = self._PRW_discharge.GetData()
		self.data['comment'] = self._TCTRL_comment.GetValue()
		self.data.save_payload()

		return True
	#----------------------------------------------------------------
	def _refresh_as_new(self):
		self._PRW_hospital.SetText(value = u'', data = None)
		self._PRW_episode.SetText(value = u'')
		self._PRW_admission.SetText(data = gmDateTime.pydt_now_here())
		self._PRW_discharge.SetText()
		self._TCTRL_comment.SetValue(u'')
		self._PRW_hospital.SetFocus()
	#----------------------------------------------------------------
	def _refresh_from_existing(self):
		self._PRW_hospital.SetText(value = u'%s @ %s' % (self.data['ward'], self.data['hospital']), data = self.data['pk_org_unit'])

		if self.data['pk_episode'] is not None:
			self._PRW_episode.SetText(value = self.data['episode'], data = self.data['pk_episode'])

		self._PRW_admission.SetText(data = self.data['admission'])
		self._PRW_discharge.SetText(data = self.data['discharge'])
		self._TCTRL_comment.SetValue(gmTools.coalesce(self.data['comment'], u''))

		self._PRW_hospital.SetFocus()
	#----------------------------------------------------------------
	def _refresh_as_new_from_existing(self):
		print "this was not expected to be used in this edit area"

#================================================================
# episode related widgets/functions
#----------------------------------------------------------------
def edit_episode(parent=None, episode=None):
	ea = cEpisodeEditAreaPnl(parent = parent, id = -1)
	ea.data = episode
	ea.mode = gmTools.coalesce(episode, 'new', 'edit')
	dlg = gmEditArea.cGenericEditAreaDlg2(parent = parent, id = -1, edit_area = ea, single_entry = True)
	dlg.SetTitle(gmTools.coalesce(episode, _('Adding a new episode'), _('Editing an episode')))
	if dlg.ShowModal() == wx.ID_OK:
		return True
	return False

#----------------------------------------------------------------
def manage_episodes(parent=None):

	pat = gmPerson.gmCurrentPatient()
	emr = pat.get_emr()

	if parent is None:
		parent = wx.GetApp().GetTopWindow()
	#-----------------------------------------
	def edit(episode=None):
		return edit_episode(parent = parent, episode = episode)
	#-----------------------------------------
	def delete(episode=None):
		if gmEMRStructItems.delete_episode(episode = episode):
			return True
		gmDispatcher.send (
			signal = u'statustext',
			msg = _('Cannot delete episode.'),
			beep = True
		)
		return False
	#-----------------------------------------
	def manage_issues(episode=None):
		return select_health_issues(parent = None, emr = emr)
	#-----------------------------------------
	def get_tooltip(data):
		if data is None:
			return None
		return data.format (
			patient = pat,
			with_summary = True,
			with_codes = True,
			with_encounters = False,
			with_documents = False,
			with_hospital_stays = False,
			with_procedures = False,
			with_family_history = False,
			with_tests = False,
			with_vaccinations = False,
			with_health_issue = True
		)
	#-----------------------------------------
	def refresh(lctrl):
		epis = emr.get_episodes(order_by = u'description')
		items = [
			[	e['description'],
				gmTools.bool2subst(e['episode_open'], _(u'ongoing'), _(u'closed'), u'<unknown>'),
				gmDateTime.pydt_strftime(e.best_guess_start_date, '%Y %b %d'),
				gmTools.coalesce(e['health_issue'], u'')
			] for e in epis
		]
		lctrl.set_string_items(items = items)
		lctrl.set_data(data = epis)
	#-----------------------------------------
	gmListWidgets.get_choices_from_list (
		parent = parent,
		msg = _('\nSelect the episode you want to edit !\n'),
		caption = _('Editing episodes ...'),
		columns = [_(u'Episode'), _('Status'), _('Started'), _(u'Health issue')],
		single_selection = True,
		edit_callback = edit,
		new_callback = edit,
		delete_callback = delete,
		refresh_callback = refresh,
		list_tooltip_callback = get_tooltip,
		left_extra_button = (_('Manage issues'), _('Manage health issues'), manage_issues)
	)

#----------------------------------------------------------------
def promote_episode_to_issue(parent=None, episode=None, emr=None):

	created_new_issue = False

	try:
		issue = gmEMRStructItems.cHealthIssue(name = episode['description'], patient = episode['pk_patient'])
	except gmExceptions.NoSuchBusinessObjectError:
		issue = None

	if issue is None:
		issue = emr.add_health_issue(issue_name = episode['description'])
		created_new_issue = True
	else:
		# issue exists already, so ask user
		dlg = gmGuiHelpers.c3ButtonQuestionDlg (
			parent,
			-1,
			caption = _('Promoting episode to health issue'),
			question = _(
				'There already is a health issue\n'
				'\n'
				' %s\n'
				'\n'
				'What do you want to do ?'
			) % issue['description'],
			button_defs = [
				{'label': _('Use existing'), 'tooltip': _('Move episode into existing health issue'), 'default': False},
				{'label': _('Create new'), 'tooltip': _('Create a new health issue with another name'), 'default': True}
			]
		)
		use_existing = dlg.ShowModal()
		dlg.Destroy()

		if use_existing == wx.ID_CANCEL:
			return

		# user wants to create new issue with alternate name
		if use_existing == wx.ID_NO:
			# loop until name modified but non-empty or cancelled
			issue_name = episode['description']
			while issue_name == episode['description']:
				dlg = wx.TextEntryDialog (
					parent = parent,
					message = _('Enter a short descriptive name for the new health issue:'),
					caption = _('Creating a new health issue ...'),
					defaultValue = issue_name,
					style = wx.OK | wx.CANCEL | wx.CENTRE
				)
				decision = dlg.ShowModal()
				if decision != wx.ID_OK:
					dlg.Destroy()
					return
				issue_name = dlg.GetValue().strip()
				dlg.Destroy()
				if issue_name == u'':
					issue_name = episode['description']

			issue = emr.add_health_issue(issue_name = issue_name)
			created_new_issue = True

	# eventually move the episode to the issue
	if not move_episode_to_issue(episode = episode, target_issue = issue, save_to_backend = True):
		# user cancelled the move so delete just-created issue
		if created_new_issue:
			# shouldn't fail as it is completely new
			gmEMRStructItems.delete_health_issue(health_issue = issue)
		return

	return

#----------------------------------------------------------------
def move_episode_to_issue(episode=None, target_issue=None, save_to_backend=False):
	"""Prepare changing health issue for an episode.

	Checks for two-open-episodes conflict. When this
	function succeeds, the pk_health_issue has been set
	on the episode instance and the episode should - for
	all practical purposes - be ready for save_payload().
	"""
	# episode is closed: should always work
	if not episode['episode_open']:
		episode['pk_health_issue'] = target_issue['pk_health_issue']
		if save_to_backend:
			episode.save_payload()
		return True

	# un-associate: should always work, too
	if target_issue is None:
		episode['pk_health_issue'] = None
		if save_to_backend:
			episode.save_payload()
		return True

	# try closing possibly expired episode on target issue if any
	db_cfg = gmCfg.cCfgSQL()
	epi_ttl = int(db_cfg.get2 (
		option = u'episode.ttl',
		workplace = gmPraxis.gmCurrentPraxisBranch().active_workplace,
		bias = 'user',
		default = 60				# 2 months
	))
	if target_issue.close_expired_episode(ttl=epi_ttl) is True:
		gmDispatcher.send(signal='statustext', msg=_('Closed episodes older than %s days on health issue [%s]') % (epi_ttl, target_issue['description']))
	existing_epi = target_issue.get_open_episode()

	# no more open episode on target issue: should work now
	if existing_epi is None:
		episode['pk_health_issue'] = target_issue['pk_health_issue']
		if save_to_backend:
			episode.save_payload()
		return True

	# don't conflict on SELF ;-)
	if existing_epi['pk_episode'] == episode['pk_episode']:
		episode['pk_health_issue'] = target_issue['pk_health_issue']
		if save_to_backend:
			episode.save_payload()
		return True

	# we got two open episodes at once, ask user
	move_range = episode.get_access_range()
	exist_range = existing_epi.get_access_range()
	question = _(
		'You want to associate the running episode:\n\n'
		' "%(new_epi_name)s" (%(new_epi_start)s - %(new_epi_end)s)\n\n'
		'with the health issue:\n\n'
		' "%(issue_name)s"\n\n'
		'There already is another episode running\n'
		'for this health issue:\n\n'
		' "%(old_epi_name)s" (%(old_epi_start)s - %(old_epi_end)s)\n\n'
		'However, there can only be one running\n'
		'episode per health issue.\n\n'
		'Which episode do you want to close ?'
	) % {
		'new_epi_name': episode['description'],
		'new_epi_start': move_range[0].strftime('%m/%y'),
		'new_epi_end': move_range[1].strftime('%m/%y'),
		'issue_name': target_issue['description'],
		'old_epi_name': existing_epi['description'],
		'old_epi_start': exist_range[0].strftime('%m/%y'),
		'old_epi_end': exist_range[1].strftime('%m/%y')
	}
	dlg = gmGuiHelpers.c3ButtonQuestionDlg (
		parent = None,
		id = -1,
		caption = _('Resolving two-running-episodes conflict'),
		question = question,
		button_defs = [
			{'label': _('old episode'), 'default': True, 'tooltip': _('close existing episode "%s"') % existing_epi['description']},
			{'label': _('new episode'), 'default': False, 'tooltip': _('close moving (new) episode "%s"') % episode['description']}
		]
	)
	decision = dlg.ShowModal()

	if decision == wx.ID_CANCEL:
		# button 3: move cancelled by user
		return False

	elif decision == wx.ID_YES:
		# button 1: close old episode
		existing_epi['episode_open'] = False
		existing_epi.save_payload()

	elif decision == wx.ID_NO:
		# button 2: close new episode
		episode['episode_open'] = False

	else:
		raise ValueError('invalid result from c3ButtonQuestionDlg: [%s]' % decision)

	episode['pk_health_issue'] = target_issue['pk_health_issue']
	if save_to_backend:
		episode.save_payload()
	return True
#----------------------------------------------------------------
class cEpisodeListSelectorDlg(gmListWidgets.cGenericListSelectorDlg):

	# FIXME: support pre-selection

	def __init__(self, *args, **kwargs):

		episodes = kwargs['episodes']
		del kwargs['episodes']

		gmListWidgets.cGenericListSelectorDlg.__init__(self, *args, **kwargs)

		self.SetTitle(_('Select the episodes you are interested in ...'))
		self._LCTRL_items.set_columns([_('Episode'), _('Status'), _('Health Issue')])
		self._LCTRL_items.set_string_items (
			items = [ 
				[	epi['description'], 
					gmTools.bool2str(epi['episode_open'], _('ongoing'), u''), 
					gmTools.coalesce(epi['health_issue'], u'')
				]
				for epi in episodes ]
		)
		self._LCTRL_items.set_column_widths()
		self._LCTRL_items.set_data(data = episodes)

#----------------------------------------------------------------
class cEpisodeDescriptionPhraseWheel(gmPhraseWheel.cPhraseWheel):
	"""Let user select an episode *description*.

	The user can select an episode description from the previously
	used descriptions across all episodes across all patients.

	Selection is done with a phrasewheel so the user can
	type the episode name and matches will be shown. Typing
	"*" will show the entire list of episodes.

	If the user types a description not existing yet a
	new episode description will be returned.
	"""
	def __init__(self, *args, **kwargs):

		mp = gmMatchProvider.cMatchProvider_SQL2 (
			queries = [
u"""
SELECT DISTINCT ON (description)
	description
		AS data,
	description
		AS field_label,
	description || ' ('
	|| CASE
		WHEN is_open IS TRUE THEN _('ongoing')
		ELSE _('closed')
	   END
	|| ')'
		AS list_label
FROM
	clin.episode
WHERE
	description %(fragment_condition)s
ORDER BY description
LIMIT 30
"""
			]
		)
		gmPhraseWheel.cPhraseWheel.__init__(self, *args, **kwargs)
		self.matcher = mp

#----------------------------------------------------------------
class cEpisodeSelectionPhraseWheel(gmPhraseWheel.cPhraseWheel):
	"""Let user select an episode.

	The user can select an episode from the existing episodes of a
	patient. Selection is done with a phrasewheel so the user
	can type the episode name and matches will be shown. Typing
	"*" will show the entire list of episodes. Closed episodes
	will be marked as such. If the user types an episode name not
	in the list of existing episodes a new episode can be created
	from it if the programmer activated that feature.

	If keyword <patient_id> is set to None or left out the control
	will listen to patient change signals and therefore act on
	gmPerson.gmCurrentPatient() changes.
	"""
	def __init__(self, *args, **kwargs):

		ctxt = {'ctxt_pat': {'where_part': u'and pk_patient = %(pat)s', 'placeholder': u'pat'}}

		mp = gmMatchProvider.cMatchProvider_SQL2 (
			queries = [
u"""(

SELECT
	pk_episode
		as data,
	description
		as field_label,
	coalesce (
		description || ' - ' || health_issue,
		description
	) as list_label,
	1 as rank
from
  	clin.v_pat_episodes
where
	episode_open is true and
	description %(fragment_condition)s
	%(ctxt_pat)s

) union all (

SELECT
	pk_episode
		as data,
	description
		as field_label,
	coalesce (
		description || _(' (closed)') || ' - ' || health_issue,
		description || _(' (closed)')
	) as list_label,
	2 as rank
from
	clin.v_pat_episodes
where
	description %(fragment_condition)s and
	episode_open is false
	%(ctxt_pat)s

)

order by rank, list_label
limit 30"""
],
			context = ctxt
		)

		try:
			kwargs['patient_id']
		except KeyError:
			kwargs['patient_id'] = None

		if kwargs['patient_id'] is None:
			self.use_current_patient = True
			self.__register_patient_change_signals()
			pat = gmPerson.gmCurrentPatient()
			if pat.connected:
				mp.set_context('pat', pat.ID)
		else:
			self.use_current_patient = False
			self.__patient_id = int(kwargs['patient_id'])
			mp.set_context('pat', self.__patient_id)

		del kwargs['patient_id']

		gmPhraseWheel.cPhraseWheel.__init__ (
			self,
			*args,
			**kwargs
		)
		self.matcher = mp
	#--------------------------------------------------------
	# external API
	#--------------------------------------------------------
	def set_patient(self, patient_id=None):
		if self.use_current_patient:
			return False
		self.__patient_id = int(patient_id)
		self.set_context('pat', self.__patient_id)
		return True
	#--------------------------------------------------------
	def GetData(self, can_create=False, as_instance=False, is_open=False):
		self.__is_open_for_create_data = is_open		# used (only) in _create_data()
		return gmPhraseWheel.cPhraseWheel.GetData(self, can_create = can_create, as_instance = as_instance)
	#--------------------------------------------------------
	def _create_data(self):

		epi_name = self.GetValue().strip()
		if epi_name == u'':
			gmDispatcher.send(signal = u'statustext', msg = _('Cannot create episode without name.'), beep = True)
			_log.debug('cannot create episode without name')
			return

		if self.use_current_patient:
			pat = gmPerson.gmCurrentPatient()
		else:
			pat = gmPerson.cPatient(aPK_obj = self.__patient_id)

		emr = pat.get_emr()
		epi = emr.add_episode(episode_name = epi_name, is_open = self.__is_open_for_create_data)
		if epi is None:
			self.data = {}
		else:
			self.SetText (
				value = epi_name,
				data = epi['pk_episode']
			)
	#--------------------------------------------------------
	def _data2instance(self):
		return gmEMRStructItems.cEpisode(aPK_obj = self.GetData())
	#--------------------------------------------------------
	# internal API
	#--------------------------------------------------------
	def __register_patient_change_signals(self):
		gmDispatcher.connect(self._pre_patient_unselection, u'pre_patient_unselection')
		gmDispatcher.connect(self._post_patient_selection, u'post_patient_selection')
	#--------------------------------------------------------
	def _pre_patient_unselection(self):
		self.__patient_id = None
		self.unset_context('pat')
		self.SetData()
		return True
	#--------------------------------------------------------
	def _post_patient_selection(self):
		if self.use_current_patient:
			patient = gmPerson.gmCurrentPatient()
			self.set_context('pat', patient.ID)
		return True

#----------------------------------------------------------------
from Gnumed.wxGladeWidgets import wxgEpisodeEditAreaPnl

class cEpisodeEditAreaPnl(gmEditArea.cGenericEditAreaMixin, wxgEpisodeEditAreaPnl.wxgEpisodeEditAreaPnl):

	def __init__(self, *args, **kwargs):

		try:
			episode = kwargs['episode']
			del kwargs['episode']
		except KeyError:
			episode = None

		wxgEpisodeEditAreaPnl.wxgEpisodeEditAreaPnl.__init__(self, *args, **kwargs)
		gmEditArea.cGenericEditAreaMixin.__init__(self)

		self.data = episode
	#----------------------------------------------------------------
	# generic Edit Area mixin API
	#----------------------------------------------------------------
	def _valid_for_save(self):

		errors = False

		if len(self._PRW_description.GetValue().strip()) == 0:
			errors = True
			self._PRW_description.display_as_valid(False)
			self._PRW_description.SetFocus()
		else:
			self._PRW_description.display_as_valid(True)
		self._PRW_description.Refresh()

		return not errors
	#----------------------------------------------------------------
	def _save_as_new(self):

		pat = gmPerson.gmCurrentPatient()
		emr = pat.get_emr()

		epi = emr.add_episode(episode_name = self._PRW_description.GetValue().strip())
		epi['summary'] = self._TCTRL_status.GetValue().strip()
		epi['episode_open'] = not self._CHBOX_closed.IsChecked()
		epi['diagnostic_certainty_classification'] = self._PRW_certainty.GetData()

		issue_name = self._PRW_issue.GetValue().strip()
		if len(issue_name) != 0:
			epi['pk_health_issue'] = self._PRW_issue.GetData(can_create = True)
			issue = gmEMRStructItems.cHealthIssue(aPK_obj = epi['pk_health_issue'])

			if not move_episode_to_issue(episode = epi, target_issue = issue, save_to_backend = False):
				gmDispatcher.send (
					signal = 'statustext',
					msg = _('Cannot attach episode [%s] to health issue [%s] because it already has a running episode.') % (
						epi['description'],
						issue['description']
					)
				)
				gmEMRStructItems.delete_episode(episode = epi)
				return False

		epi.save()

		epi.generic_codes = [ c['data'] for c in self._PRW_codes.GetData() ]

		self.data = epi
		return True
	#----------------------------------------------------------------
	def _save_as_update(self):

		self.data['description'] = self._PRW_description.GetValue().strip()
		self.data['summary'] = self._TCTRL_status.GetValue().strip()
		self.data['episode_open'] = not self._CHBOX_closed.IsChecked()
		self.data['diagnostic_certainty_classification'] = self._PRW_certainty.GetData()

		issue_name = self._PRW_issue.GetValue().strip()
		if len(issue_name) == 0:
			self.data['pk_health_issue'] = None
		else:
			self.data['pk_health_issue'] = self._PRW_issue.GetData(can_create = True)
			issue = gmEMRStructItems.cHealthIssue(aPK_obj = self.data['pk_health_issue'])

			if not move_episode_to_issue(episode = self.data, target_issue = issue, save_to_backend = False):
				gmDispatcher.send (
					signal = 'statustext',
					msg = _('Cannot attach episode [%s] to health issue [%s] because it already has a running episode.') % (
						self.data['description'],
						issue['description']
					)
				)
				return False

		self.data.save()
		self.data.generic_codes = [ c['data'] for c in self._PRW_codes.GetData() ]

		return True
	#----------------------------------------------------------------
	def _refresh_as_new(self):
		if self.data is None:
			ident = gmPerson.gmCurrentPatient()
		else:
			ident = gmPerson.cPerson(aPK_obj = self.data['pk_patient'])
		self._TCTRL_patient.SetValue(ident.get_description_gender())
		self._PRW_issue.SetText()
		self._PRW_description.SetText()
		self._TCTRL_status.SetValue(u'')
		self._PRW_certainty.SetText()
		self._CHBOX_closed.SetValue(False)
		self._PRW_codes.SetText()
	#----------------------------------------------------------------
	def _refresh_from_existing(self):
		ident = gmPerson.cPerson(aPK_obj = self.data['pk_patient'])
		self._TCTRL_patient.SetValue(ident.get_description_gender())

		if self.data['pk_health_issue'] is not None:
			self._PRW_issue.SetText(self.data['health_issue'], data=self.data['pk_health_issue'])

		self._PRW_description.SetText(self.data['description'], data=self.data['description'])

		self._TCTRL_status.SetValue(gmTools.coalesce(self.data['summary'], u''))

		if self.data['diagnostic_certainty_classification'] is not None:
			self._PRW_certainty.SetData(data = self.data['diagnostic_certainty_classification'])

		self._CHBOX_closed.SetValue(not self.data['episode_open'])

		val, data = self._PRW_codes.generic_linked_codes2item_dict(self.data.generic_codes)
		self._PRW_codes.SetText(val, data)
	#----------------------------------------------------------------
	def _refresh_as_new_from_existing(self):
		self._refresh_as_new()

#================================================================
# health issue related widgets/functions
#----------------------------------------------------------------
def edit_health_issue(parent=None, issue=None):
	ea = cHealthIssueEditAreaPnl(parent = parent, id = -1)
	ea.data = issue
	ea.mode = gmTools.coalesce(issue, 'new', 'edit')
	dlg = gmEditArea.cGenericEditAreaDlg2(parent = parent, id = -1, edit_area = ea, single_entry = (issue is not None))
	dlg.SetTitle(gmTools.coalesce(issue, _('Adding a new health issue'), _('Editing a health issue')))
	if dlg.ShowModal() == wx.ID_OK:
		dlg.Destroy()
		return True
	dlg.Destroy()
	return False
#----------------------------------------------------------------
def select_health_issues(parent=None, emr=None):

	if parent is None:
		parent = wx.GetApp().GetTopWindow()
	#-----------------------------------------
	def edit(issue=None):
		return edit_health_issue(parent = parent, issue = issue)
	#-----------------------------------------
	def delete(issue=None):
		if gmEMRStructItems.delete_health_issue(health_issue = issue):
			return True
		gmDispatcher.send (
			signal = u'statustext',
			msg = _('Cannot delete health issue.'),
			beep = True
		)
		return False
	#-----------------------------------------
	def get_tooltip(data):
		if data is None:
			return None
		patient = gmPerson.cPatient(data['pk_patient'])
		return data.format (
			patient = patient,
			with_summary = True,
			with_codes = True,
			with_episodes = True,
			with_encounters = True,
			with_medications = False,
			with_hospital_stays = False,
			with_procedures = False,
			with_family_history = False,
			with_documents = False,
			with_tests = False,
			with_vaccinations = False
		)
	#-----------------------------------------
	def refresh(lctrl):
		issues = emr.get_health_issues()
		items = [
			[
				gmTools.bool2subst(i['is_confidential'], _('CONFIDENTIAL'), u'', u''),
				i['description'],
				gmTools.bool2subst(i['clinically_relevant'], _('relevant'), u'', u''),
				gmTools.bool2subst(i['is_active'], _('active'), u'', u''),
				gmTools.bool2subst(i['is_cause_of_death'], _('fatal'), u'', u'')
			] for i in issues
		]
		lctrl.set_string_items(items = items)
		lctrl.set_data(data = issues)
	#-----------------------------------------
	return gmListWidgets.get_choices_from_list (
		parent = parent,
		msg = _('\nSelect the health issues !\n'),
		caption = _('Showing health issues ...'),
		columns = [u'', _('Health issue'), u'', u'', u''],
		single_selection = False,
		edit_callback = edit,
		new_callback = edit,
		delete_callback = delete,
		refresh_callback = refresh
	)
#----------------------------------------------------------------
class cIssueListSelectorDlg(gmListWidgets.cGenericListSelectorDlg):

	# FIXME: support pre-selection

	def __init__(self, *args, **kwargs):

		issues = kwargs['issues']
		del kwargs['issues']

		gmListWidgets.cGenericListSelectorDlg.__init__(self, *args, **kwargs)

		self.SetTitle(_('Select the health issues you are interested in ...'))
		self._LCTRL_items.set_columns([u'', _('Health Issue'), u'', u'', u''])

		for issue in issues:
			if issue['is_confidential']:
				row_num = self._LCTRL_items.InsertStringItem(sys.maxint, label = _('confidential'))
				self._LCTRL_items.SetItemTextColour(row_num, col=wx.NamedColour('RED'))
			else:
				row_num = self._LCTRL_items.InsertStringItem(sys.maxint, label = u'')

			self._LCTRL_items.SetStringItem(index = row_num, col = 1, label = issue['description'])
			if issue['clinically_relevant']:
				self._LCTRL_items.SetStringItem(index = row_num, col = 2, label = _('relevant'))
			if issue['is_active']:
				self._LCTRL_items.SetStringItem(index = row_num, col = 3, label = _('active'))
			if issue['is_cause_of_death']:
				self._LCTRL_items.SetStringItem(index = row_num, col = 4, label = _('fatal'))

		self._LCTRL_items.set_column_widths()
		self._LCTRL_items.set_data(data = issues)
#----------------------------------------------------------------
class cIssueSelectionPhraseWheel(gmPhraseWheel.cPhraseWheel):
	"""Let the user select a health issue.

	The user can select a health issue from the existing issues
	of a patient. Selection is done with a phrasewheel so the user
	can type the issue name and matches will be shown. Typing
	"*" will show the entire list of issues. Inactive issues
	will be marked as such. If the user types an issue name not
	in the list of existing issues a new issue can be created
	from it if the programmer activated that feature.

	If keyword <patient_id> is set to None or left out the control
	will listen to patient change signals and therefore act on
	gmPerson.gmCurrentPatient() changes.
	"""
	def __init__(self, *args, **kwargs):

		ctxt = {'ctxt_pat': {'where_part': u'pk_patient=%(pat)s', 'placeholder': u'pat'}}

		mp = gmMatchProvider.cMatchProvider_SQL2 (
			# FIXME: consider clin.health_issue.clinically_relevant
			queries = [u"""
				SELECT
					data,
					field_label,
					list_label
				FROM ((
					SELECT
						pk_health_issue AS data,
						description AS field_label,
						description AS list_label
					FROM clin.v_health_issues
					WHERE
						is_active IS true
							AND
						description %(fragment_condition)s
							AND
						%(ctxt_pat)s

					) UNION (

					SELECT
						pk_health_issue AS data,
						description AS field_label,
						description || _(' (inactive)') AS list_label
					FROM clin.v_health_issues
					WHERE
						is_active IS false
							AND
						description %(fragment_condition)s
							AND
						%(ctxt_pat)s
				)) AS union_query
				ORDER BY
					list_label"""
			],
			context = ctxt
		)
		try: kwargs['patient_id']
		except KeyError: kwargs['patient_id'] = None

		if kwargs['patient_id'] is None:
			self.use_current_patient = True
			self.__register_patient_change_signals()
			pat = gmPerson.gmCurrentPatient()
			if pat.connected:
				mp.set_context('pat', pat.ID)
		else:
			self.use_current_patient = False
			self.__patient_id = int(kwargs['patient_id'])
			mp.set_context('pat', self.__patient_id)

		del kwargs['patient_id']

		gmPhraseWheel.cPhraseWheel.__init__ (
			self,
			*args,
			**kwargs
		)
		self.matcher = mp
	#--------------------------------------------------------
	# external API
	#--------------------------------------------------------
	def set_patient(self, patient_id=None):
		if self.use_current_patient:
			return False
		self.__patient_id = int(patient_id)
		self.set_context('pat', self.__patient_id)
		return True
	#--------------------------------------------------------
	def _create_data(self):
		issue_name = self.GetValue().strip()
		if issue_name == u'':
			gmDispatcher.send(signal = u'statustext', msg = _('Cannot create health issue without name.'), beep = True)
			_log.debug('cannot create health issue without name')
			return

		if self.use_current_patient:
			pat = gmPerson.gmCurrentPatient()
		else:
			pat = gmPerson.cPatient(aPK_obj = self.__patient_id)

		emr = pat.get_emr()
		issue = emr.add_health_issue(issue_name = issue_name)

		if issue is None:
			self.data = {}
		else:
			self.SetText (
				value = issue_name,
				data = issue['pk_health_issue']
			)
	#--------------------------------------------------------
	def _data2instance(self):
		return gmEMRStructItems.cHealthIssue(aPK_obj = self.GetData())
	#--------------------------------------------------------
	def _get_data_tooltip(self):
		if self.GetData() is None:
			return None
		issue = self._data2instance()
		if issue is None:
			return None
		return issue.format (
			patient = None,
			with_summary = True,
			with_codes = False,
			with_episodes = True,
			with_encounters = True,
			with_medications = False,
			with_hospital_stays = False,
			with_procedures = False,
			with_family_history = False,
			with_documents = False,
			with_tests = False,
			with_vaccinations = False,
			with_external_care = True
		)
	#--------------------------------------------------------
	# internal API
	#--------------------------------------------------------
	def __register_patient_change_signals(self):
		gmDispatcher.connect(self._pre_patient_unselection, u'pre_patient_unselection')
		gmDispatcher.connect(self._post_patient_selection, u'post_patient_selection')
	#--------------------------------------------------------
	def _pre_patient_unselection(self):
		return True
	#--------------------------------------------------------
	def _post_patient_selection(self):
		if self.use_current_patient:
			patient = gmPerson.gmCurrentPatient()
			self.set_context('pat', patient.ID)
		return True
#------------------------------------------------------------
from Gnumed.wxGladeWidgets import wxgIssueSelectionDlg

class cIssueSelectionDlg(wxgIssueSelectionDlg.wxgIssueSelectionDlg):

	def __init__(self, *args, **kwargs):
		try:
			msg = kwargs['message']
		except KeyError:
			msg = None
		del kwargs['message']
		wxgIssueSelectionDlg.wxgIssueSelectionDlg.__init__(self, *args, **kwargs)
		if msg is not None:
			self._lbl_message.SetLabel(label=msg)
	#--------------------------------------------------------
	def _on_OK_button_pressed(self, event):
		event.Skip()
		pk_issue = self._PhWheel_issue.GetData(can_create=True)
		if pk_issue is None:
			gmGuiHelpers.gm_show_error (
				_('Cannot create new health issue:\n [%(issue)s]') % {'issue': self._PhWheel_issue.GetValue().strip()},
				_('Selecting health issue')
			)
			return False
		return True
#------------------------------------------------------------
from Gnumed.wxGladeWidgets import wxgHealthIssueEditAreaPnl

class cHealthIssueEditAreaPnl(gmEditArea.cGenericEditAreaMixin, wxgHealthIssueEditAreaPnl.wxgHealthIssueEditAreaPnl):
	"""Panel encapsulating health issue edit area functionality."""

	def __init__(self, *args, **kwargs):

		try:
			data = kwargs['issue']
			del kwargs['issue']
		except KeyError:
			data = None

		wxgHealthIssueEditAreaPnl.wxgHealthIssueEditAreaPnl.__init__(self, *args, **kwargs)
		gmEditArea.cGenericEditAreaMixin.__init__(self)

		self.mode = 'new'
		self.data = data
		if data is not None:
			self.mode = 'edit'

		self.__init_ui()
	#----------------------------------------------------------------
	def __init_ui(self):

		# FIXME: include more sources: coding systems/other database columns
		mp = gmMatchProvider.cMatchProvider_SQL2 (
			queries = [u"SELECT DISTINCT ON (description) description, description FROM clin.health_issue WHERE description %(fragment_condition)s LIMIT 50"]
		)
		mp.setThresholds(1, 3, 5)
		self._PRW_condition.matcher = mp

		mp = gmMatchProvider.cMatchProvider_SQL2 (
			queries = [u"""
SELECT DISTINCT ON (grouping) grouping, grouping from (

	SELECT rank, grouping from ((

		SELECT
			grouping,
			1 as rank
		from
			clin.health_issue
		where
			grouping %%(fragment_condition)s
				and
			(SELECT True from clin.encounter where fk_patient = %s and pk = clin.health_issue.fk_encounter)

	) union (

		SELECT
			grouping,
			2 as rank
		from
			clin.health_issue
		where
			grouping %%(fragment_condition)s

	)) as union_result

	order by rank

) as order_result

limit 50""" % gmPerson.gmCurrentPatient().ID
			]
		)
		mp.setThresholds(1, 3, 5)
		self._PRW_grouping.matcher = mp

		self._PRW_age_noted.add_callback_on_lose_focus(self._on_leave_age_noted)
		self._PRW_year_noted.add_callback_on_lose_focus(self._on_leave_year_noted)

#		self._PRW_age_noted.add_callback_on_modified(self._on_modified_age_noted)
#		self._PRW_year_noted.add_callback_on_modified(self._on_modified_year_noted)

		self._PRW_year_noted.Enable(True)

		self._PRW_codes.add_callback_on_lose_focus(self._on_leave_codes)

	#----------------------------------------------------------------
	# generic Edit Area mixin API
	#----------------------------------------------------------------
	def _valid_for_save(self):

		if self._PRW_condition.GetValue().strip() == '':
			self._PRW_condition.display_as_valid(False)
			self._PRW_condition.SetFocus()
			return False
		self._PRW_condition.display_as_valid(True)
		self._PRW_condition.Refresh()

		# FIXME: sanity check age/year diagnosed
		age_noted = self._PRW_age_noted.GetValue().strip()
		if age_noted != u'':
			if gmDateTime.str2interval(str_interval = age_noted) is None:
				self._PRW_age_noted.display_as_valid(False)
				self._PRW_age_noted.SetFocus()
				return False
		self._PRW_age_noted.display_as_valid(True)
		return True
	#----------------------------------------------------------------
	def _save_as_new(self):
		pat = gmPerson.gmCurrentPatient()
		emr = pat.get_emr()

		issue = emr.add_health_issue(issue_name = self._PRW_condition.GetValue().strip())

		side = u''
		if self._ChBOX_left.GetValue():
			side += u's'
		if self._ChBOX_right.GetValue():
			side += u'd'
		issue['laterality'] = side

		issue['summary'] = self._TCTRL_status.GetValue().strip()
		issue['diagnostic_certainty_classification'] = self._PRW_certainty.GetData()
		issue['grouping'] = self._PRW_grouping.GetValue().strip()
		issue['is_active'] = self._ChBOX_active.GetValue()
		issue['clinically_relevant'] = self._ChBOX_relevant.GetValue()
		issue['is_confidential'] = self._ChBOX_confidential.GetValue()
		issue['is_cause_of_death'] = self._ChBOX_caused_death.GetValue()

		age_noted = self._PRW_age_noted.GetData()
		if age_noted is not None:
			issue['age_noted'] = age_noted

		issue.save()

		issue.generic_codes = [ c['data'] for c in self._PRW_codes.GetData() ]

		self.data = issue
		return True
	#----------------------------------------------------------------
	def _save_as_update(self):

		self.data['description'] = self._PRW_condition.GetValue().strip()

		side = u''
		if self._ChBOX_left.GetValue():
			side += u's'
		if self._ChBOX_right.GetValue():
			side += u'd'
		self.data['laterality'] = side

		self.data['summary'] = self._TCTRL_status.GetValue().strip()
		self.data['diagnostic_certainty_classification'] = self._PRW_certainty.GetData()
		self.data['grouping'] = self._PRW_grouping.GetValue().strip()
		self.data['is_active'] = bool(self._ChBOX_active.GetValue())
		self.data['clinically_relevant'] = bool(self._ChBOX_relevant.GetValue())
		self.data['is_confidential'] = bool(self._ChBOX_confidential.GetValue())
		self.data['is_cause_of_death'] = bool(self._ChBOX_caused_death.GetValue())

		age_noted = self._PRW_age_noted.GetData()
		if age_noted is not None:
			self.data['age_noted'] = age_noted

		self.data.save()
		self.data.generic_codes = [ c['data'] for c in self._PRW_codes.GetData() ]

		return True
	#----------------------------------------------------------------
	def _refresh_as_new(self):
		self._PRW_condition.SetText()
		self._ChBOX_left.SetValue(0)
		self._ChBOX_right.SetValue(0)
		self._PRW_codes.SetText()
		self._on_leave_codes()
		self._PRW_certainty.SetText()
		self._PRW_grouping.SetText()
		self._TCTRL_status.SetValue(u'')
		self._PRW_age_noted.SetText()
		self._PRW_year_noted.SetText()
		self._ChBOX_active.SetValue(1)
		self._ChBOX_relevant.SetValue(1)
		self._ChBOX_confidential.SetValue(0)
		self._ChBOX_caused_death.SetValue(0)

		self._PRW_condition.SetFocus()
		return True
	#----------------------------------------------------------------
	def _refresh_from_existing(self):
		self._PRW_condition.SetText(self.data['description'])

		lat = gmTools.coalesce(self.data['laterality'], '')
		if lat.find('s') == -1:
			self._ChBOX_left.SetValue(0)
		else:
			self._ChBOX_left.SetValue(1)
		if lat.find('d') == -1:
			self._ChBOX_right.SetValue(0)
		else:
			self._ChBOX_right.SetValue(1)

		val, data = self._PRW_codes.generic_linked_codes2item_dict(self.data.generic_codes)
		self._PRW_codes.SetText(val, data)
		self._on_leave_codes()

		if self.data['diagnostic_certainty_classification'] is not None:
			self._PRW_certainty.SetData(data = self.data['diagnostic_certainty_classification'])
		self._PRW_grouping.SetText(gmTools.coalesce(self.data['grouping'], u''))
		self._TCTRL_status.SetValue(gmTools.coalesce(self.data['summary'], u''))

		if self.data['age_noted'] is None:
			self._PRW_age_noted.SetText()
		else:
			self._PRW_age_noted.SetText (
				value = '%sd' % self.data['age_noted'].days,
				data = self.data['age_noted']
			)

		self._ChBOX_active.SetValue(self.data['is_active'])
		self._ChBOX_relevant.SetValue(self.data['clinically_relevant'])
		self._ChBOX_confidential.SetValue(self.data['is_confidential'])
		self._ChBOX_caused_death.SetValue(self.data['is_cause_of_death'])

		self._TCTRL_status.SetFocus()

		return True
	#----------------------------------------------------------------
	def _refresh_as_new_from_existing(self):
		return self._refresh_as_new()
	#--------------------------------------------------------
	# internal helpers
	#--------------------------------------------------------
	def _on_leave_codes(self, *args, **kwargs):
		if not self._PRW_codes.IsModified():
			return True

		self._TCTRL_code_details.SetValue(u'- ' + u'\n- '.join([ c['list_label'] for c in self._PRW_codes.GetData() ]))
	#--------------------------------------------------------
	def _on_leave_age_noted(self, *args, **kwargs):

		if not self._PRW_age_noted.IsModified():
			return True

		age_str = self._PRW_age_noted.GetValue().strip()

		if age_str == u'':
			return True

		issue_age = gmDateTime.str2interval(str_interval = age_str)

		if issue_age is None:
			self.status_message = _('Cannot parse [%s] into valid interval.') % age_str
			self._PRW_age_noted.display_as_valid(False)
			return True

		pat = gmPerson.gmCurrentPatient()
		if pat['dob'] is not None:
			max_issue_age = pydt.datetime.now(tz=pat['dob'].tzinfo) - pat['dob']
			if issue_age >= max_issue_age:
				self.status_message = _('Health issue cannot have been noted at age %s. Patient is only %s old.') % (issue_age, pat.get_medical_age())
				self._PRW_age_noted.display_as_valid(False)
				return True

		self._PRW_age_noted.display_as_valid(True)
		self._PRW_age_noted.SetText(value = age_str, data = issue_age)

		if pat['dob'] is not None:
			fts = gmDateTime.cFuzzyTimestamp (
				timestamp = pat['dob'] + issue_age,
				accuracy = gmDateTime.acc_months
			)
			self._PRW_year_noted.SetText(value = str(fts), data = fts)

		return True
	#--------------------------------------------------------
	def _on_leave_year_noted(self, *args, **kwargs):

		if not self._PRW_year_noted.IsModified():
			return True

		year_noted = self._PRW_year_noted.GetData()

		if year_noted is None:
			if self._PRW_year_noted.GetValue().strip() == u'':
				self._PRW_year_noted.display_as_valid(True)
				return True
			self._PRW_year_noted.display_as_valid(False)
			return True

		year_noted = year_noted.get_pydt()

		if year_noted >= pydt.datetime.now(tz = year_noted.tzinfo):
			self.status_message = _('Condition diagnosed in the future.')
			self._PRW_year_noted.display_as_valid(False)
			return True

		self._PRW_year_noted.display_as_valid(True)

		pat = gmPerson.gmCurrentPatient()
		if pat['dob'] is not None:
			issue_age = year_noted - pat['dob']
			age_str = gmDateTime.format_interval_medically(interval = issue_age)
			self._PRW_age_noted.SetText(age_str, issue_age, True)

		return True
	#--------------------------------------------------------
	def _on_modified_age_noted(self, *args, **kwargs):
		wx.CallAfter(self._PRW_year_noted.SetText, u'', None, True)
		return True
	#--------------------------------------------------------
	def _on_modified_year_noted(self, *args, **kwargs):
		wx.CallAfter(self._PRW_age_noted.SetText, u'', None, True)
		return True
#================================================================
# diagnostic certainty related widgets/functions
#----------------------------------------------------------------
class cDiagnosticCertaintyClassificationPhraseWheel(gmPhraseWheel.cPhraseWheel):

	def __init__(self, *args, **kwargs):

		gmPhraseWheel.cPhraseWheel.__init__(self, *args, **kwargs)

		self.selection_only = False			# can be NULL, too

		mp = gmMatchProvider.cMatchProvider_FixedList (
			aSeq = [
				{'data': u'A', 'list_label': gmEMRStructItems.diagnostic_certainty_classification2str(u'A'), 'field_label': gmEMRStructItems.diagnostic_certainty_classification2str(u'A'), 'weight': 1},
				{'data': u'B', 'list_label': gmEMRStructItems.diagnostic_certainty_classification2str(u'B'), 'field_label': gmEMRStructItems.diagnostic_certainty_classification2str(u'B'), 'weight': 1},
				{'data': u'C', 'list_label': gmEMRStructItems.diagnostic_certainty_classification2str(u'C'), 'field_label': gmEMRStructItems.diagnostic_certainty_classification2str(u'C'), 'weight': 1},
				{'data': u'D', 'list_label': gmEMRStructItems.diagnostic_certainty_classification2str(u'D'), 'field_label': gmEMRStructItems.diagnostic_certainty_classification2str(u'D'), 'weight': 1}
			]
		)
		mp.setThresholds(1, 2, 4)
		self.matcher = mp

		self.SetToolTipString(_(
			"The diagnostic classification or grading of this assessment.\n"
			"\n"
			"This documents how certain one is about this being a true diagnosis."
		))

#================================================================
# MAIN
#----------------------------------------------------------------
if __name__ == '__main__':

	if len(sys.argv) < 2:
		sys.exit()

	if sys.argv[1] != 'test':
		sys.exit()

	from Gnumed.business import gmPersonSearch
	from Gnumed.wxpython import gmPatSearchWidgets

	#================================================================	
	class testapp (wx.App):
			"""
			Test application for testing EMR struct widgets
			"""
			#--------------------------------------------------------
			def OnInit (self):
				"""
				Create test application UI
				"""
				frame = wx.Frame (
							None,
							-4,
							'Testing EMR struct widgets',
							size=wx.Size(600, 400),
							style=wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE
						)
				filemenu= wx.Menu()
				filemenu.AppendSeparator()
				filemenu.Append(ID_EXIT,"E&xit"," Terminate test application")

				# Creating the menubar.	
				menuBar = wx.MenuBar()
				menuBar.Append(filemenu,"&File")

				frame.SetMenuBar(menuBar)

				txt = wx.StaticText( frame, -1, _("Select desired test option from the 'File' menu"),
				wx.DefaultPosition, wx.DefaultSize, 0 )

				# event handlers
				wx.EVT_MENU(frame, ID_EXIT, self.OnCloseWindow)

				# patient EMR
				self.__pat = gmPerson.gmCurrentPatient()

				frame.Show(1)
				return 1
			#--------------------------------------------------------
			def OnCloseWindow (self, e):
				"""
				Close test aplication
				"""
				self.ExitMainLoop ()

	#----------------------------------------------------------------
	def test_epsiode_edit_area_pnl():
		app = wx.PyWidgetTester(size = (200, 300))
		emr = pat.get_emr()
		epi = emr.get_episodes()[0]
		pnl = cEpisodeEditAreaPnl(app.frame, -1, episode=epi)
		app.frame.Show(True)
		app.MainLoop()
	#----------------------------------------------------------------
	def test_episode_edit_area_dialog():
		app = wx.PyWidgetTester(size = (200, 300))
		emr = pat.get_emr()
		epi = emr.get_episodes()[0]
		edit_episode(parent=app.frame, episode=epi)
	#----------------------------------------------------------------
	def test_hospital_stay_prw():
		app = wx.PyWidgetTester(size = (400, 40))
		app.SetWidget(cHospitalStayPhraseWheel, id=-1, size=(180,20), pos=(10,20))
		app.MainLoop()
	#----------------------------------------------------------------
	def test_episode_selection_prw():
		app = wx.PyWidgetTester(size = (400, 40))
		app.SetWidget(cEpisodeSelectionPhraseWheel, id=-1, size=(180,20), pos=(10,20))
#		app.SetWidget(cEpisodeSelectionPhraseWheel, id=-1, size=(350,20), pos=(10,20), patient_id=pat.ID)
		app.MainLoop()
	#----------------------------------------------------------------
	def test_health_issue_edit_area_dlg():
		app = wx.PyWidgetTester(size = (200, 300))
		edit_health_issue(parent=app.frame, issue=None)
	#----------------------------------------------------------------
	def test_health_issue_edit_area_pnl():
		app = wx.PyWidgetTester(size = (200, 300))
		app.SetWidget(cHealthIssueEditAreaPnl, id=-1, size = (400,400))
		app.MainLoop()
	#----------------------------------------------------------------
	def test_edit_procedure():
		app = wx.PyWidgetTester(size = (200, 300))
		edit_procedure(parent=app.frame)
	#================================================================

	# obtain patient
	pat = gmPersonSearch.ask_for_patient()
	if pat is None:
		print "No patient. Exiting gracefully..."
		sys.exit(0)
	gmPatSearchWidgets.set_active_patient(patient=pat)

#	try:
		# lauch emr dialogs test application
#		app = testapp(0)
#		app.MainLoop()
#	except Exception:
#		_log.exception("unhandled exception caught !")
		# but re-raise them
#		raise

	#test_epsiode_edit_area_pnl()
	#test_episode_edit_area_dialog()
	#test_health_issue_edit_area_dlg()
	#test_episode_selection_prw()
	test_hospital_stay_prw()
	#est_edit_procedure()
