v-- structure of drug database for gnumed
-- Copyright 2000, 2001 by Dr. Horst Herb
-- This is free software in the sense of the General Public License (GPL)
-- For details regarding GPL licensing see http://gnu.org
--
-- usage:
--	log into psql (database gnumed OR drugs)  as administrator
--	run the script from the prompt with "\i drugs.sql"
--
-- changelog: 20.10.01 (suggestions by Ian Haywood)
--		+ hierarchy of substance categories
--		+ drug-drug interactions removed 
-- (already have substance interactions)
--		+ therapeutic categories replaced by clinical guidelines
-- changelog: 13.10.2001
--		+ stripped down from original database
--		+ all references to gnumed_object removed
--		+ prepared for distributed servers & read-only database
--		+ prescription module separated from drug module
--		+ all permissions, triggers and rules removed
--		+ stripped all use of inheritance in favour of portability
--
-- TODO:
--	* testing
--	* debugging
-- 	* further normalization
--	* trigger maintained denormalized table(s) for fast read access of most common attributes


--=====================================================================

CREATE FUNCTION plpgsql_call_handler () RETURNS OPAQUE AS
    '/usr/lib/pgsql/plpgsql.so' LANGUAGE 'C';

CREATE TRUSTED PROCEDURAL LANGUAGE 'plpgsql'
    HANDLER plpgsql_call_handler
    LANCOMPILER 'PL/pgSQL';



CREATE TABLE entity (
	id SERIAL PRIMARY KEY,
	name  varchar(60),
	class BOOL, -- true for a class of substances
	compound BOOL -- true for compound. No significance if class is true
);

-- dump file in gmdrugs.entity.sql

COMMENT ON TABLE entity IS
'Pharmacologic entity: class, compound or substance.';

CREATE VIEW drug AS SELECT id, name FROM entity WHERE not class;
-- cannot insert, as uncetain compound or sunstance
CREATE RULE drug_upd AS ON UPDATE TO drug
        DO INSTEAD
        UPDATE entity SET
               name = NEW.name
         WHERE id = OLD.id;
CREATE RULE drug_del AS ON DELETE TO drug
        DO INSTEAD
        DELETE FROM entity
         WHERE id = OLD.id;
CREATE VIEW class AS SELECT id, name FROM entity WHERE class;
CREATE RULE insert_class AS ON INSERT TO class
        DO INSTEAD INSERT INTO entity VALUES (NEW.id, NEW.name, 't', 'f');
CREATE RULE class_upd AS ON UPDATE TO class
        DO INSTEAD
        UPDATE entity SET
               name = NEW.name
         WHERE id = OLD.id;
CREATE RULE class_del AS ON DELETE TO class
        DO INSTEAD
        DELETE FROM entity
         WHERE id = OLD.id;
CREATE VIEW substance AS SELECT id, name FROM entity WHERE not class and not compound;
CREATE RULE insert_subst AS ON INSERT TO substance
        DO INSERT INTO entity VALUES (NEW.id, NEW.name, 'f', 'f');
CREATE RULE subst_upd AS ON UPDATE TO substance
        DO INSTEAD 
        UPDATE entity SET
               name = NEW.name
         WHERE id = OLD.id;
CREATE RULE subst_del AS ON DELETE TO substance
        DO INSTEAD
        DELETE FROM entity
         WHERE id = OLD.id;
CREATE VIEW compound AS SELECT id, name FROM entity WHERE not class and compound;
CREATE RULE insertcompound AS ON INSERT TO compound
        DO INSERT INTO entity VALUES (NEW.id, NEW.name, 'f', 't');
CREATE RULE compound_upd AS ON UPDATE TO compound
        DO INSTEAD
        UPDATE entity SET
               name = NEW.name
         WHERE id = OLD.id;
CREATE RULE compound_del AS ON DELETE TO compound
        DO INSTEAD
        DELETE FROM entity
         WHERE id = OLD.id;

-- =============================================

CREATE TABLE link_class (
       class INTEGER REFERENCES entity (id),
       member INTEGER REFERENCES entity (id)
);

CREATE INDEX idx_link_class1 ON link_class(class);
CREATE INDEX idx_link_class2 ON link_class(member);

-- =============================================

CREATE TABLE link_compound_substance (
       compound_id INTEGER,
       substance_id INTEGER
);


CREATE TABLE pregnancy_cat (
	id SERIAL PRIMARY KEY,
	code char(3),
	description text,
	comment text
);


CREATE TABLE breastfeeding_cat (
	id SERIAL PRIMARY KEY,
	code char(3),
	description text,
	comment text
);

CREATE TABLE obstetric_codes (
       drug_id INTEGER,
       preg_code INTEGER REFERENCES pregnancy_cat (id),
       brst_code INTEGER REFERENCES breastfeeding_cat (id)
);

-- =============================================

CREATE TABLE amount_units (
        id SERIAL PRIMARY KEY,
        description varchar(20)
);

COMMENT ON TABLE amount_units IS
'Example: ml, each, ..';


-- =============================================

CREATE TABLE drug_units (
	id SERIAL PRIMARY KEY,
	is_SI boolean default 'y',
	description varchar(20)
);

COMMENT ON COLUMN drug_units.is_SI IS
'Example: mg, mcg, ml, U, IU, ...';

COMMENT ON TABLE drug_units IS
'true if it is a System International (SI) compliant unit';


-- =============================================

CREATE TABLE drug_route (
	id SERIAL PRIMARY KEY,
	description varchar(60)
); 

COMMENT ON table drug_route IS
'Examples: oral, i.m., i.v., s.c.';



-- =============================================

CREATE TABLE presentation (
	id SERIAL PRIMARY KEY,
	name varchar (30)
);


-- =============================================
-- This describes the physical form of the drug, distingushing between liquid
-- and tablet types. 
-- contains special fields to extract form data from the freeform PBS field
-- 'formandstrength'
CREATE TABLE drug_form (
	id SERIAL PRIMARY KEY,
	route INTEGER REFERENCES drug_route(id),
	unit INTEGER REFERENCES drug_units(id), -- measure of active substances
	amount_unit INTEGER REFERENCES amount_units(id), 
	-- "divisor" of the unit -- "each" for tabs/capsules, most likely
	-- mL for liquid drugs, and grams for powders
	presentation INTEGER REFERENCES presentation (id)
);


-- =============================================
-- alternative to therapeutic classes, just a thought


CREATE TABLE indication (
       id SERIAL PRIMARY KEY,
       diseasecode char[8],
       drug INTEGER REFERENCES entity (id),
       route INTEGER REFERENCES drug_route (id),
       unit INTEGER REFERENCES drug_units (id),
       course INTEGER, -- in days, 1 for stat dose, 0 if continuing
       paed_dose FLOAT, -- paediatric dose, units/kg
       min_dose FLOAT, -- adult minimum dose
       max_dose FLOAT, -- adult maximum dose
       comment TEXT,
       line INTEGER -- 1=first-line, 2=second-line, etc.
);

-- with this table, a list of indicated drugs would appear in a sidebox
-- when a diagnosis was entered, with interacting/contraindicated/allergic
-- drugs removed a priori. The prescriber could click on one to these to
-- bring up the prescription dialogue, pre-loaded with the drug.
-- paediatric dosing can be automatically calculated.		          

-- =============================================
-- This table corresponds to each line in the Yellow Book.
-- The manufacturer is linked to the strengths and pack sizes that they offer.
CREATE TABLE drug_package (
	id SERIAL PRIMARY KEY,
	form_id INTEGER REFERENCES drug_form(id),
	drug_id INTEGER REFERENCES entity (id),
	amount INTEGER, -- no. of tabs, capsules, etc. in pack
	max_rpts INTEGER, -- maximum repeats
	strength FLOAT -- amount of active in each tab, capsule
);

-- =============================================
-- Commercial data. Ugh!

CREATE TABLE drug_manufacturer (
	id SERIAL PRIMARY KEY,
	name varchar(60)
);

COMMENT ON TABLE drug_manufacturer IS
'Name of a drug company. Details like address etc. in separate table';

CREATE TABLE brand (
	id SERIAL PRIMARY KEY,
	drug_manufacturer_id INTEGER NOT NULL references drug_manufacturer(id),
        brand_name varchar(60)
);

CREATE TABLE link_brand_drug (
       brand_id INTEGER REFERENCES brand (id),
       drug_id INTEGER REFERENCES drug_package (id),
       price MONEY	       
);
-- =============================================
-- where does this link in?
CREATE TABLE drug_flags (
	id SERIAL PRIMARY KEY,
        description varchar(60),
        comment text
);

COMMENT ON TABLE drug_flags IS
'important searchable information relating to a drug such as sugar free, gluten free, ...';

-- sugqestion:
CREATE TABLE link_flag_preparation (
       flag_id INTEGER REFERENCES drug_flags(id),
       prep_id INTEGER REFERENCES drug_package (id)
);

-- ==============================================

CREATE TABLE pbs_authority (
       drug_id INTEGER REFERENCES entity (id),
       indication text
);

-- =============================================

CREATE TABLE drug_warning_categories (
	id SERIAL PRIMARY KEY,
        description text
);

COMMENT ON TABLE drug_warning_categories IS
'e.g. (potentially life threatening complication) (drug-disease interaction check neccessary) ...';

-- =============================================

CREATE TABLE drug_warning (
	drug_id INTEGER NOT NULL REFERENCES entity (id) ,
	drug_warning_categories_id INTEGER NOT NULL REFERENCES drug_warning_categories(id) ,
	warning text
);

COMMENT ON TABLE drug_warning IS
'allows to link searchable categories of warning messages to any drug component';

-- =============================================

CREATE TABLE severity_code (
	id SERIAL PRIMARY KEY,
	code CHAR(3),
        description text
);

COMMENT ON TABLE severity_code IS
'e.g. (contraindicated) (potentially life threatening) (not advisable) (caution) ...';


-- =============================================

-- interaction between any substance or class of substances

CREATE TABLE interaction (
       id SERIAL PRIMARY KEY,
       comment text,
       severity INTEGER REFERENCES severity_code (id)
);


-- =====================================================
CREATE TABLE link_drug_interaction (
        id SERIAL PRIMARY KEY,
	drug1_id INTEGER NOT NULL REFERENCES entity(id),
	drug2_id INTEGER NOT NULL REFERENCES entity(id),
	interaction_id INTEGER NOT NULL REFERENCES interaction (id) ,
        comment text
);


-- =============================================
CREATE TABLE link_disease_interaction (
        id SERIAL PRIMARY KEY,
	drug_id INTEGER NOT NULL REFERENCES entity (id) ,
	diseasecode char[8],
	interaction_id INTEGER NOT NULL REFERENCES interaction (id),
        comment text
);


COMMENT ON TABLE link_disease_interaction IS
'allows any number of drug-disease interactions for any given drug';

COMMENT ON COLUMN link_disease_interaction.diseasecode IS
'preferrably ICD10 codes here.';
