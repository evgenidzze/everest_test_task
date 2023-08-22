CREATE TABLE IF NOT EXISTS item

(
  id serial INTEGER PRIMARY KEY,
  title VARCHAR (100) not null,
  managers_slack VARCHAR (64),
  accountant VARCHAR (64),
  slack_notification_sent BOOLEAN NOT NULL DEFAULT FALSE
);


CREATE TABLE IF NOT EXISTS order
(
    id             INTEGER      not null
        primary key,
    first_name     VARCHAR(100) not null,
    last_name      VARCHAR(100) not null,
    country        VARCHAR(100) not null,
    city           VARCHAR(100) not null,
    address        VARCHAR(100) not null,
    status         VARCHAR(10)  not null,
    total_quantity INTEGER
);

CREATE TABLE IF NOT EXISTS order_items
(
    id         INTEGER not null
        primary key,
    order_id   INTEGER
        references main."order",
    product_id INTEGER
        references main.item,
    quantity   INTEGER
);



CREATE TABLE IF NOT EXISTS user
(
    id            INTEGER     not null
        primary key,
    username      VARCHAR(30) not null
        unique,
    email         VARCHAR(50) not null
        unique,
    password_hash VARCHAR(60) not null
);





INSERT INTO market.user (id, username, email, password_hash) VALUES (1, 'Evgen', 'evgen@gmail.com', '$2b$12$6RyENqcRmeGk5LDedQZd9O3fhZx5yeZMXffCB8ZC1bQezD9Ep2dpa');

INSERT INTO market.item (id, title, price, weight, color, image) VALUES (1, '#122 Ultramarine', 9, 100, 'Blue', 'http://127.0.0.1:5000/_uploads/photos/122_UltramarineBlue_a2x.webp');
INSERT INTO market.item (id, title, price, weight, color, image) VALUES (2, '#110 Organic Pyrrole', 15, 100, 'Orange', 'http://127.0.0.1:5000/_uploads/photos/110_OrganicOrange_a2x.webp');
INSERT INTO market.item (id, title, price, weight, color, image) VALUES (3, '#100 Burnt sienna', 12, 100, 'Oxide Green', 'http://127.0.0.1:5000/_uploads/photos/104_ChromiumOxideGreen_a2x.webp');
INSERT INTO market.item (id, title, price, weight, color, image) VALUES (4, '#116 Phthalo ', 12, 100, 'Green', 'http://127.0.0.1:5000/_uploads/photos/116_PhthaloGreen_a2x.webp');
INSERT INTO market.item (id, title, price, weight, color, image) VALUES (5, '#120 Lightfastness', 15, 100, 'Yellow Green', 'http://127.0.0.1:5000/_uploads/photos/120_YellowGreen_a_59511d56-9740-47da-ab6b-4ddf934b3adf2x.webp');
INSERT INTO market.item (id, title, price, weight, color, image) VALUES (6, '#125 Lightblue', 15, 100, 'Blue', 'http://127.0.0.1:5000/_uploads/photos/135_PhthaloTurquoise_a2x.webp');

INSERT INTO market.`order` (id, first_name, last_name, country, city, address, status, total_quantity) VALUES (3, 'Evgenidzze', 'Smetaniuk', 'Ukraine', 'Vinnytsia', 'Volodymyra Ilyka 77', 'CANCELED', 3);
INSERT INTO market.`order` (id, first_name, last_name, country, city, address, status, total_quantity) VALUES (4, 'Evgenidzze', 'Smetaniuk', 'asdasasdas', 'asdasd', 'adsas', 'PENDING', 2);

INSERT INTO market.order_items (id, order_id, product_id, quantity) VALUES (5, 3, 3, 1);
INSERT INTO market.order_items (id, order_id, product_id, quantity) VALUES (6, 3, 1, 1);
INSERT INTO market.order_items (id, order_id, product_id, quantity) VALUES (7, 3, 4, 1);
INSERT INTO market.order_items (id, order_id, product_id, quantity) VALUES (8, 4, 3, 2);