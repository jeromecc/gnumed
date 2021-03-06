#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# generated by wxGlade 0.7.1
#

import wx

# begin wxGlade: dependencies
import gettext
# end wxGlade

# begin wxGlade: extracode
# end wxGlade


class wxgUnhandledExceptionDlg(wx.Dialog):
	def __init__(self, *args, **kwds):
		# begin wxGlade: wxgUnhandledExceptionDlg.__init__
		kwds["style"] = wx.DEFAULT_DIALOG_STYLE | wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX | wx.RESIZE_BORDER
		wx.Dialog.__init__(self, *args, **kwds)
		self.__pnl_top_message = wx.Panel(self, wx.ID_ANY, style=wx.BORDER_NONE)
		self._TCTRL_comment = wx.TextCtrl(self, wx.ID_ANY, "")
		self._TCTRL_sender = wx.TextCtrl(self, wx.ID_ANY, _("Please supply your email address here !"))
		self._TCTRL_helpdesk = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.BORDER_NONE | wx.TE_READONLY)
		self._TCTRL_logfile = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.BORDER_NONE | wx.TE_READONLY)
		self._TCTRL_exc_type = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.BORDER_NONE | wx.TE_READONLY)
		self._TCTRL_exc_value = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.BORDER_NONE | wx.TE_READONLY)
		self._TCTRL_traceback = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.HSCROLL | wx.TE_MULTILINE | wx.TE_READONLY)
		self.__szr_middle_staticbox = wx.StaticBox(self, wx.ID_ANY, _("Details"))
		self._BTN_ok = wx.Button(self, wx.ID_OK, _("Keep running"))
		self._BTN_close = wx.Button(self, wx.ID_CANCEL, _("Close GNUmed"))
		self._BTN_view_log = wx.Button(self, wx.ID_ANY, _("View log"))
		self._BTN_mail = wx.Button(self, wx.ID_ANY, _("Send report"))

		self.__set_properties()
		self.__do_layout()

		self.Bind(wx.EVT_BUTTON, self._on_close_gnumed_button_pressed, id=wx.ID_CANCEL)
		self.Bind(wx.EVT_BUTTON, self._on_view_log_button_pressed, self._BTN_view_log)
		self.Bind(wx.EVT_BUTTON, self._on_mail_button_pressed, self._BTN_mail)
		# end wxGlade

	def __set_properties(self):
		# begin wxGlade: wxgUnhandledExceptionDlg.__set_properties
		self.SetTitle(_("GNUmed exception handler"))
		self.__pnl_top_message.SetBackgroundColour(wx.Colour(255, 0, 0))
		self._TCTRL_comment.SetToolTipString(_("Enter any additional data or commentary you wish to provide such as what you were about to do."))
		self._TCTRL_comment.SetFocus()
		self._TCTRL_sender.SetToolTipString(_("Please enter your email address so we can provide help to you directly.\n\nOtherwise, feedback can be given on the GNUmed mailing list (http://lists.gnu.org/mailman/listinfo/gnumed-bugs) ONLY to which you will then have to subscribe."))
		self._TCTRL_helpdesk.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_BACKGROUND))
		self._TCTRL_helpdesk.SetToolTipString(_("Find help on http://wiki.gnumed.de, too."))
		self._TCTRL_helpdesk.Enable(False)
		self._TCTRL_logfile.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_BACKGROUND))
		self._TCTRL_logfile.Enable(False)
		self._TCTRL_exc_type.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_BACKGROUND))
		self._TCTRL_exc_type.Enable(False)
		self._TCTRL_exc_value.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_BACKGROUND))
		self._TCTRL_exc_value.Enable(False)
		self._BTN_ok.SetToolTipString(_("Close this dialog but keep running GNUmed."))
		self._BTN_ok.SetDefault()
		self._BTN_close.SetToolTipString(_("Close this dialog AND the GNUmed client."))
		self._BTN_view_log.SetToolTipString(_("View the log file."))
		self._BTN_mail.SetToolTipString(_("Email a bug report to the GNUmed developers.\n\nMost questions will be answered on the mailing list so you are well advised to either subscribe or check its archive (http://lists.gnu.org/mailman/listinfo/gnumed-bugs).\n\nIf you specify your address in the Sender field above the developers will be able to contact you directly for feedback."))
		# end wxGlade

	def __do_layout(self):
		# begin wxGlade: wxgUnhandledExceptionDlg.__do_layout
		__szr_main = wx.BoxSizer(wx.VERTICAL)
		__szr_buttons = wx.BoxSizer(wx.HORIZONTAL)
		self.__szr_middle_staticbox.Lower()
		__szr_middle = wx.StaticBoxSizer(self.__szr_middle_staticbox, wx.VERTICAL)
		_gszr_details = wx.FlexGridSizer(6, 2, 3, 5)
		__szr_top_inner = wx.BoxSizer(wx.VERTICAL)
		__lbl_top_message = wx.StaticText(self.__pnl_top_message, wx.ID_ANY, _("An unhandled exception has occurred."), style=wx.ALIGN_CENTER)
		__lbl_top_message.SetBackgroundColour(wx.Colour(255, 0, 0))
		__lbl_top_message.SetForegroundColour(wx.Colour(255, 255, 0))
		__lbl_top_message.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
		__szr_top_inner.Add(__lbl_top_message, 0, wx.ALL | wx.EXPAND, 10)
		self.__pnl_top_message.SetSizer(__szr_top_inner)
		__szr_main.Add(self.__pnl_top_message, 0, wx.EXPAND, 0)
		__lbl_explanation = wx.StaticText(self, wx.ID_ANY, _("GNUmed detected an error for which no specific handler had been defined.\n\nDetails about the error can be found in the log file a copy of which has\nbeen saved away in your home directory (see below). It may contain\nbits of sensitive information so you may want to screen the content\nbefore handing it to IT staff for debugging.\n\nGNUmed will try to keep running. However, it is strongly advised to\nclose this GNUmed workplace as soon as possible. You can try to save\nunsaved data but don't count on it.\n\nIt should then be safe to restart GNUmed.\n\nDocumentation to be found at <http://wiki.gnumed.de>."))
		__szr_main.Add(__lbl_explanation, 0, wx.ALL | wx.EXPAND, 5)
		__lbl_comment = wx.StaticText(self, wx.ID_ANY, _("Comment"))
		__lbl_comment.SetToolTipString(_("Enter a short comment on what you were trying to do with GNUmed. This information will be added to the logfile for easier identification later on."))
		_gszr_details.Add(__lbl_comment, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		_gszr_details.Add(self._TCTRL_comment, 0, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 0)
		__lbl_sender = wx.StaticText(self, wx.ID_ANY, _("Sender"))
		_gszr_details.Add(__lbl_sender, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		_gszr_details.Add(self._TCTRL_sender, 0, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 0)
		__lbl_helpdesk = wx.StaticText(self, wx.ID_ANY, _("Help desk"))
		_gszr_details.Add(__lbl_helpdesk, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		_gszr_details.Add(self._TCTRL_helpdesk, 0, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 0)
		__lbl_logfile = wx.StaticText(self, wx.ID_ANY, _("Log file"))
		_gszr_details.Add(__lbl_logfile, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		_gszr_details.Add(self._TCTRL_logfile, 0, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 0)
		__lbl_type = wx.StaticText(self, wx.ID_ANY, _("Type"))
		_gszr_details.Add(__lbl_type, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		_gszr_details.Add(self._TCTRL_exc_type, 0, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 0)
		__lbl_value = wx.StaticText(self, wx.ID_ANY, _("Value"))
		_gszr_details.Add(__lbl_value, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		_gszr_details.Add(self._TCTRL_exc_value, 0, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 0)
		_gszr_details.AddGrowableCol(1)
		__szr_middle.Add(_gszr_details, 0, wx.BOTTOM | wx.EXPAND | wx.TOP, 5)
		__szr_middle.Add(self._TCTRL_traceback, 1, wx.EXPAND, 0)
		__szr_main.Add(__szr_middle, 1, wx.ALL | wx.EXPAND, 5)
		__szr_buttons.Add((20, 20), 1, wx.EXPAND, 0)
		__szr_buttons.Add(self._BTN_ok, 0, wx.EXPAND | wx.RIGHT, 3)
		__szr_buttons.Add(self._BTN_close, 0, wx.EXPAND | wx.LEFT, 3)
		__szr_buttons.Add((20, 20), 1, wx.EXPAND, 0)
		__szr_buttons.Add(self._BTN_view_log, 0, wx.EXPAND | wx.RIGHT, 3)
		__szr_buttons.Add(self._BTN_mail, 0, wx.EXPAND | wx.LEFT, 3)
		__szr_buttons.Add((20, 20), 1, wx.EXPAND, 0)
		__szr_main.Add(__szr_buttons, 0, wx.ALL | wx.EXPAND, 5)
		self.SetSizer(__szr_main)
		__szr_main.Fit(self)
		self.Layout()
		self.Centre()
		# end wxGlade

	def _on_close_gnumed_button_pressed(self, event):  # wxGlade: wxgUnhandledExceptionDlg.<event_handler>
		print "Event handler '_on_close_gnumed_button_pressed' not implemented!"
		event.Skip()

	def _on_view_log_button_pressed(self, event):  # wxGlade: wxgUnhandledExceptionDlg.<event_handler>
		print "Event handler '_on_view_log_button_pressed' not implemented!"
		event.Skip()

	def _on_mail_button_pressed(self, event):  # wxGlade: wxgUnhandledExceptionDlg.<event_handler>
		print "Event handler '_on_mail_button_pressed' not implemented!"
		event.Skip()

# end of class wxgUnhandledExceptionDlg
