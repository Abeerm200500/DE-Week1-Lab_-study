-- Lab 3: Exploring The Market in PostgreSQL
-- SOLUTIONS 

-- 1.1 Products overview (example)
SELECT * FROM products LIMIT 10;
SELECT COUNT(*) FROM products;                 

-- 1.2 Branches overview
SELECT * FROM branches;                        
SELECT COUNT(*) FROM branches;                 

-- 1.3 Customers overview
SELECT * FROM customers LIMIT 10;             
SELECT COUNT(*) FROM customers;               

-- 1.4 Sales overview
SELECT * FROM sales LIMIT 10;                  
SELECT COUNT(*) FROM sales;                   

-- 2.1 Receipts by payment method (example)
SELECT payment_method, COUNT(*) AS receipts
FROM sales
GROUP BY payment_method
ORDER BY receipts DESC;                       

-- 2.2 Products by category
SELECT category, COUNT(*) AS products
FROM products
GROUP BY category
ORDER BY products DESC;                    

-- 3.1 Sales by branch (example)
SELECT b.branch_name,
       COUNT(*)                      AS receipts,
       SUM(s.total_amount)           AS revenue,
       ROUND(AVG(s.total_amount), 2) AS avg_receipt
FROM sales s
JOIN branches b ON s.branch_id = b.branch_id
GROUP BY b.branch_name
ORDER BY revenue DESC;


-- 3.2 Meat products and their suppliers
SELECT p.product_name, p.current_price, v.vendor_name
FROM products p
JOIN vendors v ON p.vendor_id = v.vendor_id
WHERE p.category = 'Meat';                     

-- 4.1 Products ranked by price (example)
SELECT product_name, category, current_price,
       RANK() OVER (ORDER BY current_price DESC) AS price_rank
FROM products;                               

-- 4.2 Products ranked inside each category
SELECT category, product_name, current_price,
       RANK() OVER (PARTITION BY category ORDER BY current_price DESC) AS rank_in_category
FROM products
ORDER BY category, rank_in_category;    