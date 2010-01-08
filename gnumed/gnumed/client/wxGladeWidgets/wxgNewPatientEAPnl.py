#!/usr/bin/env python
# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.3 from "/home/ncq/Projekte/gm-cvs/branches/HEAD/gnumed/gnumed/client/wxg/wxgNewPatientEAPnl.wxg"

import wx

# begin wxGlade: extracode
# end wxGlade



class wxgNewPatientEAPnl(wx.Panel):
    def __init__(self, *args, **kwds):

        from Gnumed.wxpython import gmDemographicsWidgets, gmDateTimeInput

        # begin wxGlade: wxgNewPatientEAPnl.__init__
        kwds["style"] = wx.NO_BORDER|wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        self._PRW_lastname = gmDemographicsWidgets.cLastnamePhraseWheel(self, -1, "", style=wx.NO_BORDER)
        self._PRW_firstnames = gmDemographicsWidgets.cFirstnamePhraseWheel(self, -1, "", style=wx.NO_BORDER)
        self._DP_dob = gmDateTimeInput.cDateInputCtrl(self, -1, style=wx.DP_DROPDOWN|wx.DP_ALLOWNONE|wx.DP_SHOWCENTURY)
        self._TCTRL_tob = wx.TextCtrl(self, -1, "", style=wx.NO_BORDER)
        self._PRW_gender = gmDemographicsWidgets.cGenderSelectionPhraseWheel(self, -1, "", style=wx.NO_BORDER)
        self._PRW_nickname = gmDemographicsWidgets.cNicknamePhraseWheel(self, -1, "", style=wx.NO_BORDER)
        self._PRW_title = gmDemographicsWidgets.cTitlePhraseWheel(self, -1, "", style=wx.NO_BORDER)
        self._PRW_address_searcher = gmDemographicsWidgets.cAddressPhraseWheel(self, -1, "", style=wx.NO_BORDER)
        self._PRW_zip = gmDemographicsWidgets.cZipcodePhraseWheel(self, -1, "", style=wx.NO_BORDER)
        self._PRW_street = gmDemographicsWidgets.cStreetPhraseWheel(self, -1, "", style=wx.NO_BORDER)
        self._TCTRL_number = wx.TextCtrl(self, -1, "", style=wx.NO_BORDER)
        self._PRW_urb = gmDemographicsWidgets.cUrbPhraseWheel(self, -1, "", style=wx.NO_BORDER)
        self._PRW_region = gmDemographicsWidgets.cStateSelectionPhraseWheel(self, -1, "", style=wx.NO_BORDER)
        self._PRW_country = gmDemographicsWidgets.cCountryPhraseWheel(self, -1, "", style=wx.NO_BORDER)
        self._TCTRL_phone = wx.TextCtrl(self, -1, "", style=wx.NO_BORDER)
        self._PRW_external_id_type = gmDemographicsWidgets.cExternalIDTypePhraseWheel(self, -1, "", style=wx.NO_BORDER)
        self._TCTRL_external_id_value = wx.TextCtrl(self, -1, "", style=wx.NO_BORDER)
        self._PRW_occupation = gmDemographicsWidgets.cOccupationPhraseWheel(self, -1, "", style=wx.NO_BORDER)
        self._TCTRL_comment = wx.TextCtrl(self, -1, "", style=wx.NO_BORDER)

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: wxgNewPatientEAPnl.__set_properties
        self._PRW_lastname.SetToolTipString(_("Required: lastname (family name)"))
        self._PRW_lastname.SetFocus()
        self._PRW_firstnames.SetToolTipString(_("Required: surname/first name/given name"))
        self._DP_dob.SetToolTipString(_("Recommended: Date of birth. Your current time zone applies."))
        self._TCTRL_tob.SetToolTipString(_("Optional: the time of birth if known"))
        self._PRW_gender.SetToolTipString(_("Required: gender"))
        self._PRW_nickname.SetToolTipString(_("Optional: nickname (alias, preferred name, call name, warrior name, artist name, pseudonym)"))
        self._PRW_title.SetToolTipString(_("Optional: title (academic or honorary). Note that a title applies to a person, not to a particular name of that person (it will be kept even if the name changes)."))
        self._PRW_address_searcher.SetToolTipString(_("Here you can enter a postal code or street name to search for an existing address from which the fields below will be pre-filled.\n\nThat address - or a new address created from any modifications below - will be used as the person's \"home\" address.\nnYou can also just enter the relevant information into the corresponding fields without searching for an existing address."))
        self._PRW_zip.SetToolTipString(_("Primary address: zip/postal code"))
        self._PRW_street.SetToolTipString(_("Primary address: name of street"))
        self._TCTRL_number.SetToolTipString(_("Primary address: number"))
        self._PRW_urb.SetToolTipString(_("Primary address: city/town/village/dwelling/..."))
        self._PRW_region.SetToolTipString(_("Primary address: state/province/county/..."))
        self._PRW_country.SetToolTipString(_("Primary address: country of residence"))
        self._TCTRL_phone.SetToolTipString(_("Primary phone number."))
        self._PRW_external_id_type.SetToolTipString(_("The type of the external ID (selection only)."))
        self._TCTRL_external_id_value.SetToolTipString(_("The value of the external ID."))
        self._PRW_occupation.SetToolTipString(_("The current occupation."))
        self._TCTRL_comment.SetToolTipString(_("A comment on this person."))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: wxgNewPatientEAPnl.__do_layout
        __szr_main = wx.BoxSizer(wx.VERTICAL)
        __fgsizer_details = wx.FlexGridSizer(20, 2, 3, 5)
        __szr_external_id_details = wx.BoxSizer(wx.HORIZONTAL)
        __szr_other = wx.BoxSizer(wx.HORIZONTAL)
        __szr_address = wx.BoxSizer(wx.HORIZONTAL)
        __szr_dob = wx.BoxSizer(wx.HORIZONTAL)
        __szr_identity = wx.BoxSizer(wx.HORIZONTAL)
        __szr_message = wx.BoxSizer(wx.HORIZONTAL)
        __szr_message.Add((20, 20), 1, wx.EXPAND, 0)
        __lbl_message = wx.StaticText(self, -1, _("Basic demographics"), style=wx.ALIGN_CENTRE)
        __lbl_message.SetFont(wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        __szr_message.Add(__lbl_message, 0, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        __szr_message.Add((20, 20), 1, wx.EXPAND, 0)
        __szr_main.Add(__szr_message, 0, wx.EXPAND, 0)
        __HLINE_top = wx.StaticLine(self, -1)
        __szr_main.Add(__HLINE_top, 0, wx.ALL|wx.EXPAND, 3)
        __fgsizer_details.Add((20, 20), 0, wx.EXPAND, 0)
        __szr_identity.Add((20, 20), 1, wx.EXPAND, 0)
        __lbl_identity = wx.StaticText(self, -1, _("Identity"), style=wx.ALIGN_CENTRE)
        __lbl_identity.SetForegroundColour(wx.Colour(95, 159, 159))
        __szr_identity.Add(__lbl_identity, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        __szr_identity.Add((20, 20), 1, wx.EXPAND, 0)
        __fgsizer_details.Add(__szr_identity, 1, wx.EXPAND, 0)
        __lbl_lastname = wx.StaticText(self, -1, _("Last name"))
        __lbl_lastname.SetForegroundColour(wx.Colour(255, 0, 0))
        __fgsizer_details.Add(__lbl_lastname, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        __fgsizer_details.Add(self._PRW_lastname, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        __lbl_firstnames = wx.StaticText(self, -1, _("First name(s)"))
        __lbl_firstnames.SetForegroundColour(wx.Colour(255, 0, 0))
        __fgsizer_details.Add(__lbl_firstnames, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        __fgsizer_details.Add(self._PRW_firstnames, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        __lbl_dob = wx.StaticText(self, -1, _("Date of birth"))
        __lbl_dob.SetForegroundColour(wx.Colour(255, 127, 0))
        __fgsizer_details.Add(__lbl_dob, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        __szr_dob.Add(self._DP_dob, 3, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 10)
        __lbl_tob = wx.StaticText(self, -1, _("Time:"))
        __szr_dob.Add(__lbl_tob, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 3)
        __szr_dob.Add(self._TCTRL_tob, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        __szr_dob.Add((20, 20), 1, wx.EXPAND, 0)
        __fgsizer_details.Add(__szr_dob, 1, wx.EXPAND, 0)
        __lbl_gender = wx.StaticText(self, -1, _("Gender"))
        __lbl_gender.SetForegroundColour(wx.Colour(255, 0, 0))
        __fgsizer_details.Add(__lbl_gender, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        __fgsizer_details.Add(self._PRW_gender, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        __lbl_nick_name = wx.StaticText(self, -1, _("Nick name"))
        __fgsizer_details.Add(__lbl_nick_name, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        __fgsizer_details.Add(self._PRW_nickname, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        __lbl_title = wx.StaticText(self, -1, _("Title"))
        __fgsizer_details.Add(__lbl_title, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        __fgsizer_details.Add(self._PRW_title, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        __fgsizer_details.Add((20, 20), 0, wx.EXPAND, 0)
        __szr_address.Add((20, 20), 1, wx.EXPAND, 0)
        __lbl_address_heading = wx.StaticText(self, -1, _("Primary (home) address (optional)"), style=wx.ALIGN_CENTRE)
        __lbl_address_heading.SetForegroundColour(wx.Colour(95, 159, 159))
        __szr_address.Add(__lbl_address_heading, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        __szr_address.Add((20, 20), 1, wx.EXPAND, 0)
        __fgsizer_details.Add(__szr_address, 1, wx.EXPAND, 0)
        __lbl_address = wx.StaticText(self, -1, _("Search"))
        __fgsizer_details.Add(__lbl_address, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        __fgsizer_details.Add(self._PRW_address_searcher, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        __lbl_zip = wx.StaticText(self, -1, _("Postal code"))
        __lbl_zip.SetForegroundColour(wx.Colour(255, 127, 0))
        __fgsizer_details.Add(__lbl_zip, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        __fgsizer_details.Add(self._PRW_zip, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        __lbl_street = wx.StaticText(self, -1, _("Street"))
        __lbl_street.SetForegroundColour(wx.Colour(255, 127, 0))
        __fgsizer_details.Add(__lbl_street, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        __fgsizer_details.Add(self._PRW_street, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        __lbl_number = wx.StaticText(self, -1, _("Number"))
        __lbl_number.SetForegroundColour(wx.Colour(255, 127, 0))
        __fgsizer_details.Add(__lbl_number, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        __fgsizer_details.Add(self._TCTRL_number, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        __lbl_urb = wx.StaticText(self, -1, _("Place"))
        __lbl_urb.SetForegroundColour(wx.Colour(255, 127, 0))
        __fgsizer_details.Add(__lbl_urb, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        __fgsizer_details.Add(self._PRW_urb, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        __lbl_region = wx.StaticText(self, -1, _("Region"))
        __lbl_region.SetForegroundColour(wx.Colour(255, 127, 0))
        __fgsizer_details.Add(__lbl_region, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        __fgsizer_details.Add(self._PRW_region, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        __lbl_zip_copy = wx.StaticText(self, -1, _("Country"))
        __lbl_zip_copy.SetForegroundColour(wx.Colour(255, 127, 0))
        __fgsizer_details.Add(__lbl_zip_copy, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        __fgsizer_details.Add(self._PRW_country, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        __fgsizer_details.Add((20, 20), 0, wx.EXPAND, 0)
        __szr_other.Add((20, 20), 1, wx.EXPAND, 0)
        __lbl_other = wx.StaticText(self, -1, _("Other"), style=wx.ALIGN_CENTRE)
        __lbl_other.SetForegroundColour(wx.Colour(95, 159, 159))
        __szr_other.Add(__lbl_other, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        __szr_other.Add((20, 20), 1, wx.EXPAND, 0)
        __fgsizer_details.Add(__szr_other, 1, wx.EXPAND, 0)
        __lbl_phone = wx.StaticText(self, -1, _("Phone"))
        __fgsizer_details.Add(__lbl_phone, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        __fgsizer_details.Add(self._TCTRL_phone, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        __lbl_ext_id = wx.StaticText(self, -1, _("External ID"))
        __fgsizer_details.Add(__lbl_ext_id, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        __szr_external_id_details.Add(self._PRW_external_id_type, 1, wx.RIGHT|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5)
        __szr_external_id_details.Add(self._TCTRL_external_id_value, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        __fgsizer_details.Add(__szr_external_id_details, 1, wx.EXPAND, 0)
        __lbl_occupation = wx.StaticText(self, -1, _("Occupation"))
        __fgsizer_details.Add(__lbl_occupation, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        __fgsizer_details.Add(self._PRW_occupation, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        __lbl_comment = wx.StaticText(self, -1, _("Comment"))
        __fgsizer_details.Add(__lbl_comment, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        __fgsizer_details.Add(self._TCTRL_comment, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        __fgsizer_details.AddGrowableCol(1)
        __szr_main.Add(__fgsizer_details, 1, wx.EXPAND, 0)
        __HLINE_bottom = wx.StaticLine(self, -1)
        __szr_main.Add(__HLINE_bottom, 0, wx.LEFT|wx.RIGHT|wx.TOP|wx.EXPAND, 3)
        self.SetSizer(__szr_main)
        __szr_main.Fit(self)
        # end wxGlade

# end of class wxgNewPatientEAPnl


