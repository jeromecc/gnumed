"""GnuMed clinical narrative business object.

"""
#============================================================
__version__ = "$Revision: 1.44 $"
__author__ = "Carlos Moro <cfmoro1976@yahoo.es>, Karsten Hilbert <Karsten.Hilbert@gmx.net>"
__license__ = 'GPL (for details see http://gnu.org)'

import sys, logging


if __name__ == '__main__':
	sys.path.insert(0, '../../')
from Gnumed.pycommon import gmPG2, gmExceptions, gmBusinessDBObject, gmTools

try:
	_('dummy-no-need-to-translate-but-make-epydoc-happy')
except NameError:
	_ = lambda x:x

_log = logging.getLogger('gm.emr')
_log.info(__version__)


soap_cat2l10n = {
	's': _('soap_S').replace(u'soap_', u''),
	'o': _('soap_O').replace(u'soap_', u''),
	'a': _('soap_A').replace(u'soap_', u''),
	'p': _('soap_P').replace(u'soap_', u''),
	#None: _('soap_ADMIN').replace(u'soap_', u'')
	None: gmTools.u_ellipsis
}

soap_cat2l10n_str = {
	's': _('soap_Subjective').replace(u'soap_', u''),
	'o': _('soap_Objective').replace(u'soap_', u''),
	'a': _('soap_Assessment').replace(u'soap_', u''),
	'p': _('soap_Plan').replace(u'soap_', u''),
	None: _('soap_Administrative').replace(u'soap_', u'')
}

l10n2soap_cat = {
	_('soap_S').replace(u'soap_', u''): 's',
	_('soap_O').replace(u'soap_', u''): 'o',
	_('soap_A').replace(u'soap_', u''): 'a',
	_('soap_P').replace(u'soap_', u''): 'p',
	#_('soap_ADMIN').replace(u'soap_', u''): None
	gmTools.u_ellipsis: None
}
#============================================================
class cDiag(gmBusinessDBObject.cBusinessDBObject):
	"""Represents one real diagnosis.
	"""
	_cmd_fetch_payload = u"select *, xmin_clin_diag, xmin_clin_narrative from clin.v_pat_diag where pk_diag=%s"
	_cmds_store_payload = [
		u"""update clin.clin_diag set
				laterality=%()s,
				laterality=%(laterality)s,
				is_chronic=%(is_chronic)s::boolean,
				is_active=%(is_active)s::boolean,
				is_definite=%(is_definite)s::boolean,
				clinically_relevant=%(clinically_relevant)s::boolean
			where
				pk=%(pk_diag)s and
				xmin=%(xmin_clin_diag)s""",
		u"""update clin.clin_narrative set
				narrative=%(diagnosis)s
			where
				pk=%(pk_diag)s and
				xmin=%(xmin_clin_narrative)s""",
		u"""select xmin_clin_diag, xmin_clin_narrative from clin.v_pat_diag where pk_diag=%s(pk_diag)s"""
		]

	_updatable_fields = [
		'diagnosis',
		'laterality',
		'is_chronic',
		'is_active',
		'is_definite',
		'clinically_relevant'
	]
	#--------------------------------------------------------
	def get_codes(self):
		"""
			Retrieves codes linked to this diagnosis
		"""
		cmd = u"select code, coding_system from clin.v_codes4diag where diagnosis=%s"
		rows, idx = gmPG2.run_ro_queries(queries = [{'cmd': cmd, 'args': [self._payload[self._idx['diagnosis']]]}])
		return rows
	#--------------------------------------------------------
	def add_code(self, code=None, coding_system=None):
		"""
			Associates a code (from coding system) with this diagnosis.
		"""
		# insert new code
		cmd = u"select clin.add_coded_phrase (%(diag)s, %(code)s, %(sys)s)"
		args = {
			'diag': self._payload[self._idx['diagnosis']],
			'code': code,
			'sys': coding_system
		}
		gmPG2.run_rw_queries(queries = [{'cmd': cmd, 'args': args}])
		return True
#============================================================
class cNarrative(gmBusinessDBObject.cBusinessDBObject):
	"""Represents one clinical free text entry.
	"""
	_cmd_fetch_payload = u"select *, xmin_clin_narrative from clin.v_pat_narrative where pk_narrative=%s"
	_cmds_store_payload = [
		u"""update clin.clin_narrative set
				narrative = %(narrative)s,
				clin_when = %(date)s,
				soap_cat = lower(%(soap_cat)s),
				fk_encounter = %(pk_encounter)s
			where
				pk=%(pk_narrative)s and
				xmin=%(xmin_clin_narrative)s""",
		u"""select xmin_clin_narrative from clin.v_pat_narrative where pk_narrative=%(pk_narrative)s"""
		]

	_updatable_fields = [
		'narrative',
		'date',
		'soap_cat',
		'pk_episode',
		'pk_encounter'
	]

	#xxxxxxxxxxxxxxxx
	# support row_version in view

	#--------------------------------------------------------
	def get_codes(self):
		"""Retrieves codes linked to *this* narrative.
		"""
		cmd = u"select code, xfk_coding_system from clin.coded_phrase where term=%s"
		rows, idx = gmPG2.run_ro_queries(queries = [{'cmd': cmd, 'args': [self._payload[self._idx['narrative']]]}])
		return rows
	#--------------------------------------------------------
	def add_code(self, code=None, coding_system=None):
		"""
			Associates a code (from coding system) with this narrative.
		"""
		# insert new code
		cmd = u"select clin.add_coded_phrase (%(narr)s, %(code)s, %(sys)s)"
		args = {
			'narr': self._payload[self._idx['narrative']],
			'code': code,
			'sys': coding_system
		}
		gmPG2.run_rw_queries(queries = [{'cmd': cmd, 'args': args}])
		return True
	#--------------------------------------------------------
	def format(self, left_margin=u'', fancy=False, width=75):

		if fancy:
			# FIXME: add revision
			txt = gmTools.wrap (
				text = _('%s: %s by %.8s\n%s') % (
					self._payload[self._idx['date']].strftime('%x %H:%M'),
					soap_cat2l10n_str[self._payload[self._idx['soap_cat']]],
					self._payload[self._idx['provider']],
					self._payload[self._idx['narrative']]
				),
				width = width,
				initial_indent = u'',
				subsequent_indent = left_margin + u'   '
			)
		else:
			txt = u'%s [%s]: %s (%.8s)' % (
				self._payload[self._idx['date']].strftime('%x %H:%M'),
				soap_cat2l10n[self._payload[self._idx['soap_cat']]],
				self._payload[self._idx['narrative']],
				self._payload[self._idx['provider']]
			)
			if len(txt) > width:
				txt = txt[:width] + gmTools.u_ellipsis

		return txt

#		lines.append('-- %s ----------' % gmClinNarrative.soap_cat2l10n_str[soap_cat])

#============================================================
# convenience functions
#============================================================
def search_text_across_emrs(search_term=None):

	if search_term is None:
		return []

	if search_term.strip() == u'':
		return []

	cmd = u'select * from clin.v_narrative4search where narrative ~* %(term)s order by pk_patient limit 1000'
	rows, idx = gmPG2.run_ro_queries(queries = [{'cmd': cmd, 'args': {'term': search_term}}], get_col_idx = False)

	return rows
#============================================================
def create_clin_narrative(narrative=None, soap_cat=None, episode_id=None, encounter_id=None):
	"""Creates a new clinical narrative entry

		narrative - free text clinical narrative
		soap_cat - soap category
		episode_id - episodes's primary key
		encounter_id - encounter's primary key
	"""
	# any of the args being None (except soap_cat) should fail the SQL code

	# sanity checks:

	# 1) silently do not insert empty narrative
	narrative = narrative.strip()
	if narrative == u'':
		return (True, None)

	# 2) also, silently do not insert true duplicates
	# FIXME: this should check for .provider = current_user but
	# FIXME: the view has provider mapped to their staff alias
	cmd = u"""
select *, xmin_clin_narrative from clin.v_pat_narrative where
	pk_encounter = %(enc)s
	and pk_episode = %(epi)s
	and soap_cat = %(soap)s
	and narrative = %(narr)s
"""
	args = {
		'enc': encounter_id,
		'epi': episode_id,
		'soap': soap_cat,
		'narr': narrative
	}
	rows, idx = gmPG2.run_ro_queries(queries = [{'cmd': cmd, 'args': args}], get_col_idx = True)
	if len(rows) == 1:
		narrative = cNarrative(row = {'pk_field': 'pk_narrative', 'data': rows[0], 'idx': idx})
		return (True, narrative)

	# insert new narrative
	queries = [
		{'cmd': u"insert into clin.clin_narrative (fk_encounter, fk_episode, narrative, soap_cat) values (%s, %s, %s, lower(%s))",
		 'args': [encounter_id, episode_id, narrative, soap_cat]
		},
		{'cmd': u"select currval('clin.clin_narrative_pk_seq')"}
	]
	rows, idx = gmPG2.run_rw_queries(queries = queries, return_data=True)

	narrative = cNarrative(aPK_obj = rows[0][0])
	return (True, narrative)
#------------------------------------------------------------
def delete_clin_narrative(narrative=None):
	"""Deletes a clin.clin_narrative row by it's PK."""
	cmd = u"delete from clin.clin_narrative where pk=%s"
	rows, idx = gmPG2.run_rw_queries(queries = [{'cmd': cmd, 'args': [narrative]}])
	return True
#============================================================
# main
#------------------------------------------------------------
if __name__ == '__main__':

	from Gnumed.pycommon import gmI18N
	gmI18N.activate_locale()
	gmI18N.install_domain(domain = 'gnumed')

	def test_diag():
		print "\nDiagnose test"
		print  "-------------"
		diagnose = cDiag(aPK_obj=2)
		fields = diagnose.get_fields()
		for field in fields:
			print field, ':', diagnose[field]
		print "updatable:", diagnose.get_updatable_fields()
		print "codes:", diagnose.get_codes()
		#print "adding code..."
		#diagnose.add_code('Test code', 'Test coding system')
		#print "codes:", diagnose.get_codes()

	def test_narrative():
		print "\nnarrative test"
		print	"--------------"
		narrative = cNarrative(aPK_obj=7)
		fields = narrative.get_fields()
		for field in fields:
			print field, ':', narrative[field]
		print "updatable:", narrative.get_updatable_fields()
		print "codes:", narrative.get_codes()
		#print "adding code..."
		#narrative.add_code('Test code', 'Test coding system')
		#print "codes:", diagnose.get_codes()

		#print "creating narrative..."
		#status, new_narrative = create_clin_narrative(narrative = 'Test narrative', soap_cat = 'a', episode_id=1, encounter_id=2)
		#print new_narrative

	#-----------------------------------------
	def test_search_text_across_emrs():
		results = search_text_across_emrs('cut')
		for r in results:
			print r
	#-----------------------------------------

	#test_search_text_across_emrs()
	test_diag()
	test_narrative()

#============================================================
# $Log: gmClinNarrative.py,v $
# Revision 1.44  2009-12-26 19:05:08  ncq
# - improved comment
#
# Revision 1.43  2009/11/13 20:46:49  ncq
# - limit EMR search to 1000 results to remain sane
#
# Revision 1.42  2009/11/08 20:42:00  ncq
# - search across EMRs
#
# Revision 1.41  2009/06/29 14:50:30  ncq
# - use ellipsis for administrational soap rows
#
# Revision 1.40  2009/05/13 12:17:43  ncq
# - enable setting of fk_encounter
#
# Revision 1.39  2009/04/16 12:46:26  ncq
# - episode/encounter patient consistency check now moved to database
#
# Revision 1.38  2009/01/15 11:31:00  ncq
# - cleanup
#
# Revision 1.37  2008/12/27 15:49:21  ncq
# - raise exception on integrity problems in create_narrative
#
# Revision 1.36  2008/12/18 21:25:56  ncq
# - add format() to cClinNarrative
#
# Revision 1.35  2008/08/15 15:55:14  ncq
# - cleanup
#
# Revision 1.34  2008/05/07 15:15:15  ncq
# - use replace() rather than strip() to remove suffixes
#
# Revision 1.33  2008/04/22 21:11:05  ncq
# - define _() for testing
#
# Revision 1.32  2008/04/11 12:20:16  ncq
# - soap_cat2l10n_str
#
# Revision 1.31  2008/01/30 13:34:49  ncq
# - switch to std lib logging
#
# Revision 1.30  2008/01/22 22:02:29  ncq
# - add_coded_term -> add_coded_phrase
#
# Revision 1.29  2008/01/07 11:40:21  ncq
# - fix faulty comparison
#
# Revision 1.28  2008/01/06 08:08:25  ncq
# - check for duplicate narrative before insertion
#
# Revision 1.27  2007/11/05 12:09:29  ncq
# - support admin soap type
#
# Revision 1.26  2007/09/10 12:31:55  ncq
# - improve test suite
#
# Revision 1.25  2007/09/07 22:36:44  ncq
# - soap_cat2l10n and back
#
# Revision 1.24  2006/11/20 15:55:12  ncq
# - gmPG2.run_ro_queries *always* returns (rows, idx) so be aware of that
#
# Revision 1.23  2006/10/08 15:02:14  ncq
# - convert to gmPG2
# - convert to cBusinessDBObject
#
# Revision 1.22  2006/07/19 20:25:00  ncq
# - gmPyCompat.py is history
#
# Revision 1.21  2006/05/06 18:51:55  ncq
# - remove comment
#
# Revision 1.20  2005/11/27 12:44:57  ncq
# - clinical tables are in schema "clin" now
#
# Revision 1.19  2005/10/10 18:27:34  ncq
# - v_pat_narrative already HAS .provider
#
# Revision 1.18  2005/10/08 12:33:09  sjtan
# tree can be updated now without refetching entire cache; done by passing emr object to create_xxxx methods and calling emr.update_cache(key,obj);refresh_historical_tree non-destructively checks for changes and removes removed nodes and adds them if cache mismatch.
#
# Revision 1.17  2005/09/19 16:32:02  ncq
# - remove is_rfe/is_aoe/cRFE/cAOE
#
# Revision 1.16  2005/06/09 21:29:16  ncq
# - added missing s in %()s
#
# Revision 1.15  2005/05/17 08:00:09  ncq
# - in create_narrative() ignore empty narrative
#
# Revision 1.14  2005/04/11 17:53:47  ncq
# - id_patient -> pk_patient fix
#
# Revision 1.13  2005/04/08 13:27:54  ncq
# - adapt get_codes()
#
# Revision 1.12  2005/01/31 09:21:48  ncq
# - use commit2()
# - add delete_clin_narrative()
#
# Revision 1.11  2005/01/02 19:55:30  ncq
# - don't need _xmins_refetch_col_pos anymore
#
# Revision 1.10  2004/12/20 16:45:49  ncq
# - gmBusinessDBObject now requires refetching of XMIN after save_payload
#
# Revision 1.9  2004/11/03 22:32:34  ncq
# - support _cmds_lock_rows_for_update in business object base class
#
# Revision 1.8  2004/09/25 13:26:35  ncq
# - is_significant -> clinically_relevant
#
# Revision 1.7  2004/08/11 09:42:50  ncq
# - point clin_narrative VO to v_pat_narrative
# - robustify by applying lower() to soap_cat on insert/update
#
# Revision 1.6  2004/07/25 23:23:39  ncq
# - Carlos made cAOE.get_diagnosis() return a cDiag instead of a list
#
# Revision 1.5	2004/07/14 09:10:21	 ncq
# - Carlos' relentless work brings us get_codes(),
#	get_possible_codes() and adjustions for the fact
#	that we can now code any soap row
#
# Revision 1.4	2004/07/07 15:05:51	 ncq
# - syntax fixes by Carlos
# - get_codes(), get_possible_codes()
# - talk to the right views
#
# Revision 1.3	2004/07/06 00:09:19	 ncq
# - Carlos added create_clin_narrative(), cDiag, cNarrative, and unit tests - nice work !
#
# Revision 1.2	2004/07/05 10:24:46	 ncq
# - use v_pat_rfe/aoe, by Carlos
#
# Revision 1.1	2004/07/04 13:24:31	 ncq
# - add cRFE/cAOE
# - use in get_rfes(), get_aoes()
#
