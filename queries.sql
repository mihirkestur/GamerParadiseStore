select * from product;
select * from user;
select ps.Supplier_Name, p.type from product as p, product_supplier as ps where ps.supplier_id = p.supplier_id;
select type,game_name,price from game as g, product as p where g.product_id = p.product_id;
select type,accessory_name,price from accessory as a, product as p where a.product_id = p.product_id;
select u.user_id from users as u where u.user_id not in (select b.user_id from belongs_to as b);
select * from team order by total_points DESC;
select b.team_id, count(*) from belongs_to as b group by b.team_id;