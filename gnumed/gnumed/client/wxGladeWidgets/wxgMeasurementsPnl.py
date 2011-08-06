#!/usr/bin/env python
# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.1 from "/home/ncq/Projekte/gm-cvs/branches/HEAD/gnumed/gnumed/client/wxg/wxgMeasurementsPnl.wxg"

import wx
import wx.grid

# begin wxGlade: extracode
# end wxGlade



class wxgMeasurementsPnl(wx.ScrolledWindow):
    def __init__(self, *args, **kwds):

        from Gnumed.wxpython import gmMeasurementWidgets

        # begin wxGlade: wxgMeasurementsPnl.__init__
        kwds["style"] = wx.NO_BORDER|wx.TAB_TRAVERSAL
        wx.ScrolledWindow.__init__(self, *args, **kwds)
        self.data_grid = gmMeasurementWidgets.cMeasurementsGrid(self, -1, size=(1, 1))
        self._BTN_add = wx.Button(self, wx.ID_ADD, "")
        self._RBTN_my_unsigned = wx.RadioButton(self, -1, _("&Your unsigned"))
        self._RBTN_all_unsigned = wx.RadioButton(self, -1, _("&All unsigned"))
        self._BTN_select = wx.Button(self, -1, _("&Select"))
        self._BTN_review = wx.Button(self, -1, _("&Actions ... "))

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self._on_add_button_pressed, self._BTN_add)
        self.Bind(wx.EVT_BUTTON, self._on_select_button_pressed, self._BTN_select)
        self.Bind(wx.EVT_BUTTON, self._on_review_button_pressed, self._BTN_review)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: wxgMeasurementsPnl.__set_properties
        self.SetScrollRate(10, 10)
        self._BTN_add.SetToolTipString(_("Add measurments."))
        self._RBTN_my_unsigned.SetToolTipString(_("Apply selection to those unsigned results for which you are to take responsibility."))
        self._RBTN_all_unsigned.SetToolTipString(_("Apply selection to all unsigned results."))
        self._BTN_select.SetToolTipString(_("Select results according to your choice on the left."))
        self._BTN_review.SetToolTipString(_("Invoke actions on the selected measurements."))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: wxgMeasurementsPnl.__do_layout
        __szr_main = wx.BoxSizer(wx.VERTICAL)
        __szr_bottom = wx.BoxSizer(wx.HORIZONTAL)
        __szr_main.Add(self.data_grid, 1, wx.LEFT|wx.RIGHT|wx.TOP|wx.EXPAND, 5)
        __hline_buttons = wx.StaticLine(self, -1)
        __szr_main.Add(__hline_buttons, 0, wx.ALL|wx.EXPAND, 5)
        __szr_bottom.Add((20, 20), 1, wx.ALIGN_CENTER_VERTICAL, 0)
        __szr_bottom.Add(self._BTN_add, 0, wx.ALIGN_CENTER_VERTICAL, 5)
        __szr_bottom.Add((20, 20), 2, wx.ALIGN_CENTER_VERTICAL, 0)
        __szr_bottom.Add(self._RBTN_my_unsigned, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 3)
        __szr_bottom.Add(self._RBTN_all_unsigned, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 3)
        __szr_bottom.Add(self._BTN_select, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        __szr_bottom.Add(self._BTN_review, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        __szr_bottom.Add((20, 20), 1, wx.ALIGN_CENTER_VERTICAL, 0)
        __szr_main.Add(__szr_bottom, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.EXPAND, 5)
        self.SetSizer(__szr_main)
        __szr_main.Fit(self)
        # end wxGlade

    def _on_select_unsigned_button_pressed(self, event): # wxGlade: wxgMeasurementsPnl.<event_handler>
        print "Event handler `_on_select_unsigned_button_pressed' not implemented!"
        event.Skip()

    def _on_select_your_unsigned_results_button_pressed(self, event): # wxGlade: wxgMeasurementsPnl.<event_handler>
        print "Event handler `_on_select_your_unsigned_results_button_pressed' not implemented!"
        event.Skip()

    def _on_review_button_pressed(self, event): # wxGlade: wxgMeasurementsPnl.<event_handler>
        print "Event handler `_on_review_button_pressed' not implemented!"
        event.Skip()

    def _on_select_my_unsigned_results_button_pressed(self, event): # wxGlade: wxgMeasurementsPnl.<event_handler>
        print "Event handler `_on_select_my_unsigned_results_button_pressed' not implemented"
        event.Skip()

    def _on_select_all_unsigned_results_button_pressed(self, event): # wxGlade: wxgMeasurementsPnl.<event_handler>
        print "Event handler `_on_select_all_unsigned_results_button_pressed' not implemented"
        event.Skip()

    def _on_select_button_pressed(self, event): # wxGlade: wxgMeasurementsPnl.<event_handler>
        print "Event handler `_on_select_button_pressed' not implemented"
        event.Skip()

    def _on_add_button_pressed(self, event): # wxGlade: wxgMeasurementsPnl.<event_handler>
        print "Event handler `_on_add_button_pressed' not implemented"
        event.Skip()

# end of class wxgMeasurementsPnl


