#!/usr/bin/env python
# -*- coding: ISO-8859-15 -*-
# generated by wxGlade 0.4.1 on Fri Dec 22 16:54:42 2006

import wx

class wxgEncounterEditAreaDlg(wx.Dialog):
    def __init__(self, *args, **kwds):

        from Gnumed.wxpython import gmEncounterWidgets

        # begin wxGlade: wxgEncounterEditAreaDlg.__init__
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER | wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX | wx.THICK_FRAME | wx.STAY_ON_TOP
        wx.Dialog.__init__(self, *args, **kwds)
        self._PNL_edit_area = gmEncounterWidgets.cEncounterEditAreaPnl(self, -1)
        self._BTN_save = wx.Button(self, wx.ID_OK, _("&Save"))
        self._BTN_close = wx.Button(self, wx.ID_CANCEL, _("Cancel"))

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self._on_save_button_pressed, id=wx.ID_OK)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: wxgEncounterEditAreaDlg.__set_properties
        self.SetTitle(_("edit encounter details"))
        self._BTN_save.SetToolTipString(_("Save the encounter details."))
        self._BTN_save.SetDefault()
        self._BTN_close.SetToolTipString(_("Close this dialog."))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: wxgEncounterEditAreaDlg.__do_layout
        __szr_main = wx.BoxSizer(wx.VERTICAL)
        __szr_buttons = wx.BoxSizer(wx.HORIZONTAL)
        __szr_main.Add(self._PNL_edit_area, 1, wx.ALL | wx.EXPAND, 5)
        __szr_buttons.Add(self._BTN_save, 0, wx.EXPAND, 0)
        __szr_buttons.Add((20, 20), 1, wx.EXPAND, 0)
        __szr_buttons.Add(self._BTN_close, 0, wx.EXPAND, 0)
        __szr_main.Add(__szr_buttons, 0, wx.LEFT | wx.RIGHT | wx.TOP | wx.EXPAND, 5)
        self.SetSizer(__szr_main)
        __szr_main.Fit(self)
        self.Layout()
        self.Centre()
        # end wxGlade

    def _on_save_button_pressed(self, event): # wxGlade: wxgEncounterEditAreaDlg.<event_handler>
        print "Event handler `_on_save_button_pressed' not implemented!"
        event.Skip()

# end of class wxgEncounterEditAreaDlg


