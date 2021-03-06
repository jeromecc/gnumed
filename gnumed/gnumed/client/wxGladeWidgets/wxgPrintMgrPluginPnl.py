#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# generated by wxGlade 0.6.8
#

import wx

# begin wxGlade: dependencies
import gettext
# end wxGlade

# begin wxGlade: extracode
from Gnumed.wxpython.gmListWidgets import cReportListCtrl
# end wxGlade


class wxgPrintMgrPluginPnl(wx.Panel):
	def __init__(self, *args, **kwds):
		# begin wxGlade: wxgPrintMgrPluginPnl.__init__
		kwds["style"] = wx.NO_BORDER | wx.TAB_TRAVERSAL
		wx.Panel.__init__(self, *args, **kwds)
		self._RBTN_all_patients = wx.RadioButton(self, wx.ID_ANY, _("All patients"))
		self._RBTN_active_patient_only = wx.RadioButton(self, wx.ID_ANY, _("&Active patient only"))
		self._LCTRL_printouts = cReportListCtrl(self, wx.ID_ANY, style=wx.LC_REPORT | wx.NO_BORDER)
		self._BTN_view_printout = wx.Button(self, wx.ID_ANY, _("&View"), style=wx.BU_EXACTFIT)
		self._BTN_print_printouts = wx.Button(self, wx.ID_PRINT, "", style=wx.BU_EXACTFIT)
		self._BTN_export_printouts = wx.Button(self, wx.ID_ANY, _("&Export"), style=wx.BU_EXACTFIT)
		self._BTN_delete_printouts = wx.Button(self, wx.ID_DELETE, "", style=wx.BU_EXACTFIT)

		self.__set_properties()
		self.__do_layout()

		self.Bind(wx.EVT_RADIOBUTTON, self._on_all_patients_selected, self._RBTN_all_patients)
		self.Bind(wx.EVT_RADIOBUTTON, self._on_active_patient_only_selected, self._RBTN_active_patient_only)
		self.Bind(wx.EVT_LIST_ITEM_SELECTED, self._on_list_item_selected, self._LCTRL_printouts)
		self.Bind(wx.EVT_BUTTON, self._on_view_button_pressed, self._BTN_view_printout)
		self.Bind(wx.EVT_BUTTON, self._on_print_button_pressed, self._BTN_print_printouts)
		self.Bind(wx.EVT_BUTTON, self._on_export_button_pressed, self._BTN_export_printouts)
		self.Bind(wx.EVT_BUTTON, self._on_delete_button_pressed, self._BTN_delete_printouts)
		# end wxGlade

	def __set_properties(self):
		# begin wxGlade: wxgPrintMgrPluginPnl.__set_properties
		self._RBTN_all_patients.SetToolTipString(_("Select here to show documents for all patients."))
		self._RBTN_all_patients.SetValue(1)
		self._RBTN_active_patient_only.SetToolTipString(_("Select here to filter to the active patient (if any)."))
		self._RBTN_active_patient_only.Enable(False)
		self._BTN_view_printout.SetToolTipString(_("Show the topmost selected printout."))
		self._BTN_print_printouts.SetToolTipString(_("Print selected/all printouts."))
		self._BTN_export_printouts.SetToolTipString(_("Store selected printouts in patient export area (if applicable)."))
		self._BTN_delete_printouts.SetToolTipString(_("Delete the selected printouts"))
		# end wxGlade

	def __do_layout(self):
		# begin wxGlade: wxgPrintMgrPluginPnl.__do_layout
		__szr_main = wx.BoxSizer(wx.VERTICAL)
		__szr_buttons = wx.BoxSizer(wx.HORIZONTAL)
		__szr_top = wx.BoxSizer(wx.HORIZONTAL)
		__lbl_patient_filter = wx.StaticText(self, wx.ID_ANY, _("Show printouts for:"))
		__szr_top.Add(__lbl_patient_filter, 0, wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, 5)
		__szr_top.Add(self._RBTN_all_patients, 0, wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, 5)
		__szr_top.Add(self._RBTN_active_patient_only, 0, wx.ALIGN_CENTER_VERTICAL, 5)
		__szr_top.Add((20, 20), 1, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 3)
		__szr_main.Add(__szr_top, 0, wx.BOTTOM | wx.EXPAND, 3)
		__szr_main.Add(self._LCTRL_printouts, 1, wx.EXPAND, 5)
		__szr_buttons.Add((20, 20), 1, wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL, 0)
		__szr_buttons.Add(self._BTN_view_printout, 0, wx.RIGHT | wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL, 3)
		__szr_buttons.Add(self._BTN_print_printouts, 0, wx.RIGHT | wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL, 3)
		__szr_buttons.Add(self._BTN_export_printouts, 0, wx.RIGHT | wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL, 3)
		__szr_buttons.Add(self._BTN_delete_printouts, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 3)
		__szr_buttons.Add((20, 20), 1, wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL, 3)
		__szr_main.Add(__szr_buttons, 0, wx.EXPAND, 0)
		self.SetSizer(__szr_main)
		__szr_main.Fit(self)
		# end wxGlade

	def _on_all_patients_selected(self, event):  # wxGlade: wxgPrintMgrPluginPnl.<event_handler>
		print "Event handler '_on_all_patients_selected' not implemented!"
		event.Skip()

	def _on_active_patient_only_selected(self, event):  # wxGlade: wxgPrintMgrPluginPnl.<event_handler>
		print "Event handler '_on_active_patient_only_selected' not implemented!"
		event.Skip()

	def _on_list_item_selected(self, event):  # wxGlade: wxgPrintMgrPluginPnl.<event_handler>
		print "Event handler '_on_list_item_selected' not implemented!"
		event.Skip()

	def _on_view_button_pressed(self, event):  # wxGlade: wxgPrintMgrPluginPnl.<event_handler>
		print "Event handler '_on_view_button_pressed' not implemented!"
		event.Skip()

	def _on_print_button_pressed(self, event):  # wxGlade: wxgPrintMgrPluginPnl.<event_handler>
		print "Event handler '_on_print_button_pressed' not implemented!"
		event.Skip()

	def _on_export_button_pressed(self, event):  # wxGlade: wxgPrintMgrPluginPnl.<event_handler>
		print "Event handler '_on_export_button_pressed' not implemented!"
		event.Skip()

	def _on_delete_button_pressed(self, event):  # wxGlade: wxgPrintMgrPluginPnl.<event_handler>
		print "Event handler '_on_delete_button_pressed' not implemented!"
		event.Skip()

# end of class wxgPrintMgrPluginPnl
