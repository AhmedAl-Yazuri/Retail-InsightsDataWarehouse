DROP SCHEMA IF EXISTS dw CASCADE;
CREATE SCHEMA dw;

CREATE TABLE dw.dim_customers (
    customerid BIGINT PRIMARY KEY,
    customername TEXT
);

CREATE TABLE dw.dim_products (
    productid BIGINT PRIMARY KEY,
    productname TEXT,
    categoryid BIGINT,
    subcategoryid BIGINT
);

CREATE TABLE dw.dim_territories (
    territoryid BIGINT PRIMARY KEY,
    territoryname TEXT
);

CREATE TABLE dw.dim_calendar (
    dateid DATE PRIMARY KEY,
    year INT,
    month INT,
    day INT,
    weekday TEXT
);

CREATE TABLE dw.fact_sales (
    salesid TEXT PRIMARY KEY,
    customerid BIGINT REFERENCES dw.dim_customers(customerid),
    productid BIGINT REFERENCES dw.dim_products(productid),
    territoryid BIGINT REFERENCES dw.dim_territories(territoryid),
    dateid DATE REFERENCES dw.dim_calendar(dateid),
    quantity INT,
    unitprice NUMERIC,
    totalsales NUMERIC
);

INSERT INTO dw.dim_customers (customerid, customername)
SELECT DISTINCT
    c."CustomerKey" AS customerid,
    NULLIF(TRIM(CONCAT_WS(' ', c."FirstName", c."LastName")), '') AS customername
FROM public.customers c
WHERE c."CustomerKey" IS NOT NULL;

INSERT INTO dw.dim_products (productid, productname, categoryid, subcategoryid)
SELECT DISTINCT
    p."ProductKey" AS productid,
    p."ProductName" AS productname,
    ps."ProductCategoryKey" AS categoryid,
    p."ProductSubcategoryKey" AS subcategoryid
FROM public.products p
LEFT JOIN public.product_subcategories ps
    ON p."ProductSubcategoryKey" = ps."ProductSubcategoryKey"
WHERE p."ProductKey" IS NOT NULL;

INSERT INTO dw.dim_territories (territoryid, territoryname)
SELECT DISTINCT
    t."SalesTerritoryKey" AS territoryid,
    COALESCE(NULLIF(t."Region", ''), t."Country", t."Continent", CONCAT('Territory ', t."SalesTerritoryKey")) AS territoryname
FROM public.territories t
WHERE t."SalesTerritoryKey" IS NOT NULL;

INSERT INTO dw.dim_calendar (dateid, year, month, day, weekday)
SELECT DISTINCT
    TO_DATE(c."Date", 'MM/DD/YYYY') AS dateid,
    EXTRACT(YEAR FROM TO_DATE(c."Date", 'MM/DD/YYYY'))::INT AS year,
    EXTRACT(MONTH FROM TO_DATE(c."Date", 'MM/DD/YYYY'))::INT AS month,
    EXTRACT(DAY FROM TO_DATE(c."Date", 'MM/DD/YYYY'))::INT AS day,
    TRIM(TO_CHAR(TO_DATE(c."Date", 'MM/DD/YYYY'), 'Day')) AS weekday
FROM public.calendar c
WHERE c."Date" IS NOT NULL;

INSERT INTO dw.fact_sales (salesid, customerid, productid, territoryid, dateid, quantity, unitprice, totalsales)
SELECT
    CONCAT(cs."OrderNumber", '-', cs."OrderLineItem") AS salesid,
    cs."CustomerKey" AS customerid,
    cs."ProductKey" AS productid,
    cs."TerritoryKey" AS territoryid,
    cs."OrderDate"::DATE AS dateid,
    COALESCE(cs."OrderQuantity", 0)::INT AS quantity,
    COALESCE(p."ProductPrice", 0)::NUMERIC AS unitprice,
    (COALESCE(cs."OrderQuantity", 0) * COALESCE(p."ProductPrice", 0))::NUMERIC AS totalsales
FROM public.cleaned_sales cs
LEFT JOIN public.products p
    ON cs."ProductKey" = p."ProductKey"
WHERE cs."OrderNumber" IS NOT NULL
  AND cs."OrderLineItem" IS NOT NULL
  AND cs."OrderDate" IS NOT NULL;
