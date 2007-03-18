#!/usr/bin/env python
# -*- coding: ISO-8859-15 -*-
# generated by wxGlade 0.4.1 on Sat Mar 10 14:37:42 2007

import wx

class wxgAllergyEditAreaDlg(wx.Dialog):
    def __init__(self, *args, **kwds):

        from Gnumed.wxpython import gmAllergyWidgets

        # begin wxGlade: wxgAllergyEditAreaDlg.__init__
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER|wx.MAXIMIZE_BOX|wx.MINIMIZE_BOX|wx.THICK_FRAME
        wx.Dialog.__init__(self, *args, **kwds)
        self._PNL_edit_area = gmAllergyWidgets.cAllergyEditAreaPnl(self, -1, style=wx.NO_BORDER|wx.TAB_TRAVERSAL)
        self._BTN_save = wx.Button(self, wx.ID_OK, _("Save/Update"))
        self._BTN_clear = wx.Button(self, -1, _("Clear/Reset"))
        self._BTN_cancel = wx.Button(self, wx.ID_CANCEL, _("Cancel"))

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self._on_save_button_pressed, id=wx.ID_OK)
        self.Bind(wx.EVT_BUTTON, self._on_clear_button_pressed, self._BTN_clear)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: wxgAllergyEditAreaDlg.__set_properties
        self.SetTitle(_("Edit Allergy/Intolerance"))
        self.SetSize((400, 190))
        self._BTN_save.SetToolTipString(_("Save the allergy/intolerance in the database."))
        self._BTN_clear.SetToolTipString(_("Clear all fields or reset to database values."))
        self._BTN_cancel.SetToolTipString(_("Cancel editing the allergy/intolerance."))
        self._BTN_cancel.SetDefault()
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: wxgAllergyEditAreaDlg.__do_layout
        __szr_main = wx.BoxSizer(wx.VERTICAL)
        __szr_buttons = wx.BoxSizer(wx.HORIZONTAL)
        __szr_main.Add(self._PNL_edit_area, 1, wx.ALL|wx.EXPAND, 2)
        __szr_buttons.Add(self._BTN_save, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        __szr_buttons.Add(self._BTN_clear, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        __szr_buttons.Add((20, 20), 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        __szr_buttons.Add(self._BTN_cancel, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        __szr_main.Add(__szr_buttons, 0, wx.TOP|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 15)
        self.SetAutoLayout(True)
        self.SetSizer(__szr_main)
        self.Layout()
        self.Centre()
        # end wxGlade

    def _on_save_button_pressed(self, event): # wxGlade: wxgAllergyEditAreaDlg.<event_handler>
        print "Event handler `_on_save_button_pressed' not implemented!"
        event.Skip()

    def _on_clear_button_pressed(self, event): # wxGlade: wxgAllergyEditAreaDlg.<event_handler>
        print "Event handler `_on_clear_button_pressed' not implemented!"
        event.Skip()

    def _on_cancel_button_pressed(self, event): # wxGlade: wxgAllergyEditAreaDlg.<event_handler>
        print "Event handler `_on_cancel_button_pressed' not implemented!"
        event.Skip()

# end of class wxgAllergyEditAreaDlg


