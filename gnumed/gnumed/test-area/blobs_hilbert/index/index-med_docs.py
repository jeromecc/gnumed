#!/usr/bin/python

# $Source: /home/ncq/Projekte/cvs2git/vcs-mirror/gnumed/gnumed/test-area/blobs_hilbert/index/Attic/index-med_docs.py,v $
__version__ = "$Revision: 1.5 $"
__author__ = "Sebastian Hilbert <Sebastian.Hilbert@gmx.net>\
			  Karsten Hilbert <Karsten.Hilbert@gmx.net>"

from wxPython.wx import *
from wxPython.lib.anchors import LayoutAnchors

#import Image
import os, time, shutil, os.path

# location of our modules
sys.path.append(os.path.join('.', 'modules'))

import gmLog
gmLog.gmDefLog.SetAllLogLevels(gmLog.lData)

from docPatient import *
from docDocument import cDocument
from gmPhraseWheel import *
import gmCfg, gmI18N
import docXML

_log = gmLog.gmDefLog
__cfg__ = gmCfg.gmDefCfg

[wxID_INDEXFRAME, wxID_INDEXFRAMEADDITIONCOMMENTBOX, wxID_INDEXFRAMEBEFNRBOX, wxID_INDEXFRAMEBEFUNDDATE, wxID_INDEXFRAMEDATEOFBIRTHBOX, wxID_INDEXFRAMEDELPICBUTTON, wxID_INDEXFRAMEDESCRIPTIONCHOICEBOX, wxID_INDEXFRAMEFIRSTNAMEBOX, wxID_INDEXFRAMEGETPAGESBUTTON, wxID_INDEXFRAMELASTNAMEBOX, wxID_INDEXFRAMELBOXPAGES, wxID_INDEXFRAMEMAINPANEL, wxID_INDEXFRAMEREADFAXBUTTON, wxID_INDEXFRAMESAVEBUTTON, wxID_INDEXFRAMESHORTDECRIPTIONBOX, wxID_INDEXFRAMESHOWPICBUTTON, wxID_INDEXFRAMESTATICTEXT1, wxID_INDEXFRAMESTATICTEXT10, wxID_INDEXFRAMESTATICTEXT11, wxID_INDEXFRAMESTATICTEXT12, wxID_INDEXFRAMESTATICTEXT13, wxID_INDEXFRAMESTATICTEXT2, wxID_INDEXFRAMESTATICTEXT3, wxID_INDEXFRAMESTATICTEXT4, wxID_INDEXFRAMESTATICTEXT5, wxID_INDEXFRAMESTATICTEXT6, wxID_INDEXFRAMESTATICTEXT7, wxID_INDEXFRAMESTATICTEXT8, wxID_INDEXFRAMESTATICTEXT9] = map(lambda _init_ctrls: wxNewId(), range(29))

#====================================
class indexFrame(wxFrame):

	doc_pages = []
	page = 0
	selected_pic = ''
	#---------------------------------------------------------------------------
	def __init__(self, parent):

		# get valid document types from ini-file
		self.valid_doc_types = string.split(__cfg__.get("metadata", "doctypes"),',')

		# init ctrls
		self._init_ctrls(parent)

		# we are indexing data from one particular patient
		# this is a design decision
		if not self.__load_patient():
			raise ValueError
		self.__fill_pat_fields()

		# repository base
		self.repository = os.path.abspath(os.path.expanduser(__cfg__.get("repositories", "to_index")))

		# items for phraseWheel
		if not self._init_phrase_wheel():
			raise ValueError
	#---------------------------------------------------------------------------
	def _init_utils(self):
		pass
	#---------------------------------------------------------------------------
	def _init_ctrls(self, prnt):

		#-- basic frame -------------
		wxFrame.__init__(
			self,
			id = wxID_INDEXFRAME,
			name = 'indexFrame',
			parent = prnt,
			pos = wxPoint(361, 150),
			size = wxSize(763, 616),
			style = wxDEFAULT_FRAME_STYLE,
			title = _('Please select a document for this patient.')
		)
		self._init_utils()
		self.SetClientSize(wxSize(763, 616))

		#-- main panel -------------
		self.PNL_main = wxPanel(
			id = wxID_INDEXFRAMEMAINPANEL,
			name = 'main panel',
			parent = self,
			pos = wxPoint(0, 0),
			size = wxSize(763, 616),
			style = wxTAB_TRAVERSAL
		)
		self.PNL_main.SetBackgroundColour(wxColour(225, 225, 225))

		#-- load pages button -------------
		self.BTN_get_pages = wxButton(
			id = wxID_INDEXFRAMEGETPAGESBUTTON,
			label = _('load pages'),
			name = 'BTN_get_pages',
			parent = self.PNL_main,
			pos = wxPoint(48, 160),
			size = wxSize(176, 22),
			style = 0
		)
		self.BTN_get_pages.SetToolTipString(_('load the pages of this document'))
		EVT_BUTTON(self.BTN_get_pages, wxID_INDEXFRAMEGETPAGESBUTTON, self.on_get_pages)

		#-- load fax button -------------
		self.BTN_read_fax = wxButton(
			id = wxID_INDEXFRAMEREADFAXBUTTON,
			label = _('load fax document'),
			name = 'BTN_read_fax',
			parent = self.PNL_main,
			pos = wxPoint(48, 232),
			size = wxSize(176, 22),
			style = 0
		)
		self.BTN_read_fax.SetToolTipString(_('currently non-functional: load a fax document'))

		#-- list box with pages -------------
		self.LBOX_doc_pages = wxListBox(
			choices = [],
			id = wxID_INDEXFRAMELBOXPAGES,
			name = 'LBOX_doc_pages',
			parent = self.PNL_main,
			pos = wxPoint(48, 288),
			size = wxSize(182, 94),
			style = wxLB_SORT,
			validator = wxDefaultValidator
		)
		self.LBOX_doc_pages.SetToolTipString(_('these pages make up the current document'))

		#-- load pages button -------------
		self.BTN_show_page = wxButton(
			id = wxID_INDEXFRAMESHOWPICBUTTON,
			label = _('show page'),
			name = 'BTN_show_page',
			parent = self.PNL_main,
			pos = wxPoint(48, 400),
			size = wxSize(95, 22),
			style = 0
		)
		self.BTN_show_page.SetToolTipString(_('display selected part of the document'))
		EVT_BUTTON(self.BTN_show_page, wxID_INDEXFRAMESHOWPICBUTTON, self.on_show_page)


		self.delPicButton = wxButton(id = wxID_INDEXFRAMEDELPICBUTTON, label = _('delete page'), name = 'delPicButton', parent = self.PNL_main, pos = wxPoint(143, 400), size = wxSize(90, 22), style = 0)
		#EVT_BUTTON(self.delPicButton, wxID_INDEXFRAMEDELPICBUTTON, self.OnDelpicbuttonButton)


		#-- first name text box -------------
		self.TBOX_first_name = wxTextCtrl(
			id = wxID_INDEXFRAMEFIRSTNAMEBOX,
			name = 'TBOX_first_name',
			parent = self.PNL_main,
			pos = wxPoint(304, 112),
			size = wxSize(152, 22),
			style = wxTE_READONLY,
			value = 'loading ...'
		)
		self.TBOX_first_name.SetToolTipString(_('not editable, loaded from file'))
		self.TBOX_first_name.SetBackgroundColour(wxColour(255, 255, 255))

		#-- last name text box -------------
		self.TBOX_last_name = wxTextCtrl(
			id = wxID_INDEXFRAMELASTNAMEBOX,
			name = 'TBOX_last_name',
			parent = self.PNL_main,
			pos = wxPoint(304, 160),
			size = wxSize(152, 22),
			style = wxTE_READONLY,
			value = 'loading ...'
		)
		self.TBOX_last_name.SetToolTipString(_('not editable, loaded from file'))
		self.TBOX_last_name.SetBackgroundColour(wxColour(255, 255, 255))

		#-- dob text box -------------
		self.TBOX_dob = wxTextCtrl(
			id = wxID_INDEXFRAMEDATEOFBIRTHBOX,
			name = 'TBOX_dob',
			parent = self.PNL_main,
			pos = wxPoint(304, 232),
			size = wxSize(152, 22),
			style = wxTE_READONLY,
			value = 'loading ...'
		)
		self.TBOX_dob.SetToolTipString(_('not editable, loaded from file'))
		#self.TBOX_last_name.SetBackgroundColour(wxColour(255, 255, 255))

		#-- document date text box -------------
		self.TBOX_doc_date = wxTextCtrl(
			id = wxID_INDEXFRAMEBEFUNDDATE,
			name = 'TBOX_doc_date',
			parent = self.PNL_main,
			pos = wxPoint(304, 312),
			size = wxSize(152, 22),
			style = 0,
			value = _('please fill in')
		)
		self.TBOX_doc_date.SetToolTipString(_('date of creation of the document content\nformat: YYYY-MM-DD'))

		#-- short document comment text box -------------
		self.TBOX_desc_short = wxTextCtrl(
			id = wxID_INDEXFRAMESHORTDECRIPTIONBOX,
			name = 'TBOX_desc_short',
			parent = self.PNL_main,
			pos = wxPoint(304, 368),
			size = wxSize(152, 22),
			style = 0,
			value = _('please fill in')
		)
		self.TBOX_desc_short.SetToolTipString(_('a short comment on the document content'))

		#-- document type selection box -------------
		self.SelBOX_doc_type = wxComboBox(
			choices = self.valid_doc_types,
			id = wxID_INDEXFRAMEDESCRIPTIONCHOICEBOX,
			name = 'SelBOX_doc_type',
			parent = self.PNL_main,
			pos = wxPoint(304, 416),
			size = wxSize(152, 22),
			style = 0,
			validator = wxDefaultValidator,
			value = _('choose document type')
		)
		self.SelBOX_doc_type.SetLabel('')
		self.SelBOX_doc_type.SetToolTipString(_('Document types are determined by the database.\nAsk your database administrator to add more types if needed.'))

		#-- long document comment text box -------------
		self.TBOX_desc_long = wxTextCtrl(
			id = wxID_INDEXFRAMEADDITIONCOMMENTBOX,
			name = 'TBOX_desc_long',
			parent = self.PNL_main,
			pos = wxPoint(48, 488),
			size = wxSize(640, 88),
			style = wxTE_MULTILINE,
			value = '')
		self.TBOX_desc_long.SetToolTipString(_('a summary or longer comment for this document'))

		#-- save data button -------------
		self.BTN_save_data = wxButton(
			id = wxID_INDEXFRAMESAVEBUTTON,
			label = _('save data'),
			name = 'BTN_save_data',
			parent = self.PNL_main,
			pos = wxPoint(544, 112),
			size = wxSize(144, 328),
			style = 0
		)
		self.BTN_save_data.SetToolTipString(_('save entered metadata with document'))
		EVT_BUTTON(self.BTN_save_data, wxID_INDEXFRAMESAVEBUTTON, self.on_save_data)

		self.staticText1 = wxStaticText(
			id = wxID_INDEXFRAMESTATICTEXT1,
			label = _('1) select'),
			name = 'staticText1',
			parent = self.PNL_main,
			pos = wxPoint(48, 56),
			size = wxSize(19, 29),
			style = 0
		)
		self.staticText1.SetFont(wxFont(25, wxSWISS, wxNORMAL, wxNORMAL, false, ''))

		self.staticText2 = wxStaticText(
			id = wxID_INDEXFRAMESTATICTEXT2,
			label = _('2) describe'),
			name = 'staticText2',
			parent = self.PNL_main,
			pos = wxPoint(312, 56),
			size = wxSize(19, 29),
			style = 0
		)
		self.staticText2.SetFont(wxFont(25, wxSWISS, wxNORMAL, wxNORMAL, false, ''))

		self.staticText3 = wxStaticText(
			id = wxID_INDEXFRAMESTATICTEXT3,
			label = _('3) save'),
			name = 'staticText3',
			parent = self.PNL_main,
			pos = wxPoint(560, 56),
			size = wxSize(19, 29),
			style = 0
		)
		self.staticText3.SetFont(wxFont(25, wxSWISS, wxNORMAL, wxNORMAL, false, ''))

		self.staticText4 = wxStaticText(id = wxID_INDEXFRAMESTATICTEXT4, label = _('or'), name = 'staticText4', parent = self.PNL_main, pos = wxPoint(48, 192), size = wxSize(49, 29), style = 0)
		self.staticText4.SetFont(wxFont(25, wxSWISS, wxNORMAL, wxNORMAL, false, ''))

		self.staticText5 = wxStaticText(id = wxID_INDEXFRAMESTATICTEXT5, label = _('date (YYYY-MM-DD)'), name = 'staticText5', parent = self.PNL_main, pos = wxPoint(304, 288), size = wxSize(158, 16), style = 0)

		self.staticText6 = wxStaticText(id = wxID_INDEXFRAMESTATICTEXT6, label = _('date of birth'), name = 'staticText6', parent = self.PNL_main, pos = wxPoint(304, 208), size = wxSize(152, 16), style = 0)

		self.staticText7 = wxStaticText(
			id = wxID_INDEXFRAMESTATICTEXT7,
			label = _('document identifier'),
			name = 'staticText7',
			parent = self.PNL_main,
			pos = wxPoint(48, 96),
			size = wxSize(176, 16),
			style = 0
		)

		self.staticText8 = wxStaticText(
			id = wxID_INDEXFRAMESTATICTEXT8,
			label = _('document pages'),
			name = 'staticText8',
			parent = self.PNL_main,
			pos = wxPoint(48, 264),
			size = wxSize(152, 16),
			style = 0
		)

		self.staticText9 = wxStaticText(
			id = wxID_INDEXFRAMESTATICTEXT9,
			label = _('first name'),
			name = 'staticText9',
			parent = self.PNL_main,
			pos = wxPoint(304, 96),
			size = wxSize(152, 16),
			style = 0
		)

		self.staticText10 = wxStaticText(
			id = wxID_INDEXFRAMESTATICTEXT10,
			label = _('last name'),
			name = 'staticText10',
			parent = self.PNL_main,
			pos = wxPoint(304, 144),
			size = wxSize(152, 16),
			style = 0
		)

		self.staticText11 = wxStaticText(id = wxID_INDEXFRAMESTATICTEXT11, label = _('short comment'), name = 'staticText11', parent = self.PNL_main, pos = wxPoint(304, 352), size = wxSize(152, 16), style = 0)

		self.staticText12 = wxStaticText(
			id = wxID_INDEXFRAMESTATICTEXT12,
			label = _('document type'),
			name = 'staticText12',
			parent = self.PNL_main,
			pos = wxPoint(304, 400),
			size = wxSize(152, 16),
			style = 0
		)

		self.staticText13 = wxStaticText(
			id = wxID_INDEXFRAMESTATICTEXT13,
			label = _('additional comment'),
			name = 'staticText13',
			parent = self.PNL_main,
			pos=wxPoint(48, 464),
			size = wxSize(143, 16),
			style = 0
		)
	#--------------------------------
	def _init_phrase_wheel(self):
		"""Set up phrase wheel.

		- directory names in self.repository correspond to identification
		  strings on paper documents
		- when starting to type an ident the phrase wheel must
		  show matching directories
		"""

		# get document directories
		doc_dirs = os.listdir(self.repository)

		# generate list of choices
		phrase_wheel_choices = []
		for i in range(len(doc_dirs)):
			full_dir = os.path.join(self.repository, doc_dirs[i])

			# don't add stray files
			if not os.path.isdir(full_dir):
				_log.Log(gmLog.lData, "ignoring stray file [%s]" % doc_dirs[i])
				continue

			if not self.__could_be_locked(full_dir):
				_log.Log(gmLog.lInfo, "Document directory [%s] not yet checkpointed for indexing. Skipping." % full_dir)
				continue

			# same weight for all of them
			phrase_wheel_choices.append({'ID': i, 'label': doc_dirs[i], 'weight': 1})

		#<DEBUG>
		_log.Log(gmLog.lData, "document dirs: %s" % str(phrase_wheel_choices))
		#</DEBUG>

		if len(phrase_wheel_choices) == 0:
			_log.Log(gmLog.lWarn, "No document directories in repository. Nothing to do !.")
			dlg = wxMessageDialog(
				self,
				_("There are no documents in the repository.\n(%s)\n\nSeems like there's nothing to do today." % self.repository),
				_('Information'),
				wxOK | wxICON_INFORMATION
			)
			dlg.ShowModal()
			dlg.Destroy()
			return None

		# FIXME: we need to set this to non-learning mode
		mp = cMatchProvider_FixedList(phrase_wheel_choices)
		self.doc_id_wheel = cPhraseWheel(
			self.PNL_main,
			self.wheel_callback,
			pos = (48, 112),
			size = (176, 22),
			aMatchProvider = mp,
			aDelay = 400
		)
		self.doc_id_wheel.SetToolTipString(_('the document identifier is usually written or stamped onto the physical pages of the document'))
		self.doc_id_wheel.on_resize (None)

		return 1
	#----------------------------------------
	# event handlers
	#----------------------------------------
	def on_get_pages(self, event):
		_log.Log(gmLog.lData, "Trying to load document.")

		curr_doc_id = self.doc_id_wheel.GetLineText(0)

		# has the user supplied anything ?
		if curr_doc_id == '':
			_log.Log(gmLog.lErr, 'No document ID typed in yet !')
			dlg = wxMessageDialog(
				self,
				_('You must type in a document ID !\n\nUsually you will find the document ID written on\nthe physical sheet of paper. There should be only one\nper document even if there are multiple pages.'),
				_('missing document ID'),
				wxOK | wxICON_EXCLAMATION
			)
			dlg.ShowModal()
			dlg.Destroy()
			return None

		full_dir = os.path.join(self.repository, curr_doc_id)

		# lock this directory now
		if not self.__lock_for_indexing(full_dir):
			_log.Log(gmLog.lErr, "Cannot lock directory [%s] for indexing." % full_dir)
			dlg = wxMessageDialog(
				self,
				_('Cannot lock document directory for indexing.\n(%s)\n\nPlease consult the error log for details.' % full_dir),
				_('Error'),
				wxOK | wxICON_ERROR
			)
			dlg.ShowModal()
			dlg.Destroy()
			return None

		# actually try loading pages
		if not self.__load_doc(full_dir):
			_log.Log(gmLog.lErr, "Cannot load document object file list.")
			dlg = wxMessageDialog(
				self,
				_('Cannot load document object file list from xDT file.\n\nPlease consult the error log for details.'),
				_('Error'),
				wxOK | wxICON_ERROR
			)
			dlg.ShowModal()
			dlg.Destroy()
			return None

		self.__fill_doc_fields()
	#----------------------------------------
	def on_save_data(self, event):
		"""Save collected metadata into XML file."""

		event.Skip()

		if not self.__valid_input():
			return None
		else:
			full_dir = os.path.join(self.repository, self.doc_id_wheel.GetLineText(0))
			self.__dump_metadata_to_xml(full_dir)
			self.__unlock_for_import(full_dir)
			self.__clear_doc_fields()
			self.doc_id_wheel.Clear()
			# FIXME: this needs to be reloaded !
			#self.initgmPhraseWheel()
	#----------------------------------------
	def on_show_page(self, event):
		page_idx = self.LBOX_doc_pages.GetSelection()

		if page_idx != -1:
			page_data = self.LBOX_doc_pages.GetClientData(page_idx)
			page_fname = page_data['file name']

			import docMime

			mime_type = docMime.guess_mimetype(page_fname)
			viewer_cmd = docMime.get_viewer_cmd(mime_type, page_fname)

			if viewer_cmd == None:
				__log__.Log(gmLog.lWarn, "Cannot determine viewer via standard mailcap mechanism. Desperately trying to guess.")
				new_fname = docMime.get_win_fname(mime_type)
				_log.Log(gmLog.lData, "%s -> %s -> %s" % (page_fname, mime_type, new_fname))
				shutil.copyfile(page_fname, new_fname)
				os.startfile(new_fname)
			else:
				_log.Log(gmLog.lData, "%s -> %s -> %s" % (page_fname, mime_type, viewer_cmd))
				os.system(viewer_cmd)
		else:
			dlg = wxMessageDialog(
				self,
				_('You must select a page before you can view it.'),
				_('Attention'),
				wxOK | wxICON_INFORMATION
			)
			dlg.ShowModal()
			dlg.Destroy()
	#---------------------------------------------------------------------------
	def wheel_callback (self, data):
		print "Selected :%s" % data
	#----------------------------------------
	# internal methods
	#----------------------------------------
	def __load_patient(self):
		# later on we might want to provide access
		# to other methods of getting the patient

		# get patient data from BDT/XDT file
		pat_file = os.path.abspath(os.path.expanduser(__cfg__.get("metadata", "patient_file")))
		pat_format = __cfg__.get("metadata", "patient_format")
		self.myPatient = cPatient()
		if not self.myPatient.loadFromFile(pat_format, pat_file):
			_log.Log(gmLog.lPanic, "Cannot read patient from %s file [%s]" % (pat_format, pat_file))
			dlg = wxMessageDialog(
				self,
				_('Cannot load patient from %s file.\n\nPlease consult the error log for details.' % pat_format),
				_('Error'),
				wxOK | wxICON_ERROR
			)
			dlg.ShowModal()
			dlg.Destroy()
			return None

		return 1
	#----------------------------------------
	def __fill_pat_fields(self):
		self.TBOX_first_name.SetValue(self.myPatient.firstnames)
		self.TBOX_last_name.SetValue(self.myPatient.lastnames)
		self.TBOX_dob.SetValue(self.myPatient.dob)
	#----------------------------------------
	def __clear_doc_fields(self):
		# clear fields
		self.TBOX_doc_date.SetValue(_('please fill in'))
		self.TBOX_desc_short.SetValue(_('please fill in'))
		self.TBOX_desc_long.SetValue(_('please fill in'))
		#self.SelBOX_doc_type.SetSelection(-1)
		self.SelBOX_doc_type.SetValue(_('choose document type'))
		self.LBOX_doc_pages.Clear()
	#----------------------------------------
	def __load_doc(self, aDir):
		# well, so load the document from that directory
		_log.Log(gmLog.lData, 'working in [%s]' % aDir)

		# check for metadata file
		fname = os.path.join(aDir, __cfg__.get("metadata", "description"))
		if not os.path.exists (fname):
			_log.Log(gmLog.lErr, 'Cannot access metadata file [%s].' % fname)
			dlg = wxMessageDialog(self, 
				_('Cannot access metadata file\n[%s].\nPlease see error log for details.' % fname),
				_('Error'),
				wxOK | wxICON_ERROR
			)
			dlg.ShowModal()
			dlg.Destroy()
			return None

		# actually get pages
		self.myDoc = cDocument()
		if not self.myDoc.loadImgListFromXML(fname, aDir):
			_log.Log(gmLog.lErr, 'Cannot load image list from metadata file[%s].' % fname)
			dlg = wxMessageDialog(self, 
				_('Cannot load image list from metadata file\n[%s].\n\nPlease see error log for details.' % fname),
				_('Error'),
				wxOK | wxICON_ERROR
			)
			dlg.ShowModal()
			dlg.Destroy()
			return None

		return 1
	#----------------------------------------
	def __fill_doc_fields(self):
		self.__clear_doc_fields()
		objLst = self.myDoc.getMetaData()['objects']
		for obj in objLst.values():
			page_num = obj['index']
			path, name = os.path.split(obj['file name'])
			self.LBOX_doc_pages.Append(_('page %s (%s in %s)') % (page_num, name, path), obj)
	#----------------------------------------
	def __dump_metadata_to_xml(self, aDir):

		content = []

		tag = __cfg__.get("metadata", "document_tag")
		content.append('<%s>\n' % tag)

		tag = __cfg__.get("metadata", "name_tag")
		content.append('<%s>%s</%s>\n' % (tag, self.myPatient.lastnames, tag))

		tag = __cfg__.get("metadata", "firstname_tag")
		content.append('<%s>%s</%s>\n' % (tag, self.myPatient.firstnames, tag))

		tag = __cfg__.get("metadata", "birth_tag")
		content.append('<%s>%s</%s>\n' % (tag, self.myPatient.dob, tag))

		tag = __cfg__.get("metadata", "date_tag")
		content.append('<%s>%s</%s>\n' % (tag, self.TBOX_doc_date.GetLineText(0), tag))

		tag = __cfg__.get("metadata", "type_tag")
		content.append('<%s>%s</%s>\n' % (tag, self.SelBOX_doc_type.GetStringSelection(), tag))

		tag = __cfg__.get("metadata", "comment_tag")
		content.append('<%s>%s</%s>\n' % (tag, self.TBOX_desc_short.GetLineText(0), tag))

		tag = __cfg__.get("metadata", "aux_comment_tag")
		content.append('<%s>%s</%s>\n' % (tag, self.TBOX_desc_long.GetValue(), tag))

		tag = __cfg__.get("metadata", "ref_tag")
		doc_ref = self.doc_id_wheel.GetLineText(0)
		content.append('<%s>%s</%s>\n' % (tag, doc_ref, tag))

		# FIXME: take reordering into account
		tag = __cfg__.get("metadata", "obj_tag")
		objLst = self.myDoc.getMetaData()['objects']
		for object in objLst.values():
			dirname, fname = os.path.split(object['file name'])
			content.append('<%s>%s</%s>\n' % (tag, fname, tag))

		content.append('</%s>\n' % __cfg__.get("metadata", "document_tag"))

		# overwrite old XML metadata file and write new one
		xml_fname = os.path.join(aDir, __cfg__.get("metadata", "description"))
		os.remove(xml_fname)
		xml_file = open(xml_fname, "w")
		map(xml_file.write, content)
		xml_file.close()
	#----------------------------------------
	def __valid_input(self):
		# check whether values for date of record, record type, short comment and extended comment
		# have been filled in
		date = self.TBOX_doc_date.GetLineText(0)
		datechecklist = string.split(date, '-')
		shortDescription = self.TBOX_desc_short.GetLineText(0)
		docType = self.SelBOX_doc_type.GetSelection()
		# do some checking on the date
		if date == _('please fill in'):
			msg = _('document date: missing')
		elif len(date) != 10:
			msg = _('document date: must be 10 characters long')
		elif len(datechecklist) != 3:
			msg = _('document date: invalid format\n\nvalid format: YYYY-MM-DD')
		elif len(datechecklist[0]) != 4:
			msg = _('document date: year must be 4 digits')
		elif int(datechecklist[0]) < 1900:
			msg = _('document date: document from before 1900 ?!?\n\nI want a copy !')
		elif datechecklist[0] > time.strftime("%Y", time.localtime()):
			msg = _('document date: no future !')
		elif len(datechecklist[1]) != 2:
			msg = _('document date: month must be 2 digits')
		elif len(datechecklist[2]) != 2:
			msg = _('document date: day must be 2 digits')
		elif int(datechecklist[1]) not in range(1, 13):
			msg = _('document date: month must be 1 to 12')
		elif int(datechecklist[2]) not in range(1, 32):
			msg = _('document date: day must be 1 to 31')
		elif shortDescription == _('please fill in') or shortDescription == '':
			msg = _('You must type in a short document comment.')
		elif docType == -1 or docType == 'please choose':
			msg = _('You must select a document type.')
		else:
			return 1

		_log.Log(gmLog.lErr, 'Collected metadata is not fully valid.')
		_log.Log(gmLog.lData, msg)

		dlg = wxMessageDialog(
			self,
			_('The data you entered about the current document\nis not complete. Please enter the missing information.\n\n%s' % msg),
			_('data input error'),
			wxOK | wxICON_ERROR
		)
		dlg.ShowModal()
		dlg.Destroy()

		return 0
	#----------------------------------------
	def __unlock_for_import(self, aDir):
		"""three-stage locking"""

		indexing_file = os.path.join(aDir, __cfg__.get("metadata", "now_indexing"))
		can_index_file = os.path.join(aDir, __cfg__.get("metadata", "can_index"))
		can_import_file = os.path.join(aDir, __cfg__.get("metadata", "can_import"))

		# 1) set ready-for-import checkpoint
		try:
			tag_file = open(can_import_file, "w")
			tag_file.close()
		except IOError:
			exc = sys.exc_info()
			_log.LogException('Cannot write import checkpoint file [%s]. Leaving locked for indexing.' % can_import_file, exc, fatal=0)
			return None

		# 2) remove ready-for-indexing checkpoint
		os.remove(can_index_file)

		# 3) remove indexing lock
		os.remove(indexing_file)

		return 1
	#----------------------------------------
	def __could_be_locked(self, aDir):
		"""check whether we _could_ acquire the lock for indexing

		i.e., whether we should worry about this directory at all
		"""
		indexing_file = os.path.join(aDir, __cfg__.get("metadata", "now_indexing"))
		can_index_file = os.path.join(aDir, __cfg__.get("metadata", "can_index"))

		# 1) anyone indexing already ?
		if os.path.exists(indexing_file):
			_log.Log(gmLog.lInfo, 'Someone seems to be indexing this directory already. Indexing lock [%s] exists.' % indexing_file)
			return None

		# 2) check for ready-for-indexing checkpoint
		if not os.path.exists(can_index_file):
			# unlock again
			_log.Log(gmLog.lInfo, 'Not ready for indexing yet. Checkpoint [%s] does not exist.' % can_index_file)
			return None

		return 1
	#----------------------------------------
	def __lock_for_indexing(self, aDir):
		"""three-stage locking

		- there still is the possibility for a race between
		  1) and 2) by two clients attempting to start indexing
		  at the same time
		"""
		indexing_file = os.path.join(aDir, __cfg__.get("metadata", "now_indexing"))
		can_index_file = os.path.join(aDir, __cfg__.get("metadata", "can_index"))

		# 1) anyone indexing already ?
		if os.path.exists(indexing_file):
			_log.Log(gmLog.lInfo, 'Someone seems to be indexing this directory already. Indexing lock [%s] exists.' % indexing_file)
			return None

		# 2) lock for indexing by us
		try:
			tag_file = open(indexing_file, 'w')
			tag_file.close()
		except IOError:
			# this shouldn't happen
			exc = sys.exc_info()
			_log.LogException('Exception: Cannot acquire indexing lock [%s].' % indexing_file, exc, fatal = 0)
			return None

		# 3) check for ready-for-indexing checkpoint
		# this should not happen, really, since we check on _init_phrasewheel() already
		if not os.path.exists(can_index_file):
			# unlock again
			_log.Log(gmLog.lInfo, 'Not ready for indexing yet. Releasing indexing lock [%s] again.' % indexing_file)
			os.remove(indexing_file)
			return None

		return 1
	#----------------------------------------
	#----------------------------------------
	def OnDelpicbuttonButton(self, event):
		current_selection=self.LBOX_doc_pages.GetSelection()
		self.BefValue=self.doc_id_wheel.GetLineText(0)
		if current_selection == -1:
			dlg = wxMessageDialog(self, _('You did not select a page'),_('Attention'), wxOK | wxICON_INFORMATION)
			try:
				dlg.ShowModal()
			finally:
				dlg.Destroy()
			
		else:
			self.selected_pic=self.LBOX_doc_pages.GetString(current_selection)
			#del page from hdd
			try:
				os.remove(__cfg__.get("source", "repositories") + self.BefValue + '/' + self.selected_pic + '.jpg')
			except OSError:
				_log.Log (gmLog.lErr, "I was unable to wipe the file " + __cfg__.get("source", "repositories") + self.BefValue + '/' + self.selected_pic + '.jpg' + " from disk because it simply was not there ")
				dlg = wxMessageDialog(self, _('I am afraid I was not able to delete the page from disk because it was not there'),_('Attention'), wxOK | wxICON_INFORMATION)
				try:
					dlg.ShowModal()
				finally:
					dlg.Destroy()
			#now rename (decrease index by 1) all pages above the deleted one
			i = current_selection
			for i in range(i,len(self.doc_pages)-1):
				try:
					os.rename(__cfg__.get("source", "repositories") + self.BefValue + '/' + self.LBOX_doc_pages.GetString(i+1) + '.jpg',__cfg__.get("source", "repositories") + self.BefValue + '/' + self.LBOX_doc_pages.GetString(i) + '.jpg')
				except OSError:
					_log.Log (gmLog.lErr, "I was unable to rename the file " + __cfg__.get("source", "repositories") + self.BefValue + '/' + self.LBOX_doc_pages.GetString(i+1) + '.jpg' + " from disk because it simply was not there ")
				print "I renamed" +str(__cfg__.get("source", "repositories") + self.BefValue + '/' + self.LBOX_doc_pages.GetString(i+1) + '.jpg') + "into" + str(__cfg__.get("source", "repositories") + self.BefValue + '/' + self.LBOX_doc_pages.GetString(i) + '.jpg')

			#print "u want to del:" + self.selected_pic
			self.LBOX_doc_pages.Delete(current_selection)
			self.doc_pages.remove(self.selected_pic + '.jpg')
			#rebuild list to clean the gap
			i = 0
			for i in range(len(self.doc_pages)):
				if i == 0:
					self.doc_pages = []
					self.LBOX_doc_pages = wxListBox(choices = [], id = wxID_INDEXFRAMELBOXPAGES, name = 'LBOX_doc_pages', parent = self.PNL_main, pos = wxPoint(48, 288), size = wxSize(182, 94), style = 0, validator = wxDefaultValidator)
				self.UpdatePicList()

#======================================================
class IndexerApp(wxApp):
	def OnInit(self):
		wxInitAllImageHandlers()
		self.main = indexFrame(None)
		self.main.Centre(wxBOTH)
		self.main.Show(true)
		self.SetTopWindow(self.main)
		return true
#------------------------------------------------------
def main():
	application = IndexerApp(0)
	application.MainLoop()
#======================================================
# main
#------------------------------------------------------
if __name__ == '__main__':
	try:
		main()
	except:
		exc = sys.exc_info()
		_log.LogException('Unhandled exception.', exc, fatal=1)
		# remove pending indexing locks
		raise

#======================================================
# this line is a replacement for gmPhraseWhell just in case it doesn't work 
#self.doc_id_wheel = wxTextCtrl(id = wxID_INDEXFRAMEBEFNRBOX, name = 'textCtrl1', parent = self.PNL_main, pos = wxPoint(48, 112), size = wxSize(176, 22), style = 0, value = _('document#'))

	#----------------------------------------
#	def UpdatePicList(self):
#		if len(self.doc_pages) == 0:
#			self.LBOX_doc_pages.Append(_('page')+'1')
#			self.doc_pages.append(_('page')+'1')
#		else:
#			lastPageInList=self.doc_pages[len(self.doc_pages)-1]
#			biggest_number_strg=lastPageInList.replace(_('page'),'')
#			biggest_number= int(biggest_number_strg) + 1
#			self.LBOX_doc_pages.Append(_('page') + `biggest_number`)
#			self.doc_pages.append(_('page') + `biggest_number`)
