-- project: GnuMed

-- purpose: views for easier clinical data access
-- author: Karsten Hilbert
-- license: GPL (details at http://gnu.org)

-- $Source: /home/ncq/Projekte/cvs2git/vcs-mirror/gnumed/gnumed/server/sql/gmClinicalViews.sql,v $
-- $Id: gmClinicalViews.sql,v 1.23 2003-08-03 14:06:45 ncq Exp $

-- ===================================================================
-- force terminate + exit(3) on errors if non-interactive
\set ON_ERROR_STOP 1

-- =============================================
\unset ON_ERROR_STOP
drop index idx_item_encounter;
drop index idx_item_episode;
drop index idx_episode_h_issue;
drop index idx_allergy_comment;
\set ON_ERROR_STOP 1

create index idx_item_encounter on clin_root_item(id_encounter);
create index idx_item_episode on clin_root_item(id_episode);
create index idx_episode_h_issue on clin_episode(id_health_issue);

-- =============================================
\unset ON_ERROR_STOP
drop view v_i18n_enum_encounter_type;
\set ON_ERROR_STOP 1

create view v_i18n_enum_encounter_type as
select
	_enum_encounter_type.id as id,
	_(_enum_encounter_type.description) as description
from
	_enum_encounter_type
;

-- =============================================
\unset ON_ERROR_STOP
drop view v_patient_episodes;
\set ON_ERROR_STOP 1

create view v_patient_episodes as
select
	chi.id_patient as id_patient,
	cep.id as id_episode,
	cep.description as episode,
	chi.id as id_health_issue,
	chi.description as health_issue
from
	clin_episode cep, clin_health_issue chi
where
	cep.id_health_issue=chi.id
;

-- =============================================
-- clin_root_item stuff
\unset ON_ERROR_STOP
drop trigger TR_clin_item_mod on clin_root_item;
drop function F_announce_clin_item_mod();
\set ON_ERROR_STOP 1

create function F_announce_clin_item_mod() returns opaque as '
declare
	episode_id integer;
	patient_id integer;
begin
	-- get episode ID
	if TG_OP = ''DELETE'' then
		episode_id := OLD.id_episode;
	else
		episode_id := NEW.id_episode;
	end if;
	-- track back to patient ID
	select into patient_id id_patient
		from v_patient_episodes vpep
		where vpep.id_episode = episode_id
		limit 1;
	-- now, execute() the NOTIFY
	execute ''notify "item_change_db:'' || patient_id || ''"'';
	return NULL;
end;
' language 'plpgsql';

create trigger TR_clin_item_mod
	after insert or delete or update
	on clin_root_item
	for each row
		execute procedure F_announce_clin_item_mod()
;

\unset ON_ERROR_STOP
drop view v_patient_items;
\set ON_ERROR_STOP 1

create view v_patient_items as
select
	extract(epoch from cri.modified_when) as age,
	cri.modified_when as modified_when,
	cri.modified_by as modified_by,
	case cri.row_version
		when 0 then false
		else true
	end as is_modified,
	vpep.id_patient as id_patient,
	cri.pk_item as id_item,
	cri.id_encounter as id_encounter,
	cri.id_episode as id_episode,
	vpep.id_health_issue as id_health_issue,
	cri.narrative as narrative,
	sys.relname as src_table
from
	clin_root_item cri, v_patient_episodes vpep, pg_class sys
where
	vpep.id_episode=cri.id_episode
		and
	cri.tableoid=sys.oid
order by
	age
;

-- =============================================
\unset ON_ERROR_STOP
drop view v_i18n_patient_encounters;
\set ON_ERROR_STOP 1

create view v_i18n_patient_encounters as
select distinct on (vpi.id_encounter)
	ce.id as id_encounter,
	ce.id_location as id_location,
	ce.id_provider as id_provider,
	vpi.id_patient as id_patient,
	_(et.description) as type
from
	(clin_encounter ce inner join v_patient_items vpi on (ce.id=vpi.id_encounter)),
	_enum_encounter_type et
where
	et.id=ce.id_type
;

-- ==========================================================
\unset ON_ERROR_STOP
drop view v_test_result;
\set ON_ERROR_STOP 1

create view v_test_result as
	select
		tr.id as id_result,
		vpep.id_patient as id_patient,
		vpep.id_health_issue as id_health_issue,
		tr.id_episode as id_episode,
		tr.id_encounter as id_encounter,
		tr.id_type as id_type,
		tr.val_when as result_when,
		tt.code as test_code,
		tt.name as test_name,
		tr.val_num as value_num,
		tr.val_alpha as value_alpha,
		tr.val_unit as value_unit,
		tr.technically_abnormal as technically_abnormal,
		tr.val_normal_min as normal_min,
		tr.val_normal_max as normal_max,
		tr.val_normal_range as normal_range,
		tr.note_provider as comment_provider,
		tr.reviewed_by_clinician as seen_by_doc,
		tr.id_clinician as id_doc_seen,
		tr.clinically_relevant as clinically_relevant,
		tr.narrative as comment_doc
	from
		test_result tr,
		test_type tt,
		v_patient_episodes vpep
	where
		tr.id_type = tt.id
			AND
		tr.id_episode = vpep.id_episode
;

-- ==========================================================
\unset ON_ERROR_STOP
drop view v_lab_result;
\set ON_ERROR_STOP 1

create view v_lab_result as
	select
		lr.id as id_lab_result,
		vtr.*,
		lr.sample_id,
		lr.abnormal_tag,
		lr.id_sampler,
		tt.id_provider as id_lab
	from
		lab_result lr,
		v_test_result vtr,
		test_type tt
	where
		lr.id_result = vtr.id_result
			AND
		vtr.id_type = tt.id
;
-- ==========================================================
-- health issues stuff
\unset ON_ERROR_STOP
drop trigger TR_h_issues_modified on clin_health_issue;
drop function F_announce_h_issue_mod();
\set ON_ERROR_STOP 1

create function F_announce_h_issue_mod() returns opaque as '
declare
	patient_id integer;
begin
	-- get patient ID
	if TG_OP = ''DELETE'' then
		patient_id := OLD.id_patient;
	else
		patient_id := NEW.id_patient;
	end if;
	-- now, execute() the NOTIFY
	execute ''notify "health_issue_change_db:'' || patient_id || ''"'';
	return NULL;
end;
' language 'plpgsql';

create trigger TR_h_issues_modified
	after insert or delete or update
	on clin_health_issue
	for each row
		execute procedure F_announce_h_issue_mod()
;

-- ==========================================================
-- allergy stuff
\unset ON_ERROR_STOP
drop trigger TR_allergy_add_del on allergy;
drop function F_announce_allergy_add_del();
\set ON_ERROR_STOP 1

create function F_announce_allergy_add_del() returns opaque as '
declare
	episode_id integer;
	patient_id integer;
begin
	-- get episode ID
	if TG_OP = ''INSERT'' then
		episode_id := NEW.id_episode;
	else
		episode_id := OLD.id_episode;
	end if;
	-- track back to patient ID
	select into patient_id id_patient
		from v_patient_episodes vpep
		where vpep.id_episode = episode_id
		limit 1;
	-- now, execute() the NOTIFY
	execute ''notify "allergy_add_del_db:'' || patient_id || ''"'';
	return NULL;
end;
' language 'plpgsql';

create trigger TR_allergy_add_del
	after insert or delete
	on allergy
	for each row
		execute procedure F_announce_allergy_add_del()
;
-- should really be "for each statement" but that isn't supported yet by PostgreSQL
-- or maybe not since then we won't be able to separate affected patients in UPDATEs

\unset ON_ERROR_STOP
drop view v_i18n_patient_allergies;
\set ON_ERROR_STOP 1

create view v_i18n_patient_allergies as
select
	a.id as id,
	a.pk_item as id_item,
	vpep.id_patient as id_patient,
	vpep.id_health_issue as id_health_issue,
	a.id_episode as id_episode,
	a.id_encounter as id_encounter,
	a.substance as substance,
	a.substance_code as substance_code,
	a.generics as generics,
	a.allergene as allergene,
	a.atc_code as atc_code,
	a.reaction as reaction,
	a.generic_specific as generic_specific,
	a.definite as definite,
	a.id_type as id_type,
	_(at.value) as type,
	a.narrative as "comment"
from
	allergy a,
	_enum_allergy_type at,
	v_patient_episodes vpep
where
	vpep.id_episode=a.id_episode
		and
	at.id=a.id_type
;

-- ==========================================================
-- current encounter stuff
\unset ON_ERROR_STOP
drop trigger at_curr_encounter_ins on curr_encounter;
drop function f_curr_encounter_force_ins();

drop trigger at_curr_encounter_upd on curr_encounter;
drop function f_curr_encounter_force_upd();
\set ON_ERROR_STOP 1

create function f_curr_encounter_force_ins() returns opaque as '
begin
	NEW.started := CURRENT_TIMESTAMP;
	NEW.last_affirmed := CURRENT_TIMESTAMP;
	return NEW;
end;
' language 'plpgsql';

create trigger at_curr_encounter_ins
	before insert on curr_encounter
	for each row execute procedure f_curr_encounter_force_ins()
;
-- should really be "for each statement" but that isn't supported yet by PostgreSQL

create function f_curr_encounter_force_upd() returns opaque as '
begin
	NEW.id_patient := OLD.id_patient;
	NEW.id_encounter := OLD.id_encounter;
	NEW.started := OLD.started;
	NEW.last_affirmed := CURRENT_TIMESTAMP;
	return NEW;
end;
' language 'plpgsql';

create trigger at_curr_encounter_upd
	before update on curr_encounter
	for each row execute procedure f_curr_encounter_force_upd()
;
-- should really be "for each statement" but that isn't supported yet by PostgreSQL

-- =============================================
GRANT SELECT ON
	"v_i18n_enum_encounter_type",
	"v_patient_episodes",
	"v_patient_items",
	"v_i18n_patient_encounters",
	"v_i18n_patient_allergies"
TO GROUP "gm-doctors";

GRANT SELECT, INSERT, UPDATE, DELETE ON
	"v_i18n_enum_encounter_type",
	"v_patient_episodes",
	"v_patient_items",
	"v_i18n_patient_encounters",
	"v_i18n_patient_allergies"
TO GROUP "_gm-doctors";

-- =============================================
-- do simple schema revision tracking
\unset ON_ERROR_STOP
delete from gm_schema_revision where filename='$RCSfile: gmClinicalViews.sql,v $';
\set ON_ERROR_STOP 1

INSERT INTO gm_schema_revision (filename, version) VALUES('$RCSfile: gmClinicalViews.sql,v $', '$Revision: 1.23 $');

-- =============================================
-- $Log: gmClinicalViews.sql,v $
-- Revision 1.23  2003-08-03 14:06:45  ncq
-- - added measurements views
--
-- Revision 1.22  2003/07/19 20:23:47  ncq
-- - add clin_root_item triggers
-- - modify NOTIFY triggers so they include the patient ID
--   as per Ian's suggestion
--
-- Revision 1.21  2003/07/09 16:23:21  ncq
-- - add clin_health_issue triggers and functions
--
-- Revision 1.20  2003/06/29 15:24:22  ncq
-- - now clin_root_item inherits from audit_fields we can add
--    extract(epoch from modified_when) as age
--   to v_patient_items and order by that :-)
--
-- Revision 1.19  2003/06/22 16:23:35  ncq
-- - curr_encounter tracking triggers + grants
--
-- Revision 1.18  2003/06/03 13:49:06  ncq
-- - reorder v_patient_episodes/*_items for clarity
--
-- Revision 1.17  2003/06/01 11:38:12  ncq
-- - fix spelling of definate -> definite
--
-- Revision 1.16  2003/05/17 18:40:24  ncq
-- - notify triggers should come last, so make them zz*
--
-- Revision 1.15  2003/05/14 22:07:13  ncq
-- - adapt to changes in gmclinical.sql, particularly the narrative/item merge
--
-- Revision 1.14  2003/05/12 12:43:39  ncq
-- - gmI18N, gmServices and gmSchemaRevision are imported globally at the
--   database level now, don't include them in individual schema file anymore
--
-- Revision 1.13  2003/05/06 13:06:25  ncq
-- - pkey_ -> pk_
--
-- Revision 1.12  2003/05/05 11:59:50  ncq
-- - adapt to clin_narrative being an ancestor table
--
-- Revision 1.11  2003/05/05 00:31:28  ncq
-- - add grants
--
-- Revision 1.10  2003/05/05 00:27:34  ncq
-- - add as to encounter types
--
-- Revision 1.9  2003/05/05 00:19:12  ncq
-- - we do need the v_i18n_ on encounter types
--
-- Revision 1.8  2003/05/04 23:35:59  ncq
-- - major reworking to follow the formal EMR structure writeup
--
-- Revision 1.7  2003/05/03 00:44:05  ncq
-- - make patient allergies view work
--
-- Revision 1.6  2003/05/02 15:06:19  ncq
-- - make trigger return happy
-- - tweak v_i18n_patient_allergies - not done yet
--
-- Revision 1.5  2003/05/01 15:05:36  ncq
-- - function/trigger to announce insertion/deletion of allergy
-- - allergy.id_substance -> allergy.substance_code
--
-- Revision 1.4  2003/04/30 23:30:29  ncq
-- - v_i18n_patient_allergies
-- - new_allergy -> allergy_new
--
-- Revision 1.3  2003/04/29 12:34:54  ncq
-- - added more views + grants
--
-- Revision 1.2  2003/04/28 21:39:49  ncq
-- - cleanups and GRANTs
--
-- Revision 1.1  2003/04/28 20:40:48  ncq
-- - this can safely be dropped and recreated even with data in the tables
--
