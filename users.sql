-- inventory_manager
create user inventory_manager with encrypted password 'manager';
-- product, product_supplier, product_offers, offers, accessory, game, contest
grant all on product, product_supplier, product_offers, offers, accessory, game, contest to inventory_manager;

-- user (i.e. "player")
create user customer with encrypted password 'user';
grant insert,update,select, delete on team, belongs_to, participates, address, cart_item, payment to customer;
grant insert on users, complaint to customer;

grant select on product, game, contests, product_supplier, accessory, product_offers, offers to customer;