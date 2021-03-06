#!/usr/bin/env python
# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.3 from "/home/ncq/Projekte/gm-git/gnumed/gnumed/client/wxg/wxgOrgUnitAddressPnl.wxg"

import wx

# begin wxGlade: extracode
# end wxGlade



class wxgOrgUnitAddressPnl(wx.ScrolledWindow):
    def __init__(self, *args, **kwds):

        from Gnumed.wxpython.gmAddressWidgets import cAddressPhraseWheel

        # begin wxGlade: wxgOrgUnitAddressPnl.__init__
        kwds["style"] = wx.NO_BORDER|wx.TAB_TRAVERSAL
        wx.ScrolledWindow.__init__(self, *args, **kwds)
        self._LBL_message = wx.StaticText(self, -1, "", style=wx.ALIGN_CENTRE)
        self._PRW_address_searcher = cAddressPhraseWheel(self, -1, "", style=wx.NO_BORDER)
        self._BTN_save_picked_address = wx.Button(self, -1, _("&Link"), style=wx.BU_EXACTFIT)
        self._BTN_add_new_address = wx.Button(self, -1, _("Link &new"), style=wx.BU_EXACTFIT)
        self._BTN_manage_addresses = wx.Button(self, -1, _("Browse"), style=wx.BU_EXACTFIT)

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self._on_save_picked_address_button_pressed, self._BTN_save_picked_address)
        self.Bind(wx.EVT_BUTTON, self._on_add_new_address_button_pressed, self._BTN_add_new_address)
        self.Bind(wx.EVT_BUTTON, self._on_manage_addresses_button_pressed, self._BTN_manage_addresses)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: wxgOrgUnitAddressPnl.__set_properties
        self.SetScrollRate(10, 10)
        self._LBL_message.Hide()
        self._PRW_address_searcher.SetToolTipString(_("Search for matches among existing addresses and [Link] a selection, or [Link (a) new] address."))
        self._BTN_save_picked_address.SetToolTipString(_("Link the selected address with the organizational unit."))
        self._BTN_save_picked_address.Enable(False)
        self._BTN_add_new_address.SetToolTipString(_("Enter a new address and link it to the organizational unit."))
        self._BTN_manage_addresses.SetToolTipString(_("Browse all known addresses (loading can be slow)."))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: wxgOrgUnitAddressPnl.__do_layout
        __szr_main = wx.BoxSizer(wx.VERTICAL)
        __szr_buttons = wx.BoxSizer(wx.HORIZONTAL)
        __szr_address_search = wx.BoxSizer(wx.HORIZONTAL)
        __szr_main.Add(self._LBL_message, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        __lbl_searcher = wx.StaticText(self, -1, _("Address"))
        __szr_address_search.Add(__lbl_searcher, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 3)
        __szr_address_search.Add(self._PRW_address_searcher, 1, wx.ALIGN_CENTER_VERTICAL, 5)
        __szr_main.Add(__szr_address_search, 0, wx.EXPAND, 0)
        __szr_buttons.Add((20, 20), 2, wx.ALIGN_CENTER_VERTICAL, 0)
        __szr_buttons.Add(self._BTN_save_picked_address, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        __szr_buttons.Add((20, 20), 1, wx.ALIGN_CENTER_VERTICAL, 0)
        __szr_buttons.Add(self._BTN_add_new_address, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        __szr_buttons.Add((20, 20), 1, wx.ALIGN_CENTER_VERTICAL, 0)
        __szr_buttons.Add(self._BTN_manage_addresses, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        __szr_buttons.Add((20, 20), 2, wx.ALIGN_CENTER_VERTICAL, 0)
        __szr_main.Add(__szr_buttons, 0, wx.TOP|wx.EXPAND, 3)
        self.SetSizer(__szr_main)
        __szr_main.Fit(self)
        # end wxGlade

    def _on_save_picked_address_button_pressed(self, event): # wxGlade: wxgOrgUnitAddressPnl.<event_handler>
        print "Event handler `_on_save_picked_address_button_pressed' not implemented"
        event.Skip()

    def _on_add_new_address_button_pressed(self, event): # wxGlade: wxgOrgUnitAddressPnl.<event_handler>
        print "Event handler `_on_add_new_address_button_pressed' not implemented"
        event.Skip()

    def _on_manage_addresses_button_pressed(self, event): # wxGlade: wxgOrgUnitAddressPnl.<event_handler>
        print "Event handler `_on_manage_addresses_button_pressed' not implemented"
        event.Skip()

# end of class wxgOrgUnitAddressPnl


