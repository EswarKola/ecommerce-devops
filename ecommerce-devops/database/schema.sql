CREATE TABLE IF NOT EXISTS products (
  id SERIAL PRIMARY KEY,
  name VARCHAR(120) NOT NULL,
  description TEXT NOT NULL,
  price NUMERIC(10,2) NOT NULL CHECK (price >= 0)
);
INSERT INTO products(name,description,price)
SELECT v.name,v.description,v.price FROM (VALUES
 ('Wireless Headphones','Comfortable headphones for everyday listening.',2499.00),
 ('Smart Watch','Track activity and view notifications.',3999.00),
 ('Travel Backpack','A lightweight backpack for daily use.',1499.00)
) AS v(name,description,price)
WHERE NOT EXISTS (SELECT 1 FROM products);
