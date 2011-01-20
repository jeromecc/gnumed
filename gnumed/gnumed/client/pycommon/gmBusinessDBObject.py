"""GNUmed database object business class.

Overview
--------
This class wraps a source relation (table, view) which
represents an entity that makes immediate business sense
such as a vaccination or a medical document. In many if
not most cases this source relation is a denormalizing
view. The data in that view will in most cases, however,
originate from several normalized tables. One instance
of this class represents one row of said source relation.

Note, however, that this class does not *always* simply
wrap a single table or view. It can also encompass several
relations (views, tables, sequences etc) that taken together
form an object meaningful to *business* logic.

Initialization
--------------
There are two ways to initialize an instance with values.
One way is to pass a "primary key equivalent" object into
__init__(). Refetch_payload() will then pull the data from
the backend. Another way would be to fetch the data outside
the instance and pass it in via the <row> argument. In that
case the instance will not initially connect to the databse
which may offer a great boost to performance.

Values API
----------
Field values are cached for later access. They can be accessed
by a dictionary API, eg:

	old_value = object['field']
	object['field'] = new_value

The field names correspond to the respective column names
in the "main" source relation. Accessing non-existant field
names will raise an error, so does trying to set fields not
listed in self.__class__._updatable_fields. To actually
store updated values in the database one must explicitly
call save_payload().

The class will in many cases be enhanced by accessors to
related data that is not directly part of the business
object itself but are closely related, such as codes
linked to a clinical narrative entry (eg a diagnosis). Such
accessors in most cases start with get_*. Related setters
start with set_*. The values can be accessed via the
object['field'] syntax, too, but they will be cached
independantly.

Concurrency handling
--------------------
GnuMed connections always run transactions in isolation level
"serializable". This prevents transactions happening at the
*very same time* to overwrite each other's data. All but one
of them will abort with a concurrency error (eg if a
transaction runs a select-for-update later than another one
it will hang until the first transaction ends. Then it will
succeed or fail depending on what the first transaction
did). This is standard transactional behaviour.

However, another transaction may have updated our row
between the time we first fetched the data and the time we
start the update transaction. This is noticed by getting the
XMIN system column for the row when initially fetching the
data and using that value as a where condition value when
updating the row later. If the row had been updated (xmin
changed) or deleted (primary key disappeared) in the
meantime the update will touch zero rows (as no row with
both PK and XMIN matching is found) even if the query itself
syntactically succeeds.

When detecting a change in a row due to XMIN being different
one needs to be careful how to represent that to the user.
The row may simply have changed but it also might have been
deleted and a completely new and unrelated row which happens
to have the same primary key might have been created ! This
row might relate to a totally different context (eg. patient,
episode, encounter).

One can offer all the data to the user:

self.original_payload
- contains the data at the last successful refetch

self.modified_payload
- contains the modified payload just before the last
  failure of save_payload() - IOW what is currently
  in the database

self._payload
- contains the currently active payload which may or
  may not contain changes

For discussion on this see the thread starting at:

	http://archives.postgresql.org/pgsql-general/2004-10/msg01352.php

and here

	http://groups.google.com/group/pgsql.general/browse_thread/thread/e3566ba76173d0bf/6cf3c243a86d9233
	(google for "XMIN semantic at peril")

Problem cases with XMIN:

1) not unlikely
- a very old row is read with XMIN
- vacuum comes along and sets XMIN to FrozenTransactionId
  - now XMIN changed but the row actually didn't !
- an update with "... where xmin = old_xmin ..." fails
  although there is no need to fail

2) quite unlikely
- a row is read with XMIN
- a long time passes
- the original XMIN gets frozen to FrozenTransactionId
- another writer comes along and changes the row
- incidentally the exact same old row gets the old XMIN *again*
  - now XMIN is (again) the same but the data changed !
- a later update fails to detect the concurrent change !!

TODO:
The solution is to use our own column for optimistic locking
which gets updated by an AFTER UPDATE trigger.
"""
#============================================================
__version__ = "$Revision: 1.60 $"
__author__ = "K.Hilbert <Karsten.Hilbert@gmx.net>"
__license__ = "GPL"

import sys, copy, types, inspect, logging, datetime


if __name__ == '__main__':
	sys.path.insert(0, '../../')
from Gnumed.pycommon import gmExceptions, gmPG2


_log = logging.getLogger('gm.db')
_log.info(__version__)
#============================================================
class cBusinessDBObject(object):
	"""Represents business objects in the database.

	Rules:
	- instances ARE ASSUMED TO EXIST in the database
	- PK construction (aPK_obj): DOES verify its existence on instantiation
	                             (fetching data fails)
	- Row construction (row): allowed by using a dict of pairs
	                               field name: field value (PERFORMANCE improvement)
	- does NOT verify FK target existence
	- does NOT create new entries in the database
	- does NOT lazy-fetch fields on access

	Class scope SQL commands and variables:

	<_cmd_fetch_payload>
		- must return exactly one row
		- where clause argument values are expected
		  in self.pk_obj (taken from __init__(aPK_obj))
		- must return xmin of all rows that _cmds_store_payload
		  will be updating, so views must support the xmin columns
		  of their underlying tables

	<_cmds_store_payload>
		- one or multiple "update ... set ... where xmin_* = ..." statements
		  which actually update the database from the data in self._payload,
		- the last query must refetch the XMIN values needed to detect
		  concurrent updates, their field names had better be the same as
		  in _cmd_fetch_payload

	<_updatable_fields>
		- a list of fields available for update via object['field']


	A template for new child classes:

#------------------------------------------------------------
from Gnumed.pycommon import gmBusinessDBObject
from Gnumed.pycommon import gmPG2

#============================================================
# description
#------------------------------------------------------------
_SQL_get_XXX = u\"""
	SELECT *, (xmin as) xmin_XXX
	FROM XXX.v_XXX
	WHERE %s
\"""

class cXxxXxx(gmBusinessDBObject.cBusinessDBObject):

	_cmd_fetch_payload = _SQL_get_XXX % u"pk_XXX = %s"
	_cmds_store_payload = [
		u\"""
			UPDATE xxx.xxx SET
				xxx = %(xxx)s,
				xxx = gm.nullify_empty_string(%(xxx)s)
			WHERE
				pk = %(xxx)s
					AND
				xmin = %(xmin_XXX)s
			RETURNING
				pk,
				xmin as xmin_XXX
		\"""
	]
	_updatable_fields = [
		u'xxx',
		u'xxx'
	]
#------------------------------------------------------------
def get_XXX(order_by=None):
	if order_by is None:
		order_by = u'true'
	else:
		order_by = 'true ORDER BY %s' % order_by

	cmd = _SQL_get_XXX % order_by
	rows, idx = gmPG2.run_ro_queries(queries = [{'cmd': cmd}], get_col_idx = True)
	return [ cXxxXxx(row = {'data': r, 'idx': idx, 'pk_field': 'xxx'}) for r in rows ]
#------------------------------------------------------------
def create_xxx(xxx=None, xxx=None):

	args = {
		u'xxx': xxx,
		u'xxx': xxx
	}
	cmd = u\"""
		INSERT INTO xxx.xxx (
			xxx,
			xxx
		) VALUES (
			%(xxx)s,
			%(xxx)s,
			gm.nullify_empty_string(%(xxx)s)
		)
		RETURING pk
	\"""
	rows, idx = gmPG2.run_rw_queries(queries = [{'cmd': cmd, 'args': args}], return_data = True, get_col_idx = False)

	return cXxxXxx(aPK_obj = rows[0]['pk'])
#------------------------------------------------------------
def delete_xxx(xxx=None):
	args = {'pk': xxx}
	cmd = u\"""
		DELETE FROM xxx.xxx
		WHERE pk = %(pk)s
	\"""
	gmPG2.run_rw_queries(queries = [{'cmd': cmd, 'args': args}])
	return True
#------------------------------------------------------------


	"""
	#--------------------------------------------------------
	def __init__(self, aPK_obj=None, row=None):
		"""Init business object.

		Call from child classes:

			super(cChildClass, self).__init__(aPK_obj = aPK_obj, row = row)
		"""
		# initialize those "too early" because checking descendants might
		# fail which will then call __str__ in stack trace logging if --debug
		# was given which in turn needs those instance variables
		self.pk_obj = '<uninitialized>'
		self._idx = {}
		self._payload = []		# the cache for backend object values (mainly table fields)
		self._ext_cache = {}	# the cache for extended method's results
		self._is_modified = False

		# check descendants
		self.__class__._cmd_fetch_payload
		self.__class__._cmds_store_payload
		self.__class__._updatable_fields

		if aPK_obj is not None:
			self.__init_from_pk(aPK_obj=aPK_obj)
		else:
			self._init_from_row_data(row=row)

		self._is_modified = False
	#--------------------------------------------------------
	def __init_from_pk(self, aPK_obj=None):
		"""Creates a new clinical item instance by its PK.

		aPK_obj can be:
			- a simple value
			  * the primary key WHERE condition must be
				a simple column
			- a dictionary of values
			  * the primary key where condition must be a
				subselect consuming the dict and producing
				the single-value primary key
		"""
		self.pk_obj = aPK_obj
		result = self.refetch_payload()
		if result is True:
			self.original_payload = {}
			for field in self._idx.keys():
				self.original_payload[field] = self._payload[self._idx[field]]
			return True

		if result is False:
			raise gmExceptions.ConstructorError, "[%s:%s]: error loading instance" % (self.__class__.__name__, self.pk_obj)
	#--------------------------------------------------------
	def _init_from_row_data(self, row=None):
		"""Creates a new clinical item instance given its fields.

		row must be a dict with the fields:
			- pk_field: the name of the primary key field
			- idx: a dict mapping field names to position
			- data: the field values in a list (as returned by
			  cursor.fetchone() in the DB-API)

		row = {'data': row, 'idx': idx, 'pk_field': 'the PK column name'}

		rows, idx = gmPG2.run_ro_queries(queries = [{'cmd': cmd, 'args': args}], get_col_idx = True)
		objects = [ cChildClass(row = {'data': r, 'idx': idx, 'pk_field': 'the PK column name'}) for r in rows ]
		"""
		try:
			self._idx = row['idx']
			self._payload = row['data']
			self.pk_obj = self._payload[self._idx[row['pk_field']]]
		except:
			_log.exception('faulty <row> argument structure: %s' % row)
			raise gmExceptions.ConstructorError, "[%s:??]: error loading instance from row data" % self.__class__.__name__

		if len(self._idx.keys()) != len(self._payload):
			_log.critical('field index vs. payload length mismatch: %s field names vs. %s fields' % (len(self._idx.keys()), len(self._payload)))
			_log.critical('faulty <row> argument structure: %s' % row)
			raise gmExceptions.ConstructorError, "[%s:??]: error loading instance from row data" % self.__class__.__name__

		self.original_payload = {}
		for field in self._idx.keys():
			self.original_payload[field] = self._payload[self._idx[field]]
	#--------------------------------------------------------
	def __del__(self):
		if self.__dict__.has_key('_is_modified'):
			if self._is_modified:
				_log.critical('[%s:%s]: loosing payload changes' % (self.__class__.__name__, self.pk_obj))
				_log.debug('original: %s' % self.original_payload)
				_log.debug('modified: %s' % self._payload)
	#--------------------------------------------------------
	def __str__(self):
		tmp = []
		try:
			for attr in self._idx.keys():
				if self._payload[self._idx[attr]] is None:
					tmp.append(u'%s: NULL' % attr)
				else:
					tmp.append('%s: >>%s<<' % (attr, self._payload[self._idx[attr]]))
			return '[%s:%s]: %s' % (self.__class__.__name__, self.pk_obj, str(tmp))
		except:
			return 'nascent [%s @ %s], cannot show payload and primary key' %(self.__class__.__name__, id(self))
	#--------------------------------------------------------
	def __getitem__(self, attribute):
		# use try: except: as it is faster and we want this as fast as possible

		# 1) backend payload cache
		try:
			return self._payload[self._idx[attribute]]
		except KeyError:
			pass

		# 2) extension method results ...
		getter = getattr(self, 'get_%s' % attribute, None)
		if not callable(getter):
			_log.warning('[%s]: no attribute [%s]' % (self.__class__.__name__, attribute))
			_log.warning('[%s]: valid attributes: %s' % (self.__class__.__name__, str(self._idx.keys())))
			_log.warning('[%s]: no getter method [get_%s]' % (self.__class__.__name__, attribute))
			methods = filter(lambda x: x[0].startswith('get_'), inspect.getmembers(self, inspect.ismethod))
			_log.warning('[%s]: valid getter methods: %s' % (self.__class__.__name__, str(methods)))
			raise gmExceptions.NoSuchBusinessObjectAttributeError, '[%s]: cannot access [%s]' % (self.__class__.__name__, attribute)

		self._ext_cache[attribute] = getter()
		return self._ext_cache[attribute]
	#--------------------------------------------------------
	def __setitem__(self, attribute, value):

		# 1) backend payload cache
		if attribute in self.__class__._updatable_fields:
			try:
				if self._payload[self._idx[attribute]] != value:
					self._payload[self._idx[attribute]] = value
					self._is_modified = True
				return
			except KeyError:
				_log.warning('[%s]: cannot set attribute <%s> despite marked settable' % (self.__class__.__name__, attribute))
				_log.warning('[%s]: supposedly settable attributes: %s' % (self.__class__.__name__, str(self.__class__._updatable_fields)))
				raise gmExceptions.NoSuchBusinessObjectAttributeError, '[%s]: cannot access [%s]' % (self.__class__.__name__, attribute)

		# 2) setters providing extensions
		if hasattr(self, 'set_%s' % attribute):
			setter = getattr(self, "set_%s" % attribute)
			if not callable(setter):
				raise gmExceptions.NoSuchBusinessObjectAttributeError, '[%s] setter [set_%s] not callable' % (self.__class__.__name__, attribute)
			try:
				del self._ext_cache[attribute]
			except KeyError:
				pass
			if type(value) is types.TupleType:
				if setter(*value):
					self._is_modified = True
					return
				raise gmExceptions.BusinessObjectAttributeNotSettableError, '[%s]: setter [%s] failed for [%s]' % (self.__class__.__name__, setter, value)
			if setter(value):
				self._is_modified = True
				return

		# 3) don't know what to do with <attribute>
		_log.error('[%s]: cannot find attribute <%s> or setter method [set_%s]' % (self.__class__.__name__, attribute, attribute))
		_log.warning('[%s]: settable attributes: %s' % (self.__class__.__name__, str(self.__class__._updatable_fields)))
		methods = filter(lambda x: x[0].startswith('set_'), inspect.getmembers(self, inspect.ismethod))
		_log.warning('[%s]: valid setter methods: %s' % (self.__class__.__name__, str(methods)))
		raise gmExceptions.BusinessObjectAttributeNotSettableError, '[%s]: cannot set [%s]' % (self.__class__.__name__, attribute)
	#--------------------------------------------------------
	# external API
	#--------------------------------------------------------
	def same_payload(self, another_object=None):
		raise NotImplementedError('comparison between [%s] and [%s] not implemented' % (self, another_object))
	#--------------------------------------------------------
	def is_modified(self):
		return self._is_modified
	#--------------------------------------------------------
	def get_fields(self):
		try:
			return self._idx.keys()
		except AttributeError:
			return 'nascent [%s @ %s], cannot return keys' %(self.__class__.__name__, id(self))
	#--------------------------------------------------------
	def get_updatable_fields(self):
		return self.__class__._updatable_fields
	#--------------------------------------------------------
	def get_patient(self):
		_log.error('[%s:%s]: forgot to override get_patient()' % (self.__class__.__name__, self.pk_obj))
		return None
	#--------------------------------------------------------
	def refetch_payload(self, ignore_changes=False):
		"""Fetch field values from backend.
		"""
		if self._is_modified:
			if ignore_changes:
				_log.critical('[%s:%s]: loosing payload changes' % (self.__class__.__name__, self.pk_obj))
				_log.debug('original: %s' % self.original_payload)
				_log.debug('modified: %s' % self._payload)
			else:
				_log.critical('[%s:%s]: cannot reload, payload changed' % (self.__class__.__name__, self.pk_obj))
				return False

		if type(self.pk_obj) == types.DictType:
			arg = self.pk_obj
		else:
			arg = [self.pk_obj]
		rows, self._idx = gmPG2.run_ro_queries (
			queries = [{'cmd': self.__class__._cmd_fetch_payload, 'args': arg}],
			get_col_idx = True
		)
		if len(rows) == 0:
			_log.error('[%s:%s]: no such instance' % (self.__class__.__name__, self.pk_obj))
			return False
		self._payload = rows[0]
		return True
	#--------------------------------------------------------
	def __noop(self):
		pass
	#--------------------------------------------------------
	def save(self, conn=None):
		return self.save_payload(conn = conn)
	#--------------------------------------------------------
	def save_payload(self, conn=None):
		"""Store updated values (if any) in database.

		Optionally accepts a pre-existing connection
		- returns a tuple (<True|False>, <data>)
		- True: success
		- False: an error occurred
			* data is (error, message)
			* for error meanings see gmPG2.run_rw_queries()
		"""
		if not self._is_modified:
			return (True, None)

		args = {}
		for field in self._idx.keys():
			args[field] = self._payload[self._idx[field]]
		self.modified_payload = args

		close_conn = self.__noop
		if conn is None:
			conn = gmPG2.get_connection(readonly=False)
			close_conn = conn.close

		# query succeeded but failed to find the row to lock
		# because another transaction committed an UPDATE or
		# DELETE *before* we attempted to lock it ...
		# FIXME: this can fail if savepoints are used since subtransactions change the xmin/xmax ...

		queries = []
		for query in self.__class__._cmds_store_payload:
			queries.append({'cmd': query, 'args': args})
		rows, idx = gmPG2.run_rw_queries (
			link_obj = conn,
			queries = queries,
			return_data = True,
			get_col_idx = True
		)

		# this can happen if:
		# - someone else updated the row so XMIN does not match anymore
		# - the PK went away (rows was deleted from under us)
		# - another WHERE condition of the UPDATE did not produce any rows to update
		if len(rows) == 0:
			return (False, (u'cannot update row', _('[%s:%s]: row not updated (nothing returned), row in use ?') % (self.__class__.__name__, self.pk_obj)))

		# update cached XMIN values (should be in first-and-only result row of last query)
		row = rows[0]
		for key in idx:
			try:
				self._payload[self._idx[key]] = row[idx[key]]
			except KeyError:
				conn.rollback()
				close_conn()
				_log.error('[%s:%s]: cannot update instance, XMIN refetch key mismatch on [%s]' % (self.__class__.__name__, self.pk_obj, key))
				_log.error('payload keys: %s' % str(self._idx))
				_log.error('XMIN refetch keys: %s' % str(idx))
				_log.error(args)
				raise

		conn.commit()
		close_conn()

		self._is_modified = False
		# update to new "original" payload
		self.original_payload = {}
		for field in self._idx.keys():
			self.original_payload[field] = self._payload[self._idx[field]]

		return (True, None)

#============================================================
def jsonclasshintify(obj):
	# this should eventually be somewhere else
	""" turn the data into a list of dicts, adding "class hints".
		all objects get turned into dictionaries which the other end
		will interpret as "object", via the __jsonclass__ hint,
		as specified by the JSONRPC protocol standard.
	"""
	if isinstance(obj, list):
		return map(jsonclasshintify, obj)
	elif isinstance(obj, gmPG2.dbapi.tz.FixedOffsetTimezone):
		# this will get decoded as "from jsonobjproxy import {clsname}"
		# at the remote (client) end.
		res = {'__jsonclass__': ["jsonobjproxy.FixedOffsetTimezone"]}
		res['name'] = obj._name
		res['offset'] = jsonclasshintify(obj._offset)
		return res
	elif isinstance(obj, datetime.timedelta):
		# this will get decoded as "from jsonobjproxy import {clsname}"
		# at the remote (client) end.
		res = {'__jsonclass__': ["jsonobjproxy.TimeDelta"]}
		res['days'] = obj.days
		res['seconds'] = obj.seconds
		res['microseconds'] = obj.microseconds
		return res
	elif isinstance(obj, datetime.time):
		# this will get decoded as "from jsonobjproxy import {clsname}"
		# at the remote (client) end.
		res = {'__jsonclass__': ["jsonobjproxy.Time"]}
		res['hour'] = obj.hour
		res['minute'] = obj.minute
		res['second'] = obj.second
		res['microsecond'] = obj.microsecond
		res['tzinfo'] = jsonclasshintify(obj.tzinfo)
		return res
	elif isinstance(obj, datetime.datetime):
		# this will get decoded as "from jsonobjproxy import {clsname}"
		# at the remote (client) end.
		res = {'__jsonclass__': ["jsonobjproxy.DateTime"]}
		res['year'] = obj.year
		res['month'] = obj.month
		res['day'] = obj.day
		res['hour'] = obj.hour
		res['minute'] = obj.minute
		res['second'] = obj.second
		res['microsecond'] = obj.microsecond
		res['tzinfo'] = jsonclasshintify(obj.tzinfo)
		return res
	elif isinstance(obj, cBusinessDBObject):
		# this will get decoded as "from jsonobjproxy import {clsname}"
		# at the remote (client) end.
		res = {'__jsonclass__': ["jsonobjproxy.%s" % obj.__class__.__name__]}
		for k in obj.get_fields():
			t = jsonclasshintify(obj[k])
			res[k] = t
		print "props", res, dir(obj)
		for attribute in dir(obj):
			if not attribute.startswith("get_"):
				continue
			k = attribute[4:]
			if res.has_key(k):
				continue
			getter = getattr(obj, attribute, None)
			if callable(getter):
				res[k] = jsonclasshintify(getter())
		return res
	return obj

#============================================================
if __name__ == '__main__':

	if len(sys.argv) < 2:
		sys.exit()

	if sys.argv[1] != u'test':
		sys.exit()

	#--------------------------------------------------------
	class cTestObj(cBusinessDBObject):
		_cmd_fetch_payload = None
		_cmds_store_payload = None
		_updatable_fields = []
		#----------------------------------------------------
		def get_something(self):
			pass
		#----------------------------------------------------
		def set_something(self):
			pass
	#--------------------------------------------------------
	from Gnumed.pycommon import gmI18N
	gmI18N.activate_locale()
	gmI18N.install_domain()

	data = {
		'pk_field': 'bogus_pk',
		'idx': {'bogus_pk': 0, 'bogus_field': 1},
		'data': [-1, 'bogus_data']
	}
	obj = cTestObj(row=data)
	#print obj['wrong_field']
	#print jsonclasshintify(obj)
	obj['wrong_field'] = 1

#============================================================
