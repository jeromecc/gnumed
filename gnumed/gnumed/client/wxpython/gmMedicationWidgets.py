"""GNUmed medication/substances handling widgets.
"""
#================================================================
__version__ = "$Revision: 1.33 $"
__author__ = "Karsten Hilbert <Karsten.Hilbert@gmx.net>"

import logging, sys, os.path, webbrowser, decimal


import wx, wx.grid


if __name__ == '__main__':
	sys.path.insert(0, '../../')
from Gnumed.pycommon import gmDispatcher, gmCfg, gmShellAPI, gmTools, gmDateTime
from Gnumed.pycommon import gmMatchProvider, gmI18N, gmPrinting, gmCfg2
from Gnumed.business import gmPerson, gmATC, gmSurgery, gmMedication, gmForms
from Gnumed.wxpython import gmGuiHelpers, gmRegetMixin, gmAuthWidgets, gmEditArea, gmMacro
from Gnumed.wxpython import gmCfgWidgets, gmListWidgets, gmPhraseWheel, gmFormWidgets
from Gnumed.wxpython import gmAllergyWidgets


_log = logging.getLogger('gm.ui')
_log.info(__version__)

#============================================================
# generic drug database access
#============================================================
def configure_drug_data_source(parent=None):
	gmCfgWidgets.configure_string_from_list_option (
		parent = parent,
		message = _(
			'\n'
			'Please select the default drug data source from the list below.\n'
			'\n'
			'Note that to actually use it you need to have the database installed, too.'
		),
		option = 'external.drug_data.default_source',
		bias = 'user',
		default_value = None,
		choices = gmMedication.drug_data_source_interfaces.keys(),
		columns = [_('Drug data source')],
		data = gmMedication.drug_data_source_interfaces.keys(),
		caption = _('Configuring default drug data source')
	)
#============================================================
def get_drug_database(parent = None):
	dbcfg = gmCfg.cCfgSQL()

	default_db = dbcfg.get2 (
		option = 'external.drug_data.default_source',
		workplace = gmSurgery.gmCurrentPractice().active_workplace,
		bias = 'workplace'
	)

	if default_db is None:
		gmDispatcher.send('statustext', msg = _('No default drug database configured.'), beep = True)
		configure_drug_data_source(parent = parent)
		default_db = dbcfg.get2 (
			option = 'external.drug_data.default_source',
			workplace = gmSurgery.gmCurrentPractice().active_workplace,
			bias = 'workplace'
		)
		if default_db is None:
			gmGuiHelpers.gm_show_error (
				aMessage = _('There is no default drug database configured.'),
				aTitle = _('Jumping to drug database')
			)
			return None

	try:
		drug_db = gmMedication.drug_data_source_interfaces[default_db]()
	except KeyError:
		_log.error('faulty default drug data source configuration: %s', default_db)
		return None

	pat = gmPerson.gmCurrentPatient()
	if pat.connected:
		drug_db.patient = pat

	return drug_db
#============================================================
def jump_to_drug_database():
	dbcfg = gmCfg.cCfgSQL()
	drug_db = get_drug_database()
	if drug_db is None:
		return
	drug_db.switch_to_frontend(blocking = False)

#============================================================
def jump_to_ifap(import_drugs=False):

	dbcfg = gmCfg.cCfgSQL()

	ifap_cmd = dbcfg.get2 (
		option = 'external.ifap-win.shell_command',
		workplace = gmSurgery.gmCurrentPractice().active_workplace,
		bias = 'workplace',
		default = 'wine "C:\Ifapwin\WIAMDB.EXE"'
	)
	found, binary = gmShellAPI.detect_external_binary(ifap_cmd)
	if not found:
		gmDispatcher.send('statustext', msg = _('Cannot call IFAP via [%s].') % ifap_cmd)
		return False
	ifap_cmd = binary

	if import_drugs:
		transfer_file = os.path.expanduser(dbcfg.get2 (
			option = 'external.ifap-win.transfer_file',
			workplace = gmSurgery.gmCurrentPractice().active_workplace,
			bias = 'workplace',
			default = '~/.wine/drive_c/Ifapwin/ifap2gnumed.csv'
		))
		# file must exist for Ifap to write into it
		try:
			f = open(transfer_file, 'w+b').close()
		except IOError:
			_log.exception('Cannot create IFAP <-> GNUmed transfer file [%s]', transfer_file)
			gmDispatcher.send('statustext', msg = _('Cannot create IFAP <-> GNUmed transfer file [%s].') % transfer_file)
			return False

	wx.BeginBusyCursor()
	gmShellAPI.run_command_in_shell(command = ifap_cmd, blocking = import_drugs)
	wx.EndBusyCursor()

	if import_drugs:
		# COMMENT: this file must exist PRIOR to invoking IFAP
		# COMMENT: or else IFAP will not write data into it ...
		try:
			csv_file = open(transfer_file, 'rb')						# FIXME: encoding
		except:
			_log.exception('cannot access [%s]', fname)
			csv_file = None

		if csv_file is not None:
			import csv
			csv_lines = csv.DictReader (
				csv_file,
				fieldnames = u'PZN Handelsname Form Abpackungsmenge Einheit Preis1 Hersteller Preis2 rezeptpflichtig Festbetrag Packungszahl Packungsgr\xf6\xdfe'.split(),
				delimiter = ';'
			)
			pat = gmPerson.gmCurrentPatient()
			emr = pat.get_emr()
			# dummy episode for now
			epi = emr.add_episode(episode_name = _('Current medication'))
			for line in csv_lines:
				narr = u'%sx %s %s %s (\u2258 %s %s) von %s (%s)' % (
					line['Packungszahl'].strip(),
					line['Handelsname'].strip(),
					line['Form'].strip(),
					line[u'Packungsgr\xf6\xdfe'].strip(),
					line['Abpackungsmenge'].strip(),
					line['Einheit'].strip(),
					line['Hersteller'].strip(),
					line['PZN'].strip()
				)
				emr.add_clin_narrative(note = narr, soap_cat = 's', episode = epi)
			csv_file.close()

	return True

#============================================================
# ATC related widgets
#============================================================

def browse_atc_reference(parent=None):

	if parent is None:
		parent = wx.GetApp().GetTopWindow()
	#------------------------------------------------------------
	def refresh(lctrl):
		atcs = gmATC.get_reference_atcs()

		items = [ [
			a['atc'],
			a['term'],
			u'%s' % gmTools.coalesce(a['ddd'], u''),
			gmTools.coalesce(a['unit'], u''),
			gmTools.coalesce(a['administrative_route'], u''),
			gmTools.coalesce(a['comment'], u''),
			a['version'],
			a['lang']
		] for a in atcs ]
		lctrl.set_string_items(items)
		lctrl.set_data(atcs)
	#------------------------------------------------------------
	gmListWidgets.get_choices_from_list (
		parent = parent,
		msg = _('\nThe ATC codes as known to GNUmed.\n'),
		caption = _('Showing ATC codes.'),
		columns = [ u'ATC', _('Term'), u'DDD', _('Unit'), _(u'Route'), _('Comment'), _('Version'), _('Language') ],
		single_selection = True,
		refresh_callback = refresh
	)

#============================================================

def update_atc_reference_data():

	dlg = wx.FileDialog (
		parent = None,
		message = _('Choose an ATC import config file'),
		defaultDir = os.path.expanduser(os.path.join('~', 'gnumed')),
		defaultFile = '',
		wildcard = "%s (*.conf)|*.conf|%s (*)|*" % (_('config files'), _('all files')),
		style = wx.OPEN | wx.HIDE_READONLY | wx.FILE_MUST_EXIST
	)

	result = dlg.ShowModal()
	if result == wx.ID_CANCEL:
		return

	cfg_file = dlg.GetPath()
	dlg.Destroy()

	conn = gmAuthWidgets.get_dbowner_connection(procedure = _('importing ATC reference data'))
	if conn is None:
		return False

	wx.BeginBusyCursor()

	if gmATC.atc_import(cfg_fname = cfg_file, conn = conn):
		gmDispatcher.send(signal = 'statustext', msg = _('Successfully imported ATC reference data.'))
	else:
		gmDispatcher.send(signal = 'statustext', msg = _('Importing ATC reference data failed.'), beep = True)

	wx.EndBusyCursor()
	return True

#============================================================

class cATCPhraseWheel(gmPhraseWheel.cPhraseWheel):

	def __init__(self, *args, **kwargs):

		gmPhraseWheel.cPhraseWheel.__init__(self, *args, **kwargs)

		query = u"""

			SELECT DISTINCT ON (label)
				atc_code,
				label
			FROM (

				SELECT
					code as atc_code,
					(code || ': ' || term || coalesce(' (' || ddd || unit || ')', ''))
						AS label
				FROM ref.atc
				WHERE
					term %(fragment_condition)s
						OR
					code %(fragment_condition)s

				UNION ALL

				SELECT
					atc_code,
					(atc_code || ': ' || description)
						AS label
				FROM ref.consumable_substance
				WHERE
					description %(fragment_condition)s
						OR
					atc_code %(fragment_condition)s

				UNION ALL

				SELECT
					atc_code,
					(atc_code || ': ' || description || ' (' || preparation || ')')
						AS label
				FROM ref.branded_drug
				WHERE
					description %(fragment_condition)s
						OR
					atc_code %(fragment_condition)s

				-- it would be nice to be able to include clin.vacc_indication but that's hard to do in SQL

			) AS candidates
			WHERE atc_code IS NOT NULL
			ORDER BY label
			LIMIT 50"""

		mp = gmMatchProvider.cMatchProvider_SQL2(queries = query)
		mp.setThresholds(1, 2, 4)
#		mp.word_separators = '[ \t=+&:@]+'
		self.SetToolTipString(_('Select an ATC (Anatomical-Therapeutic-Chemical) code.'))
		self.matcher = mp
		self.selection_only = True

#============================================================
# consumable substances widgets
#------------------------------------------------------------
def manage_consumable_substances(parent=None):

	if parent is None:
		parent = wx.GetApp().GetTopWindow()
	#------------------------------------------------------------
	def add_from_db(substance):
		drug_db = get_drug_database(parent = parent)
		if drug_db is None:
			return False
		drug_db.import_drugs()
		return True
	#------------------------------------------------------------
	def edit(substance=None):
		return edit_consumable_substance(parent = parent, substance = substance, single_entry = (substance is not None))
	#------------------------------------------------------------
	def delete(substance):
		if substance.is_in_use_by_patients:
			gmDispatcher.send(signal = 'statustext', msg = _('Cannot delete this substance. It is in use.'), beep = True)
			return False

		return gmMedication.delete_consumable_substance(substance = substance['pk'])
	#------------------------------------------------------------
	def refresh(lctrl):
		substs = gmMedication.get_consumable_substances(order_by = 'description')
		items = [ [
			s['description'],
			s['amount'],
			s['unit'],
			gmTools.coalesce(s['atc_code'], u''),
			s['pk']
		] for s in substs ]
		lctrl.set_string_items(items)
		lctrl.set_data(substs)
	#------------------------------------------------------------
	msg = _('\nThese are the consumable substances registered with GNUmed.\n')

	gmListWidgets.get_choices_from_list (
		parent = parent,
		msg = msg,
		caption = _('Showing consumable substances.'),
		columns = [_('Substance'), _('Amount'), _('Unit'), 'ATC', u'#'],
		single_selection = True,
		new_callback = edit,
		edit_callback = edit,
		delete_callback = delete,
		refresh_callback = refresh,
		left_extra_button = (_('Import'), _('Import consumable substances from a drug database.'), add_from_db)
	)

#------------------------------------------------------------
def edit_consumable_substance(parent=None, substance=None, single_entry=False):

	if substance is not None:
		if substance.is_in_use_by_patients:
			gmDispatcher.send(signal = 'statustext', msg = _('Cannot edit this substance. It is in use.'), beep = True)
			return False

	ea = cConsumableSubstanceEAPnl(parent = parent, id = -1)
	ea.data = substance
	ea.mode = gmTools.coalesce(substance, 'new', 'edit')
	dlg = gmEditArea.cGenericEditAreaDlg2(parent = parent, id = -1, edit_area = ea, single_entry = single_entry)
	dlg.SetTitle(gmTools.coalesce(substance, _('Adding new consumable substance'), _('Editing consumable substance')))
	if dlg.ShowModal() == wx.ID_OK:
		dlg.Destroy()
		return True
	dlg.Destroy()
	return False

#============================================================
from Gnumed.wxGladeWidgets import wxgConsumableSubstanceEAPnl

class cConsumableSubstanceEAPnl(wxgConsumableSubstanceEAPnl.wxgConsumableSubstanceEAPnl, gmEditArea.cGenericEditAreaMixin):

	def __init__(self, *args, **kwargs):

		try:
			data = kwargs['substance']
			del kwargs['substance']
		except KeyError:
			data = None

		wxgConsumableSubstanceEAPnl.wxgConsumableSubstanceEAPnl.__init__(self, *args, **kwargs)
		gmEditArea.cGenericEditAreaMixin.__init__(self)

		# Code using this mixin should set mode and data
		# after instantiating the class:
		self.mode = 'new'
		self.data = data
		if data is not None:
			self.mode = 'edit'

#		self.__init_ui()
	#----------------------------------------------------------------
#	def __init_ui(self):
#		self._PRW_atc.selection_only = False
	#----------------------------------------------------------------
	# generic Edit Area mixin API
	#----------------------------------------------------------------
	def _valid_for_save(self):

		validity = True

		if self._TCTRL_substance.GetValue().strip() == u'':
			validity = False
			self.display_tctrl_as_valid(tctrl = self._TCTRL_substance, valid = False)
			self._TCTRL_substance.SetFocus()
		else:
			self.display_tctrl_as_valid(tctrl = self._TCTRL_substance, valid = True)

		try:
			decimal.Decimal(self._TCTRL_amount.GetValue().strip().replace(',', '.'))
			self.display_tctrl_as_valid(tctrl = self._TCTRL_amount, valid = True)
		except (TypeError, decimal.InvalidOperation):
			validity = False
			self.display_tctrl_as_valid(tctrl = self._TCTRL_amount, valid = False)
			self._TCTRL_amount.SetFocus()

		if self._PRW_unit.GetValue().strip() == u'':
			validity = False
			self._PRW_unit.display_as_valid(valid = False)
			self._TCTRL_substance.SetFocus()
		else:
			self._PRW_unit.display_as_valid(valid = True)

		if validity is False:
			gmDispatcher.send(signal = 'statustext', msg = _('Cannot save consumable substance. Missing essential input.'))

		return validity
	#----------------------------------------------------------------
	def _save_as_new(self):
		subst = gmMedication.create_consumable_substance (
			substance = self._TCTRL_substance.GetValue().strip(),
			atc = self._PRW_atc.GetData(),
			amount = decimal.Decimal(self._TCTRL_amount.GetValue().strip().replace(',', '.')),
			unit = gmTools.coalesce(self._PRW_unit.GetData(), self._PRW_unit.GetValue().strip(), function_initial = ('strip', None))
		)
		success, data = subst.save()
		if not success:
			err, msg = data
			_log.error(err)
			_log.error(msg)
			gmDispatcher.send(signal = 'statustext', msg = _('Cannot save consumable substance. %s') % msg, beep = True)
			return False

		self.data = subst
		return True
	#----------------------------------------------------------------
	def _save_as_update(self):
		self.data['description'] = self._TCTRL_substance.GetValue().strip()
		self.data['atc_code'] = self._PRW_atc.GetData()
		self.data['amount'] = decimal.Decimal(self._TCTRL_amount.GetValue().strip().replace(',', '.'))
		self.data['unit'] = gmTools.coalesce(self._PRW_unit.GetData(), self._PRW_unit.GetValue().strip(), function_initial = ('strip', None))
		success, data = self.data.save()

		if not success:
			err, msg = data
			_log.error(err)
			_log.error(msg)
			gmDispatcher.send(signal = 'statustext', msg = _('Cannot save consumable substance. %s') % msg, beep = True)
			return False

		return True
	#----------------------------------------------------------------
	def _refresh_as_new(self):
		self._TCTRL_substance.SetValue(u'')
		self._TCTRL_amount.SetValue(u'')
		self._PRW_unit.SetText(u'', None)
		self._PRW_atc.SetText(u'', None)

		self._TCTRL_substance.SetFocus()
	#----------------------------------------------------------------
	def _refresh_from_existing(self):
		self._TCTRL_substance.SetValue(self.data['description'])
		self._TCTRL_amount.SetValue(u'%s' % self.data['amount'])
		self._PRW_unit.SetText(self.data['unit'], self.data['unit'])
		self._PRW_atc.SetText(gmTools.coalesce(self.data['atc_code'], u''), self.data['atc_code'])

		self._TCTRL_substance.SetFocus()
	#----------------------------------------------------------------
	def _refresh_as_new_from_existing(self):
		self._refresh_as_new()

#============================================================
# drug component widgets
#------------------------------------------------------------
def manage_drug_components(parent=None):

	if parent is None:
		parent = wx.GetApp().GetTopWindow()

	#------------------------------------------------------------
	def edit(component=None):
		substance = gmMedication.cConsumableSubstance(aPK_obj = component['pk_consumable_substance'])
		return edit_consumable_substance(parent = parent, substance = substance, single_entry = True)
	#------------------------------------------------------------
	def delete(component):
		if component.is_in_use_by_patients:
			gmDispatcher.send(signal = 'statustext', msg = _('Cannot remove this component from the drug. It is in use.'), beep = True)
			return False

		return component.containing_drug.remove_component(substance = component['pk_component'])
	#------------------------------------------------------------
	def refresh(lctrl):
		comps = gmMedication.get_drug_components()
		items = [ [
			u'%s%s' % (c['brand'], gmTools.coalesce(c['atc_brand'], u'', u' [%s]')),
			u'%s%s' % (c['substance'], gmTools.coalesce(c['atc_substance'], u'', u' [%s]')),
			u'%s%s' % (c['amount'], c['unit']),
			c['preparation'],
			gmTools.coalesce(c['external_code_brand'], u'', u'%%s [%s]' % c['external_code_type_brand']),
			c['pk_component']
		] for c in comps ]
		lctrl.set_string_items(items)
		lctrl.set_data(comps)
	#------------------------------------------------------------
	msg = _('\nThese are the components in the drug brands known to GNUmed.\n')

	gmListWidgets.get_choices_from_list (
		parent = parent,
		msg = msg,
		caption = _('Showing drug brand components.'),
		columns = [_('Brand'), _('Substance'), _('Strength'), _('Preparation'), _('Code'), u'#'],
		single_selection = True,
		#new_callback = edit,
		edit_callback = edit,
		delete_callback = delete,
		refresh_callback = refresh
	)

#------------------------------------------------------------
def edit_drug_component(parent=None, drug_component=None, single_entry=False):
	ea = cDrugComponentEAPnl(parent = parent, id = -1)
	ea.data = drug_component
	ea.mode = gmTools.coalesce(drug_component, 'new', 'edit')
	dlg = gmEditArea.cGenericEditAreaDlg2(parent = parent, id = -1, edit_area = ea, single_entry = single_entry)
	dlg.SetTitle(gmTools.coalesce(drug_component, _('Adding new drug component'), _('Editing drug component')))
	if dlg.ShowModal() == wx.ID_OK:
		dlg.Destroy()
		return True
	dlg.Destroy()
	return False

#============================================================
from Gnumed.wxGladeWidgets import wxgDrugComponentEAPnl

class cDrugComponentEAPnl(wxgDrugComponentEAPnl.wxgDrugComponentEAPnl, gmEditArea.cGenericEditAreaMixin):

	def __init__(self, *args, **kwargs):

		try:
			data = kwargs['component']
			del kwargs['component']
		except KeyError:
			data = None

		wxgDrugComponentEAPnl.wxgDrugComponentEAPnl.__init__(self, *args, **kwargs)
		gmEditArea.cGenericEditAreaMixin.__init__(self)

		# Code using this mixin should set mode and data
		# after instantiating the class:
		self.mode = 'new'
		self.data = data
		if data is not None:
			self.mode = 'edit'

		#self.__init_ui()
	#----------------------------------------------------------------
#	def __init_ui(self):
#		# adjust phrasewheels etc
	#----------------------------------------------------------------
	# generic Edit Area mixin API
	#----------------------------------------------------------------
	def _valid_for_save(self):
		if self.data is not None:
			if self.data['is_in_use']:
				gmDispatcher.send(signal = 'statustext', msg = _('Cannot edit drug component. It is in use.'), beep = True)
				return False

		validity = True

		if self._PRW_substance.GetData() is None:
			validity = False
			self._PRW_substance.display_as_valid(False)
		else:
			self._PRW_substance.display_as_valid(True)

		val = self._TCTRL_amount.GetValue().strip().replace(',', u'.', 1)
		try:
			decimal.Decimal(val)
			self.display_tctrl_as_valid(tctrl = self._TCTRL_amount, valid = True)
		except:
			validity = False
			self.display_tctrl_as_valid(tctrl = self._TCTRL_amount, valid = False)

		if self._PRW_unit.GetValue().strip() == u'':
			validity = False
			self._PRW_unit.display_as_valid(False)
		else:
			self._PRW_unit.display_as_valid(True)

		if validity is False:
			gmDispatcher.send(signal = 'statustext', msg = _('Cannot save drug component. Invalid or missing essential input.'))

		return validity
	#----------------------------------------------------------------
	def _save_as_new(self):
		# save the data as a new instance
		data = 1
		data[''] = 1
		data[''] = 1
#		data.save()

		# must be done very late or else the property access
		# will refresh the display such that later field
		# access will return empty values
#		self.data = data
		return False
		return True
	#----------------------------------------------------------------
	def _save_as_update(self):
		self.data['pk_consumable_substance'] = self._PRW_substance.GetData(can_create = True)
		self.data['amount'] = decimal.Decimal(self._TCTRL_amount.GetValue().strip().replace(',', u'.', 1))
		self.data['unit'] = self._PRW_unit.GetValue().strip()
		return self.data.save()
	#----------------------------------------------------------------
	def _refresh_as_new(self):
		self._TCTRL_brand.SetValue(u'')
		self._TCTRL_components.SetValue(u'')
		self._TCTRL_codes.SetValue(u'')
		self._PRW_substance.SetText(u'', None)
		self._TCTRL_amount.SetValue(u'')
		self._PRW_unit.SetText(u'', None)

		self._PRW_substance.SetFocus()
	#----------------------------------------------------------------
	def _refresh_from_existing(self):
		self._TCTRL_brand.SetValue(u'%s (%s)' % (self.data['brand'], self.data['preparation']))
		self._TCTRL_components.SetValue(u' / '.join(self.data.containing_drug['components']))
		details = []
		if self.data['atc_brand'] is not None:
			details.append(u'ATC: %s' % self.data['atc_brand'])
		if self.data['external_code_brand'] is not None:
			details.append(u'%s: %s' % (self.data['external_code_type_brand'], self.data['external_code_brand']))
		self._TCTRL_codes.SetValue(u'; '.join(details))

		self._PRW_substance.SetText(self.data['substance'], self.data['pk_consumable_substance'])
		self._TCTRL_amount.SetValue(u'%s' % self.data['amount'])
		self._PRW_unit.SetText(self.data['unit'], self.data['unit'])

		self._PRW_substance.SetFocus()
	#----------------------------------------------------------------
	def _refresh_as_new_from_existing(self):
		#self._PRW_brand.SetText(u'', None)
		#self._TCTRL_prep.SetValue(u'')
		#self._TCTRL_brand_details.SetValue(u'')
		self._PRW_substance.SetText(u'', None)
		self._TCTRL_amount.SetValue(u'')
		self._PRW_unit.SetText(u'', None)

		self._PRW_substance.SetFocus()

#============================================================
class cDrugComponentPhraseWheel(gmPhraseWheel.cPhraseWheel):

	def __init__(self, *args, **kwargs):

		query = u"""
			SELECT
				pk_component,
				(substance || ' ('  || amount || unit || ' ' || preparation || ')')
					AS component
			FROM ref.v_drug_components
			WHERE substance %(fragment_condition)s
			ORDER BY substance, amount, preparation
			LIMIT 50"""

		mp = gmMatchProvider.cMatchProvider_SQL2(queries = query)
		mp.setThresholds(2, 3, 4)
		gmPhraseWheel.cPhraseWheel.__init__(self, *args, **kwargs)
		self.SetToolTipString(_('A drug component.'))
		self.matcher = mp
		self.selection_only = False

#============================================================
#============================================================
class cSubstancePreparationPhraseWheel(gmPhraseWheel.cPhraseWheel):

	def __init__(self, *args, **kwargs):

		query = u"""
(
	SELECT DISTINCT ON (preparation)
		preparation as prep, preparation
	FROM ref.branded_drug
	WHERE preparation %(fragment_condition)s
) UNION (
	SELECT DISTINCT ON (preparation)
		preparation as prep, preparation
	FROM clin.substance_intake
	WHERE preparation %(fragment_condition)s
)
ORDER BY prep
limit 30"""

		mp = gmMatchProvider.cMatchProvider_SQL2(queries = query)
		mp.setThresholds(1, 2, 4)
		gmPhraseWheel.cPhraseWheel.__init__(self, *args, **kwargs)
		self.SetToolTipString(_('The preparation (form) of the substance or brand.'))
		self.matcher = mp
		self.selection_only = False
#============================================================
class cSubstancePhraseWheel(gmPhraseWheel.cPhraseWheel):

	def __init__(self, *args, **kwargs):

		query = u"""
(
	SELECT
		pk::text,
		description as subst
		--(description || coalesce(' [' || atc_code || ']', '')) as subst
	FROM ref.consumable_substance
	WHERE description %(fragment_condition)s

) UNION (

	SELECT
		term,
		term as subst
		--NULL,
		--(term || ' [' || atc || ']') as subst
	FROM ref.v_atc
	WHERE
		is_group_code IS FALSE
			AND
		term %(fragment_condition)s
)
ORDER BY subst
LIMIT 50"""

		mp = gmMatchProvider.cMatchProvider_SQL2(queries = query)
		mp.setThresholds(1, 2, 4)
		gmPhraseWheel.cPhraseWheel.__init__(self, *args, **kwargs)
		self.SetToolTipString(_('The preparation (form) of the substance or brand in question.'))
		self.matcher = mp
		self.selection_only = False
	#---------------------------------------------------------
	def GetData(self, can_create=False, as_instance=False):

		if self.data is not None:
			try:
				int(self.data)
			except ValueError:
				self.data = None

		return super(cSubstancePhraseWheel, self).GetData(can_create = can_create, as_instance = as_instance)

#============================================================
# branded drugs widgets
#------------------------------------------------------------
def manage_components_of_branded_drug(parent=None, brand=None):

	if brand is not None:
		if brand['is_in_use']:
			gmGuiHelpers.gm_show_info (
				aTitle = _('Managing components of a drug'),
				aMessage = _(
					'Cannot manage the components of the branded drug product\n'
					'\n'
					' "%s" (%s)\n'
					'\n'
					'because it is currently taken by patients.\n'
				) % (brand['brand'], brand['preparation'])
			)
			return False
	#--------------------------------------------------------
	if parent is None:
		parent = wx.GetApp().GetTopWindow()
	#--------------------------------------------------------
	if brand is None:
		msg = _('Pick the substances which are components of this drug.')
		right_col = _('Components of drug')
		comp_substs = []
	else:
		right_col = u'%s (%s)' % (brand['brand'], brand['preparation'])
		msg = _(
			'Adjust the components of "%s"\n'
			'\n'
			'The drug must contain at least one component. Any given\n'
			'substance can only be included once per drug.'
		) % right_col
		comp_substs = [ c.substance for c in brand.components ]

	substs = gmMedication.get_consumable_substances(order_by = 'description')
	choices = [ u'%s %s%s' % (s['description'], s['amount'], s['unit']) for s in substs ]
	picks = [ u'%s %s%s' % (c['description'], c['amount'], c['unit']) for c in comp_substs ]

	picker = gmListWidgets.cItemPickerDlg (
		parent,
		-1,
		title = _('Managing components of a drug ...'),
		msg = msg
	)
	picker.set_columns(['Substances'], [right_col])
	picker.set_choices(choices = choices, data = substs)
	picker.set_picks(picks = picks, data = comp_substs)

	btn_pressed = picker.ShowModal()
	substs = picker.get_picks()
	picker.Destroy()

	if btn_pressed != wx.ID_OK:
		return (False, None)

	if brand is not None:
		brand.set_substances_as_components(substances = substs)

	return (True, substs)
#------------------------------------------------------------
def manage_branded_drugs(parent=None):

	if parent is None:
		parent = wx.GetApp().GetTopWindow()
	#------------------------------------------------------------
	def add_from_db(brand):
		drug_db = get_drug_database(parent = parent)
		if drug_db is None:
			return False
		drug_db.import_drugs()
		return True
	#------------------------------------------------------------
	def get_tooltip(brand=None):
		tt = u'%s %s\n' % (brand['brand'], brand['preparation'])
		tt += u'\n'
		tt += u'%s%s%s\n' % (
			gmTools.bool2subst(brand.is_vaccine, u'%s, ' % _('Vaccine'), u''),
			u'%s, ' % gmTools.bool2subst(brand['is_in_use'], _('in use'), _('not in use')),
			gmTools.bool2subst(brand['is_fake_brand'], _('fake'), u'')
		)
		tt += gmTools.coalesce(brand['atc'], u'', _('ATC: %s\n'))
		tt += gmTools.coalesce(brand['external_code'], u'', u'%s: %%s\n' % brand['external_code_type'])
		if brand['components'] is not None:
			tt += u'- %s' % u'\n- '.join(brand['components'])
		return tt
	#------------------------------------------------------------
	def edit(brand=None):
		if brand.is_vaccine:
			gmGuiHelpers.gm_show_info (
				aTitle = _('Editing medication'),
				aMessage = _(
					'Cannot edit the medication\n'
					'\n'
					' "%s" (%s)\n'
					'\n'
					'because it is a vaccine. Please edit it\n'
					'from the vaccine management section !\n'
				) % (brand['brand'], brand['preparation'])
			)
			return False

		return edit_branded_drug(parent = parent, branded_drug = brand, single_entry = True)
	#------------------------------------------------------------
	def delete(brand):
		if brand.is_vaccine:
			gmGuiHelpers.gm_show_info (
				aTitle = _('Deleting medication'),
				aMessage = _(
					'Cannot delete the medication\n'
					'\n'
					' "%s" (%s)\n'
					'\n'
					'because it is a vaccine. Please delete it\n'
					'from the vaccine management section !\n'
				) % (brand['brand'], brand['preparation'])
			)
			return False
		gmMedication.delete_branded_drug(brand = brand['pk_brand'])
		return True
	#------------------------------------------------------------
	def new():
		return edit_branded_drug(parent = parent, branded_drug = None, single_entry = False)
	#------------------------------------------------------------
	def refresh(lctrl):
		drugs = gmMedication.get_branded_drugs()
		items = [ [
			u'%s%s' % (
				d['brand'],
				gmTools.bool2subst(d['is_fake_brand'], ' (%s)' % _('fake'), u'')
			),
			d['preparation'],
			gmTools.coalesce(d['atc'], u''),
			gmTools.coalesce(d['components'], u''),
			gmTools.coalesce(d['external_code'], u'', u'%%s [%s]' % d['external_code_type']),
			d['pk_brand']
		] for d in drugs ]
		lctrl.set_string_items(items)
		lctrl.set_data(drugs)
	#------------------------------------------------------------
	msg = _('\nThese are the drug brands known to GNUmed.\n')

	gmListWidgets.get_choices_from_list (
		parent = parent,
		msg = msg,
		caption = _('Showing branded drugs.'),
		columns = [_('Name'), _('Preparation'), _('ATC'), _('Components'), _('Code'), u'#'],
		single_selection = True,
		refresh_callback = refresh,
		new_callback = new,
		edit_callback = edit,
		delete_callback = delete,
		list_tooltip_callback = get_tooltip,
		left_extra_button = (_('Import'), _('Import substances and brands from a drug database.'), add_from_db)
		#, middle_extra_button = (_('Clone'), _('Clone selected drug into a new entry for editing.'), clone_from_existing)
		#, right_extra_button = (_('Reassign'), _('Reassign all patients taking the selected drug to another drug.'), reassign_patients)
	)

#------------------------------------------------------------
def edit_branded_drug(parent=None, branded_drug=None, single_entry=False):
	if branded_drug is not None:
		if branded_drug['is_in_use']:
			gmGuiHelpers.gm_show_info (
				aTitle = _('Editing drug'),
				aMessage = _(
					'Cannot edit the branded drug product\n'
					'\n'
					' "%s" (%s)\n'
					'\n'
					'because it is currently taken by patients.\n'
				) % (branded_drug['brand'], branded_drug['preparation'])
			)
			return False

	ea = cBrandedDrugEAPnl(parent = parent, id = -1)
	ea.data = branded_drug
	ea.mode = gmTools.coalesce(branded_drug, 'new', 'edit')
	dlg = gmEditArea.cGenericEditAreaDlg2(parent = parent, id = -1, edit_area = ea, single_entry = single_entry)
	dlg.SetTitle(gmTools.coalesce(branded_drug, _('Adding new drug brand'), _('Editing drug brand')))
	if dlg.ShowModal() == wx.ID_OK:
		dlg.Destroy()
		return True
	dlg.Destroy()
	return False

#============================================================
from Gnumed.wxGladeWidgets import wxgBrandedDrugEAPnl

class cBrandedDrugEAPnl(wxgBrandedDrugEAPnl.wxgBrandedDrugEAPnl, gmEditArea.cGenericEditAreaMixin):

	def __init__(self, *args, **kwargs):

		try:
			data = kwargs['drug']
			del kwargs['drug']
		except KeyError:
			data = None

		wxgBrandedDrugEAPnl.wxgBrandedDrugEAPnl.__init__(self, *args, **kwargs)
		gmEditArea.cGenericEditAreaMixin.__init__(self)

		self.mode = 'new'
		self.data = data
		if data is not None:
			self.mode = 'edit'
			self.__component_substances = data.components_as_substances

		#self.__init_ui()
	#----------------------------------------------------------------
#	def __init_ui(self):
		# adjust external type PRW
	#----------------------------------------------------------------
	# generic Edit Area mixin API
	#----------------------------------------------------------------
	def _valid_for_save(self):

		if self.data is not None:
			if self.data['is_in_use']:
				gmDispatcher.send(signal = 'statustext', msg = _('Cannot edit drug brand. It is in use.'), beep = True)
				return False

		validity = True

		if self._PRW_brand.GetValue().strip() == u'':
			validity = False
			self._PRW_brand.display_as_valid(False)
		else:
			self._PRW_brand.display_as_valid(True)

		if self._PRW_preparation.GetValue().strip() == u'':
			validity = False
			self._PRW_preparation.display_as_valid(False)
		else:
			self._PRW_preparation.display_as_valid(True)

		if validity is False:
			gmDispatcher.send(signal = 'statustext', msg = _('Cannot save branded drug. Invalid or missing essential input.'))

		return validity
	#----------------------------------------------------------------
	def _save_as_new(self):

		drug = gmMedication.create_branded_drug (
			brand_name = self._PRW_brand.GetValue().strip(),
			preparation = gmTools.coalesce (
				self._PRW_preparation.GetData(),
				self._PRW_preparation.GetValue()
			).strip(),
			return_existing = True
		)
		drug['is_fake_brand'] = self._CHBOX_is_fake.GetValue()
		drug['atc'] = self._PRW_atc.GetData()
		code = self._TCTRL_external_code.GetValue().strip()
		if code != u'':
			drug['external_code'] = code
			drug['external_code_type'] = self._PRW_external_code_type.GetData().strip()

		drug.save()

		if len(self.__component_substances) > 0:
			drug.set_substances_as_components(substances = self.__component_substances)

		self.data = drug

		return True
	#----------------------------------------------------------------
	def _save_as_update(self):
		self.data['brand'] = self._PRW_brand.GetValue().strip()
		self.data['preparation'] = gmTools.coalesce (
			self._PRW_preparation.GetData(),
			self._PRW_preparation.GetValue()
		).strip()
		self.data['is_fake_brand'] = self._CHBOX_is_fake.GetValue()
		self.data['atc'] = self._PRW_atc.GetData()
		code = self._TCTRL_external_code.GetValue().strip()
		if code != u'':
			self.data['external_code'] = code
			self.data['external_code_type'] = self._PRW_external_code_type.GetData().strip()
		success, data = self.data.save()
		if not success:
			err, msg = data
			_log.error('problem saving')
			_log.error('%s', err)
			_log.error('%s', msg)
		return (success is True)
	#----------------------------------------------------------------
	def _refresh_as_new(self):
		self._PRW_brand.SetText(u'', None)
		self._PRW_preparation.SetText(u'', None)
		self._CHBOX_is_fake.SetValue(False)
		self._TCTRL_components.SetValue(u'')
		self._PRW_atc.SetText(u'', None)
		self._TCTRL_external_code.SetValue(u'')
		self._PRW_external_code_type.SetText(u'', None)

		self._PRW_brand.SetFocus()

		self.__component_substances = []
	#----------------------------------------------------------------
	def _refresh_as_new_from_existing(self):
		self._refresh_as_new()
	#----------------------------------------------------------------
	def _refresh_from_existing(self):
		self._PRW_brand.SetText(self.data['brand'], self.data['pk_brand'])
		self._PRW_preparation.SetText(self.data['preparation'], self.data['preparation'])
		self._CHBOX_is_fake.SetValue(self.data['is_fake_brand'])
		comps = u''
		if self.data['components'] is not None:
			comps = u'- %s' % u'\n- '.join(self.data['components'])
		self._TCTRL_components.SetValue(comps)
		self._PRW_atc.SetText(gmTools.coalesce(self.data['atc'], u''), self.data['atc'])
		self._TCTRL_external_code.SetValue(gmTools.coalesce(self.data['external_code'], u''))
		t = gmTools.coalesce(self.data['external_code_type'], u'')
		self._PRW_external_code_type.SetText(t, t)

		self._PRW_brand.SetFocus()

		self.__component_substances = self.data.components_as_substances
	#----------------------------------------------------------------
	# event handler
	#----------------------------------------------------------------
	def _on_manage_components_button_pressed(self, event):
		event.Skip()
		OKed, substs = manage_components_of_branded_drug(parent = self, brand = self.data)
		if OKed is True:
			self.__component_substances = substs
			comps = u''
			if len(substs) > 0:
				comps = u'- %s' % u'\n- '.join([ u'%s %s%s' % (s['description'], s['amount'], s['unit']) for s in substs ])
			self._TCTRL_components.SetValue(comps)
#============================================================
class cBrandedDrugPhraseWheel(gmPhraseWheel.cPhraseWheel):

	def __init__(self, *args, **kwargs):

		query = u"""
			SELECT
				pk,
				(description || ' (' || preparation || ')' || coalesce(' [' || atc_code || ']', ''))
					AS brand
			FROM ref.branded_drug
			WHERE description %(fragment_condition)s
			ORDER BY brand
			LIMIT 50"""

		mp = gmMatchProvider.cMatchProvider_SQL2(queries = query)
		mp.setThresholds(2, 3, 4)
		gmPhraseWheel.cPhraseWheel.__init__(self, *args, **kwargs)
		self.SetToolTipString(_('The brand name of the drug.'))
		self.matcher = mp
		self.selection_only = False

#============================================================
# current substance intake widgets
#------------------------------------------------------------
class cSubstanceSchedulePhraseWheel(gmPhraseWheel.cPhraseWheel):

	def __init__(self, *args, **kwargs):

		query = u"""
SELECT DISTINCT ON (sched)
	schedule as sched,
	schedule
FROM clin.substance_intake
WHERE schedule %(fragment_condition)s
ORDER BY sched
LIMIT 50"""

		mp = gmMatchProvider.cMatchProvider_SQL2(queries = query)
		mp.setThresholds(1, 2, 4)
		mp.word_separators = '[ \t=+&:@]+'
		gmPhraseWheel.cPhraseWheel.__init__(self, *args, **kwargs)
		self.SetToolTipString(_('The schedule for taking this substance.'))
		self.matcher = mp
		self.selection_only = False

#============================================================
from Gnumed.wxGladeWidgets import wxgCurrentMedicationEAPnl

class cCurrentMedicationEAPnl(wxgCurrentMedicationEAPnl.wxgCurrentMedicationEAPnl, gmEditArea.cGenericEditAreaMixin):

	def __init__(self, *args, **kwargs):

		try:
			data = kwargs['substance']
			del kwargs['substance']
		except KeyError:
			data = None

		wxgCurrentMedicationEAPnl.wxgCurrentMedicationEAPnl.__init__(self, *args, **kwargs)
		gmEditArea.cGenericEditAreaMixin.__init__(self)
		self.mode = 'new'
		self.data = data
		if data is not None:
			self.mode = 'edit'

		self.__init_ui()
	#----------------------------------------------------------------
	def __init_ui(self):

		self._PRW_brand.add_callback_on_lose_focus(callback = self._on_leave_brand)
		self._PRW_substance.add_callback_on_lose_focus(callback = self._on_leave_substance)
	#----------------------------------------------------------------
	def __refresh_allergies(self):
		emr = gmPerson.gmCurrentPatient().get_emr()

		state = emr.allergy_state
		if state['last_confirmed'] is None:
			confirmed = _('never')
		else:
			confirmed = state['last_confirmed'].strftime('%Y %B %d').decode(gmI18N.get_encoding())
		msg = _(u'%s, last confirmed %s\n') % (state.state_string, confirmed)
		msg += gmTools.coalesce(state['comment'], u'', _('Comment (%s): %%s\n') % state['modified_by'])
		msg += u'\n'

		for allergy in emr.get_allergies():
			msg += u'%s (%s, %s): %s\n' % (
				allergy['descriptor'],
				allergy['l10n_type'],
				gmTools.bool2subst(allergy['definite'], _('definite'), _('suspected'), u'?'),
				gmTools.coalesce(allergy['reaction'], _('reaction not recorded'))
			)

		self._LBL_allergies.SetLabel(msg)
	#----------------------------------------------------------------
	def __refresh_brand_and_components(self):

		if self._PRW_brand.GetData() is None:
			self._TCTRL_brand_ingredients.SetValue(u'')
			if self.data is None:
				return
			if self.data['pk_brand'] is None:
				return
			self._PRW_brand.SetText(self.data['brand'], self.data['pk_brand'])

		brand = gmMedication.cBrandedDrug(aPK_obj = self._PRW_brand.GetData())

		if self.data is None:
			self._PRW_preparation.SetText(brand['preparation'], None)
		else:
			self._PRW_preparation.SetText (
				gmTools.coalesce(self.data['preparation'], brand['preparation']),
				self.data['preparation']
			)

#		comps = brand.components
#
#		if comps is None:
#			return
#
#		if len(comps) == 0:
#			return
#
#		comps = u' / '.join([ u'%s%s' % (c['description'], gmTools.coalesce(c['atc_code'], u'', u' (%s)')) for c in comps ])
#		self._TCTRL_brand_ingredients.SetValue(comps)
		if brand['components'] is None:
			self._TCTRL_brand_ingredients.SetValue(u'')
		else:
			self._TCTRL_brand_ingredients.SetValue(u' / '.join(brand['components']))
	#----------------------------------------------------------------
	# generic Edit Area mixin API
	#----------------------------------------------------------------
	def _valid_for_save(self):

		validity = True

		has_brand = (self._PRW_brand.GetData() is not None)
		has_substance = (self._PRW_substance.GetValue().strip() == u'')

		# must have either brand or substance
		if not (has_brand or has_substance):
			self._PRW_substance.display_as_valid(False)
			self._PRW_brand.display_as_valid(False)
			validity = False
		else:
			self._PRW_substance.display_as_valid(True)
			self._PRW_brand.display_as_valid(True)

		# brands must have components or they cannot be used
		if has_brand:
			brand = gmMedication.cBrandedDrug(aPK_obj = self._PRW_brand.GetData())
			if len(brand.components) == 0:
				self._PRW_brand.display_as_valid(False)
				validity = False

		# brands already have a preparation, so only required for substances
		if not has_brand:
			if self._PRW_preparation.GetValue().strip() == u'':
				self._PRW_preparation.display_as_valid(False)
				validity = False
			else:
				self._PRW_preparation.display_as_valid(True)

		# episode must be set if intake is to be approved of
		if self._CHBOX_approved.IsChecked():
			if self._PRW_episode.GetValue().strip() == u'':
				self._PRW_episode.display_as_valid(False)
				validity = False
			else:
				self._PRW_episode.display_as_valid(True)

		# huh ?
		if self._CHBOX_approved.IsChecked() is True:
			self._PRW_duration.display_as_valid(True)
		else:
			if self._PRW_duration.GetValue().strip() in [u'', gmTools.u_infinity]:
				self._PRW_duration.display_as_valid(True)
			else:
				if gmDateTime.str2interval(self._PRW_duration.GetValue()) is None:
					self._PRW_duration.display_as_valid(False)
					validity = False
				else:
					self._PRW_duration.display_as_valid(True)

		# end must be > start if at all
		end = self._DP_discontinued.GetValue(as_pydt = True, invalid_as_none = True)
		if end is not None:
			start = self._DP_started.GetValue(as_pydt = True)
			if start > end:
				self._DP_started.display_as_valid(False)
				self._DP_discontinued.display_as_valid(False)
				validity = False
			else:
				self._DP_started.display_as_valid(True)
				self._DP_discontinued.display_as_valid(True)

		if validity is False:
			gmDispatcher.send(signal = 'statustext', msg = _('Cannot save substance intake. Invalid or missing essential input.'))

		return validity
	#----------------------------------------------------------------
	def _save_as_new(self):

		pk_brand = self._PRW_brand.GetData()
		brand = None

		if pk_brand is None:
			prep = self._PRW_preparation.GetValue()
			if self._PRW_substance.GetData() is None:
				subst = self._PRW_substance.GetValue().strip()
			else:
				# normalize, do not simply re-use name from phrasewheel
				subst = gmMedication.cConsumableSubstance(aPK_obj = self._PRW_substance.GetData())['description']
			substances = [
				[subst['description'], self._PRW_strength.GetValue()]
			]
		else:
			brand = gmMedication.cBrandedDrug(aPK_obj = pk_brand)
			prep = brand['preparation']
			comps = brand.components
			if len(comps) == 1:
				substances = [
					[comps['substance'], self._PRW_strength.GetValue()]
				]
			else:
				# loop and ask for strengths
				print "missing"

		emr = gmPerson.gmCurrentPatient().get_emr()
		epi = self._PRW_episode.GetData(can_create = True)

		# now loop over substances either from brand or from input
		last_intake = None
		for subst, strength in substances:
			intake = emr.add_substance_intake (
				substance = subst,
				episode = epi,
				preparation = prep,
				amount = None,				# FIXME
				unit = None
			)
			intake['strength'] = strength
			intake['started'] = self._DP_started.GetValue(as_pydt = True, invalid_as_none = True)
			intake['discontinued'] = self._DP_discontinued.GetValue(as_pydt = True, invalid_as_none = True)
			if intake['discontinued'] is None:
				intake['discontinue_reason'] = None
			else:
				intake['discontinue_reason'] = self._PRW_discontinue_reason().GetValue().strip()
			intake['schedule'] = self._PRW_schedule.GetValue()
			intake['aim'] = self._PRW_aim.GetValue()
			intake['notes'] = self._PRW_notes.GetValue()
			intake['is_long_term'] = self._CHBOX_long_term.IsChecked()
			intake['intake_is_approved_of'] = self._CHBOX_approved.IsChecked()
			if self._PRW_duration.GetValue().strip() in [u'', gmTools.u_infinity]:
				intake['duration'] = None
			else:
				intake['duration'] = gmDateTime.str2interval(self._PRW_duration.GetValue())
			intake['pk_brand'] = pk_brand
			intake.save()
			last_intake = intake

		self.data = last_intake

		if self._CHBOX_is_allergy.IsChecked():
			if brand is None:
				allg = self.data.turn_into_allergy(encounter_id = emr.active_encounter['pk_encounter'])
			else:
				allg = brand.turn_into_allergy(encounter_id = emr.active_encounter['pk_encounter'])
			# open for editing
			dlg = gmAllergyWidgets.cAllergyManagerDlg(parent = self, id = -1)
			dlg.ShowModal()

		return True

#		# brand pre-selected ?
#		if pk_brand is None:
#			# no, so ...
#			desc = self._PRW_brand.GetValue().strip()
#			if desc != u'':
#				# ... create or get it
#				brand = gmMedication.create_branded_drug (
#					brand_name = desc,
#					preparation = self._PRW_preparation.GetValue().strip(),
#					return_existing = True
#				)
#				pk_brand = brand['pk']
#		else:
#			# yes, so get it
#			brand = gmMedication.cBrandedDrug(aPK_obj = pk_brand)
#
#		# brand neither creatable nor pre-selected
#		if brand is None:
#			self.data = intake
#			return True
#
#		# 4) add substance to brand as component (because
#		#    that's effectively what we are saying here)
#		# FIXME: we may want to ask the user here
#		# FIXME: or only do it if there are no components yet
#		if self._PRW_substance.GetData() is None:
#			brand.add_component(substance = self._PRW_substance.GetValue().strip())
#		else:
#			# normalize substance name
#			subst = gmMedication.cConsumableSubstance(aPK_obj = self._PRW_substance.GetData())['description']
#			if subst is not None:
#				brand.add_component(substance = subst['description'])
#
	#----------------------------------------------------------------
	def _save_as_update(self):

		if self._PRW_substance.GetData() is None:
			raise NotImplementedError('need to add amount/unit')
			self.data['pk_substance'] = gmMedication.create_consumable_substance (
				substance = self._PRW_substance.GetValue().strip()
			)['pk']
		else:
			self.data['pk_substance'] = self._PRW_substance.GetData()

		self.data['started'] = self._DP_started.GetValue(as_pydt = True, invalid_as_none = True)
		self.data['discontinued'] = self._DP_discontinued.GetValue(as_pydt = True, invalid_as_none = True)
		if self.data['discontinued'] is None:
			self.data['discontinue_reason'] = None
		else:
			self.data['discontinue_reason'] = self._PRW_discontinue_reason.GetValue().strip()
		self.data['preparation'] = self._PRW_preparation.GetValue()
		self.data['strength'] = self._PRW_strength.GetValue()
		self.data['schedule'] = self._PRW_schedule.GetValue()
		self.data['aim'] = self._PRW_aim.GetValue()
		self.data['notes'] = self._PRW_notes.GetValue()
		self.data['is_long_term'] = self._CHBOX_long_term.IsChecked()
		self.data['intake_is_approved_of'] = self._CHBOX_approved.IsChecked()
		self.data['pk_episode'] = self._PRW_episode.GetData(can_create = True)

		if self._PRW_duration.GetValue().strip() in [u'', gmTools.u_infinity]:
			self.data['duration'] = None
		else:
			self.data['duration'] = gmDateTime.str2interval(self._PRW_duration.GetValue())

		if self._PRW_brand.GetData() is None:
			desc = self._PRW_brand.GetValue().strip()
			if desc != u'':
				# create or get brand
				self.data['pk_brand'] = gmMedication.create_branded_drug (
					brand_name = desc,
					preparation = self._PRW_preparation.GetValue().strip(),
					return_existing = True
				)['pk']
		else:
			self.data['pk_brand'] = self._PRW_brand.GetData()

		self.data.save()

		if self._CHBOX_is_allergy.IsChecked():
			allg = self.data.turn_into_allergy(encounter_id = emr.active_encounter['pk_encounter'])
			# open for editing
			dlg = gmAllergyWidgets.cAllergyManagerDlg(parent = self, id = -1)
			dlg.ShowModal()

		return True
	#----------------------------------------------------------------
	def _refresh_as_new(self):
		self._PRW_brand.SetText(u'', None)
		self._TCTRL_brand_ingredients.SetValue(u'')

		self._PRW_substance.SetText(u'', None)
		self._PRW_substance.Enable(True)

		self._PRW_strength.SetText(u'', None)
		self._PRW_strength.Enable(True)

		self._PRW_preparation.SetText(u'', None)
		self._PRW_preparation.Enable(True)

		self._PRW_schedule.SetText(u'', None)
		self._PRW_duration.SetText(u'', None)
		self._PRW_aim.SetText(u'', None)
		self._PRW_notes.SetText(u'', None)
		self._PRW_episode.SetText(u'', None)

		self._CHBOX_long_term.SetValue(False)
		self._CHBOX_approved.SetValue(True)

		self._DP_started.SetValue(gmDateTime.pydt_now_here())
		self._DP_discontinued.SetValue(None)
		self._PRW_discontinue_reason.SetValue(u'')

		#self.__refresh_brand_and_components()
		self.__refresh_allergies()

		self._PRW_brand.SetFocus()
	#----------------------------------------------------------------
	def _refresh_from_existing(self):

		self._PRW_substance.SetText(self.data['substance'], self.data['pk_substance'])
		self._PRW_strength.SetText(gmTools.coalesce(self.data['strength'], u''), self.data['strength'])
		self._PRW_preparation.SetText(self.data['preparation'], self.data['preparation'])

		if self.data['is_long_term']:
	 		self._CHBOX_long_term.SetValue(True)
			self._PRW_duration.Enable(False)
			self._PRW_duration.SetText(gmTools.u_infinity, None)
			self._BTN_discontinued_as_planned.Enable(False)
		else:
			self._CHBOX_long_term.SetValue(False)
			self._PRW_duration.Enable(True)
			self._BTN_discontinued_as_planned.Enable(True)
			if self.data['duration'] is None:
				self._PRW_duration.SetText(u'', None)
			else:
				self._PRW_duration.SetText(gmDateTime.format_interval(self.data['duration'], gmDateTime.acc_days), self.data['duration'])
		self._PRW_aim.SetText(gmTools.coalesce(self.data['aim'], u''), self.data['aim'])
		self._PRW_notes.SetText(gmTools.coalesce(self.data['notes'], u''), self.data['notes'])
		self._PRW_episode.SetData(self.data['pk_episode'])
		self._PRW_schedule.SetText(gmTools.coalesce(self.data['schedule'], u''), self.data['schedule'])

		self._CHBOX_approved.SetValue(self.data['intake_is_approved_of'])

		self._DP_started.SetValue(self.data['started'])
		self._DP_discontinued.SetValue(self.data['discontinued'])
		self._PRW_discontinue_reason.SetValue(gmTools.coalesce(self.data['discontinue_reason'], u''))

		self.__refresh_brand_and_components()
		self.__refresh_allergies()

		self._PRW_substance.SetFocus()
	#----------------------------------------------------------------
	def _refresh_as_new_from_existing(self):
		self._refresh_as_new()
	#----------------------------------------------------------------
	# event handlers
	#----------------------------------------------------------------
	def _on_leave_brand(self):
		if self._PRW_brand.GetData() is None:
			self._PRW_brand.SetText(u'', None)
			self._LBL_substance.Enable(True)
			self._PRW_substance.Enable(True)
			self._BTN_database_substance.Enable(True)
			self._LBL_strength.Enable(True)
			self._PRW_strength.Enable(True)
			self._LBL_preparation.Enable(True)
			self._PRW_preparation.Enable(True)
			self._PRW_preparation.SetText(u'', None)
			self._TCTRL_brand_ingredients.SetValue(u'')
		else:
			brand = gmMedication.cBrandedDrug(aPK_obj = self._PRW_brand.GetData())
			comps = brand.components

			self._LBL_substance.Enable(False)
			self._PRW_substance.Enable(False)
			self._BTN_database_substance.Enable(False)
			if len(comps) == 1:
				self._LBL_strength.Enable(True)
				self._PRW_strength.Enable(True)
			else:
				self._LBL_strength.Enable(False)
				self._PRW_strength.Enable(False)
			self._LBL_preparation.Enable(False)
			self._PRW_preparation.Enable(False)
			self._PRW_preparation.SetText(brand['preparation'], None)
			self._TCTRL_brand_ingredients.SetValue(u' / '.join ([
				u'%s%s' % (
					c['substance'],
					gmTools.coalesce(c['atc_substance'], u'', u' (%s)')
				) for c in comps
			]))
	#----------------------------------------------------------------
	def _on_leave_substance(self):
		if self._PRW_substance.GetValue().strip() == u'':
			self._PRW_brand.Enable(True)
			self._BTN_database_brand.Enable(True)

			self._LBL_preparation.Enable(False)
			self._PRW_preparation.Enable(False)
		else:
			self._PRW_brand.SetText(u'', None)
			self._PRW_brand.Enable(False)
			self._BTN_database_brand.Enable(False)
			self._TCTRL_brand_ingredients.SetValue(u'')

			self._LBL_strength.Enable(True)
			self._PRW_strength.Enable(True)
			self._LBL_preparation.Enable(True)
			self._PRW_preparation.Enable(True)
			self._PRW_preparation.SetText(u'', None)
	#----------------------------------------------------------------
	def _on_discontinued_date_changed(self, event):
		if self._DP_discontinued.GetValue() is None:
			self._PRW_discontinue_reason.Enable(False)
			self._CHBOX_is_allergy.Enable(False)
			#self._LBL_reason.Enable(False)
		else:
			self._PRW_discontinue_reason.Enable(True)
			self._CHBOX_is_allergy.Enable(True)
			#self._LBL_reason.Enable(True)
	#----------------------------------------------------------------
	def _on_get_substance_button_pressed(self, event):
		drug_db = get_drug_database()
		if drug_db is None:
			return

		result = drug_db.import_drugs()
		if result is None:
			return

		new_drugs, new_substances = result
		if len(new_substances) == 0:
			return

		# FIXME: could usefully
		# FIXME: a) ask which to post-process
		# FIXME: b) remember the others for post-processing
		first = new_substances[0]
		self._PRW_substance.SetText(first['description'], first['pk'])
	#----------------------------------------------------------------
	def _on_get_brand_button_pressed(self, event):
		drug_db = get_drug_database()
		self.__refresh_allergies()
		if drug_db is None:
			return

		result = drug_db.import_drugs()
		self.__refresh_allergies()
		if result is None:
			return

		new_drugs, new_substances = result
		if len(new_drugs) == 0:
			return
		# FIXME: could usefully
		# FIXME: a) ask which to post-process
		# FIXME: b) remember the others for post-processing
		first = new_drugs[0]
		self._PRW_brand.SetText(first['description'], first['pk'])

		self.__refresh_brand_and_components()
	#----------------------------------------------------------------
	def _on_discontinued_as_planned_button_pressed(self, event):

		now = gmDateTime.pydt_now_here()

		self.__refresh_allergies()

		# do we have a (full) plan ?
		if None not in [self.data['started'], self.data['duration']]:
			planned_end = self.data['started'] + self.data['duration']
			# the plan hasn't ended so [Per plan] can't apply ;-)
			if planned_end > now:
				return
			self._DP_discontinued.SetValue(planned_end)
			self._PRW_discontinue_reason.Enable(True)
			self._PRW_discontinue_reason.SetValue(u'')
			self._CHBOX_is_allergy.Enable(True)
			return

		# we know started but not duration: apparently the plan is to stop today
		if self.data['started'] is not None:
			# but we haven't started yet so we can't stop
			if self.data['started'] > now:
				return

		self._DP_discontinued.SetValue(now)
		self._PRW_discontinue_reason.Enable(True)
		self._PRW_discontinue_reason.SetValue(u'')
		self._CHBOX_is_allergy.Enable(True)
	#----------------------------------------------------------------
	def _on_chbox_long_term_checked(self, event):
		if self._CHBOX_long_term.IsChecked() is True:
			self._PRW_duration.Enable(False)
			self._BTN_discontinued_as_planned.Enable(False)
			self._PRW_discontinue_reason.Enable(False)
			self._CHBOX_is_allergy.Enable(False)
		else:
			self._PRW_duration.Enable(True)
			self._BTN_discontinued_as_planned.Enable(True)
			self._PRW_discontinue_reason.Enable(True)
			self._CHBOX_is_allergy.Enable(True)

		self.__refresh_allergies()
	#----------------------------------------------------------------
	def _on_chbox_is_allergy_checked(self, event):
		if self._CHBOX_is_allergy.IsChecked() is True:
			val = self._PRW_discontinue_reason.GetValue().strip()
			if not val.startswith(_('not tolerated:')):
				self._PRW_discontinue_reason.SetValue(u'%s %s' % (_('not tolerated:'), val))

		self.__refresh_allergies()
#============================================================
def delete_substance_intake(parent=None, substance=None):

	subst = gmMedication.cSubstanceIntakeEntry(aPK_obj = substance)
	msg = _(
		'\n'
		'[%s]\n'
		'\n'
		'It may be prudent to edit (before deletion) the details\n'
		'of this substance intake entry so as to leave behind\n'
		'some indication of why it was deleted.\n'
	) % subst.format()

	dlg = gmGuiHelpers.c3ButtonQuestionDlg (
		parent,
		-1,
		caption = _('Deleting medication / substance intake'),
		question = msg,
		button_defs = [
			{'label': _('&Edit'), 'tooltip': _('Allow editing of substance intake entry before deletion.'), 'default': True},
			{'label': _('&Delete'), 'tooltip': _('Delete immediately without editing first.')},
			{'label': _('&Cancel'), 'tooltip': _('Abort. Do not delete or edit substance intake entry.')}
		]
	)

	edit_first = dlg.ShowModal()
	dlg.Destroy()

	if edit_first == wx.ID_CANCEL:
		return

	if edit_first == wx.ID_YES:
		edit_intake_of_substance(parent = parent, substance = subst)
		delete_it = gmGuiHelpers.gm_show_question (
			aMessage = _('Now delete substance intake entry ?'),
			aTitle = _('Deleting medication / substance intake')
		)
	else:
		delete_it = True

	if not delete_it:
		return

	gmMedication.delete_substance_intake(substance = substance)
#------------------------------------------------------------
def edit_intake_of_substance(parent = None, substance=None):
	ea = cCurrentMedicationEAPnl(parent = parent, id = -1, substance = substance)
	dlg = gmEditArea.cGenericEditAreaDlg2(parent = parent, id = -1, edit_area = ea, single_entry = (substance is not None))
	dlg.SetTitle(gmTools.coalesce(substance, _('Adding substance intake'), _('Editing substance intake')))
	if dlg.ShowModal() == wx.ID_OK:
		dlg.Destroy()
		return True
	dlg.Destroy()
	return False

#============================================================
# current substances grid
#------------------------------------------------------------
def configure_medication_list_template(parent=None):

	if parent is None:
		parent = wx.GetApp().GetTopWindow()

	template = gmFormWidgets.manage_form_templates (
		parent = parent,
		template_types = ['current medication list']
	)
	option = u'form_templates.medication_list'

	if template is None:
		gmDispatcher.send(signal = 'statustext', msg = _('No medication list template configured.'), beep = True)
		return None

	if template['engine'] != u'L':
		gmDispatcher.send(signal = 'statustext', msg = _('No medication list template configured.'), beep = True)
		return None

	dbcfg = gmCfg.cCfgSQL()
	dbcfg.set (
		workplace = gmSurgery.gmCurrentPractice().active_workplace,
		option = option,
		value = u'%s - %s' % (template['name_long'], template['external_version'])
	)

	return template
#------------------------------------------------------------
def print_medication_list(parent=None, cleanup=True):

	if parent is None:
		parent = wx.GetApp().GetTopWindow()

	# 1) get template
	dbcfg = gmCfg.cCfgSQL()
	option = u'form_templates.medication_list'

	template = dbcfg.get2 (
		option = option,
		workplace = gmSurgery.gmCurrentPractice().active_workplace,
		bias = 'user'
	)

	if template is None:
		template = configure_medication_list_template(parent = parent)
		if template is None:
			gmGuiHelpers.gm_show_error (
				aMessage = _('There is no medication list template configured.'),
				aTitle = _('Printing medication list')
			)
			return False
	else:
		try:
			name, ver = template.split(u' - ')
		except:
			_log.exception('problem splitting medication list template name [%s]', template)
			gmDispatcher.send(signal = 'statustext', msg = _('Problem loading medication list template.'), beep = True)
			return False
		template = gmForms.get_form_template(name_long = name, external_version = ver)
		if template is None:
			gmGuiHelpers.gm_show_error (
				aMessage = _('Cannot load medication list template [%s - %s]') % (name, ver),
				aTitle = _('Printing medication list')
			)
			return False

	# 2) process template
	try:
		meds_list = template.instantiate()
	except KeyError:
		_log.exception('cannot instantiate medication list template [%s]', template)
		gmGuiHelpers.gm_show_error (
			aMessage = _('Invalid medication list template [%s - %s (%s)]') % (name, ver, template['engine']),
			aTitle = _('Printing medication list')
		)
		return False

	ph = gmMacro.gmPlaceholderHandler()
	#ph.debug = True
	meds_list.substitute_placeholders(data_source = ph)
	pdf_name = meds_list.generate_output(cleanup = cleanup)
	if cleanup:
		meds_list.cleanup()
	if pdf_name is None:
		gmGuiHelpers.gm_show_error (
			aMessage = _('Error generating the medication list.'),
			aTitle = _('Printing medication list')
		)
		return False

	# 3) print template
	printed = gmPrinting.print_file_by_shellscript(filename = pdf_name, jobtype = 'medication_list')
	if not printed:
		gmGuiHelpers.gm_show_error (
			aMessage = _('Error printing the medication list.'),
			aTitle = _('Printing medication list')
		)
		return False

	pat = gmPerson.gmCurrentPatient()
	emr = pat.get_emr()
	epi = emr.add_episode(episode_name = 'administration', is_open = False)
	emr.add_clin_narrative (
		soap_cat = None,
		note = _('medication list printed from template [%s - %s]') % (template['name_long'], template['external_version']),
		episode = epi
	)

	return True
#------------------------------------------------------------
class cCurrentSubstancesGrid(wx.grid.Grid):
	"""A grid class for displaying current substance intake.

	- does NOT listen to the currently active patient
	- thereby it can display any patient at any time
	"""
	def __init__(self, *args, **kwargs):

		wx.grid.Grid.__init__(self, *args, **kwargs)

		self.__patient = None
		self.__row_data = {}
		self.__prev_row = None
		self.__prev_tooltip_row = None
		self.__prev_cell_0 = None
		self.__grouping_mode = u'episode'
		self.__filter_show_unapproved = False
		self.__filter_show_inactive = False

		self.__grouping2col_labels = {
			u'episode': [
				_('Episode'),
				_('Substance'),
				_('Dose'),
				_('Schedule'),
				_('Started'),
				_('Duration'),
				_('Brand')
			],
			u'brand': [
				_('Brand'),
				_('Schedule'),
				_('Substance'),
				_('Dose'),
				_('Started'),
				_('Duration'),
				_('Episode')
			]
		}

		self.__grouping2order_by_clauses = {
			u'episode': u'pk_health_issue nulls first, episode, substance, started',
			u'brand': u'brand nulls last, substance, started'
		}

		self.__init_ui()
		self.__register_events()
	#------------------------------------------------------------
	# external API
	#------------------------------------------------------------
	def get_selected_cells(self):

		sel_block_top_left = self.GetSelectionBlockTopLeft()
		sel_block_bottom_right = self.GetSelectionBlockBottomRight()
		sel_cols = self.GetSelectedCols()
		sel_rows = self.GetSelectedRows()

		selected_cells = []

		# individually selected cells (ctrl-click)
		selected_cells += self.GetSelectedCells()

		# selected rows
		selected_cells += list (
			(row, col)
				for row in sel_rows
				for col in xrange(self.GetNumberCols())
		)

		# selected columns
		selected_cells += list (
			(row, col)
				for row in xrange(self.GetNumberRows())
				for col in sel_cols
		)

		# selection blocks
		for top_left, bottom_right in zip(self.GetSelectionBlockTopLeft(), self.GetSelectionBlockBottomRight()):
			selected_cells += [
				(row, col)
					for row in xrange(top_left[0], bottom_right[0] + 1)
					for col in xrange(top_left[1], bottom_right[1] + 1)
			]

		return set(selected_cells)
	#------------------------------------------------------------
	def get_selected_rows(self):
		rows = {}

		for row, col in self.get_selected_cells():
			rows[row] = True

		return rows.keys()
	#------------------------------------------------------------
	def get_selected_data(self):
		return [ self.__row_data[row] for row in self.get_selected_rows() ]
	#------------------------------------------------------------
	def repopulate_grid(self):

		self.empty_grid()

		if self.__patient is None:
			return

		emr = self.__patient.get_emr()
		meds = emr.get_current_substance_intake (
			order_by = self.__grouping2order_by_clauses[self.__grouping_mode],
			include_unapproved = self.__filter_show_unapproved,
			include_inactive = self.__filter_show_inactive
		)
		if not meds:
			return

		self.BeginBatch()

		# columns
		labels = self.__grouping2col_labels[self.__grouping_mode]
		if self.__filter_show_unapproved:
			self.AppendCols(numCols = len(labels) + 1)
		else:
			self.AppendCols(numCols = len(labels))
		for col_idx in range(len(labels)):
			self.SetColLabelValue(col_idx, labels[col_idx])
		if self.__filter_show_unapproved:
			self.SetColLabelValue(len(labels), u'OK?')
			self.SetColSize(len(labels), 40)

		self.AppendRows(numRows = len(meds))

		# loop over data
		for row_idx in range(len(meds)):
			med = meds[row_idx]
			self.__row_data[row_idx] = med

			if med['is_currently_active'] is True:
				atcs = []
				if med['atc_substance'] is not None:
					atcs.append(med['atc_substance'])
#				if med['atc_brand'] is not None:
#					atcs.append(med['atc_brand'])
#				allg = emr.is_allergic_to(atcs = tuple(atcs), inns = (med['substance'],), brand = med['brand'])
				allg = emr.is_allergic_to(atcs = tuple(atcs), inns = (med['substance'],))
				if allg not in [None, False]:
					attr = self.GetOrCreateCellAttr(row_idx, 0)
					if allg['type'] == u'allergy':
						attr.SetTextColour('red')
					else:
						attr.SetTextColour('yellow')
					self.SetRowAttr(row_idx, attr)
			else:
				attr = self.GetOrCreateCellAttr(row_idx, 0)
				attr.SetTextColour('grey')
				self.SetRowAttr(row_idx, attr)

			if self.__grouping_mode == u'episode':
				if med['pk_episode'] is None:
					self.__prev_cell_0 = None
					self.SetCellValue(row_idx, 0, gmTools.u_diameter)
				else:
					if self.__prev_cell_0 != med['episode']:
						self.__prev_cell_0 = med['episode']
						self.SetCellValue(row_idx, 0, gmTools.coalesce(med['episode'], u''))

				self.SetCellValue(row_idx, 1, med['substance'])
				self.SetCellValue(row_idx, 2, u'%s%s' % (med['amount'], med['unit']))
				self.SetCellValue(row_idx, 3, gmTools.coalesce(med['schedule'], u''))
				self.SetCellValue(row_idx, 4, med['started'].strftime('%Y-%m-%d'))

				if med['is_long_term']:
					self.SetCellValue(row_idx, 5, gmTools.u_infinity)
				else:
					if med['duration'] is None:
						self.SetCellValue(row_idx, 5, u'')
					else:
						self.SetCellValue(row_idx, 5, gmDateTime.format_interval(med['duration'], gmDateTime.acc_days))

				if med['pk_brand'] is None:
					self.SetCellValue(row_idx, 6, gmTools.coalesce(med['brand'], u''))
				else:
					if med['fake_brand']:
						self.SetCellValue(row_idx, 6, gmTools.coalesce(med['brand'], u'', _('%s (fake)')))
					else:
						self.SetCellValue(row_idx, 6, gmTools.coalesce(med['brand'], u''))

			elif self.__grouping_mode == u'brand':

				if med['pk_brand'] is None:
					self.__prev_cell_0 = None
					self.SetCellValue(row_idx, 0, gmTools.u_diameter)
				else:
					if self.__prev_cell_0 != med['brand']:
						self.__prev_cell_0 = med['brand']
						if med['fake_brand']:
							self.SetCellValue(row_idx, 0, gmTools.coalesce(med['brand'], u'', _('%s (fake)')))
						else:
							self.SetCellValue(row_idx, 0, gmTools.coalesce(med['brand'], u''))

				self.SetCellValue(row_idx, 1, gmTools.coalesce(med['schedule'], u''))
				self.SetCellValue(row_idx, 2, med['substance'])
				self.SetCellValue(row_idx, 3, u'%s%s' % (med['amount'], med['unit']))
				self.SetCellValue(row_idx, 4, med['started'].strftime('%Y-%m-%d'))

				if med['is_long_term']:
					self.SetCellValue(row_idx, 5, gmTools.u_infinity)
				else:
					if med['duration'] is None:
						self.SetCellValue(row_idx, 5, u'')
					else:
						self.SetCellValue(row_idx, 5, gmDateTime.format_interval(med['duration'], gmDateTime.acc_days))

				if med['pk_episode'] is None:
					self.SetCellValue(row_idx, 6, u'')
				else:
					self.SetCellValue(row_idx, 6, gmTools.coalesce(med['episode'], u''))

			else:
				raise ValueError('unknown grouping mode [%s]' % self.__grouping_mode)

			if self.__filter_show_unapproved:
				self.SetCellValue (
					row_idx,
					len(labels),
					gmTools.bool2subst(med['intake_is_approved_of'], gmTools.u_checkmark_thin, u'', u'?')
				)

			#self.SetCellAlignment(row, col, horiz = wx.ALIGN_RIGHT, vert = wx.ALIGN_CENTRE)

		self.EndBatch()
	#------------------------------------------------------------
	def empty_grid(self):
		self.BeginBatch()
		self.ClearGrid()
		# Windows cannot do "nothing", it rather decides to assert()
		# on thinking it is supposed to do nothing
		if self.GetNumberRows() > 0:
			self.DeleteRows(pos = 0, numRows = self.GetNumberRows())
		if self.GetNumberCols() > 0:
			self.DeleteCols(pos = 0, numCols = self.GetNumberCols())
		self.EndBatch()
		self.__row_data = {}
		self.__prev_cell_0 = None
	#------------------------------------------------------------
	def show_info_on_entry(self):

		if len(self.__row_data) == 0:
			return

		sel_rows = self.get_selected_rows()
		if len(sel_rows) != 1:
			return

		drug_db = get_drug_database()
		if drug_db is None:
			return

		drug_db.show_info_on_substance(substance = self.get_selected_data()[0])
	#------------------------------------------------------------
	def show_renal_insufficiency_info(self):

		if len(self.__row_data) == 0:
			return

		sel_rows = self.get_selected_rows()

		if len(sel_rows) != 1:
			return

		webbrowser.open (
			url = gmMedication.drug2renal_insufficiency_url(search_term = self.get_selected_data()[0]),
			new = False,
			autoraise = True
		)
	#------------------------------------------------------------
	def report_ADR(self):

		dbcfg = gmCfg.cCfgSQL()

		url = dbcfg.get2 (
			option = u'external.urls.report_ADR',
			workplace = gmSurgery.gmCurrentPractice().active_workplace,
			bias = u'user',
			default = u'https://dcgma.org/uaw/meldung.php'		# http://www.akdae.de/Arzneimittelsicherheit/UAW-Meldung/UAW-Meldung-online.html
		)

		webbrowser.open(url = url, new = False, autoraise = True)
	#------------------------------------------------------------
	def check_interactions(self):

		if len(self.__row_data) == 0:
			return

		drug_db = get_drug_database()
		if drug_db is None:
			return

		if len(self.get_selected_rows()) > 1:
			drug_db.check_drug_interactions(substances = self.get_selected_data())
		else:
			drug_db.check_drug_interactions(substances = self.__row_data.values())
	#------------------------------------------------------------
	def add_substance(self):
		edit_intake_of_substance(parent = self, substance = None)
	#------------------------------------------------------------
	def edit_substance(self):

		rows = self.get_selected_rows()

		if len(rows) == 0:
			return

		if len(rows) > 1:
			gmDispatcher.send(signal = 'statustext', msg = _('Cannot edit more than one substance at once.'), beep = True)
			return

		subst = self.get_selected_data()[0]
		edit_intake_of_substance(parent = self, substance = subst)
	#------------------------------------------------------------
	def delete_substance(self):

		rows = self.get_selected_rows()

		if len(rows) == 0:
			return

		if len(rows) > 1:
			gmDispatcher.send(signal = 'statustext', msg = _('Cannot delete more than one substance at once.'), beep = True)
			return

		subst = self.get_selected_data()[0]
		delete_substance_intake(parent = self, substance = subst['pk_substance_intake'])
	#------------------------------------------------------------
	def create_allergy_from_substance(self):
		rows = self.get_selected_rows()

		if len(rows) == 0:
			return

		if len(rows) > 1:
			gmDispatcher.send(signal = 'statustext', msg = _('Cannot create allergy from more than one substance at once.'), beep = True)
			return

		subst = self.get_selected_data()[0]
		if subst['is_currently_active']:
			subst['discontinued'] = gmDateTime.pydt_now_here()
		if subst['discontinue_reason'] is None:
			subst['discontinue_reason'] = _('discontinued due to allergy or intolerance')
		subst.save()

		emr = self.__patient.get_emr()
		allg = subst.turn_into_allergy(encounter_id = emr.active_encounter['pk_encounter'])
		dlg = gmAllergyWidgets.cAllergyManagerDlg(parent = self, id = -1)
		dlg.ShowModal()
	#------------------------------------------------------------
	def print_medication_list(self):
		# there could be some filtering/user interaction going on here
		_cfg = gmCfg2.gmCfgData()
		print_medication_list(parent = self, cleanup = _cfg.get(option = 'debug'))
	#------------------------------------------------------------
	def get_row_tooltip(self, row=None):

		try:
			entry = self.__row_data[row]
		except KeyError:
			return u' '

		emr = self.__patient.get_emr()
		atcs = []
		if entry['atc_substance'] is not None:
			atcs.append(entry['atc_substance'])
#		if entry['atc_brand'] is not None:
#			atcs.append(entry['atc_brand'])
#		allg = emr.is_allergic_to(atcs = tuple(atcs), inns = (entry['substance'],), brand = entry['brand'])
		allg = emr.is_allergic_to(atcs = tuple(atcs), inns = (entry['substance'],))

		tt = _('Substance intake entry (%s, %s)   [#%s]                     \n') % (
			gmTools.bool2subst (
				boolean = entry['is_currently_active'],
				true_return = gmTools.bool2subst (
					boolean = entry['seems_inactive'],
					true_return = _('active, needs check'),
					false_return = _('active'),
					none_return = _('assumed active')
				),
				false_return = _('inactive')
			),
			gmTools.bool2subst (
				boolean = entry['intake_is_approved_of'],
				true_return = _('approved'),
				false_return = _('unapproved')
			),
			entry['pk_substance_intake']
		)

		if allg not in [None, False]:
			certainty = gmTools.bool2subst(allg['definite'], _('definite'), _('suspected'))
			tt += u'\n'
			tt += u' !! ---- Cave ---- !!\n'
			tt += u' %s (%s): %s (%s)\n' % (
				allg['l10n_type'],
				certainty,
				allg['descriptor'],
				gmTools.coalesce(allg['reaction'], u'')[:40]
			)
			tt += u'\n'

		tt += u' ' + _('Substance: %s   [#%s]\n') % (entry['substance'], entry['pk_substance'])
		tt += u' ' + _('Preparation: %s\n') % entry['preparation']
		tt += u' ' + _('Amount per dose: %s%s') % (entry['amount'], entry['unit'])
		if entry.ddd is not None:
			tt += u' (DDD: %s %s)' % (entry.ddd['ddd'], entry.ddd['unit'])
		tt += u'\n'
		tt += gmTools.coalesce(entry['atc_substance'], u'', _(' ATC (substance): %s\n'))

		tt += u'\n'

		tt += gmTools.coalesce (
			entry['brand'],
			u'',
			_(' Brand name: %%s   [#%s]\n') % entry['pk_brand']
		)
		tt += gmTools.coalesce(entry['atc_brand'], u'', _(' ATC (brand): %s\n'))

		tt += u'\n'

		tt += gmTools.coalesce(entry['schedule'], u'', _(' Regimen: %s\n'))

		if entry['is_long_term']:
			duration = u' %s %s' % (gmTools.u_right_arrow, gmTools.u_infinity)
		else:
			if entry['duration'] is None:
				duration = u''
			else:
				duration = u' %s %s' % (gmTools.u_right_arrow, gmDateTime.format_interval(entry['duration'], gmDateTime.acc_days))

		tt += _(' Started %s%s%s\n') % (
			entry['started'].strftime('%Y %B %d').decode(gmI18N.get_encoding()),
			duration,
			gmTools.bool2subst(entry['is_long_term'], _(' (long-term)'), _(' (short-term)'), u'')
		)

		if entry['discontinued'] is not None:
			tt += _(' Discontinued %s\n') % (
				entry['discontinued'].strftime('%Y %B %d').decode(gmI18N.get_encoding()),
			)
			tt += _(' Reason: %s\n') % entry['discontinue_reason']

		tt += u'\n'

		tt += gmTools.coalesce(entry['aim'], u'', _(' Aim: %s\n'))
		tt += gmTools.coalesce(entry['episode'], u'', _(' Episode: %s\n'))
		tt += gmTools.coalesce(entry['notes'], u'', _(' Advice: %s\n'))

		tt += u'\n'

		tt += _(u'Revision: #%(row_ver)s, %(mod_when)s by %(mod_by)s.') % ({
			'row_ver': entry['row_version'],
			'mod_when': entry['modified_when'].strftime('%c').decode(gmI18N.get_encoding()),
			'mod_by': entry['modified_by']
		})

		return tt
	#------------------------------------------------------------
	# internal helpers
	#------------------------------------------------------------
	def __init_ui(self):
		self.CreateGrid(0, 1)
		self.EnableEditing(0)
		self.EnableDragGridSize(1)
		self.SetSelectionMode(wx.grid.Grid.wxGridSelectRows)

		self.SetColLabelAlignment(wx.ALIGN_LEFT, wx.ALIGN_CENTER)

		self.SetRowLabelSize(0)
		self.SetRowLabelAlignment(horiz = wx.ALIGN_RIGHT, vert = wx.ALIGN_CENTRE)
	#------------------------------------------------------------
	# properties
	#------------------------------------------------------------
	def _get_patient(self):
		return self.__patient

	def _set_patient(self, patient):
		self.__patient = patient
		self.repopulate_grid()

	patient = property(_get_patient, _set_patient)
	#------------------------------------------------------------
	def _get_grouping_mode(self):
		return self.__grouping_mode

	def _set_grouping_mode(self, mode):
		self.__grouping_mode = mode
		self.repopulate_grid()

	grouping_mode = property(_get_grouping_mode, _set_grouping_mode)
	#------------------------------------------------------------
	def _get_filter_show_unapproved(self):
		return self.__filter_show_unapproved

	def _set_filter_show_unapproved(self, val):
		self.__filter_show_unapproved = val
		self.repopulate_grid()

	filter_show_unapproved = property(_get_filter_show_unapproved, _set_filter_show_unapproved)
	#------------------------------------------------------------
	def _get_filter_show_inactive(self):
		return self.__filter_show_inactive

	def _set_filter_show_inactive(self, val):
		self.__filter_show_inactive = val
		self.repopulate_grid()

	filter_show_inactive = property(_get_filter_show_inactive, _set_filter_show_inactive)
	#------------------------------------------------------------
	# event handling
	#------------------------------------------------------------
	def __register_events(self):
		# dynamic tooltips: GridWindow, GridRowLabelWindow, GridColLabelWindow, GridCornerLabelWindow
		self.GetGridWindow().Bind(wx.EVT_MOTION, self.__on_mouse_over_cells)
		#self.GetGridRowLabelWindow().Bind(wx.EVT_MOTION, self.__on_mouse_over_row_labels)
		#self.GetGridColLabelWindow().Bind(wx.EVT_MOTION, self.__on_mouse_over_col_labels)

		# editing cells
		self.Bind(wx.grid.EVT_GRID_CELL_LEFT_DCLICK, self.__on_cell_left_dclicked)
	#------------------------------------------------------------
	def __on_mouse_over_cells(self, evt):
		"""Calculate where the mouse is and set the tooltip dynamically."""

		# Use CalcUnscrolledPosition() to get the mouse position within the
		# entire grid including what's offscreen
		x, y = self.CalcUnscrolledPosition(evt.GetX(), evt.GetY())

		# use this logic to prevent tooltips outside the actual cells
		# apply to GetRowSize, too
#        tot = 0
#        for col in xrange(self.NumberCols):
#            tot += self.GetColSize(col)
#            if xpos <= tot:
#                self.tool_tip.Tip = 'Tool tip for Column %s' % (
#                    self.GetColLabelValue(col))
#                break
#            else:  # mouse is in label area beyond the right-most column
#            self.tool_tip.Tip = ''

		row, col = self.XYToCell(x, y)

		if row == self.__prev_tooltip_row:
			return

		self.__prev_tooltip_row = row

		try:
			evt.GetEventObject().SetToolTipString(self.get_row_tooltip(row = row))
		except KeyError:
			pass
	#------------------------------------------------------------
	def __on_cell_left_dclicked(self, evt):
		row = evt.GetRow()
		data = self.__row_data[row]
		edit_intake_of_substance(parent = self, substance = data)
#============================================================
from Gnumed.wxGladeWidgets import wxgCurrentSubstancesPnl

class cCurrentSubstancesPnl(wxgCurrentSubstancesPnl.wxgCurrentSubstancesPnl, gmRegetMixin.cRegetOnPaintMixin):

	"""Panel holding a grid with current substances. Used as notebook page."""

	def __init__(self, *args, **kwargs):

		wxgCurrentSubstancesPnl.wxgCurrentSubstancesPnl.__init__(self, *args, **kwargs)
		gmRegetMixin.cRegetOnPaintMixin.__init__(self)

		self.__register_interests()
	#-----------------------------------------------------
	# reget-on-paint mixin API
	#-----------------------------------------------------
	def _populate_with_data(self):
		"""Populate cells with data from model."""
		pat = gmPerson.gmCurrentPatient()
		if pat.connected:
			self._grid_substances.patient = pat
		else:
			self._grid_substances.patient = None
		return True
	#--------------------------------------------------------
	# event handling
	#--------------------------------------------------------
	def __register_interests(self):
		gmDispatcher.connect(signal = u'pre_patient_selection', receiver = self._on_pre_patient_selection)
		gmDispatcher.connect(signal = u'post_patient_selection', receiver = self._schedule_data_reget)
		gmDispatcher.connect(signal = u'substance_intake_mod_db', receiver = self._schedule_data_reget)
		# active_substance_mod_db
		# substance_brand_mod_db
	#--------------------------------------------------------
	def _on_pre_patient_selection(self):
		wx.CallAfter(self.__on_pre_patient_selection)
	#--------------------------------------------------------
	def __on_pre_patient_selection(self):
		self._grid_substances.patient = None
	#--------------------------------------------------------
	def _on_add_button_pressed(self, event):
		self._grid_substances.add_substance()
	#--------------------------------------------------------
	def _on_edit_button_pressed(self, event):
		self._grid_substances.edit_substance()
	#--------------------------------------------------------
	def _on_delete_button_pressed(self, event):
		self._grid_substances.delete_substance()
	#--------------------------------------------------------
	def _on_info_button_pressed(self, event):
		self._grid_substances.show_info_on_entry()
	#--------------------------------------------------------
	def _on_interactions_button_pressed(self, event):
		self._grid_substances.check_interactions()
	#--------------------------------------------------------
	def _on_episode_grouping_selected(self, event):
		self._grid_substances.grouping_mode = 'episode'
	#--------------------------------------------------------
	def _on_brand_grouping_selected(self, event):
		self._grid_substances.grouping_mode = 'brand'
	#--------------------------------------------------------
	def _on_show_unapproved_checked(self, event):
		self._grid_substances.filter_show_unapproved = self._CHBOX_show_unapproved.GetValue()
	#--------------------------------------------------------
	def _on_show_inactive_checked(self, event):
		self._grid_substances.filter_show_inactive = self._CHBOX_show_inactive.GetValue()
	#--------------------------------------------------------
	def _on_print_button_pressed(self, event):
		self._grid_substances.print_medication_list()
	#--------------------------------------------------------
	def _on_allergy_button_pressed(self, event):
		self._grid_substances.create_allergy_from_substance()
	#--------------------------------------------------------
	def _on_button_kidneys_pressed(self, event):
		self._grid_substances.show_renal_insufficiency_info()
	#--------------------------------------------------------
	def _on_adr_button_pressed(self, event):
		self._grid_substances.report_ADR()
#============================================================
# main
#------------------------------------------------------------
if __name__ == '__main__':

	if len(sys.argv) < 2:
		sys.exit()

	if sys.argv[1] != 'test':
		sys.exit()

	from Gnumed.pycommon import gmI18N

	gmI18N.activate_locale()
	gmI18N.install_domain(domain = 'gnumed')

	#----------------------------------------
	app = wx.PyWidgetTester(size = (600, 600))
	app.SetWidget(cATCPhraseWheel, -1)
	app.MainLoop()

#============================================================
