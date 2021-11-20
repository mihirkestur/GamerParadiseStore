\echo QUERY 1 ) select all product details
\echo
select * from product;
\echo QUERY 2 ) select all user details
\echo
select * from users;
\echo QUERY 3 ) select all product suppliers for each product
\echo
select ps.Supplier_Name, p.type from product as p, product_supplier as ps where ps.supplier_id = p.supplier_id;
\echo QUERY 4 ) select all games
\echo
select type,game_name,price from game as g, product as p where g.product_id = p.product_id;
\echo QUERY 5 ) select all accessories
\echo
select type,accessory_name,price from accessory as a, product as p where a.product_id = p.product_id;

\echo QUERY 6 ) display total points in decreasing order
\echo
select * from team order by total_points DESC;
\echo QUERY 7 ) display number of people in each team
\echo
select b.team_id, count(*) from belongs_to as b group by b.team_id;

\echo QUERY 8 ) select users that are not in a team
\echo
select u.user_id from users as u where u.user_id not in (
    select b.user_id from belongs_to as b
    );

\echo QUERY 9 ) select all games in a cart of user 1
\echo
select g.game_name from game as g where product_id in (
    select ci.product_id from cart_item as ci, cart as c, users as u where ci.cart_id = c.cart_id and c.user_id = u.user_id and u.user_id = 1
    );
\echo QUERY 10 ) select all accessories in a cart of user 1
\echo
select a.accessory_name from accessory as a where product_id in (
    select ci.product_id from cart_item as ci, cart as c, users as u where ci.cart_id = c.cart_id and c.user_id = u.user_id and u.user_id = 1
    );
\echo QUERY 11 ) display total points for each game for all teams
\echo
select t.team_id,t.total_points,c.game_name from contest as c, participates as p, team as t where t.team_id = p.team_id and p.contest_id = c.contest_id;


\echo QUERY 12 ) find the number of games sold on payment date = XXXX
\echo
-- find the number of games sold on payment date = XXXX
explain analyze select count(g.product_id) as games_sold from game as g where g.product_id in (
    select ci.product_id from cart_item as ci, cart as c, payment as p where p.cart_id = c.cart_id and c.cart_id = ci.cart_id and p.payment_date='2020-10-05 14:01:10-08'
    );

explain analyze select count(g.product_id) as games_sold from game as g where g.product_id in (
    select ci.product_id from cart_item as ci where ci.cart_id in ( 
        select c.cart_id from cart as c where c.cart_id in(
            select p.cart_id from payment as p where p.payment_date='2020-10-05 14:01:10-08'
            )
        )
    );



