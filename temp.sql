select game_name as name, price * quantity_wished as cost, quantity_wished as QTY from 
product p, cart_item c, game g
where p.product_id = c.product_id and p.product_id = g.product_id and cart_id = 1

union

select accessory_name as name, price * quantity_wished as cost, quantity_wished as QTY from 
product p, cart_item c, accessory a
where p.product_id = c.product_id and p.product_id = a.product_id and cart_id = 1;