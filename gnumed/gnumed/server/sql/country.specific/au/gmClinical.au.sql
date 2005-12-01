-- Project: GnuMed - service "clinical" -- Australian specific stuff
-- ===================================================================
-- $Source: /home/ncq/Projekte/cvs2git/vcs-mirror/gnumed/gnumed/server/sql/country.specific/au/gmClinical.au.sql,v $
-- $Revision: 1.1 $
-- license: GPL
-- author: Ian Haywood

-- This file populates the tables in the reference service with Australian-specific content.
-- ===================================================================
-- force terminate + exit(3) on errors if non-interactive
\set ON_ERROR_STOP 1

-- ===================================================================
create schema au authorization "gm-dbo";

-- =============================================
--create table au.referral (
--	id serial primary key,
--	fk_referee integer
--		not null
--		references clin.xlnk_identity(xfk_identity)
--		on update cascade
--		on delete restrict,
--	fk_form integer
--		not null
--		references clin.form_instances (pk)
--) inherits (clin.clin_root_item);

--alter table au.referral add foreign key (fk_encounter)
--		references clin.clin_encounter(id)
--		on update cascade
--		on delete restrict;
--alter table au.referral add foreign key (fk_episode)
--		references clin.clin_episode(pk)
--		on update cascade
--		on delete restrict;

--select add_table_for_audit ('au', 'referral');

--comment on table au.referral is 'table for referrals to defined individuals';
--comment on column au.referral.fk_referee is 'person to whom the referral is directed';
--comment on column au.referral.narrative is
--	'inherited from clin.clin_root_item;
--	 stores text of referral letter';
--comment on column au.referral.fk_form is 'foreign key to the form instance of
--this referral.';

-- ===================================================================
-- $Log: gmClinical.au.sql,v $
-- Revision 1.1  2005-12-01 16:46:50  ncq
-- - added schema "au"
--
--
