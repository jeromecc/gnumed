-- ==============================================================
-- GNUmed database schema change script
--
-- License: GPL v2 or later
-- Author: karsten.hilbert@gmx.net
-- 
-- ==============================================================
\set ON_ERROR_STOP 1

-- --------------------------------------------------------------
ALTER DATABASE gnumed_v16
	SET datestyle to 'ISO';

ALTER DATABASE gnumed_v16
	SET default_transaction_isolation to 'read committed';

ALTER DATABASE gnumed_v16
	SET sql_inheritance to 'on';

-- --------------------------------------------------------------
select gm.log_script_insertion('v16-db-default_settings.sql', 'v16');

-- ==============================================================