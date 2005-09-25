-- project: GNUMed
-- database GIS - spanish counties, according to National Institute of Statistics (http://www.ine.es)

-- ===================================================================
-- $Source: /home/ncq/Projekte/cvs2git/vcs-mirror/gnumed/gnumed/server/sql/country.specific/es/gmDemographics-Data.es.sql,v $
-- $Id: gmDemographics-Data.es.sql,v 1.5 2005-09-25 17:52:45 ncq Exp $
-- author: Carlos Moro
-- license: GPL

-- ===================================================================
-- force terminate + exit(3) on errors if non-interactive
\set ON_ERROR_STOP 1

set client_encoding to 'LATIN1';
-- ===================================================================
select i18n_upd_tx('es_ES', 'Spain', 'Espa�a');

-- Carlos, please reconcile:
--INSERT INTO state(code, country, name) VALUES ('AN','ES',i18n('Andalusia'));
--INSERT INTO state(code, country, name) VALUES ('AR','ES',i18n('Aragon'));
--INSERT INTO state(code, country, name) VALUES ('AS','ES',i18n('Asturias'));
--INSERT INTO state(code, country, name) VALUES ('BI','ES',i18n('Balearic Islands'));
--INSERT INTO state(code, country, name) VALUES ('BC','ES',i18n('Basque Country'));
--INSERT INTO state(code, country, name) VALUES ('CI','ES',i18n('Canary Islands'));
--INSERT INTO state(code, country, name) VALUES ('CA','ES',i18n('Cantabria'));
--INSERT INTO state(code, country, name) VALUES ('CL','ES',i18n('Castilla y Leon'));
--INSERT INTO state(code, country, name) VALUES ('CM','ES',i18n('Castilla-La Mancha'));
--INSERT INTO state(code, country, name) VALUES ('CT','ES',i18n('Catalonia'));
--INSERT INTO state(code, country, name) VALUES ('EX','ES',i18n('Extremadura'));
--INSERT INTO state(code, country, name) VALUES ('GA','ES',i18n('Galicia'));
--INSERT INTO state(code, country, name) VALUES ('LR','ES',i18n('La Rioja'));
--INSERT INTO state(code, country, name) VALUES ('MA','ES',i18n('Madrid'));
--INSERT INTO state(code, country, name) VALUES ('MU','ES',i18n('Murcia'));
--INSERT INTO state(code, country, name) VALUES ('NA','ES',i18n('Navarre'));
--INSERT INTO state(code, country, name) VALUES ('VA','ES',i18n('Valencia'));

-- spanish geographic information (mostly of type 'state')
INSERT INTO state(code,country,name) VALUES ('01','ES',i18n('�lava'));
INSERT INTO state(code,country,name) VALUES ('02','ES',i18n('Albacete'));
INSERT INTO state(code,country,name) VALUES ('03','ES',i18n('Alicante'));
INSERT INTO state(code,country,name) VALUES ('04','ES',i18n('Almer�a'));
INSERT INTO state(code,country,name) VALUES ('33','ES',i18n('Asturias'));
INSERT INTO state(code,country,name) VALUES ('05','ES',i18n('�vila'));
INSERT INTO state(code,country,name) VALUES ('06','ES',i18n('Badajoz'));
INSERT INTO state(code,country,name) VALUES ('07','ES',i18n('Baleares'));
INSERT INTO state(code,country,name) VALUES ('08','ES',i18n('Barcelona'));
INSERT INTO state(code,country,name) VALUES ('09','ES',i18n('Burgos'));
INSERT INTO state(code,country,name) VALUES ('10','ES',i18n('C�ceres'));
INSERT INTO state(code,country,name) VALUES ('11','ES',i18n('C�diz'));
INSERT INTO state(code,country,name) VALUES ('12','ES',i18n('Castell�n'));
INSERT INTO state(code,country,name) VALUES ('13','ES',i18n('Ciudad Real'));
INSERT INTO state(code,country,name) VALUES ('14','ES',i18n('C�rdoba'));
INSERT INTO state(code,country,name) VALUES ('15','ES',i18n('Coru�a'));
INSERT INTO state(code,country,name) VALUES ('16','ES',i18n('Cuenca'));
INSERT INTO state(code,country,name) VALUES ('17','ES',i18n('Gerona'));
INSERT INTO state(code,country,name) VALUES ('18','ES',i18n('Granada'));
INSERT INTO state(code,country,name) VALUES ('19','ES',i18n('Guadalajara'));
INSERT INTO state(code,country,name) VALUES ('20','ES',i18n('Guip�zcoa'));
INSERT INTO state(code,country,name) VALUES ('21','ES',i18n('Huelva'));
INSERT INTO state(code,country,name) VALUES ('22','ES',i18n('Huesca'));
INSERT INTO state(code,country,name) VALUES ('23','ES',i18n('Ja�n'));
INSERT INTO state(code,country,name) VALUES ('24','ES',i18n('Le�n'));
INSERT INTO state(code,country,name) VALUES ('25','ES',i18n('L�rida'));
INSERT INTO state(code,country,name) VALUES ('27','ES',i18n('Lugo'));
INSERT INTO state(code,country,name) VALUES ('28','ES',i18n('Madrid'));
INSERT INTO state(code,country,name) VALUES ('29','ES',i18n('M�laga'));
INSERT INTO state(code,country,name) VALUES ('30','ES',i18n('Murcia'));
INSERT INTO state(code,country,name) VALUES ('31','ES',i18n('Navarra'));
INSERT INTO state(code,country,name) VALUES ('32','ES',i18n('Orense'));
INSERT INTO state(code,country,name) VALUES ('34','ES',i18n('Palencia'));
INSERT INTO state(code,country,name) VALUES ('35','ES',i18n('Palmas (Las)'));
INSERT INTO state(code,country,name) VALUES ('36','ES',i18n('Pontevedra'));
INSERT INTO state(code,country,name) VALUES ('26','ES',i18n('Rioja (La)'));
INSERT INTO state(code,country,name) VALUES ('37','ES',i18n('Salamanca'));
INSERT INTO state(code,country,name) VALUES ('38','ES',i18n('Santa Cruz de Tenerife'));
INSERT INTO state(code,country,name) VALUES ('40','ES',i18n('Segovia'));
INSERT INTO state(code,country,name) VALUES ('41','ES',i18n('Sevilla'));
INSERT INTO state(code,country,name) VALUES ('42','ES',i18n('Soria'));
INSERT INTO state(code,country,name) VALUES ('43','ES',i18n('Tarragona'));
INSERT INTO state(code,country,name) VALUES ('44','ES',i18n('Teruel'));
INSERT INTO state(code,country,name) VALUES ('45','ES',i18n('Toledo'));
INSERT INTO state(code,country,name) VALUES ('46','ES',i18n('Valencia'));
INSERT INTO state(code,country,name) VALUES ('47','ES',i18n('Valladolid'));
INSERT INTO state(code,country,name) VALUES ('48','ES',i18n('Vizcaya'));
INSERT INTO state(code,country,name) VALUES ('49','ES',i18n('Zamora'));
INSERT INTO state(code,country,name) VALUES ('50','ES',i18n('Zaragoza'));

select gm_upd_default_states();

-- ===================================================================
-- do simple revision tracking
delete from gm_schema_revision where filename = '$RCSfile: gmDemographics-Data.es.sql,v $';
INSERT INTO gm_schema_revision (filename, version) VALUES ('$RCSfile: gmDemographics-Data.es.sql,v $', '$Revision: 1.5 $');

-- ===================================================================
-- $Log: gmDemographics-Data.es.sql,v $
-- Revision 1.5  2005-09-25 17:52:45  ncq
-- - carlos needs to take a look, his data and the data from Jim's file
--   are different
--
-- Revision 1.4  2005/09/19 16:27:05  ncq
-- - update default states
--
-- Revision 1.3  2005/07/14 21:31:43  ncq
-- - partially use improved schema revision tracking
--
-- Revision 1.2  2005/06/10 07:22:53  ncq
-- - translate Spain into Spanish
--
-- Revision 1.1  2005/05/15 12:03:51  ncq
-- - Spanish counties/states
--
