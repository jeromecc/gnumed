#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# generated by wxGlade 0.7.2
#

import wx

# begin wxGlade: dependencies
import gettext
# end wxGlade

# begin wxGlade: extracode
from Gnumed.wxpython.gmMeasurementWidgets import cUnitPhraseWheel
from Gnumed.wxpython.gmTextCtrl import cTextCtrl
from Gnumed.wxpython.gmSubstanceMgmtWidgets import cSubstancePhraseWheel
# end wxGlade


class wxgSingleComponentGenericDrugEAPnl(wx.ScrolledWindow):
	def __init__(self, *args, **kwds):

		from Gnumed.wxpython.gmMedicationWidgets import cSubstancePreparationPhraseWheel

		# begin wxGlade: wxgSingleComponentGenericDrugEAPnl.__init__
		kwds["style"] = wx.BORDER_NONE | wx.TAB_TRAVERSAL
		wx.ScrolledWindow.__init__(self, *args, **kwds)
		self._LBL_drug_name = wx.StaticText(self, wx.ID_ANY, "")
		self._PRW_substance = cSubstancePhraseWheel(self, wx.ID_ANY, "", style=wx.BORDER_NONE)
		self._TCTRL_amount = cTextCtrl(self, wx.ID_ANY, "", style=wx.BORDER_NONE)
		self._PRW_unit = cUnitPhraseWheel(self, wx.ID_ANY, "", style=wx.BORDER_NONE)
		self._PRW_dose_unit = cUnitPhraseWheel(self, wx.ID_ANY, "", style=wx.BORDER_NONE)
		self._PRW_preparation = cSubstancePreparationPhraseWheel(self, wx.ID_ANY, "", style=wx.BORDER_NONE)

		self.__set_properties()
		self.__do_layout()
		# end wxGlade

	def __set_properties(self):
		# begin wxGlade: wxgSingleComponentGenericDrugEAPnl.__set_properties
		self.SetScrollRate(10, 10)
		self._PRW_substance.SetToolTipString(_("The active component of this generic drug."))
		self._TCTRL_amount.SetToolTipString(_("Enter the amount of substance (such as the \"5\" in \"5mg/ml\")."))
		self._PRW_unit.SetToolTipString(_("The unit of the amount of substance (such as the \"mg\" in \"5mg/ml\")."))
		self._PRW_dose_unit.SetToolTipString(_("The unit of the reference amount (such as the \"ml\" in \"5mg/ml\"). If left empty it means \"per delivery unit\" (such as tablet, sachet, capsule, suppository)."))
		# end wxGlade

	def __do_layout(self):
		# begin wxGlade: wxgSingleComponentGenericDrugEAPnl.__do_layout
		_gszr_main = wx.FlexGridSizer(5, 2, 1, 3)
		__szr_unit = wx.BoxSizer(wx.HORIZONTAL)
		__lbl_drug_name = wx.StaticText(self, wx.ID_ANY, _("Drug name"))
		_gszr_main.Add(__lbl_drug_name, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		_gszr_main.Add(self._LBL_drug_name, 0, wx.EXPAND, 0)
		__lbl_substance = wx.StaticText(self, wx.ID_ANY, _("Substance"))
		_gszr_main.Add(__lbl_substance, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		_gszr_main.Add(self._PRW_substance, 0, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 0)
		__lbl_amount = wx.StaticText(self, wx.ID_ANY, _("Amount"))
		_gszr_main.Add(__lbl_amount, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		_gszr_main.Add(self._TCTRL_amount, 0, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 10)
		__lbl_unit = wx.StaticText(self, wx.ID_ANY, _("Unit"))
		_gszr_main.Add(__lbl_unit, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		__szr_unit.Add(self._PRW_unit, 0, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND | wx.RIGHT, 5)
		__lbl_dose_unit = wx.StaticText(self, wx.ID_ANY, _("per"))
		__szr_unit.Add(__lbl_dose_unit, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
		__szr_unit.Add(self._PRW_dose_unit, 0, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 10)
		_gszr_main.Add(__szr_unit, 1, 0, 0)
		__lbl_preparation = wx.StaticText(self, wx.ID_ANY, _("Preparation"))
		_gszr_main.Add(__lbl_preparation, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		_gszr_main.Add(self._PRW_preparation, 1, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 10)
		self.SetSizer(_gszr_main)
		_gszr_main.Fit(self)
		_gszr_main.AddGrowableCol(1)
		self.Layout()
		# end wxGlade

# end of class wxgSingleComponentGenericDrugEAPnl
