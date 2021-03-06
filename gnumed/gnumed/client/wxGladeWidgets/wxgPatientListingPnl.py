#!/usr/bin/env python
# -*- coding: utf-8 -*-
# generated by wxGlade 0.5 on Thu Jul  5 22:05:25 2007 from /home/ncq/Projekte/gm-cvs/branches/HEAD/gnumed/gnumed/client/wxg/wxgPatientListingPnl.wxg

import wx

class wxgPatientListingPnl(wx.ScrolledWindow):
    def __init__(self, *args, **kwds):

        from Gnumed.wxpython import gmDataMiningWidgets

        # begin wxGlade: wxgPatientListingPnl.__init__
        kwds["style"] = wx.NO_BORDER|wx.TAB_TRAVERSAL
        wx.ScrolledWindow.__init__(self, *args, **kwds)
        self._lbl_msg = wx.StaticText(self, -1, _("Activate the respective patient by double-clicking a row."))
        self._LCTRL_items = gmDataMiningWidgets.cPatientListingCtrl(self, -1, style=wx.LC_REPORT|wx.LC_HRULES|wx.LC_VRULES|wx.SIMPLE_BORDER)
        self._BTN_1 = wx.Button(self, -1, "")
        self._BTN_2 = wx.Button(self, -1, "")
        self._BTN_3 = wx.Button(self, -1, "")
        self._BTN_4 = wx.Button(self, -1, "")
        self._BTN_5 = wx.Button(self, -1, "")

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self._on_BTN_1_pressed, self._BTN_1)
        self.Bind(wx.EVT_BUTTON, self._on_BTN_2_pressed, self._BTN_2)
        self.Bind(wx.EVT_BUTTON, self._on_BTN_3_pressed, self._BTN_3)
        self.Bind(wx.EVT_BUTTON, self._on_BTN_4_pressed, self._BTN_4)
        self.Bind(wx.EVT_BUTTON, self._on_BTN_5_pressed, self._BTN_5)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: wxgPatientListingPnl.__set_properties
        self.SetScrollRate(10, 10)
        self._BTN_1.Enable(False)
        self._BTN_2.Enable(False)
        self._BTN_3.Enable(False)
        self._BTN_4.Enable(False)
        self._BTN_5.Enable(False)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: wxgPatientListingPnl.__do_layout
        __szr_main = wx.BoxSizer(wx.VERTICAL)
        __szr_buttons = wx.BoxSizer(wx.HORIZONTAL)
        __szr_main.Add(self._lbl_msg, 0, wx.ALL|wx.EXPAND, 5)
        __szr_main.Add(self._LCTRL_items, 1, wx.ALL|wx.EXPAND, 5)
        __szr_buttons.Add((20, 20), 1, wx.EXPAND, 0)
        __szr_buttons.Add(self._BTN_1, 0, wx.RIGHT|wx.EXPAND, 5)
        __szr_buttons.Add(self._BTN_2, 0, wx.RIGHT|wx.EXPAND, 5)
        __szr_buttons.Add(self._BTN_3, 0, wx.RIGHT|wx.EXPAND, 5)
        __szr_buttons.Add(self._BTN_4, 0, wx.RIGHT|wx.EXPAND, 5)
        __szr_buttons.Add(self._BTN_5, 0, wx.EXPAND, 5)
        __szr_buttons.Add((20, 20), 1, wx.EXPAND, 0)
        __szr_main.Add(__szr_buttons, 0, wx.ALL|wx.EXPAND, 5)
        self.SetSizer(__szr_main)
        __szr_main.Fit(self)
        # end wxGlade

    def _on_BTN_1_pressed(self, event): # wxGlade: wxgPatientListingPnl.<event_handler>
        print "Event handler `_on_BTN_1_pressed' not implemented"
        event.Skip()

    def _on_BTN_2_pressed(self, event): # wxGlade: wxgPatientListingPnl.<event_handler>
        print "Event handler `_on_BTN_2_pressed' not implemented"
        event.Skip()

    def _on_BTN_3_pressed(self, event): # wxGlade: wxgPatientListingPnl.<event_handler>
        print "Event handler `_on_BTN_3_pressed' not implemented"
        event.Skip()

    def _on_BTN_4_pressed(self, event): # wxGlade: wxgPatientListingPnl.<event_handler>
        print "Event handler `_on_BTN_4_pressed' not implemented"
        event.Skip()

    def _on_BTN_5_pressed(self, event): # wxGlade: wxgPatientListingPnl.<event_handler>
        print "Event handler `_on_BTN_5_pressed' not implemented"
        event.Skip()

# end of class wxgPatientListingPnl


