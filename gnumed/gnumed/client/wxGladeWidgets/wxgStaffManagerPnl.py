#!/usr/bin/env python
# -*- coding: ISO-8859-15 -*-
# generated by wxGlade 0.4cvs on Tue Jan 17 17:46:58 2006

import wx

class wxgStaffManagerPnl(wx.ScrolledWindow):
    def __init__(self, *args, **kwds):
        # begin wxGlade: wxgStaffManagerPnl.__init__
        kwds["style"] = wx.SIMPLE_BORDER|wx.TAB_TRAVERSAL
        wx.ScrolledWindow.__init__(self, *args, **kwds)
        self._LCTRL_users = wx.ListCtrl(self, -1, style=wx.LC_REPORT|wx.LC_ALIGN_LEFT|wx.LC_SINGLE_SEL|wx.LC_SORT_ASCENDING|wx.LC_HRULES|wx.LC_VRULES|wx.NO_BORDER)
        self._btn_edit_staff_details = wx.Button(self, -1, _("Edit staff details"))
        self._btn_discharge_staff = wx.Button(self, -1, _("Discharge staff"))
        self._btn_enlist_current_patient = wx.Button(self, -1, _("Enlist current patient"))
        self._pwheel_db_account = gmPhraseWheel.cPhraseWheel(self, -1, "", style=wx.NO_BORDER)
        self._pwheel_role = gmPhraseWheel.cPhraseWheel(self, -1, "", style=wx.NO_BORDER)
        self._txt_sign = wx.TextCtrl(self, -1, "", style=wx.NO_BORDER)
        self._txt_comment = wx.TextCtrl(self, -1, "", style=wx.NO_BORDER)
        self.button_1 = wx.Button(self, -1, _("button_1"))

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self._btn_edit_staff_details_pressed, self._btn_edit_staff_details)
        self.Bind(wx.EVT_BUTTON, self._btn_discharge_staff_pressed, self._btn_discharge_staff)
        self.Bind(wx.EVT_BUTTON, self._btn_enlist_current_patient_pressed, self._btn_enlist_current_patient)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: wxgStaffManagerPnl.__set_properties
        self.SetScrollRate(10, 10)
        self._LCTRL_users.SetToolTipString(_("Lists the existing users in the GNUmed system."))
        self._btn_edit_staff_details.SetToolTipString(_("Edit details of selected staff member."))
        self._btn_edit_staff_details.Enable(False)
        self._btn_discharge_staff.SetToolTipString(_("Discharge the selected person from the staff list."))
        self._btn_discharge_staff.Enable(False)
        self._btn_enlist_current_patient.SetToolTipString(_("Add a new user to the GNUmed system."))
        self._pwheel_db_account.SetFocus()
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: wxgStaffManagerPnl.__do_layout
        __szr_main = wx.BoxSizer(wx.HORIZONTAL)
        __szr_right_pane = wx.BoxSizer(wx.VERTICAL)
        __szr_btns_right = wx.BoxSizer(wx.HORIZONTAL)
        __szr_staff_details = wx.FlexGridSizer(3, 2, 3, 2)
        __szr_left_pane = wx.BoxSizer(wx.VERTICAL)
        __szr_btns_left = wx.BoxSizer(wx.HORIZONTAL)
        __szr_left_pane.Add(self._LCTRL_users, 1, wx.BOTTOM|wx.EXPAND, 2)
        __szr_btns_left.Add(self._btn_edit_staff_details, 0, wx.ADJUST_MINSIZE, 0)
        __szr_btns_left.Add(self._btn_discharge_staff, 0, wx.ADJUST_MINSIZE, 0)
        __szr_btns_left.Add(self._btn_enlist_current_patient, 0, wx.ADJUST_MINSIZE, 0)
        __szr_left_pane.Add(__szr_btns_left, 0, 0, 0)
        __szr_main.Add(__szr_left_pane, 1, wx.EXPAND, 0)
        __line_vert_sep = wx.StaticLine(self, -1, style=wx.LI_VERTICAL)
        __szr_main.Add(__line_vert_sep, 0, wx.EXPAND, 0)
        __lbl_db_account = wx.StaticText(self, -1, _("Account"), style=wx.ALIGN_RIGHT)
        __lbl_db_account.SetToolTipString(_("Required: The database account assigned to this staff member. Must exist in the database."))
        __szr_staff_details.Add(__lbl_db_account, 0, wx.ADJUST_MINSIZE, 0)
        __szr_staff_details.Add(self._pwheel_db_account, 0, wx.EXPAND|wx.ADJUST_MINSIZE, 2)
        __lbl_role = wx.StaticText(self, -1, _("Role"), style=wx.ALIGN_RIGHT)
        __lbl_role.SetToolTipString(_("Required: The organisation role for this staff member. Currently the only supported role is \"doctor\"."))
        __szr_staff_details.Add(__lbl_role, 0, wx.ADJUST_MINSIZE, 0)
        __szr_staff_details.Add(self._pwheel_role, 0, wx.EXPAND|wx.ADJUST_MINSIZE, 2)
        __lbl_sign = wx.StaticText(self, -1, _("Sign"), style=wx.ALIGN_RIGHT)
        __lbl_sign.SetToolTipString(_("Required: A short signature for this staff member such as the concatenated initials. Preferably not more than 5 characters."))
        __szr_staff_details.Add(__lbl_sign, 0, wx.ADJUST_MINSIZE, 0)
        __szr_staff_details.Add(self._txt_sign, 0, wx.EXPAND|wx.ADJUST_MINSIZE, 2)
        __lbl_comment = wx.StaticText(self, -1, _("Comment"))
        __lbl_comment.SetToolTipString(_("Optional: A free-text comment on this staff member."))
        __szr_staff_details.Add(__lbl_comment, 0, wx.ADJUST_MINSIZE, 0)
        __szr_staff_details.Add(self._txt_comment, 0, wx.EXPAND|wx.ADJUST_MINSIZE, 0)
        __szr_staff_details.AddGrowableCol(1)
        __szr_right_pane.Add(__szr_staff_details, 1, wx.EXPAND, 0)
        __szr_btns_right.Add(self.button_1, 0, wx.ADJUST_MINSIZE, 0)
        __szr_right_pane.Add(__szr_btns_right, 0, wx.EXPAND, 0)
        __szr_main.Add(__szr_right_pane, 1, wx.EXPAND, 0)
        self.SetAutoLayout(True)
        self.SetSizer(__szr_main)
        __szr_main.Fit(self)
        __szr_main.SetSizeHints(self)
        # end wxGlade

    def _btn_edit_staff_details_pressed(self, event): # wxGlade: wxgStaffManagerPnl.<event_handler>
        print "Event handler `_btn_edit_staff_details_pressed' not implemented!"
        event.Skip()

    def _btn_discharge_staff_pressed(self, event): # wxGlade: wxgStaffManagerPnl.<event_handler>
        print "Event handler `_btn_discharge_staff_pressed' not implemented!"
        event.Skip()

    def _btn_enlist_current_patient_pressed(self, event): # wxGlade: wxgStaffManagerPnl.<event_handler>
        print "Event handler `_btn_enlist_current_patient_pressed' not implemented!"
        event.Skip()

# end of class wxgStaffManagerPnl


