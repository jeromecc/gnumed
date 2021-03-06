"""GNUmed hooks framework.

This module provides convenience functions and definitions
for accessing the GNUmed hooks framework.

This framework calls the script

	~/.gnumed/scripts/hook_script.py

at various times during client execution. The script must
contain a function

def run_script(hook=None):
	pass

which accepts a single argument <hook>. That argument will
contain the hook that is being activated.
"""
# ========================================================================
__author__  = "K. Hilbert <Karsten.Hilbert@gmx.net>"
__license__ = "GPL v2 or later (details at http://www.gnu.org)"

# stdlib
import os
import sys
import stat
import logging
import io


# GNUmed libs
if __name__ == '__main__':
	sys.path.insert(0, '../../')
from Gnumed.pycommon import gmDispatcher
from Gnumed.pycommon import gmTools


_log = logging.getLogger('gm.hook')
# ========================================================================
known_hooks = [
	u'post_patient_activation',
	u'post_person_creation',

	u'shutdown-post-GUI',
	u'startup-after-GUI-init',
	u'startup-before-GUI',

	u'request_user_attention',
	u'app_activated_startup',
	u'app_activated',
	u'app_deactivated',

	u'after_substance_intake_modified',
	u'after_test_result_modified',
	u'after_soap_modified',
	u'after_code_link_modified',

	u'after_new_doc_created',
	u'before_print_doc',
	u'before_fax_doc',
	u'before_mail_doc',
	u'before_print_doc_part',
	u'before_fax_doc_part',
	u'before_mail_doc_part',
	u'before_external_doc_access',

	u'db_maintenance_warning'
]

_log.debug('known hooks:')
for hook in known_hooks:
	_log.debug(hook)

# ========================================================================
hook_module = None

def import_hook_module(reimport=False):

	global hook_module
	if not reimport:
		if hook_module is not None:
			return True

	# hardcoding path and script name allows us to
	# not need configuration for it, the environment
	# can always be detected at runtime (workplace etc)
	script_name = 'hook_script.py'
	script_path = os.path.expanduser(os.path.join('~', '.gnumed', 'scripts'))
	full_script = os.path.join(script_path, script_name)

	if not os.access(full_script, os.F_OK):
		_log.warning('creating default hook script')
		f = io.open(full_script, mode = u'wt', encoding = u'utf8')
		f.write(u"""
# known hooks:
#  %s

def run_script(hook=None):
	pass
""" % '#  '.join(known_hooks))
		f.close()
		os.chmod(full_script, 384)

	if os.path.islink(full_script):
		gmDispatcher.send (
			signal = 'statustext',
			msg = _('Script must not be a link: [%s].') % full_script
		)
		return False

	if not os.access(full_script, os.R_OK):
		gmDispatcher.send (
			signal = 'statustext',
			msg = _('Script must be readable by the calling user: [%s].') % full_script
		)
		return False

	script_stat_val = os.stat(full_script)
	_log.debug('hook script stat(): %s', script_stat_val)
	script_perms = stat.S_IMODE(script_stat_val.st_mode)
	_log.debug('hook script mode: %s (oktal: %s)', script_perms, oct(script_perms))
	if script_perms != 384:				# octal 0600
		if os.name in ['nt']:
			_log.warning('this platform does not support os.stat() file permission checking')
		else:
			gmDispatcher.send (
				signal = 'statustext',
				msg = _('Script must be readable by the calling user only (permissions "0600"): [%s].') % full_script
			)
			return False

	try:
		tmp = gmTools.import_module_from_directory(script_path, script_name)
	except Exception:
		_log.exception('cannot import hook script')
		return False

	hook_module = tmp
#	if reimport:
#		reload(tmp)			# this has well-known shortcomings !

	_log.info('hook script: %s', full_script)
	return True
# ========================================================================
__current_hook_stack = []

def run_hook_script(hook=None):
	# NOTE: this just *might* be a huge security hole

	_log.info('told to pull hook [%s]', hook)

	if hook not in known_hooks:
		raise ValueError('run_hook_script(): unknown hook [%s]' % hook)

	if not import_hook_module(reimport = False):
		_log.debug('cannot import hook module, not pulling hook')
		return False

	if hook in __current_hook_stack:
		_log.error('hook-code cycle detected, aborting')
		_log.error('current hook stack: %s', __current_hook_stack)
		return False

	__current_hook_stack.append(hook)

	try:
		hook_module.run_script(hook = hook)
	except Exception:
		_log.exception('error running hook script for [%s]', hook)
		gmDispatcher.send (
			signal = u'statustext',
			msg = _('Error running hook [%s] script.') % hook,
			beep = True
		)
		if __current_hook_stack[-1] != hook:
			_log.error('hook nesting errror detected')
			_log.error('latest hook: expected [%s], found [%s]', hook, __current_hook_stack[-1])
			_log.error('current hook stack: %s', __current_hook_stack)
		else:
			__current_hook_stack.pop()
		return False

	if __current_hook_stack[-1] != hook:
		_log.error('hook nesting errror detected')
		_log.error('latest hook: expected [%s], found [%s]', hook, __current_hook_stack[-1])
		_log.error('current hook stack: %s', __current_hook_stack)
	else:
		__current_hook_stack.pop()

	return True
# ========================================================================
if __name__ == '__main__':

	if len(sys.argv) < 2:
		sys.exit()

	if sys.argv[1] != u'test':
		sys.exit()

	run_hook_script(hook = 'shutdown-post-GUI')
	run_hook_script(hook = 'invalid hook')

# ========================================================================
