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
comment on table bill.bill is 'actual bills';

select audit.register_table_for_auditing('bill', 'bill');
select gm.register_notifying_table('bill', 'bill');

grant select, insert, delete, update on
	bill.bill
to group "gm-doctors";

grant select on
	bill.bill
to group "gm-public";

grant usage on
	bill.bill_pk_seq
to group "gm-public";

-- --------------------------------------------------------------
-- .invoice_id
comment on column bill.bill.invoice_id is 'the ID of the bill';

\unset ON_ERROR_STOP
alter table bill.bill drop constraint bill_bill_sane_invoice_id;
\set ON_ERROR_STOP 1

alter table bill.bill
	add constraint bill_bill_sane_invoice_id check (
		gm.is_null_or_blank_string(invoice_id) is False
	);

-- --------------------------------------------------------------
-- .payment_method
comment on column bill.bill.payment_method is 'the method the customer is supposed to pay by';

alter table bill.bill
	alter column payment_method
		set default 'cash'::text;

\unset ON_ERROR_STOP
alter table bill.bill drop constraint bill_bill_sane_pay_method;
\set ON_ERROR_STOP 1

alter table bill.bill
	add constraint bill_bill_sane_pay_method check
		(gm.is_null_or_blank_string(payment_method) is False);

-- --------------------------------------------------------------
-- .close_date
comment on column bill.bill.close_date is 'cannot add further bill_items after this date if not NULL';

alter table bill.bill
	alter column close_date
		set default NULL;

-- --------------------------------------------------------------
-- .fk_receiver_identity
comment on column bill.bill.fk_receiver_identity is 'link to the receiver as a GNUmed identity, if known';

alter table bill.bill
	alter column fk_receiver_identity
		set default NULL;

\unset ON_ERROR_STOP
alter table bill.bill.fk_receiver_identity drop constraint bill_fk_receiver_identity_fkey cascade;
\set ON_ERROR_STOP 1

alter table bill.bill
	add foreign key (fk_receiver_identity)
		references dem.identity(pk)
		on update cascade
		on delete restrict;

-- --------------------------------------------------------------
-- .receiver_address
comment on column bill.bill.receiver_address is 'the address of the receiver of the invoice, retrieved at close time';

\unset ON_ERROR_STOP
alter table bill.bill drop constraint bill_bill_sane_recv_adr;
\set ON_ERROR_STOP 1

alter table bill.bill
	add constraint bill_bill_sane_recv_adr check (
		(close_date is NULL)
		-- nice but not safe:
		--or (close_date > now())
			or
		(gm.is_null_or_blank_string(receiver_address) is False)
	);

-- --------------------------------------------------------------
\unset ON_ERROR_STOP
drop view bill.v_bills cascade;
\set ON_ERROR_STOP 1

create or replace view bill.v_bills as

SELECT
	b_b.pk
		as pk_bill,
	b_b.invoice_id,
	b_b.receiver_address,
	b_b.fk_receiver_identity
		as pk_receiver_identity,
	-- assumes that all bill_items have the same currency
	(select sum(final_amount) from bill.v_bill_items where pk_bill = b_b.pk)
		as total_amount,
	-- assumes that all bill_items have the same currency
	(select currency from bill.v_bill_items where pk_bill = b_b.pk limit 1)
		as currency,
	b_b.payment_method,
	b_b.close_date,
	-- assumes all bill items point to encounters of one patient
	(select fk_patient from clin.encounter where clin.encounter.pk = (
		select fk_encounter from bill.bill_item where fk_bill = b_b.pk limit 1
	))	as pk_patient,
	(select array_agg(bill.bill_item.pk) from bill.bill_item where fk_bill = b_b.pk)
		as pk_bill_items,
	(select array_agg(bill.v_bill_items.currency) from bill.v_bill_items where pk_bill = b_b.pk limit 1)
		as item_currencies
FROM
	bill.bill b_b
;

grant select on bill.v_bills to group "gm-doctors";


\unset ON_ERROR_STOP
insert into bill.bill (invoice_id, receiver_address, close_date) values ('GNUmed@Enterprise / 2012 / 1', 'Star Fleet Health Fund', now() - '1 week'::interval);
update bill.bill_item set fk_bill = currval('bill.bill_item_pk_seq') where fk_bill is NULL and description = 'Reiseberatung';
\set ON_ERROR_STOP 1

-- --------------------------------------------------------------
\unset ON_ERROR_STOP
drop view bill.v_export4accounting cascade;
\set ON_ERROR_STOP 1

create or replace view bill.v_export4accounting as

select
	me.*,
	'Rg. '::text || me.invoice_id
		|| ' vom '::text || me.value_date
		|| ', KdNr. '::text || coalesce(me.pk_receiver_identity::text, '<?>')
	as description
from (
		SELECT
			b_vb.pk_bill,
			'Income'::text
				AS account,
			b_vb.invoice_id,
			b_vb.pk_receiver_identity,
			b_vb.close_date
				AS value_date,
			- b_vb.total_amount
				AS amount,
			b_vb.currency
		FROM
			bill.v_bills b_vb
		WHERE
			b_vb.close_date is not NULL

		UNION ALL

		SELECT
			b_vb.pk_bill,
			'Debitor '::text || coalesce(b_vb.pk_receiver_identity::text, '<?>')
				as account,
			b_vb.invoice_id,
			b_vb.pk_receiver_identity,
			b_vb.close_date
				AS value_date,
			b_vb.total_amount
				as amount,
			b_vb.currency
		FROM
			bill.v_bills b_vb
		WHERE
			b_vb.close_date is not NULL
) as me;


GRANT SELECT ON TABLE bill.v_export4accounting TO "gm-staff";
GRANT SELECT ON TABLE bill.v_export4accounting TO "gm-doctors";
GRANT SELECT ON TABLE bill.v_export4accounting TO "gm-dbo";

-- --------------------------------------------------------------
create or replace function bill.get_bill_receiver_identity(integer)
	returns integer
	LANGUAGE SQL
	AS '
select
	value
from (
	select
		id.pk_id,
		id.value::integer
	from
		dem.v_external_ids4identity id
			join dem.identity d_i on (id.value = d_i.pk::text)
	where
		id.pk_type = 18		-- xxxxxxxxxxxx
			and
		id.pk_identity = $1

	union all

	select
		0,
		$1
) me
order by pk_id desc
limit 1;';

-- --------------------------------------------------------------
create or replace function bill.get_invoice_address(integer)
	returns text
	LANGUAGE SQL
	AS '
select label1_3::text
from (
	select
		(lastnames || '', '' || firstnames || E''\n''
			|| street || '' '' || number || coalesce(subunit, '''') || E''\n''
			|| code_country || ''-'' || postcode || '' '' || urb
		) as label1_3,
		address_type
	from
		dem.v_pat_addresses
	where
		pk_identity = $1

	union all

	select
		lastnames || '', '' || firstnames || E''\n'' || ''in Praxis'',
		''zzz''
	from
		dem.v_basic_person
	where pk_identity = $1
) me
order by address_type = ''bill'' desc
limit 1;';

-- --------------------------------------------------------------
select gm.log_script_insertion('v17-bill-bill-dynamic.sql', '17.0');
