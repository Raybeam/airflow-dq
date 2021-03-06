DROP TABLE IF EXISTS Costs;
CREATE TABLE Costs(id SERIAL, cost DECIMAL);
INSERT INTO Costs(cost) values(20), (25), (15), (45);

DROP TABLE IF EXISTS Sales;
CREATE TABLE Sales(sale_price DECIMAL, date DATE);
INSERT INTO Sales VALUES(23.99, '2019-12-20'), (15.99, NOW() - INTERVAL '2 week'), (14.49, NOW() - INTERVAL '2 week'), (12.00, '2019-11-23');