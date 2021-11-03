-- Creating database
drop database gamer_paradise;
create database gamer_paradise;
\c gamer_paradise

create table users (
    user_id int generated always as identity primary key,                --PK
    first_name char(10), 
    last_name char(10), 
    e_mail varchar, 
    phone char(10)
);

create table product_supplier (
    supplier_id int generated always as identity primary key,            --PK
    supplier_phone char(10),
    supplier_name varchar(20),
    country_of_origin char(30)
);

/*
Insert : Take Product details and insert to all the necessary tables (Inventory manager)
         Eg: Inserting a listing for headphones:
            * Insert Supplier details (only if not present in the Supplier table)
            * Generic product details -> Product table
            * Specific accessory related details -> Accessory table (Foreign key for the generic details have to be referenced)
            * Periodically update the Offers table (Give button in front end to change offer details)
         
         Eg: Inserting a listing for a video game:
            * Insert Supplier details (only if not present in the Supplier table)
            * Generic product details -> Product table
            * Specific game related details -> Game table (Foreign key for the generic details have to be referenced)
            * Periodically update the Offers table (Give button in front end to change offer details)
            * Periodically update the contests table (Give button in front end to change contest details)
Update : 
Delete : Delete the entry from Accessory/Game, product offers, cartItem and cart tables.(cascading)
*/

-- Incorporate quantity available
create table product (
    product_id int generated always as identity primary key,  --PK
    supplier_id int references product_supplier(supplier_id) on delete cascade, --FK
    price numeric(10, 2),
    rating numeric(5, 1),
    description varchar(50),
    type varchar(10)
);

create table offers (
    offer_id int generated always as identity primary key,               --PK
    offer_description varchar(50)
);

create table cart (
    cart_id int generated always as identity primary key,                --PK
    user_id int references users(user_id) on delete cascade                                --FK
);

create table complaint (
    complaint_id int generated always as identity primary key,           --PK
    user_id int references users(user_id) on delete set null,                     --FK
    complaint_description varchar(50),
    complaint_date timestamp
);

create table team (
    team_id int generated always as identity primary key,                --PK
    total_points int
);

create table game (
    game_name varchar(30) primary key,                                   --PK
    product_id int references product(product_id) on delete cascade,            --FK
    genre varchar(20),
    specifications varchar(50),
    platform varchar(10),
    release_date timestamp
);

create table contest (
    contest_id int generated always as identity primary key,             --PK
    game_name varchar(30) references game(game_name) 
                          on delete cascade 
                          on update cascade,         --FK
    contest_description varchar, 
    start_date timestamp,
    end_date timestamp
);

create table payment (
    payment_id int generated always as identity primary key,             --PK
    cart_id int references cart(cart_id) on delete set null,             --FK
    payment_mode varchar(10),
    payment_date timestamp,
    amount_paid int
);

create table accessory (
    accessory_name varchar(30) primary key,                               --PK
    product_id int references product(product_id) on delete cascade,            --FK
    length int,
    breadth int,
    width int,
    quantity int,
    sub_category varchar(10)
);

create table cart_item (
    product_id int references product(product_id) on delete cascade,            --FK
    cart_id int references cart(cart_id) on delete cascade,                     --FK
    date_added timestamp, 
    quantity_wished int,
    primary key(product_id, cart_id)
);

create table product_offers (
    product_id int references product(product_id) on delete cascade,            --FK
    offer_id int references offers(offer_id) on delete cascade,                 --FK
    end_time timestamp,
    primary key(product_id, offer_id)
);

create table address (
    user_id int references users(user_id) on delete cascade,                     --FK
    address varchar(50),
    primary key(user_id, address)
);

-- Maybe notify the participating teams about the ending of the contest
create table participates (
    contest_id int references contest(contest_id) on delete cascade,            --FK
    team_id int references team(team_id) on delete cascade,                     --FK
    points_gained int,
    prize_won varchar(30),
    primary key(contest_id, team_id)
);

create table belongs_to (
    user_id int references users(user_id) on delete cascade,                    --FK 
    team_id int references team(team_id) on delete cascade,                     --FK
    primary key(user_id, team_id)
);