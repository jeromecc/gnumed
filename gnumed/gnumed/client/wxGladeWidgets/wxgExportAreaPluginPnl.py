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


class wxgExportAreaPluginPnl(wx.Panel):
	def __init__(self, *args, **kwds):
		# begin wxGlade: wxgExportAreaPluginPnl.__init__
		kwds["style"] = wx.NO_BORDER | wx.TAB_TRAVERSAL
		wx.Panel.__init__(self, *args, **kwds)
		self._LCTRL_items = cReportListCtrl(self, wx.ID_ANY, style=wx.LC_REPORT | wx.NO_BORDER)
		self._BTN_show_item = wx.Button(self, wx.ID_ANY, _("&View"), style=wx.BU_EXACTFIT)
		self._BTN_add_items = wx.Button(self, wx.ID_ANY, _(u"\u21a2 &Disk"), style=wx.BU_LEFT | wx.BU_EXACTFIT)
		self._BTN_add_from_archive = wx.Button(self, wx.ID_ANY, _(u"\u21a2 &Archive"), style=wx.BU_LEFT | wx.BU_EXACTFIT)
		self._BTN_scan_items = wx.Button(self, wx.ID_ANY, _(u"\u21a2 S&can"), style=wx.BU_LEFT | wx.BU_EXACTFIT)
		self._BTN_clipboard_items = wx.Button(self, wx.ID_ANY, _(u"\u21a2 C&lipboard"), style=wx.BU_LEFT | wx.BU_EXACTFIT)
		self._BTN_remove_items = wx.Button(self, wx.ID_ANY, _("&Remove"), style=wx.BU_EXACTFIT)
		self._BTN_print_items = wx.Button(self, wx.ID_ANY, _("&Print"), style=wx.BU_EXACTFIT)
		self._BTN_remote_print = wx.Button(self, wx.ID_ANY, _("&Print Mgr"), style=wx.BU_EXACTFIT)
		self._BTN_burn_items = wx.Button(self, wx.ID_ANY, _("&Burn"), style=wx.BU_EXACTFIT)
		self._BTN_save_items = wx.Button(self, wx.ID_ANY, _("&Save"), style=wx.BU_EXACTFIT)
		self._BTN_mail_items = wx.Button(self, wx.ID_ANY, _("E-&Mail"), style=wx.BU_EXACTFIT)
		self._BTN_fax_items = wx.Button(self, wx.ID_ANY, _("&Fax"), style=wx.BU_EXACTFIT)
		self._BTN_archive_items = wx.Button(self, wx.ID_ANY, _(u"\u21f6 Archive"), style=wx.BU_EXACTFIT)

		self.__set_properties()
		self.__do_layout()

		self.Bind(wx.EVT_LIST_ITEM_SELECTED, self._on_list_item_selected, self._LCTRL_items)
		self.Bind(wx.EVT_BUTTON, self._on_show_item_button_pressed, self._BTN_show_item)
		self.Bind(wx.EVT_BUTTON, self._on_add_items_button_pressed, self._BTN_add_items)
		self.Bind(wx.EVT_BUTTON, self._on_add_from_archive_button_pressed, self._BTN_add_from_archive)
		self.Bind(wx.EVT_BUTTON, self._on_scan_items_button_pressed, self._BTN_scan_items)
		self.Bind(wx.EVT_BUTTON, self._on_clipboard_items_button_pressed, self._BTN_clipboard_items)
		self.Bind(wx.EVT_BUTTON, self._on_remove_items_button_pressed, self._BTN_remove_items)
		self.Bind(wx.EVT_BUTTON, self._on_print_items_button_pressed, self._BTN_print_items)
		self.Bind(wx.EVT_BUTTON, self._on_remote_print_button_pressed, self._BTN_remote_print)
		self.Bind(wx.EVT_BUTTON, self._on_burn_items_button_pressed, self._BTN_burn_items)
		self.Bind(wx.EVT_BUTTON, self._on_save_items_button_pressed, self._BTN_save_items)
		self.Bind(wx.EVT_BUTTON, self._on_mail_items_button_pressed, self._BTN_mail_items)
		self.Bind(wx.EVT_BUTTON, self._on_fax_items_button_pressed, self._BTN_fax_items)
		self.Bind(wx.EVT_BUTTON, self._on_archive_items_button_pressed, self._BTN_archive_items)
		# end wxGlade

	def __set_properties(self):
		# begin wxGlade: wxgExportAreaPluginPnl.__set_properties
		self._BTN_show_item.SetToolTipString(_("Show the topmost selected document."))
		self._BTN_add_items.SetToolTipString(_("Add document(s) from file(s)."))
		self._BTN_add_from_archive.SetToolTipString(_("Add document(s) from archive."))
		self._BTN_scan_items.SetToolTipString(_("Acquire images from image source (scanner, ...)."))
		self._BTN_clipboard_items.SetToolTipString(_("Acquire file or text from the clipboard."))
		self._BTN_remove_items.SetToolTipString(_("Remove the selected documents."))
		self._BTN_print_items.SetToolTipString(_("Print selected/all documents."))
		self._BTN_remote_print.SetToolTipString(_("Put selected/all documents into remote print manager."))
		self._BTN_burn_items.SetToolTipString(_("Burn selected/all documents onto CD/DVD."))
		self._BTN_save_items.SetToolTipString(_("Save selected/all items to disk."))
		self._BTN_mail_items.SetToolTipString(_("E-mail selected/all documents."))
		self._BTN_fax_items.SetToolTipString(_("Fax selected/all documents."))
		self._BTN_archive_items.SetToolTipString(_("Store selected/all documents in document archive."))
		# end wxGlade

	def __do_layout(self):
		# begin wxGlade: wxgExportAreaPluginPnl.__do_layout
		__szr_main = wx.BoxSizer(wx.HORIZONTAL)
		__szr_buttons_right = wx.BoxSizer(wx.VERTICAL)
		__szr_main.Add(self._LCTRL_items, 1, wx.RIGHT | wx.EXPAND, 5)
		__szr_buttons_right.Add((20, 20), 0, wx.BOTTOM | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 3)
		__szr_buttons_right.Add(self._BTN_show_item, 0, wx.BOTTOM | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 3)
		__szr_buttons_right.Add(self._BTN_add_items, 0, wx.BOTTOM | wx.EXPAND, 3)
		__szr_buttons_right.Add(self._BTN_add_from_archive, 0, wx.BOTTOM | wx.EXPAND, 3)
		__szr_buttons_right.Add(self._BTN_scan_items, 0, wx.BOTTOM | wx.EXPAND, 3)
		__szr_buttons_right.Add(self._BTN_clipboard_items, 0, wx.BOTTOM | wx.EXPAND, 3)
		__szr_buttons_right.Add(self._BTN_remove_items, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 3)
		__szr_buttons_right.Add((20, 20), 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 0)
		__szr_buttons_right.Add(self._BTN_print_items, 0, wx.BOTTOM | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 3)
		__szr_buttons_right.Add(self._BTN_remote_print, 0, wx.BOTTOM | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 3)
		__szr_buttons_right.Add(self._BTN_burn_items, 0, wx.BOTTOM | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 3)
		__szr_buttons_right.Add(self._BTN_save_items, 0, wx.BOTTOM | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 3)
		__szr_buttons_right.Add(self._BTN_mail_items, 0, wx.BOTTOM | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 3)
		__szr_buttons_right.Add(self._BTN_fax_items, 0, wx.BOTTOM | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 3)
		__szr_buttons_right.Add(self._BTN_archive_items, 0, wx.BOTTOM | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 3)
		__szr_main.Add(__szr_buttons_right, 0, wx.EXPAND, 0)
		self.SetSizer(__szr_main)
		__szr_main.Fit(self)
		# end wxGlade

	def _on_list_item_selected(self, event):  # wxGlade: wxgExportAreaPluginPnl.<event_handler>
		print "Event handler '_on_list_item_selected' not implemented!"
		event.Skip()

	def _on_show_item_button_pressed(self, event):  # wxGlade: wxgExportAreaPluginPnl.<event_handler>
		print "Event handler '_on_show_item_button_pressed' not implemented!"
		event.Skip()

	def _on_add_items_button_pressed(self, event):  # wxGlade: wxgExportAreaPluginPnl.<event_handler>
		print "Event handler '_on_add_items_button_pressed' not implemented!"
		event.Skip()

	def _on_add_from_archive_button_pressed(self, event):  # wxGlade: wxgExportAreaPluginPnl.<event_handler>
		print "Event handler '_on_add_from_archive_button_pressed' not implemented!"
		event.Skip()

	def _on_scan_items_button_pressed(self, event):  # wxGlade: wxgExportAreaPluginPnl.<event_handler>
		print "Event handler '_on_scan_items_button_pressed' not implemented!"
		event.Skip()

	def _on_clipboard_items_button_pressed(self, event):  # wxGlade: wxgExportAreaPluginPnl.<event_handler>
		print "Event handler '_on_clipboard_items_button_pressed' not implemented!"
		event.Skip()

	def _on_remove_items_button_pressed(self, event):  # wxGlade: wxgExportAreaPluginPnl.<event_handler>
		print "Event handler '_on_remove_items_button_pressed' not implemented!"
		event.Skip()

	def _on_print_items_button_pressed(self, event):  # wxGlade: wxgExportAreaPluginPnl.<event_handler>
		print "Event handler '_on_print_items_button_pressed' not implemented!"
		event.Skip()

	def _on_remote_print_button_pressed(self, event):  # wxGlade: wxgExportAreaPluginPnl.<event_handler>
		print "Event handler '_on_remote_print_button_pressed' not implemented!"
		event.Skip()

	def _on_burn_items_button_pressed(self, event):  # wxGlade: wxgExportAreaPluginPnl.<event_handler>
		print "Event handler '_on_burn_items_button_pressed' not implemented!"
		event.Skip()

	def _on_save_items_button_pressed(self, event):  # wxGlade: wxgExportAreaPluginPnl.<event_handler>
		print "Event handler '_on_save_items_button_pressed' not implemented!"
		event.Skip()

	def _on_mail_items_button_pressed(self, event):  # wxGlade: wxgExportAreaPluginPnl.<event_handler>
		print "Event handler '_on_mail_items_button_pressed' not implemented!"
		event.Skip()

	def _on_fax_items_button_pressed(self, event):  # wxGlade: wxgExportAreaPluginPnl.<event_handler>
		print "Event handler '_on_fax_items_button_pressed' not implemented!"
		event.Skip()

	def _on_archive_items_button_pressed(self, event):  # wxGlade: wxgExportAreaPluginPnl.<event_handler>
		print "Event handler '_on_archive_items_button_pressed' not implemented!"
		event.Skip()

# end of class wxgExportAreaPluginPnl
