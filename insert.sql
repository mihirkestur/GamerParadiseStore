/*
TODO
Use triggers for product id going to games and accessories
What do you want to display on the front end?
Aggregate, group by and order by,
In not in exist, complex queries
Transaction (No need concurrency)
Create multiple users and show updates in one user displayed in the other user
While creating a user, give permissions accordingly (specific attribute or the entire table)
Create view and give permission to the user (in case we need to give a subset of attributes permissions)
*/

insert into users(first_name, last_name, e_mail, phone) values ('Fame1', 'Lname1', 'mohalk@gmail.com', 7825780817);
insert into users(first_name, last_name, e_mail, phone) values ('Fame2', 'Lname2', 'mohalk@gmail.com', 7825780817);
insert into users(first_name, last_name, e_mail, phone) values ('Fame3', 'Lname3', 'mohalk@gmail.com', 7825780817);
insert into users(first_name, last_name, e_mail, phone) values ('Fame4', 'Lname4', 'mohalk@gmail.com', 7825780817);
insert into users(first_name, last_name, e_mail, phone) values ('Fame5', 'Lname5', 'mohalk@gmail.com', 7825780817);
insert into users(first_name, last_name, e_mail, phone) values ('Fame6', 'Lname6', 'mohalk@gmail.com', 7825780817);
insert into users(first_name, last_name, e_mail, phone) values ('Fame7', 'Lname7', 'mohalk@gmail.com', 7825780817);
insert into users(first_name, last_name, e_mail, phone) values ('Fame8', 'Lname8', 'mohalk@gmail.com', 7825780817);
insert into users(first_name, last_name, e_mail, phone) values ('Fame9', 'Lname9', 'mohalk@gmail.com', 7825780817);
insert into users(first_name, last_name, e_mail, phone) values ('Fame10', 'Lname10', 'mohalk@gmail.com', 7825780817);

insert into product_supplier(supplier_phone, supplier_name, country_of_origin) values (9902144238,'Supplier1','Country1');
insert into product_supplier(supplier_phone, supplier_name, country_of_origin) values (8723107347,'Supplier2','Country2');
insert into product_supplier(supplier_phone, supplier_name, country_of_origin) values (7834578245,'Supplier3','Country3');
insert into product_supplier(supplier_phone, supplier_name, country_of_origin) values (9785267547,'Supplier4','Country4');
insert into product_supplier(supplier_phone, supplier_name, country_of_origin) values (9902345658,'Supplier5','Country5');

insert into product(supplier_id, price, rating, description, type) values (1,  200, 4.5, 'Description1', 'game');
insert into product(supplier_id, price, rating, description, type) values (1, 1000, 3.5, 'Description2', 'accessory');
insert into product(supplier_id, price, rating, description, type) values (2,  800, 4.0, 'Description3', 'accessory');
insert into product(supplier_id, price, rating, description, type) values (4,  275, 4.2, 'Description4', 'game');
insert into product(supplier_id, price, rating, description, type) values (2,    0, 4.8, 'Description5', 'game');
insert into product(supplier_id, price, rating, description, type) values (5,  350, 3.0, 'Description6', 'accessory');
insert into product(supplier_id, price, rating, description, type) values (3,  800, 3.8, 'Description7', 'game');

insert into offers(offer_description) values ('Offer Description1');
insert into offers(offer_description) values ('Offer Description2');
insert into offers(offer_description) values ('Offer Description3');
insert into offers(offer_description) values ('Offer Description4');
insert into offers(offer_description) values ('Offer Description5');
insert into offers(offer_description) values ('Offer Description6');
insert into offers(offer_description) values ('Offer Description7');

insert into cart(user_id) values (1);
insert into cart(user_id) values (2);
insert into cart(user_id) values (3);
insert into cart(user_id) values (4);
insert into cart(user_id) values (5);
insert into cart(user_id) values (6);

insert into complaint(user_id, complaint_description, complaint_date) values (1, 'Complaint Description1', '2020-10-05 14:01:10-08');
insert into complaint(user_id, complaint_description, complaint_date) values (1, 'Complaint Description2', '2020-10-05 14:01:10-08');
insert into complaint(user_id, complaint_description, complaint_date) values (1, 'Complaint Description3', '2020-10-05 14:01:10-08');
insert into complaint(user_id, complaint_description, complaint_date) values (1, 'Complaint Description4', '2020-10-05 14:01:10-08');
insert into complaint(user_id, complaint_description, complaint_date) values (1, 'Complaint Description5', '2020-10-05 14:01:10-08');
insert into complaint(user_id, complaint_description, complaint_date) values (1, 'Complaint Description6', '2020-10-05 14:01:10-08');

insert into team(total_points) values (10);
insert into team(total_points) values (10);
insert into team(total_points) values (10);
insert into team(total_points) values (10);
insert into team(total_points) values (10);
insert into team(total_points) values (10);
insert into team(total_points) values (10);
insert into team(total_points) values (10);

insert into game values ('Valorant', 1, 'Action', '1GB', 'PC', '2020-10-05 14:01:10-08');
insert into game values ('COD', 2, 'Romance', '2GB', 'Phone', '2020-10-05 14:01:10-08');
insert into game values ('CSGO', 3, 'FPS', '1GB', 'Xbox', '2020-10-05 14:01:10-08');


insert into contest(game_name, contest_description, start_date, end_date) values('COD','battle royale comp with 25 teams last team to survie wins','2020-10-05 14:01:10-08','2020-10-05 14:01:10-08');
insert into contest(game_name, contest_description, start_date, end_date) values('COD','Hardpoint,Domination,Team Death match','2020-10-05 14:01:10-08', '2020-10-05 14:01:10-08');
insert into contest(game_name, contest_description, start_date, end_date) values('Valorant','Description','2020-10-05 14:01:10-08', '2020-10-05 14:01:10-08');
insert into contest(game_name, contest_description, start_date, end_date) values('Valorant','Description','2020-10-05 14:01:10-08', '2020-10-05 14:01:10-08');
insert into contest(game_name, contest_description, start_date, end_date) values('CSGO','Description','2020-10-05 14:01:10-08', '2020-10-05 14:01:10-08');
insert into contest(game_name, contest_description, start_date, end_date) values('CSGO','Description','2020-10-05 14:01:10-08', '2020-10-05 14:01:10-08');

insert into payment(cart_id, payment_mode, payment_date, amount_paid) values (1, 'COD', '2020-10-05 14:01:10-08', 200);
insert into payment(cart_id, payment_mode, payment_date, amount_paid) values (2, 'DEBIT', '2020-10-05 14:01:10-08', 300);
insert into payment(cart_id, payment_mode, payment_date, amount_paid) values (3, 'CREDIT', '2020-10-05 14:01:10-08', 200);
insert into payment(cart_id, payment_mode, payment_date, amount_paid) values (4, 'DEBIT', '2020-10-05 14:01:10-08', 400);

insert into accessory values ('headphones 1', 1, 30, 40, 60,2,'category 1');
insert into accessory values ('keyboard 1', 2, 50, 70, 80, 10, 'category 1');
insert into accessory values ('shirt 1', 3, 70, 50, 10, 20, 'category 2');

insert into cart_item values (1, 1, '2020-10-05 14:01:10-08', 1);
insert into cart_item values (2, 1, '2020-10-05 14:01:10-08', 1);
insert into cart_item values (3, 1, '2020-10-05 14:01:10-08', 1);

insert into product_offers values (1, 1, '2020-10-05 14:01:10-08');
insert into product_offers values (2, 2, '2020-10-05 14:01:10-08');
insert into product_offers values (3, 1, '2020-10-05 14:01:10-08');
insert into product_offers values (4, 1, '2020-10-05 14:01:10-08');

insert into address values(1, 'Address1');
insert into address values(1, 'Address2');
insert into address values(2, 'Address1');
insert into address values(4, 'Address1');
insert into address values(2, 'Address2');
insert into address values(3, 'Address1');
insert into address values(3, 'Address2');
insert into address values(3, 'Address3');


insert into participates values (1, 1, 5, 10);
insert into participates values (2, 2, 5, 10);
insert into participates values (3, 3, 5, 10);
insert into participates values (4, 4, 5, 10);

insert into belongs_to values(1, 2);
insert into belongs_to values(2, 2);
insert into belongs_to values(3, 2);
insert into belongs_to values(4, 1);
insert into belongs_to values(5, 1);
insert into belongs_to values(6, 1);