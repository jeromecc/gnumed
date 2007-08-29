"""GNUmed form/letter handling widgets.
"""
#================================================================
# $Source: /home/ncq/Projekte/cvs2git/vcs-mirror/gnumed/gnumed/client/wxpython/gmFormWidgets.py,v $
# $Id: gmFormWidgets.py,v 1.2 2007-08-29 14:38:55 ncq Exp $
__version__ = "$Revision: 1.2 $"
__author__ = "Karsten Hilbert <Karsten.Hilbert@gmx.net>"

import os.path, sys


import wx


if __name__ == '__main__':
	sys.path.insert(0, '../../')
from Gnumed.pycommon import gmLog, gmI18N
from Gnumed.business import gmForms
from Gnumed.wxpython import gmGuiHelpers, gmListWidgets, gmMacro
from Gnumed.wxGladeWidgets import wxgFormTemplateEditAreaPnl, wxgFormTemplateEditAreaDlg


_log = gmLog.gmDefLog
_log.Log(gmLog.lInfo, __version__)

#============================================================
# convenience functions
#============================================================
def let_user_select_form_template(parent=None):

	def edit(template=None):
		dlg = cFormTemplateEditAreaDlg(parent, -1, template=template)
		dlg.ShowModal()

	def delete(template):
		print "form template deletion not yet implemented"
		pass

	templates = gmForms.get_form_templates(engine = gmForms.engine_ooo, active_only = False)
	template = gmListWidgets.get_choices_from_list (
		parent = parent,
		caption = _('Select letter or form template.'),
		choices = [ [t['name_long'], t['external_version'], gmForms.engine_names[t['engine']]] for t in templates ],
		columns = [_('Template'), _('Version'), _('Type')],
		data = templates,
		editor_callback = edit,
		new_callback = edit,
		delete_callback = delete,
		single_selection = True
	)

	return template
#------------------------------------------------------------
def create_new_letter(parent=None):

	# 1) have user select template
	template = let_user_select_form_template(parent = parent)
	if template is None:
		return

	# 2) export template to file
	filename = template.export_to_file()
	if filename is None:
		gmGuiHelpers.gm_show_error (
			_(	'Error exporting form template\n'
				'\n'
				' "%s" (%s)'
			) % (template['name_long'], template['external_version']),
			_('Letter template export')
		)
		return

	doc = gmForms.cOOoLetter(template_file = filename, instance_type = template['instance_type'])
	doc.open_in_ooo()
	doc.show(False)
	ph_handler = gmMacro.gmPlaceholderHandler()
	doc.replace_placeholders(handler = ph_handler)
	filename = filename.replace('.ott', '.odt').replace('-FormTemplate-', '-FormInstance-')
	doc.save_in_ooo(filename = filename)
	doc.show(True)
#============================================================
class cFormTemplateEditAreaPnl(wxgFormTemplateEditAreaPnl.wxgFormTemplateEditAreaPnl):

	def __init__(self, *args, **kwargs):
		try:
			self.__template = kwargs['template']
			del kwargs['template']
		except KeyError:
			self.__template = None

		wxgFormTemplateEditAreaPnl.wxgFormTemplateEditAreaPnl.__init__(self, *args, **kwargs)

		self._PRW_name_long.matcher = gmForms.cFormTemplateNameLong_MatchProvider()
		self._PRW_name_short.matcher = gmForms.cFormTemplateNameShort_MatchProvider()
		self._PRW_template_type.matcher = gmForms.cFormTemplateType_MatchProvider()

		self.refresh()
	#--------------------------------------------------------
	def refresh(self, template = None):
		if template is not None:
			self.__template = template

		if self.__template is None:
			self._PRW_name_long.SetText(u'')
			self._PRW_name_short.SetText(u'')
			self._TCTRL_external_version.SetValue(u'')
			self._PRW_template_type.SetText(u'')
			self._PRW_instance_type.SetText(u'')
			self._TCTRL_filename.SetValue(u'')
			# FIXME: add engine handling
			self._CHBOX_active.SetValue(True)
			
			self._TCTRL_date_modified.SetValue(u'')
			self._TCTRL_modified_by.SetValue(u'')

		else:
			self._PRW_name_long.SetText(self.__template['name_long'])
			self._PRW_name_short.SetText(self.__template['name_short'])
			self._TCTRL_external_version.SetValue(self.__template['external_version'])
			self._PRW_template_type.SetText(self.__template['l10n_template_type'], data = self.__template['pk_template_type'])
			self._PRW_instance_type.SetText(self.__template['l10n_instance_type'], data = self.__template['instance_type'])
			self._TCTRL_filename.SetValue(self.__template['filename'])
			# FIXME: add engine handling
			self._CHBOX_active.SetValue(self.__template['in_use'])
			
			self._TCTRL_date_modified.SetValue(self.__template['last_modified'].strftime('%x'))
			self._TCTRL_modified_by.SetValue(self.__template['modified_by'])

			self._TCTRL_filename.Enable(True)
			self._BTN_load.Enable(False)

		self._PRW_name_long.SetFocus()
	#--------------------------------------------------------
	def _on_load_button_pressed(self, evt):
		dlg = wx.FileDialog (
			parent = self,
			message = _('Choose a form template file'),
			defaultDir = os.path.expanduser(os.path.join('~', 'gnumed')),
			defaultFile = '',
			wildcard = "%s (*.ott)|*.ott|%s (*)|*|%s (*.*)|*.*" % (_('OOo templates'), _('all files'), _('all files (Win)')),
			style = wx.OPEN | wx.HIDE_READONLY | wx.FILE_MUST_EXIST
		)
		result = dlg.ShowModal()
		if result != wx.ID_CANCEL:
			fname = os.path.split(dlg.GetPath())[1]
			self._TCTRL_filename.SetValue(fname)
		dlg.Destroy()
	#--------------------------------------------------------
	def save(self):
		print "saving form template not yet implemented"
#============================================================
class cFormTemplateEditAreaDlg(wxgFormTemplateEditAreaDlg.wxgFormTemplateEditAreaDlg):

	def __init__(self, *args, **kwargs):
		try:
			template = kwargs['template']
			del kwargs['template']
		except KeyError:
			template = None

		wxgFormTemplateEditAreaDlg.wxgFormTemplateEditAreaDlg.__init__(self, *args, **kwargs)

		self._PNL_edit_area.refresh(template=template)
	#--------------------------------------------------------
	def _on_save_button_pressed(self, evt):
		if self._PNL_edit_area.save():
			if self.IsModal():
				self.EndModal(wx.ID_OK)
			else:
				self.Close()
#============================================================
# main
#------------------------------------------------------------
if __name__ == '__main__':
	_log.SetAllLogLevels(gmLog.lData)
	gmI18N.activate_locale()
	gmI18N.install_domain(domain = 'gnumed')

	#----------------------------------------
	def test_cFormTemplateEditAreaPnl():
		app = wx.PyWidgetTester(size = (400, 300))
		pnl = cFormTemplateEditAreaPnl(app.frame, -1, template = gmForms.cFormTemplate(aPK_obj=4))
		app.frame.Show(True)
		app.MainLoop()
		return
	#----------------------------------------
	if (len(sys.argv) > 1) and (sys.argv[1] == 'test'):
		test_cFormTemplateEditAreaPnl()

#============================================================
# $Log: gmFormWidgets.py,v $
# Revision 1.2  2007-08-29 14:38:55  ncq
# - remove spurious ,
#
# Revision 1.1  2007/08/28 14:40:12  ncq
# - factored out from gmMedDocWidgets.py
#
#


#============================================================
# Log: gmMedDocWidgets.py
# Revision 1.142  2007/08/28 14:18:13  ncq
# - no more gm_statustext()