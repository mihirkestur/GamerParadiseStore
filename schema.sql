-- STRONG ENTITIES

create table product_supplier (
    int supplier_id generated always as identity,            --PK
    char(10) supplier_phone,
    varchar(20) supplier_name,
    char(30) country_of_origin
);

create table user (
    int user_id generated always as identity,                --PK
    char(10) first_name, 
    char(10) last_name, 
    varchar e_mail, 
    char(10) phone
);

create table product (
    int product_id generated always as identity,             --PK
    int supplier_id references product_supplier.supplier_id, --FK
    numeric(10, 2) price,
    numeric(5,1) rating,
    varchar(50) description,
    varchar(10) type
);

create table offers (
    int offer_id generated always as identity,               --PK
    varchar(50) offer_description
);

create table cart (
    int cart_id generated always as identity,                --PK
    int user_id references user.user_id,                     --FK
);

create table complaint (
    int complaint_id generated always as identity,           --PK
    int user_id references user.user_id,                     --FK
    varchar(50), complaint_description,
    timestamp complaint_date
);

create table team (
    int team_id generated always as identity,                --PK
    int total_points
);

create table contest (
    int contest_id generated always as identity,             --PK
    varchar(30) game_name references game.game_name,         --FK
    varchar(50) contest_description, 
    timestamp start_date,
    timestamp end_date
);

create table payment (
    int payment_id generated always as identity,             --PK
    int cart_id references cart.cart_id,                     --FK
    varchar(10) payment_mode,
    timestamp payment_date,
    int amount_paid
);

-- WEAK ENTITIES

create table accessory (
    varchar(30) accessory_name generated always as identity, --PK
    int product_id references product.product_id,            --FK
    int length,
    int breadth,
    int width,
    int quantity,
    varchar(10) sub_category
);

create table game (
    varchar(30) game_name,                                   --PK
    int product_id references product.product_id,            --FK
    varchar(20) genre,
    varchar(50) specifications,
    varchar(10) platform,
    timestamp release_date
);

create table cart_item (
    int product_id references product.product_id,            --FK
    int cart_id references cart.cart_id,                     --FK
    timestamp date_added, 
    int quantity_wished,
    primary key(product_id, cart_id)
);

-- Relation/Attribute tables

create table product_offers (
    int product_id references product.product_id,            --FK
    int offer_id references offers.offer_id,                 --FK
    timestamp end_time,
    primary key(product_id, offer_id)
);

create table address (
    int user_id references user.user_id,                     --FK
    varchar(50) address,
    primary key(user_id, address)
);

create table participates (
    int contest_id references contest.contest_id,            --FK
    int team_id references team.team_id,                     --FK
    int points_gained,
    int prize_won,
    primary key(contest_id, team_id)
);

create table belongs_to (
    int user_id references user.user_id,                     --FK 
    int team_id references team.team_id,                     --FK
    primary key(user_id, team_id)
);