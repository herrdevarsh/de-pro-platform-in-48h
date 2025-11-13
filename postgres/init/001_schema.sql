create table if not exists customers (
  customer_id bigint primary key,
  email text not null,
  country text not null,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  is_active boolean not null default true
);
create index if not exists idx_customers_updated on customers(updated_at);

create table if not exists orders (
  order_id bigint primary key,
  customer_id bigint references customers(customer_id),
  order_ts timestamptz not null,
  currency text not null default 'EUR',
  total_amount_eur numeric(12,2) not null,
  updated_at timestamptz not null default now()
);
create index if not exists idx_orders_updated on orders(updated_at);

create table if not exists events (
  event_id bigserial primary key,
  customer_id bigint,
  event_ts timestamptz not null,
  event_type text not null,
  session_id text,
  updated_at timestamptz not null default now()
);
create index if not exists idx_events_updated on events(updated_at);

insert into customers(customer_id,email,country,created_at,updated_at,is_active) values
(1,'alice@example.com','DE',now()-interval '60 days',now(),true),
(2,'bob@example.com','DE',now()-interval '40 days',now(),true)
on conflict do nothing;

insert into orders(order_id,customer_id,order_ts,currency,total_amount_eur,updated_at) values
(1001,1,now()-interval '7 days','EUR',59.90,now()),
(1002,2,now()-interval '2 days','EUR',42.50,now())
on conflict do nothing;
