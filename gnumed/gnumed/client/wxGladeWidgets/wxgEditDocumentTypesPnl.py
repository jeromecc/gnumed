#!/usr/bin/env python
# -*- coding: ISO-8859-15 -*-
# generated by wxGlade 0.4.1 on Thu Dec  7 16:01:45 2006

import wx

class wxgEditDocumentTypesPnl(wx.ScrolledWindow):
    def __init__(self, *args, **kwds):

        from Gnumed.wxpython import gmListWidgets

        # begin wxGlade: wxgEditDocumentTypesPnl.__init__
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.ScrolledWindow.__init__(self, *args, **kwds)
        self._LCTRL_doc_type = gmListWidgets.cReportListCtrl(self, -1, style=wx.LC_REPORT|wx.LC_SINGLE_SEL|wx.SIMPLE_BORDER)
        self._TCTRL_type = wx.TextCtrl(self, -1, "", style=wx.NO_BORDER)
        self._TCTRL_l10n_type = wx.TextCtrl(self, -1, "", style=wx.NO_BORDER)
        self._BTN_set_translation = wx.Button(self, -1, _("Set &translation"))
        self._BTN_add = wx.Button(self, wx.ID_ADD, "")
        self._BTN_delete = wx.Button(self, wx.ID_DELETE, "")
        self._BTN_reassign = wx.Button(self, -1, _("&Reassign"))
        self._BTN_dismiss = wx.Button(self, wx.ID_CANCEL, _("&Close"))

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self._on_list_item_selected, self._LCTRL_doc_type)
        self.Bind(wx.EVT_TEXT, self._on_type_modified, self._TCTRL_type)
        self.Bind(wx.EVT_BUTTON, self._on_set_translation_button_pressed, self._BTN_set_translation)
        self.Bind(wx.EVT_BUTTON, self._on_add_button_pressed, self._BTN_add)
        self.Bind(wx.EVT_BUTTON, self._on_delete_button_pressed, self._BTN_delete)
        self.Bind(wx.EVT_BUTTON, self._on_reassign_button_pressed, self._BTN_reassign)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: wxgEditDocumentTypesPnl.__set_properties
        self.SetScrollRate(10, 10)
        self._LCTRL_doc_type.SetToolTipString(_("This lists the available document types."))
        self._LCTRL_doc_type.SetFocus()
        self._TCTRL_type.SetToolTipString(_("The document type, usually in Englisch."))
        self._TCTRL_l10n_type.SetToolTipString(_("The document type in the local language."))
        self._BTN_set_translation.SetToolTipString(_("Change translation of selected document type for your local language."))
        self._BTN_set_translation.Enable(False)
        self._BTN_add.SetToolTipString(_("Add above input as a new document type."))
        self._BTN_add.Enable(False)
        self._BTN_delete.SetToolTipString(_("Delete selected document type. Note that you can only delete document types that are not in use."))
        self._BTN_delete.Enable(False)
        self._BTN_reassign.SetToolTipString(_("Change the type of all documents currently having the selected document type."))
        self._BTN_reassign.Enable(False)
        self._BTN_dismiss.SetDefault()
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: wxgEditDocumentTypesPnl.__do_layout
        _szr_main = wx.BoxSizer(wx.VERTICAL)
        _szr_buttons = wx.BoxSizer(wx.HORIZONTAL)
        _gszr_editor = wx.FlexGridSizer(2, 2, 2, 2)
        _szr_main.Add(self._LCTRL_doc_type, 1, wx.EXPAND, 5)
        _lbl_name = wx.StaticText(self, -1, _("Type (English)"))
        _gszr_editor.Add(_lbl_name, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        _gszr_editor.Add(self._TCTRL_type, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        _lbl_local_name = wx.StaticText(self, -1, _("Local language"))
        _gszr_editor.Add(_lbl_local_name, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        _gszr_editor.Add(self._TCTRL_l10n_type, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        _gszr_editor.AddGrowableCol(1)
        _szr_main.Add(_gszr_editor, 0, wx.TOP|wx.BOTTOM|wx.EXPAND, 5)
        _szr_buttons.Add(self._BTN_set_translation, 0, wx.RIGHT, 3)
        _szr_buttons.Add(self._BTN_add, 0, wx.RIGHT, 3)
        _szr_buttons.Add(self._BTN_delete, 0, wx.RIGHT, 3)
        _szr_buttons.Add(self._BTN_reassign, 0, 0, 3)
        _szr_buttons.Add((5, 5), 1, wx.EXPAND, 0)
        _szr_buttons.Add(self._BTN_dismiss, 0, 0, 0)
        _szr_main.Add(_szr_buttons, 0, wx.EXPAND, 0)
        self.SetSizer(_szr_main)
        _szr_main.Fit(self)
        # end wxGlade

    def _on_list_item_selected(self, event): # wxGlade: wxgEditDocumentTypesPnl.<event_handler>
        print "Event handler `_on_list_item_selected' not implemented!"
        event.Skip()

    def _on_add_button_pressed(self, event): # wxGlade: wxgEditDocumentTypesPnl.<event_handler>
        print "Event handler `_on_add_button_pressed' not implemented!"
        event.Skip()

    def _on_delete_button_pressed(self, event): # wxGlade: wxgEditDocumentTypesPnl.<event_handler>
        print "Event handler `_on_delete_button_pressed' not implemented!"
        event.Skip()

    def _on_type_modified(self, event): # wxGlade: wxgEditDocumentTypesPnl.<event_handler>
        print "Event handler `_on_type_modified' not implemented"
        event.Skip()

    def _on_set_translation_button_pressed(self, event): # wxGlade: wxgEditDocumentTypesPnl.<event_handler>
        print "Event handler `_on_set_translation_button_pressed' not implemented"
        event.Skip()

    def _on_reassign_button_pressed(self, event): # wxGlade: wxgEditDocumentTypesPnl.<event_handler>
        print "Event handler `_on_reassign_button_pressed' not implemented"
        event.Skip()

# end of class wxgEditDocumentTypesPnl


