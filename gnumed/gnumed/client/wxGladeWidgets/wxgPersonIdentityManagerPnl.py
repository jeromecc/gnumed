#!/usr/bin/env python
# -*- coding: utf-8 -*-
# generated by wxGlade 0.5 on Mon Nov 26 13:17:24 2007 from /home/ncq/Projekte/gm-cvs/branches/HEAD/gnumed/gnumed/client/wxg/wxgPersonIdentityManagerPnl.wxg

import wx

class wxgPersonIdentityManagerPnl(wx.ScrolledWindow):
    def __init__(self, *args, **kwds):

        from Gnumed.wxpython import gmDemographicsWidgets

        # begin wxGlade: wxgPersonIdentityManagerPnl.__init__
        kwds["style"] = wx.NO_BORDER|wx.TAB_TRAVERSAL
        wx.ScrolledWindow.__init__(self, *args, **kwds)
        self._PNL_names = gmDemographicsWidgets.cPersonNamesManagerPnl(self, -1, style=wx.NO_BORDER|wx.TAB_TRAVERSAL)
        self._PNL_ids = gmDemographicsWidgets.cPersonIDsManagerPnl(self, -1, style=wx.NO_BORDER|wx.TAB_TRAVERSAL)

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: wxgPersonIdentityManagerPnl.__set_properties
        self.SetFocus()
        self.SetScrollRate(10, 10)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: wxgPersonIdentityManagerPnl.__do_layout
        __szr_main = wx.BoxSizer(wx.VERTICAL)
        __szr_main.Add(self._PNL_names, 1, wx.ALL|wx.EXPAND, 5)
        __szr_main.Add(self._PNL_ids, 1, wx.ALL|wx.EXPAND, 5)
        self.SetSizer(__szr_main)
        __szr_main.Fit(self)
        # end wxGlade

# end of class wxgPersonIdentityManagerPnl

