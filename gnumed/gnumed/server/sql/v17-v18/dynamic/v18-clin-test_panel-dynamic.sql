-- ==============================================================
-- GNUmed database schema change script
--
-- License: GPL v2 or later
-- Author: karsten.hilbert@gmx.net
--
-- ==============================================================
\set ON_ERROR_STOP 1

set check_function_bodies to on;
--set default_transaction_read_only to off;

-- --------------------------------------------------------------
comment on table clin.test_panel is
	'Panels of tests. The same test can appear in several panels.';


select gm.register_notifying_table('clin', 'test_panel');
select audit.register_table_for_auditing('clin', 'test_panel');


grant insert, update, delete on table
	clin.test_panel
to group "gm-public";


grant usage on clin.test_panel_pk_seq to group "gm-public";

-- --------------------------------------------------------------
-- .description
comment on column clin.test_panel.description is
	'A description/label for this panel.';


\unset ON_ERROR_STOP
alter table clin.test_panel drop constraint clin_test_panel_sane_desc cascade;
\set ON_ERROR_STOP 1

alter table clin.test_panel
	add constraint clin_test_panel_sane_desc check (
		(gm.is_null_or_blank_string(description) is False)
	);

-- --------------------------------------------------------------
-- .comment
comment on column clin.test_panel.comment is
	'An arbitrary comment on this panel.';


\unset ON_ERROR_STOP
alter table clin.test_panel drop constraint clin_test_panel_sane_cmt cascade;
\set ON_ERROR_STOP 1

alter table clin.test_panel
	add constraint clin_test_panel_sane_cmt check (
		(gm.is_null_or_non_empty_string(comment) is True)
	);

-- --------------------------------------------------------------
-- .pk_test_types
comment on column clin.test_panel.pk_test_types is
	'Links to test types which belong to this panel.';


\unset ON_ERROR_STOP
drop function clin.trf_ins_upd_validate_test_type_pks() cascade;
\set ON_ERROR_STOP 1

create or replace function clin.trf_ins_upd_validate_test_type_pks()
	returns trigger
	language 'plpgsql'
	as '
DECLARE
	_msg text;
	_func text;
	_pk integer;
BEGIN
	if NEW.pk_test_types is NULL then
		return NEW;
	end if;

	_func := ''[clin.trf_ins_upd_validate_test_type_pks]: '';

	if array_ndims(NEW.pk_test_types) <> 1 then
		_msg := _func || ''pk_test_types is not a one-dimensional array'' || array_to_string(NEW.pk_test_types, ''/'', ''<NULL>'');
		raise exception foreign_key_violation using message = _msg;
	end if;

	FOR _pk IN SELECT unnest(NEW.pk_test_types) LOOP
		perform 1 from clin.test_type where pk = _pk;
		if not found then
			_msg := _func || ''pk_test_types element ('' || coalesce(_pk::text, ''<NULL>'')  || '') not found in clin.test_type.pk column'';
			raise exception foreign_key_violation using message = _msg;
		end if;
	END LOOP;

	return NEW;
END;';


comment on function clin.trf_ins_upd_validate_test_type_pks() is
	'Explicit foreign key-like check.';


create trigger tr_ins_upd_validate_test_type_pks
	before insert or update on clin.test_panel
	for each row execute procedure clin.trf_ins_upd_validate_test_type_pks();

-- --------------------------------------------------------------
delete from clin.test_panel where description = 'EML base';

insert into clin.test_panel (
	description,
	comment,
	pk_test_types
) values (
	'EML base',
	'Enterprise Main Lab rapid screening panel.',
	(select array_agg(pk) from clin.test_type where abbrev like '%-EML')
);


-- --------------------------------------------------------------
select gm.log_script_insertion('v18-clin-test_panel-dynamic.sql', '18.0');
