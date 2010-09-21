-- ==============================================================
-- GNUmed database schema change script
--
-- License: GPL
-- Author: karsten.hilbert@gmx.net
-- 
-- ==============================================================
\set ON_ERROR_STOP 1

-- --------------------------------------------------------------
-- .end
alter table clin.procedure
	add column clin_end
		timestamp with time zone;

alter table audit.log_procedure
	add column clin_end
		timestamp with time zone;

-- --------------------------------------------------------------
select gm.log_script_insertion('v15-clin-procedure-static.sql', 'Revision: 1.1');
