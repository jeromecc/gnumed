#!/usr/bin/env python
# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.5 from "/home/ncq/Projekte/gm-git/gnumed/gnumed/client/wxg/wxgBillItemEAPnl.wxg"

import wx

# begin wxGlade: extracode
# end wxGlade


class wxgBillItemEAPnl(wx.ScrolledWindow):
    def __init__(self, *args, **kwds):

        from Gnumed.wxpython.gmEncounterWidgets import cEncounterPhraseWheel
        from Gnumed.wxpython.gmDateTimeInput import cDateInputPhraseWheel
        from Gnumed.wxpython.gmBillingWidgets import cBillablePhraseWheel

        # begin wxGlade: wxgBillItemEAPnl.__init__
        kwds["style"] = wx.NO_BORDER | wx.TAB_TRAVERSAL
        wx.ScrolledWindow.__init__(self, *args, **kwds)
        self._PRW_billable = cBillablePhraseWheel(self, -1, "", style=wx.NO_BORDER)
        self._PRW_encounter = cEncounterPhraseWheel(self, -1, "", style=wx.NO_BORDER)
        self._PRW_date = cDateInputPhraseWheel(self, -1, "", style=wx.NO_BORDER)
        self._TCTRL_count = wx.TextCtrl(self, -1, "", style=wx.NO_BORDER)
        self._TCTRL_amount = wx.TextCtrl(self, -1, "", style=wx.NO_BORDER)
        self._LBL_currency = wx.StaticText(self, -1, _("EUR"))
        self._TCTRL_factor = wx.TextCtrl(self, -1, "", style=wx.NO_BORDER)
        self._TCTRL_comment = wx.TextCtrl(self, -1, "", style=wx.NO_BORDER)

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: wxgBillItemEAPnl.__set_properties
        self.SetScrollRate(10, 10)
        self._PRW_billable.SetToolTipString(_("The billable from which to create the bill item."))
        self._PRW_encounter.SetToolTipString(_("The encounter this item belongs to (or was created under)."))
        self._PRW_date.SetToolTipString(_("Optional: Pick the date at which to bill this item. If this is left blank the bill will show the date of the corresponding encounter."))
        self._TCTRL_count.SetToolTipString(_("How many units of the item are to be charged."))
        self._TCTRL_amount.SetToolTipString(_("Base amount w/o VAT."))
        self._TCTRL_factor.SetToolTipString(_("The factor by which to multiply the base amount. Normally 1.\n\n 0: complimentary items\n >1: increases\n <1: rebates\n <0:  credit notes"))
        self._TCTRL_comment.SetToolTipString(_("Optional: An item-specific comment to be put on the bill."))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: wxgBillItemEAPnl.__do_layout
        __gszr_main = wx.FlexGridSizer(7, 2, 1, 3)
        __szr_amount = wx.BoxSizer(wx.HORIZONTAL)
        __lbl_billable = wx.StaticText(self, -1, _("Item"))
        __gszr_main.Add(__lbl_billable, 0, 0, 0)
        __gszr_main.Add(self._PRW_billable, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 0)
        __lbl_encounter = wx.StaticText(self, -1, _("Encounter"))
        __gszr_main.Add(__lbl_encounter, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        __gszr_main.Add(self._PRW_encounter, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 0)
        __lbl_name = wx.StaticText(self, -1, _("Charge Date"))
        __gszr_main.Add(__lbl_name, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        __gszr_main.Add(self._PRW_date, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        __lbl_count = wx.StaticText(self, -1, _("No of Units"))
        __gszr_main.Add(__lbl_count, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        __gszr_main.Add(self._TCTRL_count, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        __lbl_amount = wx.StaticText(self, -1, _("Value"))
        __gszr_main.Add(__lbl_amount, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        __szr_amount.Add(self._TCTRL_amount, 0, wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, 3)
        __szr_amount.Add(self._LBL_currency, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        __gszr_main.Add(__szr_amount, 1, wx.EXPAND, 0)
        __lbl_factor = wx.StaticText(self, -1, _("Factor"))
        __gszr_main.Add(__lbl_factor, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        __gszr_main.Add(self._TCTRL_factor, 0, 0, 0)
        __lbl_comment = wx.StaticText(self, -1, _("Comment"))
        __gszr_main.Add(__lbl_comment, 0, 0, 0)
        __gszr_main.Add(self._TCTRL_comment, 0, wx.EXPAND, 0)
        self.SetSizer(__gszr_main)
        __gszr_main.Fit(self)
        __gszr_main.AddGrowableCol(1)
        # end wxGlade

# end of class wxgBillItemEAPnl
