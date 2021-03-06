#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# generated by wxGlade 0.6.8
#

import wx

# begin wxGlade: dependencies
import gettext
# end wxGlade

# begin wxGlade: extracode
from Gnumed.wxpython import gmPhraseWheel
# end wxGlade


class wxgMetaTestTypeEAPnl(wx.ScrolledWindow):
	def __init__(self, *args, **kwds):
		# begin wxGlade: wxgMetaTestTypeEAPnl.__init__
		kwds["style"] = wx.NO_BORDER | wx.TAB_TRAVERSAL
		wx.ScrolledWindow.__init__(self, *args, **kwds)
		self._PRW_name = gmPhraseWheel.cPhraseWheel(self, wx.ID_ANY, "", style=wx.NO_BORDER)
		self._PRW_abbreviation = gmPhraseWheel.cPhraseWheel(self, wx.ID_ANY, "", style=wx.NO_BORDER)
		self._PRW_loinc = gmPhraseWheel.cPhraseWheel(self, wx.ID_ANY, "", style=wx.NO_BORDER)
		self._TCTRL_loinc_info = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.NO_BORDER)
		self._TCTRL_comment = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.NO_BORDER)
		self._LBL_member_detail = wx.StaticText(self, wx.ID_ANY, "")

		self.__set_properties()
		self.__do_layout()
		# end wxGlade

	def __set_properties(self):
		# begin wxGlade: wxgMetaTestTypeEAPnl.__set_properties
		self.SetScrollRate(10, 10)
		self._PRW_name.SetToolTipString(_("Mandatory: A descriptive name for this meta test type."))
		self._PRW_abbreviation.SetToolTipString(_("Mandatory: An abbreviation for this meta test type."))
		self._PRW_loinc.SetToolTipString(_("Optional: The LOINC for the meta test type."))
		self._TCTRL_loinc_info.Enable(False)
		self._TCTRL_comment.SetToolTipString(_("Optional: A comment on this meta test type."))
		# end wxGlade

	def __do_layout(self):
		# begin wxGlade: wxgMetaTestTypeEAPnl.__do_layout
		_gszr_main = wx.FlexGridSizer(6, 2, 1, 3)
		__lbl_meta_name = wx.StaticText(self, wx.ID_ANY, _("Name"))
		__lbl_meta_name.SetForegroundColour(wx.Colour(255, 0, 0))
		_gszr_main.Add(__lbl_meta_name, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		_gszr_main.Add(self._PRW_name, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 0)
		__lbl_abbreviation = wx.StaticText(self, wx.ID_ANY, _("Abbreviation"))
		__lbl_abbreviation.SetForegroundColour(wx.Colour(255, 0, 0))
		_gszr_main.Add(__lbl_abbreviation, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		_gszr_main.Add(self._PRW_abbreviation, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 0)
		__lbl_loinc = wx.StaticText(self, wx.ID_ANY, _("LOINC"))
		_gszr_main.Add(__lbl_loinc, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		_gszr_main.Add(self._PRW_loinc, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 0)
		_gszr_main.Add((20, 20), 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 0)
		_gszr_main.Add(self._TCTRL_loinc_info, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 0)
		__lbl_comment = wx.StaticText(self, wx.ID_ANY, _("Comment"))
		_gszr_main.Add(__lbl_comment, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		_gszr_main.Add(self._TCTRL_comment, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 0)
		__lbl_members = wx.StaticText(self, wx.ID_ANY, _("Contains"))
		_gszr_main.Add(__lbl_members, 0, 0, 0)
		_gszr_main.Add(self._LBL_member_detail, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 0)
		self.SetSizer(_gszr_main)
		_gszr_main.Fit(self)
		_gszr_main.AddGrowableRow(5)
		_gszr_main.AddGrowableCol(1)
		# end wxGlade

# end of class wxgMetaTestTypeEAPnl
