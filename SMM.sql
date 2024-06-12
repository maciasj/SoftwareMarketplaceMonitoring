-- Insertar manualmente los marketplaces
INSERT INTO SMM_database.Marketplace VALUES ('microsoft store');
-- Selecionar marketplaces
select * from SMM_database.marketplace;
select * from SMM_database.Category where marketplace = "microsoft";
select * from SMM_database.Market;
select * from SMM_database.CategoryInProduct;
select * from SMM_database.Product where identifier ="3799227";
select * from SMM_database.Keywords;
select * from SMM_database.ProductKeyword;


