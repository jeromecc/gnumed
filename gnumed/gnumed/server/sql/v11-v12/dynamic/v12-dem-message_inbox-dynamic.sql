-- ==============================================================
-- GNUmed database schema change script
--
-- License: GPL
-- Author: karsten.hilbert@gmx.net
--
-- ==============================================================
-- $Id: v12-dem-message_inbox-dynamic.sql,v 1.1 2009-08-28 12:47:29 ncq Exp $
-- $Revision: 1.1 $

-- --------------------------------------------------------------
\set ON_ERROR_STOP 1

--set default_transaction_read_only to off;

-- --------------------------------------------------------------
delete from audit.audited_tables where
	schema = 'dem'
		and
	table_name = 'provider_inbox'
;


\unset ON_ERROR_STOP
drop function audit.ft_ins_provider_inbox() cascade;
drop function audit.ft_del_provider_inbox() cascade;
drop function audit.ft_upd_provider_inbox() cascade;
\set ON_ERROR_STOP 1


select audit.add_table_for_audit('dem', 'message_inbox');

-- --------------------------------------------------------------
delete from gm.notifying_tables where
	schema_name = 'dem'
		and
	table_name = 'provider_inbox'
;


\unset ON_ERROR_STOP
drop function dem.trf_announce_provider_inbox_mod_no_pk() cascade;
\set ON_ERROR_STOP 1


select gm.add_table_for_notifies('dem'::name, 'message_inbox'::name);

-- --------------------------------------------------------------
alter table dem.message_inbox
	alter column fk_patient
		set default null;


alter table dem.message_inbox
	alter column fk_staff
		drop not null;



\unset ON_ERROR_STOP
alter table dem.message_inbox
	drop constraint message_must_have_recipient
		cascade;
\set ON_ERROR_STOP 1

alter table dem.message_inbox
	add constraint message_must_have_recipient
		check (
			(
				(fk_staff is null)
					and
				(fk_patient is null)
			) is False
		)
;



--\unset ON_ERROR_STOP
--alter table dem.message_inbox
--	drop constraint provider_inbox_comment_check
--		cascade;
--drop trigger tr_message_inbox_nullify_empty_comment on dem.message_inbox;
--\set ON_ERROR_STOP 1

--create trigger tr_message_inbox_nullify_empty_comment
--	before insert or update on dem.message_inbox
--		for each row execute procedure gm.trf_nullify_empty_string('comment')
--;

-- --------------------------------------------------------------
comment on table dem.message_inbox is
'messages in GNUmed relating to a patient, a provider, and a context';

-- --------------------------------------------------------------
\unset ON_ERROR_STOP
drop view dem.v_provider_inbox cascade;
drop view dem.v_message_inbox cascade;
\set ON_ERROR_STOP 1


create view dem.v_message_inbox as

select
	mi.modified_when as received_when,
	(select short_alias from dem.staff where dem.staff.pk = mi.fk_staff) as provider,
	mi.importance,
	vit.category,
	vit.l10n_category,
	vit.type,
	vit.l10n_type,
	mi.comment,
	mi.ufk_context as pk_context,
	mi.data as data,
	mi.pk as pk_message_inbox,
	mi.fk_staff as pk_staff,
	vit.pk_category,
	mi.fk_inbox_item_type as pk_type,
	mi.fk_patient as pk_patient
from
	dem.message_inbox mi,
	dem.v_inbox_item_type vit
where
	mi.fk_inbox_item_type = vit.pk_type

union

select
	now() as received_when,
	(select short_alias from dem.staff where dem.staff.pk = vo4dnd.pk_intended_reviewer)
		as provider,
	0	as importance,
	'clinical'
		as category,
	_('clinical')
		as l10n_category,
	'review docs'
		as type,
	_('review docs')
		as l10n_type,
	(select _('unreviewed documents for patient') || ' ['
		|| dn.lastnames || ', '
		|| dn.firstnames || ']'
	 from dem.names dn
	 where
	 	dn.id_identity = vo4dnd.pk_patient
	 		and
	 	dn.active is True
	)
	 	as comment,
	NULL
		as pk_context,
	NULL
		as data,
	NULL
		as pk_message_inbox,
	vo4dnd.pk_intended_reviewer
		as pk_staff,
	(select pk_category from dem.v_inbox_item_type where type = 'review docs')
		as pk_category,
	(select pk_type from dem.v_inbox_item_type where type = 'review docs')
		as pk_type,
	vo4dnd.pk_patient as pk_patient
from
	blobs.v_obj4doc_no_data vo4dnd
where
	reviewed is False

union

select
	now() as received_when,
	(select short_alias from dem.staff where dem.staff.pk = vtr.pk_intended_reviewer)
		as provider,
	0	as importance,
	'clinical'
		as category,
	_('clinical')
		as l10n_category,
	'review results'
		as type,
	_('review results')
		as l10n_type,
	(select _('unreviewed results for patient') || ' ['
		|| dn.lastnames || ', '
		|| dn.firstnames || ']'
	 from dem.names dn
	 where
	 	dn.id_identity = vtr.pk_patient
	 		and
	 	dn.active is True
	)
		as comment,
	NULL
		as pk_context,
	NULL
		as data,
	NULL
		as pk_message_inbox,
	vtr.pk_intended_reviewer
		as pk_staff,
	(select pk_category from dem.v_inbox_item_type where type = 'review results')
		as pk_category,
	(select pk_type from dem.v_inbox_item_type where type = 'review results')
		as pk_type,
	vtr.pk_patient as pk_patient
from
	clin.v_test_results vtr
where
	reviewed is False

;


comment on view dem.v_message_inbox is
'Denormalized messages for the providers and/or patients.
Using UNION makes sure we get the right level of uniqueness.';


grant select on dem.v_message_inbox to group "gm-doctors";


-- --------------------------------------------------------------
select gm.log_script_insertion('$RCSfile: v12-dem-message_inbox-dynamic.sql,v $', '$Revision: 1.1 $');

-- ==============================================================
-- $Log: v12-dem-message_inbox-dynamic.sql,v $
-- Revision 1.1  2009-08-28 12:47:29  ncq
-- - adjust to renaming
-- - allow fk_provider nullable provider fk_patient isn't null
--
--
