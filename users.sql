drop user manager;
drop user customer;

-- inventory_manager
create user manager with encrypted password 'manager';
-- product, product_supplier, product_offers, offers, accessory, game, contest
grant all on product, product_supplier, product_offers, offers, accessory, game, contest to inventory_manager;

-- user (i.e. "player")
create user customer with encrypted password 'customer';

grant insert, update, select, delete on team, belongs_to, participates, address, cart_item, payment, users, complaint to customer;
grant select on product, game, contest, product_supplier, accessory, product_offers, offers to customer;