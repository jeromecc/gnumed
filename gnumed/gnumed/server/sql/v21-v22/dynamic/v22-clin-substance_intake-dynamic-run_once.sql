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
-- make sure we only run this once (these should be
-- gone after a successful run):
select 1 from ref.consumable_substance;
select 1 from ref.lnk_substance2brand;
select fk_substance, preparation from clin.substance_intake limit 1;
select 1 from clin.v_nonbrand_intakes;
select 1 from clin.v_brand_intakes;
select 1 from clin.v_substance_intakes;

-- --------------------------------------------------------------
-- convert foreign keys in clin.substance_intake

-- prepare table
alter table clin.substance_intake
	drop constraint if exists substance_intake_fk_drug_component_fkey cascade;

alter table clin.substance_intake
	drop constraint if exists substance_intake_fk_substance_fkey cascade;

alter table clin.substance_intake
	alter column fk_substance
		drop not null;

alter table clin.substance_intake
	drop constraint if exists clin_subst_intake_sane_prep cascade;

drop function if exists clin.trf_upd_intake_set_substance_from_component() cascade;
drop function if exists clin.trf_update_intake_must_link_all_drug_components() cascade;
drop function if exists clin.trf_upd_intake_updates_all_drug_components() cascade;

-- create conversion function
drop function if exists _tmp_convert_substance_intakes() cascade;

create function _tmp_convert_substance_intakes()
	returns boolean
	language 'plpgsql'
	as '
DECLARE
	_intake_row record;
	_pk_dose integer;
	_pk_brand integer;
	_pk_component integer;
BEGIN
	-- update branded intakes ------------------
	raise notice ''[_tmp_convert_substance_intakes]: start'';
	raise notice ''- converting branded intakes'';
	for _intake_row in
		select * from clin.v_brand_intakes
	loop
		raise notice ''- converting [%]'', _intake_row;
		select pk_dose into strict _pk_dose from ref.v_substance_doses r_vsd where
			r_vsd.substance = _intake_row.substance
				and
			r_vsd.amount = _intake_row.amount
				and
			r_vsd.unit = _intake_row.unit
		;
		if not FOUND then
			raise exception ''[_tmp_convert_substance_intakes]: ref.dose dose not contain row for branded intake [%]'', _intake_row;
			return FALSE;
		end if;
		raise notice ''- dose PK: [%]'', _pk_dose;

		select pk into strict _pk_component from ref.lnk_dose2drug r_ld2d where
			r_ld2d.fk_dose = _pk_dose
				and
			r_ld2d.fk_brand = _intake_row.pk_brand
		;
		if not FOUND then
			raise exception ''[_tmp_convert_substance_intakes]: ref.lnk_dose2drug dose not contain row for branded intake [%]'', _intake_row;
			return FALSE;
		end if;
		raise notice ''- component PK: [%]'', _pk_component;

		raise notice ''- UPDATE of [%] [%] [%] [%] [%]'', _intake_row.brand, _intake_row.substance, _intake_row.amount, _intake_row.unit, _intake_row.preparation;
		update clin.substance_intake set
			fk_drug_component = _pk_component,
			preparation = NULL,
			fk_substance = NULL
		where
			pk = _intake_row.pk_substance_intake
		;
	end loop;

	-- update generic intakes --------------------
	raise notice ''- converting generic intakes'';
	for _intake_row in
		select * from clin.v_nonbrand_intakes
	loop
		raise notice ''- converting [%]'', _intake_row;
		-- check for generic brand
		select pk_brand into _pk_brand from ref._tmp_v_branded_drugs r_tvbd where
			r_tvbd.brand = _intake_row.substance
				and
			r_tvbd.is_fake_brand is TRUE
				and
			r_tvbd.preparation = _intake_row.preparation
				and
			_intake_row.pk_substance = ANY(r_tvbd.pk_substances)
				and
			array_ndims(r_tvbd.pk_substances) = 1
				and
			array_length(r_tvbd.pk_substances, 1) = 1
		;
		if FOUND then
			raise notice ''- generic brand found: [%]'', _pk_brand;
		else
			raise notice ''- adding generic brand for [%]'', _intake_row;
			select pk_dose into _pk_dose from ref.v_substance_doses r_vsd where
				r_vsd.amount = _intake_row.amount
					and
				r_vsd.unit = _intake_row.unit
					and
				r_vsd.substance = _intake_row.substance
			;
			if FOUND then
				raise notice ''- generic dose found: [%]'', _pk_dose;
			else
				raise notice ''- creating dose for generic brand as [%] [%] [%]'', _intake_row.pk_substance, _intake_row.amount,	_intake_row.unit;
				insert into ref.dose (
					fk_substance,
					amount,
					unit
				) values (
					_intake_row.pk_substance,
					_intake_row.amount,
					_intake_row.unit
				) returning pk into strict _pk_dose;
			end if;

			raise notice ''- creating generic brand for [%] [%] [atc=%s] [is_fake=TRUE] '', _intake_row.substance, _intake_row.preparation, coalesce(_intake_row.atc_brand::text, _intake_row.atc_substance::text, ''NULL''::text);
			insert into ref.branded_drug (
				description,
				preparation,
				atc_code,
				is_fake
			) values (
				_intake_row.substance,
				_intake_row.preparation,
				coalesce(_intake_row.atc_brand::text, _intake_row.atc_substance::text),
				TRUE
			) returning pk into strict _pk_brand;

			raise notice ''- linking generic dose [%] to generic brand [%]'', _pk_dose, _pk_brand;
			insert into ref.lnk_dose2drug (
				fk_brand,
				fk_dose
			) values (
				_pk_brand,
				_pk_dose
			);
		end if;

		select pk_dose into strict _pk_dose from ref.v_substance_doses r_vsd where
			r_vsd.substance = _intake_row.substance
				and
			r_vsd.amount = _intake_row.amount
				and
			r_vsd.unit = _intake_row.unit
		;
		if not FOUND then
			raise exception ''[_tmp_convert_substance_intakes]: ref.dose does not contain row for generic intake [%]'', _intake_row;
			return FALSE;
		end if;
		raise notice ''- dose PK: [%]'', _pk_dose;

		select pk into strict _pk_component from ref.lnk_dose2drug r_ld2d where
			r_ld2d.fk_dose = _pk_dose
				and
			r_ld2d.fk_brand = _pk_brand
		;
		if not FOUND then
			raise exception ''[_tmp_convert_substance_intakes]: ref.lnk_dose2drug dose not contain row for generic intake [%]'', _intake_row;
			return FALSE;
		end if;
		raise notice ''- component PK: [%]'', _pk_component;

		raise notice ''- UPDATE of [%] [%] [%] [%]'', _intake_row.substance, _intake_row.amount, _intake_row.unit, _intake_row.preparation;
		update clin.substance_intake set
			fk_drug_component = _pk_component,
			preparation = NULL,
			fk_substance = NULL
		where
			pk = _intake_row.pk_substance_intake
		;
	end loop;

	perform 1 from clin.substance_intake where fk_drug_component is NULL;
	if FOUND then
		raise exception ''[_tmp_convert_substance_intakes]: failed to convert some rows'';
		return FALSE;
	end if;

	raise notice ''[_tmp_convert_substance_intakes]: end, success'';
	return TRUE;
END;';

-- convert
select _tmp_convert_substance_intakes();

drop function if exists _tmp_convert_substance_intakes() cascade;
drop view if exists ref._tmp_v_branded_drugs cascade;

-- --------------------------------------------------------------
select gm.log_script_insertion('v22-clin-substance_intake-dynamic-run_once.sql', '22.0');
