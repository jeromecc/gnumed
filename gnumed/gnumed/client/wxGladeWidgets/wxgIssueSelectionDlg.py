#!/usr/bin/env python
# -*- coding: ISO-8859-15 -*-
# generated by wxGlade 0.4cvs on Sat Jun 24 20:56:42 2006

import wx

class wxgIssueSelectionDlg(wx.Dialog):
    def __init__(self, *args, **kwds):

        from Gnumed.wxpython import gmEMRStructWidgets

        # begin wxGlade: wxgIssueSelectionDlg.__init__
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER|wx.MAXIMIZE_BOX|wx.MINIMIZE_BOX|wx.THICK_FRAME
        wx.Dialog.__init__(self, *args, **kwds)
        self._lbl_message = wx.StaticText(self, -1, _("Please select a health issue:"))
        self._PhWheel_issue = gmEMRStructWidgets.cIssueSelectionPhraseWheel(self, -1)
        self._BTN_OK = wx.Button(self, wx.ID_OK, _("OK"))
        self._BTN_dismiss = wx.Button(self, wx.ID_CANCEL, _("Close"))

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self._on_OK_button_pressed, id=wx.ID_OK)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: wxgIssueSelectionDlg.__set_properties
        self.SetTitle(_("Health issue selector"))
        self.SetSize((300, 150))
        self._PhWheel_issue.SetFocus()
        self._BTN_OK.SetDefault()
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: wxgIssueSelectionDlg.__do_layout
        _szr_main = wx.BoxSizer(wx.VERTICAL)
        _szr_buttons = wx.BoxSizer(wx.HORIZONTAL)
        _szr_main.Add(self._lbl_message, 1, wx.ALL|wx.EXPAND, 3)
        _szr_main.Add(self._PhWheel_issue, 0, wx.EXPAND, 0)
        _szr_buttons.Add(self._BTN_OK, 0, 0, 0)
        _szr_buttons.Add((20, 20), 1, wx.EXPAND, 0)
        _szr_buttons.Add(self._BTN_dismiss, 0, 0, 0)
        _szr_main.Add(_szr_buttons, 0, wx.EXPAND, 0)
        self.SetAutoLayout(True)
        self.SetSizer(_szr_main)
        self.Layout()
        self.Centre()
        # end wxGlade

    def _on_OK_button_pressed(self, event): # wxGlade: wxgIssueSelectionDlg.<event_handler>
        print "Event handler `_on_OK_button_pressed' not implemented"
        event.Skip()

# end of class wxgIssueSelectionDlg


