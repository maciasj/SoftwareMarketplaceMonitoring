from MonitoringSoftwareMarketplaces.models import *

class Repository:


        
    def deleteProduct(id, marketplace):
        try:
            product = Product.objects.get(identifier=id, marketplace=marketplace)
            product.delete()
            return True
        except Product.DoesNotExist:
            print("No existe el producto")
            return Product.DoesNotExist

    def getProductById(id, marketplace):
        try: 
            product = Product.objects.get(identifier=id, marketplace=marketplace)
            product = {
            'identifier': product.identifier,
            'name': product.name,
            'description': product.description,
            'type': product.type,
            'creator': product.creator,
            'marketplace': product.marketplace,
            'url': product.url}
            return product
        except Product.DoesNotExist:
            print("No existe el producto")
            return None

    def searchProduct(query, marketplace):
        try:
            products = Product.objects.filter(name__icontains=query, marketplace=marketplace)
            object_products = []
            for product in products:
                product = {
                    'identifier': product.identifier,
                    'name': product.name,
                    'description': product.description,
                    'type': product.type,
                    'creator': product.creator,
                    'api_name': product.api_name,
                    'marketplace': product.marketplace,
                    'url': product.url
                }
                object_products.append(product)
            return object_products
        except Product.DoesNotExist:
            print("No se pudo encontrar el producto")
            return None
    
    def getCategories(marketplace):
        categories = Category.objects.filter(marketplace=marketplace)
        categories_list = []
        for category in categories:
            category_dict = {
                'identifier': category.identifier,
                'name': category.name,
                'api_name': category.api_name,
                'url': category.url,
                'description': category.description,
                'marketplace': category.marketplace
            }
            categories_list.append(category_dict)
        return categories_list
    def getMarkets(marketplace):
        markets = Market.objects.filter(marketplace=marketplace)
        serialized_markets = []
        for market in markets:
            market = {
                'identifier': market.identifier,
                'url': market.url,
                'name': market.name,
                'marketplace': marketplace
            }
            serialized_markets.append(market)
        return serialized_markets
    
    def getProductsByQuery(query, marketplace):
        products = Product.objects.filter(name__icontains=query, marketplace=marketplace)
        object_products = []
        for product in products:
            product = {
                'identifier': product.identifier,
                'name': product.name,
                'description': product.description,
                'type': product.type,
                'creator': product.creator,
                'marketplace': product.marketplace,
                'url': product.url
            }
            object_products.append(product)
        return object_products
    
    def getKeywords(marketplace):
        keywords = Keyword.objects.filter(marketplace=marketplace).values('name')
        serialized_keywords = []
        for keyword in keywords:
            serialized_keywords.append(keyword['name'])
        return serialized_keywords

    def getProductByKeyword(keyword, marketplace):
        products = ProductKeyword.objects.filter(keywords=keyword, marketplace=marketplace).values_list('product', flat=True)
        print(products) 
        json_products = []
        for product in products:
            json_products.append(Repository.getProductById(product,marketplace))
        return json_products
    
    def getProductByCategory(category,marketplace):
        try:
            if(marketplace == "eclipse"):
                print("Ecplise")
                categoryName = Category.objects.get(identifier=category, marketplace=marketplace).name
            elif(marketplace == "mozilla"):
                print("Mozilla")
                categoryName = Category.objects.get(name=category, marketplace=marketplace).api_name
            print(categoryName)
            productsIds = CategoryInProduct.objects.filter(category=categoryName,marketplace=marketplace).values_list('product', flat=True)
            print("Productos: ", productsIds)
            json_products = []
            for product in list(productsIds):
                json_products.append(Repository.getProductById(product,marketplace))
            return json_products
        except Product.DoesNotExist:    
            return 2
        
    def insertCategoriesE(categories):
        for category in categories:
            try:
                category_obj = Category(
                    identifier=category['identifier'],
                    name=category['name'],
                    url=category['url'], 
                    marketplace="eclipse")
                print("Insertando categoria: ", category['name'])
                category_obj.save()
            except Exception as e:
                print("Error al insertar categoria: ", category['name'], e)
   
    def insertCategoriesM(categories):
        for category in categories:
            category_obj = Category(
                identifier=category['id'], 
                name=category['name'], 
                api_name=category['slug'], 
                marketplace="mozilla",
                description=category['description'],
                type=category['type'],)
            print("Insertando categoria: ", category['name'] )
            category_obj.save()
    def insertMarkets(markets, marketplace):
        for market in markets:
            try:
                market_obj = Market(identifier=market['identifier'], url=market['url'], name=market['name'], marketplace=marketplace)
                print("Insertando market: ", market['name'] )
                market_obj.save()
            except Exception as e:
                print("Error al insertar market: ", market['name'], e)
#MIRAR
    def insertCategoriesMS(categories):
        count = 0
        for category in categories:
            category_obj = Category(
                identifier=count, 
                name=category['name'], 
                api_name=category['api_name'], 
                marketplace="microsoft",
                )
            count = count + 1
            print("Insertando categoria: ", category['name'] )
            category_obj.save()
    def insertCategoryInMarket(categories,marketplace):
        print ("Insertando categorias en market")
        for category in categories:
            category_obj = Category.objects.get(identifier=category['identifier'])
            for market in category['market']:
                market_obj = Marketplace.objects.get(identifier=market, marketplace= marketplace)
                category_in_market = CategoryInMarket( category=category_obj, market=market_obj, marketplace=marketplace)
                category_in_market.save()
                print("Insertando categoria en market: ", category_in_market )
    
    def insertSingleProduct(product, marketplace):
        product_obj = Product(identifier=product['identifier'], 
                                url=product['url'],
                                name=product['name'], 
                                description=product['description'], 
                                type=product['type'], 
                                creator=product['creator'],
                                marketplace=marketplace)
        print("Insertando producto: ", product['name'])
        product_obj.description = product_obj.description.encode('utf-8')
        product_obj.name = product_obj.name.encode('utf-8')
        product_obj.save()

        #Insertar categorias en producto
        for category in product['categories']:
            category_in_product = CategoryInProduct(product=product['identifier'], category=category, marketplace=marketplace)
            if(not CategoryInProduct.objects.filter(product=product['identifier'], category=category).exists()):
                category_in_product.save()
                print("Insertando categoria en producto: ", category, "nombre  " , product['name'] )
        numKeywords = len(Keyword.objects.filter(marketplace=marketplace))
        #Insertar tags en producto    
        for keyword in product['keywords']:
            keywords_in_product = ProductKeyword(product=product['identifier'], keywords=keyword, marketplace=marketplace)
            if(not Keyword.objects.filter(name=keyword, marketplace=marketplace).exists()):
                newKeyword = Keyword(identifier=numKeywords+1, name=keyword, marketplace=marketplace)
                numKeywords = numKeywords + 1
                newKeyword.save()
                
            if(not ProductKeyword.objects.filter(product=product['identifier'], keywords=keyword).exists()):
                keywords_in_product.save()
                print("Insertando Tag en producto: ", keyword, "nombre  " , product['name'] )

    def insertKeywords(keywords, marketplace):
        cont = 1
        parsed_keywords = []
        for keyword in keywords:
            keyword_obj = Keyword(identifier=cont, name=keyword, marketplace=marketplace)
            cont = cont + 1
            keyword_obj.save()
            parsed_keywords.append(keyword)
        return parsed_keywords
    
    def existeCategory(category,makertplace):
        Newcategory = Category.objects.filter(name=category, marketplace=makertplace)
        return Newcategory.exists()
        
    
    def existeKewyword(keyword, marketplace):
        keyword = Keyword.objects.filter(name=keyword,marketplace=marketplace)
        return keyword.exists()
    
    def getCategoryInfo(category,makertplace):
        newcategory = Category.objects.filter(name=category, marketplace=makertplace).values('name', 'api_name')
        objectCategory ={
            "category": newcategory[0]['name'],
            "api_name": newcategory[0]['api_name'],
        }
        return objectCategory
    
    def insertGroupProducts(products, marketplace):
        for product in products:
            Repository.insertSingleProduct(product, marketplace)
        