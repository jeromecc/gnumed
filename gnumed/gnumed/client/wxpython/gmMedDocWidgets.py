"""GNUmed medical document handling widgets.
"""
# $Source: /home/ncq/Projekte/cvs2git/vcs-mirror/gnumed/gnumed/client/wxpython/gmMedDocWidgets.py,v $
__version__ = "$Revision: 1.61 $"
__author__ = "Karsten Hilbert <Karsten.Hilbert@gmx.net>"
#================================================================
import os.path, sys, re, time

try:
	import wxversion
	import wx
except ImportError:
	from wxPython import wx

from Gnumed.pycommon import gmLog, gmI18N, gmCfg, gmWhoAmI, gmPG, gmMimeLib, gmExceptions, gmMatchProvider, gmDispatcher, gmSignals
from Gnumed.business import gmPerson, gmMedDoc
from Gnumed.wxpython import gmGuiHelpers, gmRegetMixin
from Gnumed.wxGladeWidgets import wxgScanIdxPnl, wxgReviewDocPartDlg, wxgSelectablySortedDocTreePnl

_log = gmLog.gmDefLog
_whoami = gmWhoAmI.cWhoAmI()

if __name__ == '__main__':
	_log.SetAllLogLevels(gmLog.lData)
else:
	from Gnumed.pycommon import gmGuiBroker

_log.Log(gmLog.lInfo, __version__)

wx.ID_PNL_main = wx.NewId()
wx.ID_TB_BTN_show_page = wx.NewId()

#============================================================
class cReviewDocPartDlg(wxgReviewDocPartDlg.wxgReviewDocPartDlg):
	def __init__(self, *args, **kwds):
		self.__part = kwds['part']
		del kwds['part']
		wxgReviewDocPartDlg.wxgReviewDocPartDlg.__init__(self, *args, **kwds)
		self.__init_ui_data()
	#--------------------------------------------------------
	# internal API
	#--------------------------------------------------------
	def __init_ui_data(self):
		# add list headers
		self._LCTRL_existing_reviews.InsertColumn(0, _('reviewer'))
		self._LCTRL_existing_reviews.InsertColumn(1, _('when'))
		self._LCTRL_existing_reviews.InsertColumn(2, _('abnormal'))
		self._LCTRL_existing_reviews.InsertColumn(3, _('relevant'))
		self._LCTRL_existing_reviews.InsertColumn(4, _('comment'))
		self.__reload_existing_reviews()
	#--------------------------------------------------------
	def __reload_existing_reviews(self):
		self._LCTRL_existing_reviews.DeleteAllItems()
		revs = self.__part.get_reviews()
		if len(revs) == 0:
			return True
		# find special reviews
		review_by_me = None
		review_by_responsible_doc = None
		reviews_by_others = []
		for rev in revs:
			if rev[4]:
				review_by_responsible_doc = rev
			if rev[5]:
				review_by_me = rev
			if not (rev[4] and rev[5]):
				reviews_by_others.append(rev)
		# display them
		if review_by_me is not None:
			row_num = self._LCTRL_existing_reviews.InsertStringItem(sys.maxint, label=_('%s (you)') % review_by_me[0])
			self._LCTRL_existing_reviews.SetStringItem(index = row_num, col=0, label = _('%s (you)') % review_by_me[0])
			self._LCTRL_existing_reviews.SetStringItem(index = row_num, col=1, label=review_by_me[1].Format('%Y-%m-%d %H:%M'))
			if review_by_me[2]:
				self._LCTRL_existing_reviews.SetStringItem(index = row_num, col=2, label='X')
			if review_by_me[3]:
				self._LCTRL_existing_reviews.SetStringItem(index = row_num, col=3, label='X')
			self._LCTRL_existing_reviews.SetStringItem(index = row_num, col=4, label=review_by_me[6])
		if review_by_responsible_doc is not None:
			row_num = self._LCTRL_existing_reviews.InsertStringItem(sys.maxint, label=review_by_responsible_doc[0])
			self._LCTRL_existing_reviews.SetItemBackgroundColour(row_num, col=wx.BLUE)
			self._LCTRL_existing_reviews.SetStringItem(index = row_num, col=0, label=review_by_responsible_doc[0])
			self._LCTRL_existing_reviews.SetStringItem(index = row_num, col=1, label=review_by_responsible_doc[1].Format('%Y-%m-%d %H:%M'))
			if review_by_responsible_doc[2]:
				self._LCTRL_existing_reviews.SetStringItem(index = row_num, col=2, label='X')
			if review_by_responsible_doc[3]:
				self._LCTRL_existing_reviews.SetStringItem(index = row_num, col=3, label='X')
			self._LCTRL_existing_reviews.SetStringItem(index = row_num, col=4, label=review_by_responsible_doc[6])
			row_num += 1
		for rev in reviews_by_others:
			row_num = self._LCTRL_existing_reviews.InsertStringItem(sys.maxint, label=rev[0])
			self._LCTRL_existing_reviews.SetStringItem(index = row_num, col=0, label=rev[0])
			self._LCTRL_existing_reviews.SetStringItem(index = row_num, col=1, label=rev[1].Format('%Y-%m-%d %H:%M'))
			if rev[2]:
				self._LCTRL_existing_reviews.SetStringItem(index = row_num, col=2, label='X')
			if rev[3]:
				self._LCTRL_existing_reviews.SetStringItem(index = row_num, col=3, label='X')
			self._LCTRL_existing_reviews.SetStringItem(index = row_num, col=4, label=rev[6])
		return True
	#--------------------------------------------------------
	# event handlers
	#--------------------------------------------------------
	def _on_cancel_button_pressed(self, evt):
		self.OnCancel()
#============================================================
# FIXME: this must listen to patient change signals ...
class cScanIdxDocsPnl(wxgScanIdxPnl.wxgScanIdxPnl):
	def __init__(self, *args, **kwds):
		# init ancestor
		wxgScanIdxPnl.wxgScanIdxPnl.__init__(self, *args, **kwds)
		# now we *are* a wxgScanIdxDocsPnl child without any additional properties
	
		# from here on we can init other stuff
		# that's not part of the wxGlade GUI

		# setup episode phrasewheel with match provider
		mp = gmMatchProvider.cMatchProvider_SQL2 (
			service = 'clinical',
			queries = [
"""select pk_episode, description, 1 from clin.v_pat_episodes where
		episode_open is true and
		pk_patient=%%(pat)s and
		description %(fragment_condition)s""",
"""select pk_episode, description, 1 from clin.v_pat_episodes where
		pk_patient=%%(pat)s and
		description %(fragment_condition)s
"""]
		)
		self._PhWheel_episode.setMatchProvider(mp = mp)
		self._PhWheel_episode.add_callback_on_set_focus(callback=self._on_enter_episode_phrasewheel)

		self.__init_ui_data()

		# do not import globally since we might want to use
		# this module without requiring any scanner to be available
		from Gnumed.pycommon import gmScanBackend
		self.scan_module = gmScanBackend
	#--------------------------------------------------------
	# internal API
	#--------------------------------------------------------
	def __init_ui_data(self):
		self._PhWheel_episode.SetValue('')
		# provide choices for document types
		self._SelBOX_doc_type.Clear()
		for doc_type in gmMedDoc.get_document_types():
			self._SelBOX_doc_type.Append(doc_type[1], doc_type[0])
		# FIXME: make this configurable: either now() or last_date()
		self._TBOX_doc_date.SetValue(time.strftime('%Y-%m-%d', time.localtime()))
		self._TBOX_doc_comment.SetValue('')
		self._TBOX_description.SetValue('')
		# FIXME: set from config item
		self._ChBOX_reviewed.SetValue(False)
		# the list holding our page files
		self._LBOX_doc_pages.Clear()
		self.acquired_pages = []
	#--------------------------------------------------------
	def __reload_LBOX_doc_pages(self):
		self._LBOX_doc_pages.Clear()
		if len(self.acquired_pages) > 0:
			for i in range(len(self.acquired_pages)):
				fname = self.acquired_pages[i]
				self._LBOX_doc_pages.Append(_('page %s: %s' % (i+1, fname)), fname)
	#--------------------------------------------------------
	def __valid_for_save(self):
		title = _('saving document')

		if self.acquired_pages is None or len(self.acquired_pages) == 0:
			gmGuiHelpers.gm_show_error (
				aMessage = _('No pages to save. Aquire some pages first.'),
				aTitle = title
				)
			return False

		sel = self._SelBOX_doc_type.GetStringSelection()
		if sel == ''or sel is None or sel < 0:
			gmGuiHelpers.gm_show_error (
				aMessage = _('No document type applied. Choose a document type'),
				aTitle = title
			)
			return False

		if self._TBOX_doc_comment.GetValue().strip() == '':
			gmGuiHelpers.gm_show_error (
				aMessage = _('No document comment supplied. Add a comment for this document.'),
				aTitle = title
			)
			return False

		if self._PhWheel_episode.GetValue().strip() == '':
			gmGuiHelpers.gm_show_error (
				aMessage = _('You must select an episode to save this document under.'),
				aTitle = title
			)
			return False

		return True
	#--------------------------------------------------------
	# event handling API
	#--------------------------------------------------------
	def _scan_btn_pressed(self, evt):
		device_names = []
		device_objects = {}
		devices = self.scan_module.get_devices()
		for device in devices:
			device_names.append('%s (%s)' % (device[2], device[0]))

		# wxpython does not support client data in wxSingleChoiceDialog
		device_idx = gmGuiHelpers.gm_SingleChoiceDialog (
			aMessage = _('Select an image capture device'),
			aTitle = _('device selection'),
			choices = device_names
		)
		# FIXME: load directory from backend config
		fname = self.scan_module.acquire_page_into_file (
			device = devices[device_idx][0],
			filename = 'test',
			delay = 5,
			calling_window = self
		)
		if fname is None:
			gmGuiHelpers.gm_show_error (
				aMessage = _('Page could not be acquired from source.'),
				aTitle = _('acquiring page')
			)
			return None
		self.acquired_pages.append(fname)
		# update list of pages in GUI
		self.__reload_LBOX_doc_pages()
	#--------------------------------------------------------
	def _load_btn_pressed(self, evt):
		# patient file chooser
		dlg = wx.FileDialog(
			parent = None,
			message = _('Choose a file'),
			defaultDir = os.path.expanduser(os.path.join('~', 'gnumed')),
			defaultFile = '',
			wildcard = "all (*.*)|*.*|TIFFs (*.tif)|*.tif|JPEGs (*.jpg)|*.jpg",
			style = wx.OPEN | wx.HIDE_READONLY | wx.FILE_MUST_EXIST | wx.MULTIPLE
		)
		result = dlg.ShowModal()
		if result != wx.ID_CANCEL:
			files = dlg.GetPaths()
			for file in files:
				self.acquired_pages.append(file)
			self.__reload_LBOX_doc_pages()
		dlg.Destroy()
	#--------------------------------------------------------
	def _show_btn_pressed(self, evt):
		# did user select a page ?
		page_idx = self._LBOX_doc_pages.GetSelection()
		if page_idx == -1:
			gmGuiHelpers.gm_show_info (
				aMessage = _('You must select a page before you can view it.'),
				aTitle = _('displaying page')
			)
			return None
		# now, which file was that again ?
		page_fname = self._LBOX_doc_pages.GetClientData(page_idx)
		(result, msg) = gmMimeLib.call_viewer_on_file(page_fname)
		if not result:
			gmGuiHelpers.gm_show_error (
				aMessage = _('Cannot display document part:\n%s') % msg,
				aTitle = _('displaying page')
			)
			return None
		return 1
	#--------------------------------------------------------
	def _del_btn_pressed(self, event):
		page_idx = self._LBOX_doc_pages.GetSelection()
		if page_idx == -1:
			gmGuiHelpers.gm_show_info (
				aMessage = _('You must select a page before you can delete it.'),
				aTitle = _('deleting page')
			)
			return None
		page_fname = self._LBOX_doc_pages.GetClientData(page_idx)

		# 1) del item from self.acquired_pages
		self.acquired_pages[page_idx:(page_idx+1)] = []

		# 2) reload list box
		self.__reload_LBOX_doc_pages()

		# 3) kill file in the file system
		do_delete = gmGuiHelpers.gm_show_question (
			_(
"""Do you want to permanently delete the file

 [%s]

from your computer ?

If it is a temporary file for a page you just scanned
in this makes a lot of sense. In other cases you may
not want to lose the file.

Pressing [YES] will permanently remove the file
from your computer.""") % page_fname,
			_('deleting page')
		)
		if do_delete:
			try:
				os.remove(page_fname)
			except:
				_log.LogException('Error deleting file.')
				gmGuiHelpers.gm_show_error (
					aMessage = _('Cannot delete page in file [%s].\n\nYou may not have write access to it.') % page_fname,
					aTitle = _('deleting page')
				)

		return 1
	#--------------------------------------------------------
	def _save_btn_pressed(self, evt):

		if not self.__valid_for_save():
			return False

		wx.BeginBusyCursor()

		pat = gmPerson.gmCurrentPatient()
		doc_folder = pat.get_document_folder()
		emr = pat.get_emr()

		# create new document
		episode = self._PhWheel_episode.GetData()
		if episode is None:
			episode = emr.add_episode (
				episode_name = self._PhWheel_episode.GetValue().strip(),
				is_open = True
			)
			if episode is None:
				wx.EndBusyCursor()
				gmGuiHelpers.gm_show_error (
					aMessage = _('Cannot start episode [%s].') % self._PhWheel_episode.GetValue().strip(),
					aTitle = _('saving document')
				)
				return False

		encounter = emr.get_active_encounter()['pk_encounter']

		idx = self._SelBOX_doc_type.GetSelection()
		document_type = self._SelBOX_doc_type.GetClientData(idx)

		new_doc = doc_folder.add_document(document_type, encounter, episode)
		if new_doc is None:
			wx.EndBusyCursor()
			gmGuiHelpers.gm_show_error (
				aMessage = _('Cannot create new document.'),
				aTitle = _('saving document')
			)
			return False

		# update business object with metadata
		# - date of generation
		new_doc['date'] = self._TBOX_doc_date.GetLineText(0).strip()
		# - external reference
		ref = gmMedDoc.get_ext_ref()
		if ref is not None:
			new_doc['ext_ref'] = ref
		# - comment
		comment = self._TBOX_doc_comment.GetLineText(0).strip()
		if comment != '':
			new_doc['comment'] = comment
		# - save it
		if not new_doc.save_payload():
			wx.EndBusyCursor()
			gmGuiHelpers.gm_show_error (
				aMessage = _('Cannot update document metadata.'),
				aTitle = _('saving document')
			)
			return False
		# - long description
		description = self._TBOX_description.GetValue().strip()
		if description != '':
			if not new_doc.add_description(description):
				wx.EndBusyCursor()
				gmGuiHelpers.gm_show_error (
					aMessage = _('Cannot add document description.'),
					aTitle = _('saving document')
				)
				return False

		# add document parts from files
		success, msg, filename = new_doc.add_parts_from_files(files=self.acquired_pages)
		if not success:
			wx.EndBusyCursor()
			gmGuiHelpers.gm_show_error (
				aMessage = msg,
				aTitle = _('saving document')
			)
			return False

		# set reviewed status
		if self._ChBOX_reviewed.GetValue():
			if not new_doc.set_reviewed (
				technically_abnormal = self._ChBOX_abnormal.GetValue(),
				clinically_relevant = self._ChBOX_relevant.GetValue()
			):
				msg = _('Error setting "reviewed" status of new document.')

		cfg = gmCfg.cCfgSQL()
		show_id = cfg.get_by_user(option = 'horstspace.scan_index.show_doc_id')
		wx.EndBusyCursor()
		if show_id and (ref is not None):
			msg = _(
"""The reference ID for the new document is:

 <%s>

You probably want to write it down on the
original documents.

If you don't care about the ID you can switch
off this message in the GNUmed configuration.""") % ref
			gmGuiHelpers.gm_show_info (
				aMessage = msg,
				aTitle = _('saving document')
			)

		# prepare for next document
		self.__init_ui_data()
		return True
	#--------------------------------------------------------
	def _startover_btn_pressed(self, evt):
		self.__init_ui_data()
	#--------------------------------------------------------
	def _reviewed_box_checked(self, evt):	
		print "must enable relevant/abnormal checkboxes here"
	#--------------------------------------------------------
	def _on_enter_episode_phrasewheel(self):
		pat = gmPerson.gmCurrentPatient()
		self._PhWheel_episode.set_context('pat', pat.getID())
		return True

#============================================================
class cSelectablySortedDocTreePnl(wxgSelectablySortedDocTreePnl.wxgSelectablySortedDocTreePnl, gmRegetMixin.cRegetOnPaintMixin):
	"""A document tree that can be sorted."""
	def __init__(self, *args, **kwds):
		wxgSelectablySortedDocTreePnl.wxgSelectablySortedDocTreePnl.__init__(self, *args, **kwds)
		self._doc_tree.Layout()
		gmRegetMixin.cRegetOnPaintMixin.__init__(self)
		self.__register_interests()
	#-------------------------------------------------------
	# reget mixin API
	#--------------------------------------------------------
	def __register_interests(self):
		gmDispatcher.connect(signal=gmSignals.patient_selected(), receiver=self._schedule_data_reget)
	#-------------------------------------------------------
	def _populate_with_data(self):
		if not self._doc_tree.refresh():
			_log.Log(gmLog.lErr, "cannot update document tree")
			return False
		self._doc_tree.SelectItem(self._doc_tree.root)
		return True
	#--------------------------------------------------------
	# inherited event handlers
	#--------------------------------------------------------
	def _on_sort_by_age_selected(self, evt):
		self._doc_tree.set_sort_mode(mode = 'age')
		self._doc_tree.refresh()
	#--------------------------------------------------------
	def _on_sort_by_review_selected(self, evt):
		self._doc_tree.set_sort_mode(mode = 'review')
		self._doc_tree.refresh()
	#--------------------------------------------------------
	def _on_sort_by_episode_selected(self, evt):
		self._doc_tree.set_sort_mode(mode = 'episode')
		self._doc_tree.refresh()
#============================================================
		# NOTE:	 For some reason tree items have to have a data object in
		#		 order to be sorted.  Since our compare just uses the labels
		#		 we don't need any real data, so we'll just use None.

class cDocTree(wx.TreeCtrl):
	"""This wx.TreeCtrl derivative displays a tree view of stored medical documents.
	"""
	_sort_modes = ['age', 'review', 'episode']
	_root_node_labels = None
	#--------------------------------------------------------
	def __init__(self, parent, id, *args, **kwds):
		"""Set up our specialised tree.
		"""
		wx.TreeCtrl.__init__(self, parent, id, style=wx.TR_NO_BUTTONS)

		tmp = _('available documents (%s)')
		cDocTree._root_node_labels = {
			'age': tmp % _('most recent on top'),
			'review': tmp % _('unreviewed on top'),
			'episode': tmp % _('sorted by episode')
		}

		self.root = None
		self.__sort_mode = None
		self.set_sort_mode()
		self.__pat = gmPerson.gmCurrentPatient()

		self.__register_events()

#		self.tree = MyTreeCtrl(self, tID, wx.DefaultPosition, wx.DefaultSize,
#								wxTR_HAS_BUTTONS | wxTR_EDIT_LABELS# | wxTR_MULTIPLE
#								, self.log)

	#--------------------------------------------------------
	# external API
	#--------------------------------------------------------
	def refresh(self):
		if not self.__pat.is_connected():
			gmGuiHelpers.gm_beep_statustext (
				_('Cannot load documents. No active patient.'),
				gmLog.lErr
			)
			return False

		if not self.__populate_tree():
			return False

		return True
	#--------------------------------------------------------
	def set_sort_mode(self, mode='age'):
		if mode not in cDocTree._sort_modes:
			_log.Log(gmLog.Err, 'invalid document tree sort mode [%s], valid modes: %s' % (mode, cDocTree._sort_modes))
		if self.__sort_mode == mode:
			return True
		self.__sort_mode = mode
	#--------------------------------------------------------
	# internal API
	#--------------------------------------------------------
	def __register_events(self):
		# connect handlers
		wx.EVT_TREE_ITEM_ACTIVATED (self, self.GetId(), self._on_activate)
		wx.EVT_TREE_ITEM_RIGHT_CLICK (self, self.GetId(), self.__on_right_click)

#		 wx.EVT_TREE_ITEM_EXPANDED	 (self, tID, self.OnItemExpanded)
#		 wx.EVT_TREE_ITEM_COLLAPSED (self, tID, self.OnItemCollapsed)
#		 wx.EVT_TREE_SEL_CHANGED	 (self, tID, self.OnSelChanged)
#		 wx.EVT_TREE_BEGIN_LABEL_EDIT(self, tID, self.OnBeginEdit)
#		 wx.EVT_TREE_END_LABEL_EDIT (self, tID, self.OnEndEdit)

#		 wx.EVT_LEFT_DCLICK(self.tree, self.OnLeftDClick)
	#--------------------------------------------------------
	def __populate_tree(self):

		wx.BeginBusyCursor()
		# clean old tree
		if self.root is not None:
			self.DeleteAllItems()

		# init new tree
		self.root = self.AddRoot(cDocTree._root_node_labels[self.__sort_mode], -1, -1)
		self.SetPyData(self.root, None)
		self.SetItemHasChildren(self.root, False)

		# read documents from database
		docs_folder = self.__pat.get_document_folder()
		docs = docs_folder.get_documents()
		if docs is None:
			name = self.__pat.get_identity().get_names()
			gmGuiHelpers.gm_show_error (
				aMessage = _('Error searching documents for patient\n[%s %s].') % (name['first'], name['last']),
				aTitle = _('loading document list')
			)
			# avoid recursion of GUI updating
			wx.EndBusyCursor()
			return True

		if len(docs) == 0:
			wx.EndBusyCursor()
			return True

		# fill new tree from document list
		self.SetItemHasChildren(self.root, True)

		# add our documents as first level nodes
		for doc in docs:
			if doc['comment'] is not None:
				cmt = '%s' % doc['comment']
			else:
				cmt = _('no comment available')

			parts = doc.get_parts()
			page_num = len(parts)

			if doc['ext_ref'] is not None:
				ref = '>%s<' % doc['ext_ref']
			else:
				ref = _('no reference ID found')

			label = _('%10s %25s: %s (%s page(s), %s)') % (
				doc['date'][:11].ljust(10),
				doc['l10n_type'][:26],
				cmt,
				page_num,
				ref
			)

			doc_node = self.AppendItem(parent = self.root, text = label)
			self.SetItemBold(doc_node, bold=True)
			self.SetPyData(doc_node, doc)
			if len(parts) > 0:
				self.SetItemHasChildren(doc_node, True)

			# now add parts as child nodes
			for part in parts:

				pg = _('page %2s') % part['seq_idx']

				if part['obj_comment'] is None:
					cmt = _("no comment available")
				else:
					cmt = part['obj_comment']

				if part['size'] == 0:
					sz = _('0 bytes - data missing ?')
				else:
					sz = _('%s bytes') % part['size']

				if part['reviewed'] or part['reviewed_by_you'] or part['reviewed_by_intended_reviewer']:
					rev = ''
				else:
					rev = ' [%s]' % _('unreviewed')

#				if part['clinically_relevant']:
#					rel = ' [%s]' % _('Cave')
#				else:
#					rel = ''

				label = '%s%s: "%s" (%s)' % (pg, rev, cmt, sz)

				part_node = self.AppendItem(parent = doc_node, text = label)
				self.SetPyData(part_node, part)

		wx.TreeCtrl.SortChildren(self, self.root)

		# and uncollapse
		self.Expand(self.root)

		wx.EndBusyCursor()
		return True
	#------------------------------------------------------------------------
	def OnCompareItems (self, node1=None, node2=None):
		"""Used in sorting items.

		-1: 1 < 2
		 0: 1 = 2
		 1: 1 > 2
		"""
		item1 = self.GetPyData(node1)
		item2 = self.GetPyData(node2)

		# doc node
		if isinstance(item1, gmMedDoc.cMedDoc):

			# FIXME: should be "date" but have to wait until fuzzy date problem solved
			#date_field = 'date'
			date_field = 'modified_when'

			if self.__sort_mode == 'age':
				# reverse sort by date
				if item1[date_field] > item2[date_field]:
					return -1
				if item1[date_field] == item2[date_field]:
					return 0
				return 1

			elif self.__sort_mode == 'episode':
				if item1['episode'] < item2['episode']:
					return -1
				if item1['episode'] == item2['episode']:
					# inner sort: reverse by date
					if item1[date_field] > item2[date_field]:
						return -1
					if item1[date_field] == item2[date_field]:
						return 0
					return 1
				return 1

			elif self.__sort_mode == 'review':
				# equality
				if item1.has_unreviewed_parts() == item2.has_unreviewed_parts():
					# inner sort: reverse by date
					if item1[date_field] > item2[date_field]:
						return -1
					if item1[date_field] == item2[date_field]:
						return 0
					return 1
				if item1.has_unreviewed_parts():
					return -1
				return 1

			else:
				_log.Log(gmLog.lErr, 'unknown document sort mode [%s], reverse-sorting by age' % self.__sort_mode)
				# reverse sort by date
				if item1[date_field] > item2[date_field]:
					return -1
				if item1[date_field] == item2[date_field]:
					return 0
				return 1

		# part node
		if isinstance(item1, gmMedDoc.cMedDocPart):
			# compare sequence IDs (= "page" numbers)
			if item1['seq_idx'] < item2['seq_idx']:
				return -1
			if item1['seq_idx'] == item2['seq_idx']:
				return 0
			return 1
		# error out
		_log.Log(gmLog.lErr, 'do not know how to compare [%s] with [%s]' % (type(item1), type(item2)))
		return None
	#------------------------------------------------------------------------
	# event handlers
	#------------------------------------------------------------------------
	def _on_activate (self, event):
		node = event.GetItem()
		node_data = self.GetPyData(node)

		# exclude pseudo root node
		if node_data is None:
			return None

		# do nothing with documents yet
		if isinstance(node_data, gmMedDoc.cMedDoc):
			return None

		self.__display_part(part = node_data)
	#--------------------------------------------------------
	def __on_right_click(self, evt):
		node = evt.GetItem()
		self.__curr_node_data = self.GetPyData(node)

		# exclude pseudo root node
		if self.__curr_node_data is None:
			return None

		# documents
		if isinstance(self.__curr_node_data, gmMedDoc.cMedDoc):
			self.__handle_doc_context()

		# parts
		if isinstance(self.__curr_node_data, gmMedDoc.cMedDocPart):
			self.__handle_part_context()

		del self.__curr_node_data
		evt.Skip()
	#--------------------------------------------------------
	# internal API
	#--------------------------------------------------------
	def __handle_doc_context(self):
		# build menu
		descriptions = self.__curr_node_data.get_descriptions()
		desc_menu = wx.Menu()
		for desc in descriptions:
			d_id = wx.NewId()
			# contract string
			tmp = re.split('\r\n+|\r+|\n+|\s+|\t+', desc)
			tmp = ' '.join(tmp)
			# but only use first 30 characters
			tmp = "%s ..." % tmp[:30]
			desc_menu.AppendItem(wx.MenuItem(desc_menu, d_id, tmp))
			# connect handler
			wx.EVT_MENU(desc_menu, d_id, self.__show_description)
		ID_load_submenu = wx.NewId()
		menu = wx.Menu(title = _('document menu'))
		menu.AppendMenu(ID_load_submenu, _('descriptions ...'), desc_menu)
		self.PopupMenu(menu, wx.DefaultPosition)
		menu.Destroy()
	#--------------------------------------------------------
	def __handle_part_context(self):
		# build menu
		menu = wx.Menu(title = _('page menu'))
		# display file
		ID = wx.NewId()
		menu.AppendItem(wx.MenuItem(menu, ID, 'Display'))
		wx.EVT_MENU(menu, ID, self.__display_curr_part)
		# review item
		ID = wx.NewId()
		menu.AppendItem(wx.MenuItem(menu, ID, 'Review/Initial'))
		wx.EVT_MENU(menu, ID, self.__review_curr_part)
		# show menu
		self.PopupMenu(menu, wx.DefaultPosition)
		menu.Destroy()
	#--------------------------------------------------------
	def __display_curr_part(self, evt):
		self.__display_part(part=self.__curr_node_data)
	#--------------------------------------------------------
	def __display_part(self, part):
		"""Display document part."""

		# sanity check
		if part['size'] == 0:
			_log.Log(gmLog.lErr, 'cannot display part [%s] - 0 bytes' % part['pk_obj'])
			gmGuiHelpers.gm_show_error(
				aMessage = _('Document part does not seem to exist in database !'),
				aTitle = _('showing document')
			)
			return None

		# get export directory for temporary files
		def_tmp_dir = os.path.join('~', 'gnumed', 'tmp')
		cfg = gmCfg.cCfgSQL()
		tmp_dir = cfg.get_by_workplace (
			option = "horstspace.tmp_dir",
			workplace = _whoami.get_workplace(),
			default = def_tmp_dir
		)
		exp_base = os.path.abspath(os.path.expanduser(os.path.join(tmp_dir, 'docs')))
		if not os.path.exists(exp_base):
			_log.Log(gmLog.lErr, "The directory [%s] does not exist ! Falling back to default temporary directory." % exp_base) # which is None == tempfile.tempdir == use system defaults
			exp_base = None
		else:
			_log.Log(gmLog.lData, "working into directory [%s]" % exp_base)

		# determine database export chunk size
		chunksize = int(cfg.get_by_workplace (
			option = "horstspace.blob_export_chunk_size",
			workplace = _whoami.get_workplace(),
			default = 1 * 1024 * 1024		# 1 MB
		))
		if chunksize is None:
			chunksize = 1 * 1024 * 1024		# 1 MB

		# retrieve doc part
		fname = part.export_to_file(aTempDir = exp_base, aChunkSize = chunksize)
		if fname is None:
			_log.Log(gmLog.lErr, "cannot export doc part [%s] data from database" % part['pk_obj'])
			gmGuiHelpers.gm_show_error (
				aMessage = _('Cannot export document part from database to file.'),
				aTitle = _('showing document')
			)
			return None

		# display it
		(result, msg) = gmMimeLib.call_viewer_on_file(fname)
		if not result:
			gmGuiHelpers.gm_show_error (
				aMessage = _('Cannot display document part:\n%s') % msg,
				aTitle = _('displaying page')
			)
			return None

		# handle review if wanted
		review_after_display = cfg.get2 (
			option = 'horstspace.document_viewer.review_after_display',
			workplace = _whoami.get_workplace(),
			bias = 'user',
			default = 1
		)
		# always review
		if review_after_display == 1:
			self.__review_part(part=part)
		# review if no review by me exists
		elif review_after_display == 2:
			review_by_me = filter(lambda rev: rev['is_review_by_you'], part.get_reviews())
			if len(review_by_me) == 0:
				self.__review_part(part=part)

		return 1
	#--------------------------------------------------------
	def __review_curr_part(self, evt):
		self.__review_part(part=self.__curr_node_data)
	#--------------------------------------------------------
	def __review_part(self, part=None):
		dlg = cReviewDocPartDlg (
			parent = self,
			id = -1,
			part = part
		)
		dlg.ShowModal()
	#--------------------------------------------------------
	def __show_description(self, evt):
		print "showing description"
#============================================================
# main
#------------------------------------------------------------
if __name__ == '__main__':
	print "==> the syntax seems OK"
	print "==> please write a real unit test"

#============================================================
# $Log: gmMedDocWidgets.py,v $
# Revision 1.61  2006-05-08 16:35:32  ncq
# - cleanup
# - add event handlers for sorting
# - make tree really sort - wxPython seems to forget to call
#   SortChildren() so call it ourselves
#
# Revision 1.60  2006/05/07 15:34:01  ncq
# - add cSelectablySortedDocTreePnl
#
# Revision 1.59  2006/05/01 18:49:30  ncq
# - better named variables
# - match provider in ScanIdxPnl
# - episode handling on save
# - as user before deleting files from disc
# - fix node formatting in doc tree
#
# Revision 1.58  2006/04/30 15:52:53  shilbert
# - event handler for document loading was added
#
# Revision 1.57  2006/02/27 15:42:14  ncq
# - implement cancel button in review dialog
# - invoke review after displaying doc part depending on cfg
#
# Revision 1.56  2006/02/13 19:10:14  ncq
# - actually display previous reviews in list
#
# Revision 1.55  2006/02/13 08:29:19  ncq
# - further work on the doc review control
#
# Revision 1.54  2006/02/10 16:33:19  ncq
# - popup review dialog from doc part right-click menu
#
# Revision 1.53  2006/02/05 15:03:22  ncq
# - doc tree:
#   - document part popup menu, stub for review dialog
#   - improved part display in doc tree
# - start handling relevant/abnormal check boxes in scan/index
#
# Revision 1.52  2006/02/05 14:16:29  shilbert
# - more checks for required values before commiting document to database
#
# Revision 1.51  2006/01/27 22:33:44  ncq
# - display reviewed/signed status in document tree
#
# Revision 1.50  2006/01/24 22:32:14  ncq
# - allow multiple files to be selected at once from file selection dialog
#
# Revision 1.49  2006/01/23 22:11:36  ncq
# - improve display
#
# Revision 1.48  2006/01/23 17:36:32  ncq
# - cleanup
# - display/use full path with file name after "load file" in scan&index
# - only add loaded file to file list if not cancelled
#
# Revision 1.47  2006/01/22 18:09:30  ncq
# - improve file name string in scanned pages list
# - force int() on int from db cfg
#
# Revision 1.46  2006/01/21 23:57:18  shilbert
# - acquire file from filesystem has been added
#
# Revision 1.45  2006/01/16 22:10:10  ncq
# - some cleanup
#
# Revision 1.44  2006/01/16 20:03:02  shilbert
# *** empty log message ***
#
# Revision 1.43  2006/01/16 19:37:25  ncq
# - use get_devices()
#
# Revision 1.42  2006/01/15 13:14:12  shilbert
# - support for multiple image source finished
#
# Revision 1.41  2006/01/15 10:02:23  shilbert
# - initial support for multiple image scanner devices
#
# Revision 1.40  2006/01/14 23:21:19  shilbert
# - fix for correct doc type (pk) handling
#
# Revision 1.39  2006/01/14 10:34:53  shilbert
# - fixed some some bugs which prevented document to be saved in DB
#
# Revision 1.38  2006/01/13 11:06:33  ncq
# - properly use gmGuiHelpers
# - properly fall back to default temporary directory
#
# Revision 1.37  2006/01/01 18:14:25  shilbert
# - fixed indentation problem
#
# Revision 1.36  2006/01/01 17:44:43  ncq
# - comment on proper user of emr.add_document()
#
# Revision 1.35  2006/01/01 17:23:29  ncq
# - properly use backend option for temp dir to
#   temporarily export docs into for viewing
#
# Revision 1.34  2005/12/16 12:04:25  ncq
# - fix silly indentation bug
#
# Revision 1.33  2005/12/14 17:01:03  ncq
# - use document_folder class and other gmMedDoc.py goodies
#
# Revision 1.32  2005/12/14 15:54:01  ncq
# - cleanup
#
# Revision 1.31  2005/12/14 15:40:54  ncq
# - add my changes regarding new config handling
#
# Revision 1.30  2005/12/14 14:08:24  shilbert
# - minor cleanup of ncq's changes
#
# Revision 1.29  2005/12/14 10:42:11  ncq
# - use cCfgSQL.get_by_user in scan&index panel on showing document reference ID
#
# Revision 1.28  2005/12/13 21:44:31  ncq
# - start _save_btn_pressed() so people see where we are going
#
# Revision 1.27  2005/12/06 17:59:12  ncq
# - make scan/index panel work more
#
# Revision 1.26  2005/12/02 22:46:21  shilbert
# - fixed inconsistent naming of vaiables which caused a bug
#
# Revision 1.25  2005/12/02 17:31:05  shilbert
# - readd document types as per Ian's suggestion
#
# Revision 1.24  2005/12/02 02:09:02  shilbert
# - quite a few feature updates within the scope of scan&idx panel
#
# Revision 1.23  2005/11/29 19:00:09  ncq
# - some cleanup
#
# Revision 1.22  2005/11/27 12:46:21  ncq
# - cleanup
#
# Revision 1.21  2005/11/27 01:57:28  shilbert
# - moved some of the feature back in
#
# Revision 1.20  2005/11/26 21:08:00  shilbert
# - some more iterations on the road
#
# Revision 1.19  2005/11/26 16:56:04  shilbert
# - initial working version with scan /index documents support
#
# Revision 1.18  2005/11/26 16:38:55  shilbert
# - slowly readding features
#
# Revision 1.17  2005/11/26 08:21:37  ncq
# - scan/index wxGlade child class fleshed out a bit more
#
# Revision 1.16  2005/11/25 23:02:49  ncq
# - start scan/idx panel inheriting from wxGlade base class
#
# Revision 1.15  2005/09/28 21:27:30  ncq
# - a lot of wx2.6-ification
#
# Revision 1.14  2005/09/28 15:57:48  ncq
# - a whole bunch of wx.Foo -> wx.Foo
#
# Revision 1.13  2005/09/26 18:01:51  ncq
# - use proper way to import wx26 vs wx2.4
# - note: THIS WILL BREAK RUNNING THE CLIENT IN SOME PLACES
# - time for fixup
#
# Revision 1.12  2005/09/24 09:17:29  ncq
# - some wx2.6 compatibility fixes
#
# Revision 1.11  2005/03/06 14:54:19  ncq
# - szr.AddWindow() -> Add() such that wx2.5 works
# - 'demographic record' -> get_identity()
#
# Revision 1.10  2005/01/31 10:37:26  ncq
# - gmPatient.py -> gmPerson.py
#
# Revision 1.9  2004/10/17 15:57:36  ncq
# - after pat.get_documents():
#   1) separate len(docs) == 0 from docs is None
#   2) only the second really is an error
#   3) however, return True from it, too, as we
#      informed the user about the error already
#
# Revision 1.8  2004/10/17 00:05:36  sjtan
#
# fixup for paint event re-entry when notification dialog occurs over medDocTree graphics
# area, and triggers another paint event, and another notification dialog , in a loop.
# Fixup is set flag to stop _repopulate_tree, and to only unset this flag when
# patient activating signal gmMedShowDocs to schedule_reget, which is overridden
# to include resetting of flag, before calling mixin schedule_reget.
#
# Revision 1.7  2004/10/14 12:11:50  ncq
# - __on_activate -> _on_activate
#
# Revision 1.6  2004/10/11 19:56:03  ncq
# - cleanup, robustify, attach doc/part VO directly to node
#
# Revision 1.5  2004/10/01 13:34:26  ncq
# - don't fail to display just because some metadata is missing
#
# Revision 1.4  2004/09/19 15:10:44  ncq
# - lots of cleanup
# - use status message instead of error box on missing patient
#   so that we don't get an endless loop
#   -> paint_event -> update_gui -> no-patient message -> paint_event -> ...
#
# Revision 1.3  2004/07/19 11:50:43  ncq
# - cfg: what used to be called "machine" really is "workplace", so fix
#
# Revision 1.2  2004/07/18 20:30:54  ncq
# - wxPython.true/false -> Python.True/False as Python tells us to do
#
# Revision 1.1  2004/06/26 23:39:34  ncq
# - factored out widgets for re-use
#
