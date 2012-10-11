-- ==============================================================
-- GNUmed database schema change script
--
-- License: GPL v2 or later
-- Author: karsten.hilbert@gmx.net
--
-- ==============================================================
\set ON_ERROR_STOP 1

--set default_transaction_read_only to off;
-- --------------------------------------------------------------
delete from ref.keyword_expansion where keyword = 'LMcC-GKV_Stempel-LaTeX_picture_environment';

insert into ref.keyword_expansion (
	fk_staff,
	keyword,
	textual_data
) values (
	null,
	'LMcC-GKV_Stempel-LaTeX_picture_environment',
	'%----- Stempel für LMcC ---------------
% da der Stempel in verschiedenen Forumularen an verschiedenen
% Stellen gesetzt wird, wird hier mit einem Offset gearbeitet,
% -> nur der Offset ist (im Formulartemplate !) anzupassen, z.B.:
%\stempeloffsetx=17
%\stempeloffsety=-80

\put(\stempeloffsetx,\stempeloffsety){***BSNR/LANR***}

%\advance\stempeloffsetx by 22
%\advance\stempeloffsety by 3
%\put(\stempeloffsetx,\stempeloffsety){*KV*}
%\advance\stempeloffsety by -3
%\put(\stempeloffsetx,\stempeloffsety){*Kobl-Tr*}
%\advance\stempeloffsetx by -22

\advance\stempeloffsety by -5
\put(\stempeloffsetx,\stempeloffsety){*Dr.Leonard McCoy*}

\advance\stempeloffsety by -5
\put(\stempeloffsetx,\stempeloffsety){*FA für Allgemeinmedizin*}

\advance\stempeloffsety by -5
\put(\stempeloffsetx,\stempeloffsety){*Am Sternentor 17*}

\advance\stempeloffsety by -5
\put(\stempeloffsetx,\stempeloffsety){*94413 Houston*}
%----- Stempel ---------------
'
);

-- --------------------------------------------------------------
select gm.log_script_insertion('v18-LMcC_GKV_Stempel.sql', '18.0');
