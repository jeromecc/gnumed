-- Projekt GNUmed
-- Impfkalender der STIKO (Deutschland)

-- Quellen:
-- Kinder�rztliche Praxis (2002)
-- Sonderheft "Impfen 2002"
-- Kirchheim-Verlag Mainz

-- author: Karsten Hilbert <Karsten.Hilbert@gmx.net>
-- license: GPL v2 or later
-- $Source: /home/ncq/Projekte/cvs2git/vcs-mirror/gnumed/gnumed/server/sql/country.specific/de/STIKO-Impfkalender.sql,v $
-- $Revision: 1.20 $
-- =============================================
-- force terminate + exit(3) on errors if non-interactive
\set ON_ERROR_STOP 1

set client_encoding to 'latin1';
-- =============================================
delete from clin.vaccination_schedule where name like '%(STIKO)%';
delete from clin.vaccination_course where fk_recommended_by = (select pk from ref_source where name_short='STIKO');

-- FIXME: we currently assume that the services [reference]
-- and [historica] reside in the same database (see fk_recommended_by)
delete from ref_source where name_short = 'STIKO';
insert into ref_source (
	name_short,
	name_long,
	version,
	description,
	source
) values (
	'STIKO',
	'St�ndige Impfkommission, Robert-Koch-Institut',
	'Juli 2002',
	'Standardimpfungen f�r S�uglinge, Kinder, Jugendliche und Erwachsene',
	'"Kinder�rztliche Praxis" (2002), Sonderheft "Impfen 2002", Kirchheim-Verlag Mainz'
);

------------
-- Masern --
------------
-- Impfplan definieren
insert into clin.vaccination_course
	(fk_recommended_by, fk_indication)
values (
	currval('ref_source_pk_seq'),
	(select id from clin.vacc_indication where description='measles')
);

-- Impfzeitpunkte festlegen
insert into clin.vaccination_definition
	(fk_course, seq_no, min_age_due, max_age_due)
values (
	currval('clin.vaccination_course_pk_seq'),
	1,
	'11 months'::interval,
	'14 months'::interval
);

insert into clin.vaccination_definition
	(fk_course, seq_no, min_age_due, max_age_due, min_interval)
values (
	currval('clin.vaccination_course_pk_seq'),
	2,
	'15 months'::interval,
	'23 months'::interval,
	'4 weeks'::interval
);

-----------
-- Mumps --
-----------
-- Impfplan definieren
insert into clin.vaccination_course
	(fk_recommended_by, fk_indication)
values (
	currval('ref_source_pk_seq'),
	(select id from clin.vacc_indication where description='mumps')
);

-- Impfzeitpunkte festlegen
insert into clin.vaccination_definition
	(fk_course, seq_no, min_age_due, max_age_due)
values (
	currval('clin.vaccination_course_pk_seq'),
	1,
	'11 months'::interval,
	'14 months'::interval
);

insert into clin.vaccination_definition
	(fk_course, seq_no, min_age_due, max_age_due, min_interval)
values (
	currval('clin.vaccination_course_pk_seq'),
	2,
	'15 months'::interval,
	'23 months'::interval,
	'4 weeks'::interval
);

------------
-- R�teln --
------------
-- Impfplan definieren
insert into clin.vaccination_course
	(fk_recommended_by, fk_indication)
values (
	currval('ref_source_pk_seq'),
	(select id from clin.vacc_indication where description='rubella')
);

-- Impfzeitpunkte festlegen
insert into clin.vaccination_definition
	(fk_course, seq_no, min_age_due, max_age_due)
values (
	currval('clin.vaccination_course_pk_seq'),
	1,
	'11 months'::interval,
	'14 months'::interval
);

insert into clin.vaccination_definition
	(fk_course, seq_no, min_age_due, max_age_due, min_interval)
values (
	currval('clin.vaccination_course_pk_seq'),
	2,
	'15 months'::interval,
	'23 months'::interval,
	'4 weeks'::interval
);

------------------
-- MMR-Schedule --
------------------
insert into clin.vaccination_schedule (name, comment) values (
	'MMR (STIKO)',
	'Mindestabstand zwischen 2 Impfungen: 4 Wochen'
);

-- Masern
insert into clin.lnk_vaccination_course2schedule (fk_course, fk_schedule) values (
	(select pk_course from clin.v_vaccination_courses where indication = 'measles' and recommended_by_name_short = 'STIKO'),
	(select pk from clin.vaccination_schedule where name = 'MMR (STIKO)')
);
-- Mumps
insert into clin.lnk_vaccination_course2schedule (fk_course, fk_schedule) values (
	(select pk_course from clin.v_vaccination_courses where indication = 'mumps' and recommended_by_name_short = 'STIKO'),
	(select pk from clin.vaccination_schedule where name = 'MMR (STIKO)')
);
-- R�teln
insert into clin.lnk_vaccination_course2schedule (fk_course, fk_schedule) values (
	(select pk_course from clin.v_vaccination_courses where indication = 'rubella' and recommended_by_name_short = 'STIKO'),
	(select pk from clin.vaccination_schedule where name = 'MMR (STIKO)')
);

-------------
-- Tetanus --
-------------
-- Impfplan definieren
insert into clin.vaccination_course
	(fk_recommended_by, fk_indication)
values (
	currval('ref_source_pk_seq'),
	(select id from clin.vacc_indication where description='tetanus')
);

-- Impfzeitpunkte festlegen
insert into clin.vaccination_definition
	(fk_course, seq_no, min_age_due, max_age_due)
values (
	currval('clin.vaccination_course_pk_seq'),
	1,
	'2 months'::interval,
	'2 months'::interval
);

insert into clin.vaccination_definition
	(fk_course, seq_no, min_age_due, max_age_due, min_interval)
values (
	currval('clin.vaccination_course_pk_seq'),
	2,
	'3 months'::interval,
	'3 months'::interval,
	'4 weeks'::interval
);

insert into clin.vaccination_definition
	(fk_course, seq_no, min_age_due, max_age_due, min_interval)
values
	(currval('clin.vaccination_course_pk_seq'), 3, '4 months'::interval, '4 months'::interval, '4 weeks'::interval);

insert into clin.vaccination_definition
	(fk_course, seq_no, min_age_due, max_age_due, min_interval)
values
	(currval('clin.vaccination_course_pk_seq'), 4, '11 months'::interval, '14 months'::interval, '4 weeks'::interval);

insert into clin.vaccination_definition
	(fk_course, seq_no, min_age_due, max_age_due, min_interval)
values
	(currval('clin.vaccination_course_pk_seq'), 5, '4 years'::interval, '5 years'::interval, '4 weeks'::interval);

insert into clin.vaccination_definition
	(fk_course, seq_no, min_age_due, max_age_due, min_interval)
values
	(currval('clin.vaccination_course_pk_seq'), 6, '9 years'::interval, '17 years'::interval, '4 weeks'::interval);

insert into clin.vaccination_definition
	(fk_course, seq_no, min_age_due, max_age_due, is_booster, min_interval, comment)
values (
	currval('clin.vaccination_course_pk_seq'),
	null,
	'5 years'::interval,
	'10 years'::interval,
	true,
	'10 years'::interval,
	'nach 10 Jahren falls keine Verletzung, nach 7 Jahren bei kleinen Verletzungen, bei gro�en Verletzungen nach 5 Jahren'
);

----------------
-- Diphtherie --
----------------
-- Impfplan definieren
insert into clin.vaccination_course
	(fk_recommended_by, fk_indication)
values (
	currval('ref_source_pk_seq'),
	(select id from clin.vacc_indication where description='diphtheria')
);

-- Impfzeitpunkte festlegen
insert into clin.vaccination_definition
	(fk_course, seq_no, min_age_due, max_age_due)
values
	(currval('clin.vaccination_course_pk_seq'), 1, '2 months'::interval, '2 months'::interval);

insert into clin.vaccination_definition
	(fk_course, seq_no, min_age_due, max_age_due, min_interval)
values
	(currval('clin.vaccination_course_pk_seq'), 2, '3 months'::interval, '3 months'::interval, '4 weeks'::interval);

insert into clin.vaccination_definition
	(fk_course, seq_no, min_age_due, max_age_due, min_interval)
values
	(currval('clin.vaccination_course_pk_seq'), 3, '4 months'::interval, '4 months'::interval, '4 weeks'::interval);

insert into clin.vaccination_definition
	(fk_course, seq_no, min_age_due, max_age_due, min_interval)
values
	(currval('clin.vaccination_course_pk_seq'), 4, '11 months'::interval, '14 months'::interval, '4 weeks'::interval);

insert into clin.vaccination_definition
	(fk_course, seq_no, min_age_due, max_age_due, min_interval)
values
	(currval('clin.vaccination_course_pk_seq'), 5, '4 years'::interval, '5 years'::interval, '4 weeks'::interval);

insert into clin.vaccination_definition
	(fk_course, seq_no, min_age_due, max_age_due, min_interval, comment)
values (
	currval('clin.vaccination_course_pk_seq'),
	6,
	'9 years'::interval,
	'17 years'::interval,
	'4 weeks'::interval,
	'Impfstoff mit reduziertem Toxoidgehalt (d) verwenden !'
);

insert into clin.vaccination_definition
	(fk_course, seq_no, min_age_due, max_age_due, is_booster, min_interval, comment)
values (
	currval('clin.vaccination_course_pk_seq'),
	null,
	'5 years'::interval,
	'10 years'::interval,
	true,
	'10 years'::interval,
	'Impfstoff mit reduziertem Toxoidgehalt (d) verwenden !'
);

---------------
-- Pertussis --
---------------
-- Impfplan definieren
insert into clin.vaccination_course
	(fk_recommended_by, fk_indication)
values (
	currval('ref_source_pk_seq'),
	(select id from clin.vacc_indication where description='pertussis')
);

-- Impfzeitpunkte festlegen
insert into clin.vaccination_definition
	(fk_course, seq_no, min_age_due, max_age_due)
values
	(currval('clin.vaccination_course_pk_seq'), 1, '2 months'::interval, '2 months'::interval);

insert into clin.vaccination_definition
	(fk_course, seq_no, min_age_due, max_age_due, min_interval)
values
	(currval('clin.vaccination_course_pk_seq'), 2, '3 months'::interval, '3 months'::interval, '4 weeks'::interval);

insert into clin.vaccination_definition
	(fk_course, seq_no, min_age_due, max_age_due, min_interval)
values
	(currval('clin.vaccination_course_pk_seq'), 3, '4 months'::interval, '4 months'::interval, '4 weeks'::interval);

insert into clin.vaccination_definition
	(fk_course, seq_no, min_age_due, max_age_due, min_interval)
values
	(currval('clin.vaccination_course_pk_seq'), 4, '11 months'::interval, '14 months'::interval, '4 weeks'::interval);

insert into clin.vaccination_definition
	(fk_course, seq_no, min_age_due, max_age_due, min_interval)
values (
	currval('clin.vaccination_course_pk_seq'),
	5,
	'9 years'::interval,
	'17 years'::interval,
	'5 years'::interval
);

---------
-- HiB --
---------
-- Impfplan definieren
insert into clin.vaccination_course
	(fk_recommended_by, fk_indication, comment)
values (
	currval('ref_source_pk_seq'),
	(select id from clin.vacc_indication where description='haemophilus influenzae b'),
	'falls Mehrfachimpfstoff mit Pertussis (aP), dann Schema wie DTaP/Dt/Td anwenden'
);

-- Impfzeitpunkte festlegen
insert into clin.vaccination_definition
	(fk_course, seq_no, min_age_due, max_age_due)
values (
	currval('clin.vaccination_course_pk_seq'),
	1,
	'2 months'::interval,
	'2 months'::interval
);

insert into clin.vaccination_definition
	(fk_course, seq_no, min_age_due, max_age_due, min_interval)
values (
	currval('clin.vaccination_course_pk_seq'),
	2,
	'4 months'::interval,
	'4 months'::interval,
	'4 weeks'::interval
);

insert into clin.vaccination_definition
	(fk_course, seq_no, min_age_due, max_age_due, min_interval)
values (
	currval('clin.vaccination_course_pk_seq'),
	3,
	'11 months'::interval,
	'14 months'::interval,
	'4 weeks'::interval
);

----------
-- HepB --
----------
-- Impfplan definieren
insert into clin.vaccination_course
	(fk_recommended_by, fk_indication, comment)
values (
	currval('ref_source_pk_seq'),
	(select id from clin.vacc_indication where description='hepatitis B'),
	'falls Mehrfachimpfstoff mit Pertussis (aP), dann Schema wie DTaP/Dt/Td anwenden,
	 fehlende Grundimmunisierung/Komplettierung zwischen 9 und 17 Jahren'
);

-- Impfzeitpunkte festlegen
insert into clin.vaccination_definition
	(fk_course, seq_no, min_age_due, max_age_due)
values (
	currval('clin.vaccination_course_pk_seq'),
	1,
	'2 months'::interval,
	'2 months'::interval
);

insert into clin.vaccination_definition
	(fk_course, seq_no, min_age_due, max_age_due, min_interval)
values (
	currval('clin.vaccination_course_pk_seq'),
	2,
	'4 months'::interval,
	'4 months'::interval,
	'4 weeks'::interval
);

insert into clin.vaccination_definition
	(fk_course, seq_no, min_age_due, max_age_due, min_interval)
values (
	currval('clin.vaccination_course_pk_seq'),
	3,
	'11 months'::interval,
	'14 months'::interval,
	'4 weeks'::interval
);

-----------
-- Polio --
-----------
-- Impfplan definieren
insert into clin.vaccination_course
	(fk_recommended_by, fk_indication, comment)
values (
	currval('ref_source_pk_seq'),
	(select id from clin.vacc_indication where description='poliomyelitis'),
	'falls Mehrfachimpfstoff mit Pertussis (aP), dann Schema wie DTaP/Dt/Td anwenden'
);

-- Impfzeitpunkte festlegen
insert into clin.vaccination_definition
	(fk_course, seq_no, min_age_due, max_age_due)
values (
	currval('clin.vaccination_course_pk_seq'),
	1,
	'2 months'::interval,
	'2 months'::interval
);

insert into clin.vaccination_definition
	(fk_course, seq_no, min_age_due, max_age_due, min_interval)
values (
	currval('clin.vaccination_course_pk_seq'),
	2,
	'4 months'::interval,
	'4 months'::interval,
	'4 weeks'::interval
);

insert into clin.vaccination_definition
	(fk_course, seq_no, min_age_due, max_age_due, min_interval)
values (
	currval('clin.vaccination_course_pk_seq'),
	3,
	'11 months'::interval,
	'14 months'::interval,
	'4 weeks'::interval
);

insert into clin.vaccination_definition
	(fk_course, seq_no, min_age_due, max_age_due, min_interval)
values (
	currval('clin.vaccination_course_pk_seq'),
	4,
	'9 years'::interval,
	'17 years'::interval,
	'5 years'::interval
);

---------------
-- Influenza --
---------------
-- Impfplan definieren
insert into clin.vaccination_course
	(fk_recommended_by, fk_indication)
values (
	currval('ref_source_pk_seq'),
	(select id from clin.vacc_indication where description='influenza')
);

-- Impfzeitpunkte festlegen
insert into clin.vaccination_definition
	(fk_course, seq_no, min_age_due, comment)
values (
	currval('clin.vaccination_course_pk_seq'),
	1,
	'18 years'::interval,
	'j�hrlich neu von WHO empfohlener Impfstoff'
);

insert into clin.vaccination_definition
	(fk_course, seq_no, min_age_due, is_booster, min_interval, comment)
values (
	currval('clin.vaccination_course_pk_seq'),
	null,
	'19 years'::interval,
	true,
	'1 year'::interval,
	'j�hrlich neu von WHO empfohlener Impfstoff'
);

------------------
-- Pneumokokken --
------------------
-- Impfplan definieren (STIKO)
insert into clin.vaccination_course
	(fk_recommended_by, fk_indication, comment)
values (
	currval('ref_source_pk_seq'),
	(select id from clin.vacc_indication where description='pneumococcus'),
	'ab 18 Jahre'
);

-- Impfzeitpunkte (STIKO) festlegen
insert into clin.vaccination_definition
	(fk_course, seq_no, min_age_due, comment)
values (
	currval('clin.vaccination_course_pk_seq'),
	1,
	'18 years'::interval,
	'Polysaccharid-Impfstoff'
);

insert into clin.vaccination_definition
	(fk_course, seq_no, min_age_due, is_booster, min_interval, comment)
values (
	currval('clin.vaccination_course_pk_seq'),
	null,
	'24 years'::interval,
	true,
	'6 years'::interval,
	'Polysaccharid-Impfstoff'
);

---------------------
-- Meningokokken C --
---------------------
-- Impfplan definieren
insert into clin.vaccination_course
	(fk_recommended_by, fk_indication, comment)
values (
	currval('ref_source_pk_seq'),
	(select id from clin.vacc_indication where description='meningococcus C'),
	'2-12 Monate, Meningokokken C'
);

-- Impfzeitpunkte festlegen
insert into clin.vaccination_definition
	(fk_course, seq_no, min_age_due, max_age_due)
values (
	currval('clin.vaccination_course_pk_seq'),
	1,
	'2 months'::interval,
	'12 months'::interval
);

insert into clin.vaccination_definition
	(fk_course, seq_no, min_age_due, max_age_due, min_interval)
values (
	currval('clin.vaccination_course_pk_seq'),
	2,
	'4 months'::interval,
	'14 months'::interval,
	'2 months'::interval
);

-- Impfplan definieren
insert into clin.vaccination_course
	(fk_recommended_by, fk_indication, comment)
values (
	currval('ref_source_pk_seq'),
	(select id from clin.vacc_indication where description='meningococcus C'),
	'ab 12 Monaten, Meningokokken C'
);

-- Impfzeitpunkte festlegen
insert into clin.vaccination_definition
	(fk_course, seq_no, min_age_due)
values (
	currval('clin.vaccination_course_pk_seq'),
	1,
	'12 months'::interval
);


-- =============================================
-- do simple revision tracking
select log_script_insertion('$RCSfile: STIKO-Impfkalender.sql,v $', '$Revision: 1.20 $');

-- =============================================
-- $Log: STIKO-Impfkalender.sql,v $
-- Revision 1.20  2006-03-08 09:25:55  ncq
-- - a bunch of cleanup/rename adjustment
-- - add first aggregate schedule: MMR
--
-- Revision 1.19  2006/03/04 16:24:39  ncq
-- - adjust to table name changes
--
-- Revision 1.18  2006/01/01 20:43:14  ncq
-- - adjust to tightened constraints
--
-- Revision 1.17  2005/11/25 15:07:28  ncq
-- - create schema "clin" and move all things clinical into it
--
-- Revision 1.16  2005/09/19 16:38:52  ncq
-- - adjust to removed is_core from gm_schema_revision
--
-- Revision 1.15  2005/07/14 21:31:43  ncq
-- - partially use improved schema revision tracking
--
-- Revision 1.14  2004/10/12 11:23:31  ncq
-- - fix Polio regime being wrongly linked to HepB indication
--
-- Revision 1.13  2004/04/14 20:03:59  ncq
-- - fix check constraints on intervals
--
-- Revision 1.12  2004/04/14 13:33:04  ncq
-- - need to adjust min_interval for seq_no=1 after tightening interval checks
--
-- Revision 1.11  2004/03/18 09:58:50  ncq
-- - removed is_booster reference where is false
--
-- Revision 1.10  2003/12/29 16:01:21  uid66147
-- - use lnk_vacc2vacc_def
-- - add STIKO gmReference entry
-- - more appropriate vacc_regime.name values
-- - add HiB/HepB
--
-- Revision 1.9  2003/12/03 19:09:46  ncq
-- - NeisVac-C
--
-- Revision 1.8  2003/12/01 23:53:18  ncq
-- - delete more selectively
--
-- Revision 1.7  2003/12/01 22:22:41  ncq
-- - vastly improve strings
--
-- Revision 1.6  2003/11/26 23:19:08  ncq
-- - vacc_def now links to vacc_regime instead of vacc_indication
--
-- Revision 1.5  2003/10/31 23:30:28  ncq
-- - cleanup
--
-- Revision 1.4  2003/10/26 09:41:03  ncq
-- - truncate -> delete from
--
-- Revision 1.3  2003/10/25 16:45:19  ncq
-- - seq_id -> seq_no
--
-- Revision 1.2  2003/10/21 15:04:49  ncq
-- - update vaccination schedules for Germany
--
-- Revision 1.1  2003/10/19 15:17:41  ncq
-- - German vaccination regimes recommended by the STIKO
--
