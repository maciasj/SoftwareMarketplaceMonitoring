-- Insertar manualmente los marketplaces
INSERT INTO SMM_database.Marketplace VALUES ('microsoft store');
-- Selecionar marketplaces
select * from SMM_database.Marketplace;
select * from SMM_database.Category where marketplace = "mozilla";
select * from SMM_database.Market;
select * from SMM_database.CategoryInProduct;
select * from SMM_database.TagInProduct;
select * from SMM_database.Product;
select * from SMM_database.Keywords;



