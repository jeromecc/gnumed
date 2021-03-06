#!/usr/bin/env python
# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.5 from "/home/ncq/Projekte/gm-git/gnumed/gnumed/client/wxg/wxgEditStaffListDlg.wxg"

import wx

# begin wxGlade: extracode
# end wxGlade


class wxgEditStaffListDlg(wx.Dialog):
    def __init__(self, *args, **kwds):

        from Gnumed.wxpython.gmStaffWidgets import cUserRolePRW

        # begin wxGlade: wxgEditStaffListDlg.__init__
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER | wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX | wx.THICK_FRAME
        wx.Dialog.__init__(self, *args, **kwds)
        self._LCTRL_staff = wx.ListCtrl(self, -1, style=wx.LC_REPORT | wx.LC_ALIGN_LEFT | wx.LC_SINGLE_SEL | wx.LC_SORT_ASCENDING | wx.NO_BORDER)
        self._TCTRL_name = wx.TextCtrl(self, -1, "", style=wx.TE_READONLY | wx.NO_BORDER)
        self._TCTRL_alias = wx.TextCtrl(self, -1, "", style=wx.NO_BORDER)
        self._TCTRL_account = wx.TextCtrl(self, -1, "", style=wx.NO_BORDER)
        self._PRW_user_role = cUserRolePRW(self, -1, "", style=wx.NO_BORDER)
        self._TCTRL_comment = wx.TextCtrl(self, -1, "", style=wx.NO_BORDER)
        self._btn_save = wx.Button(self, -1, _("Save"))
        self._btn_activate = wx.Button(self, -1, _("Activate"))
        self._btn_deactivate = wx.Button(self, -1, _("Deactivate"))
        self._btn_delete = wx.Button(self, -1, _("Delete"))
        self._btn_close = wx.Button(self, wx.ID_CANCEL, _("Close"))

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self._on_listitem_deselected, self._LCTRL_staff)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self._on_listitem_selected, self._LCTRL_staff)
        self.Bind(wx.EVT_BUTTON, self._on_save_button_pressed, self._btn_save)
        self.Bind(wx.EVT_BUTTON, self._on_activate_button_pressed, self._btn_activate)
        self.Bind(wx.EVT_BUTTON, self._on_deactivate_button_pressed, self._btn_deactivate)
        self.Bind(wx.EVT_BUTTON, self._on_delete_button_pressed, self._btn_delete)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: wxgEditStaffListDlg.__set_properties
        self.SetTitle(_("Edit staff list"))
        self.SetSize((682, 480))
        self._LCTRL_staff.SetToolTipString(_("The list of currently existing GNUmed users."))
        self._LCTRL_staff.SetFocus()
        self._TCTRL_name.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_BACKGROUND))
        self._TCTRL_alias.SetToolTipString(_("Short alias for the GNUmed user. Must be unique for this system."))
        self._TCTRL_account.SetToolTipString(_("The database account for this GNUmed user. Note that you cannot change your *own* database account."))
        self._PRW_user_role.SetToolTipString(_("Select the role of this GNUmed staff member.\n\nThe selected role defines the range of access rights."))
        self._TCTRL_comment.SetToolTipString(_("A short comment on this GNUmed user."))
        self._btn_save.SetToolTipString(_("Save modified user details.\n\nYou will need to know the password for the GNUmed database administrator <gm-dbo>."))
        self._btn_save.Enable(False)
        self._btn_activate.SetToolTipString(_("Activate selected user.\n\nYou will need to know the password for the GNUmed database administrator <gm-dbo>."))
        self._btn_activate.Enable(False)
        self._btn_deactivate.SetToolTipString(_("Deactivate selected user.\n\nYou will need to know the password for the GNUmed database administrator <gm-dbo>."))
        self._btn_deactivate.Enable(False)
        self._btn_delete.SetToolTipString(_("Entirely remove the GNUmed user (including the database account).\n\nThis will only be possible if no patient data was saved under this account. If any data exists the entry will be deactivated instead.\n\nYou will need to know the password for the GNUmed database administrator <gm-dbo>."))
        self._btn_delete.Enable(False)
        self._btn_close.SetToolTipString(_("Close this dialog."))
        self._btn_close.SetDefault()
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: wxgEditStaffListDlg.__do_layout
        __szr_main = wx.BoxSizer(wx.VERTICAL)
        __szr_buttons = wx.BoxSizer(wx.HORIZONTAL)
        _gszr_staff_editor = wx.FlexGridSizer(4, 2, 2, 2)
        __szr_account_details = wx.BoxSizer(wx.HORIZONTAL)
        __szr_main.Add(self._LCTRL_staff, 1, wx.EXPAND, 0)
        _lbl_name = wx.StaticText(self, -1, _("Name"))
        _gszr_staff_editor.Add(_lbl_name, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        _gszr_staff_editor.Add(self._TCTRL_name, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 0)
        _lbl_alias = wx.StaticText(self, -1, _("Alias"))
        _gszr_staff_editor.Add(_lbl_alias, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        _gszr_staff_editor.Add(self._TCTRL_alias, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 0)
        _lbl_account = wx.StaticText(self, -1, _("Account"))
        _gszr_staff_editor.Add(_lbl_account, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        __szr_account_details.Add(self._TCTRL_account, 1, wx.RIGHT | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 10)
        __lbl_role = wx.StaticText(self, -1, _("Role:"))
        __szr_account_details.Add(__lbl_role, 0, wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, 5)
        __szr_account_details.Add(self._PRW_user_role, 1, wx.ALIGN_CENTER_VERTICAL, 0)
        _gszr_staff_editor.Add(__szr_account_details, 1, wx.EXPAND, 0)
        _lbl_comment = wx.StaticText(self, -1, _("Comment"))
        _gszr_staff_editor.Add(_lbl_comment, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        _gszr_staff_editor.Add(self._TCTRL_comment, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 0)
        _gszr_staff_editor.AddGrowableCol(1)
        __szr_main.Add(_gszr_staff_editor, 0, wx.ALL | wx.EXPAND, 2)
        __szr_buttons.Add(self._btn_save, 0, 0, 0)
        __szr_buttons.Add((20, 20), 1, wx.EXPAND, 0)
        __szr_buttons.Add(self._btn_activate, 0, 0, 0)
        __szr_buttons.Add(self._btn_deactivate, 0, 0, 0)
        __szr_buttons.Add(self._btn_delete, 0, 0, 0)
        __szr_buttons.Add((20, 20), 1, wx.EXPAND, 0)
        __szr_buttons.Add(self._btn_close, 0, 0, 0)
        __szr_main.Add(__szr_buttons, 0, wx.EXPAND, 0)
        self.SetSizer(__szr_main)
        self.Layout()
        self.Centre()
        # end wxGlade

    def _on_listitem_deselected(self, event):  # wxGlade: wxgEditStaffListDlg.<event_handler>
        print "Event handler `_on_listitem_deselected' not implemented!"
        event.Skip()

    def _on_listitem_selected(self, event):  # wxGlade: wxgEditStaffListDlg.<event_handler>
        print "Event handler `_on_listitem_selected' not implemented!"
        event.Skip()

    def _on_save_button_pressed(self, event):  # wxGlade: wxgEditStaffListDlg.<event_handler>
        print "Event handler `_on_save_button_pressed' not implemented!"
        event.Skip()

    def _on_activate_button_pressed(self, event):  # wxGlade: wxgEditStaffListDlg.<event_handler>
        print "Event handler `_on_activate_button_pressed' not implemented!"
        event.Skip()

    def _on_deactivate_button_pressed(self, event):  # wxGlade: wxgEditStaffListDlg.<event_handler>
        print "Event handler `_on_deactivate_button_pressed' not implemented!"
        event.Skip()

    def _on_delete_button_pressed(self, event):  # wxGlade: wxgEditStaffListDlg.<event_handler>
        print "Event handler `_on_delete_button_pressed' not implemented!"
        event.Skip()

# end of class wxgEditStaffListDlg
if __name__ == "__main__":
    import gettext
    gettext.install("app") # replace with the appropriate catalog name

    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    dialog_1 = wxgEditStaffListDlg(None, -1, "")
    app.SetTopWindow(dialog_1)
    dialog_1.Show()
    app.MainLoop()
