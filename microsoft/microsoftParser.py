from MonitoringSoftwareMarketplaces.JSONParser import JSONParser

class microsoftParser(JSONParser):

    def parseCategories(data):
        categories = []
        for cat in data:
            categories.append(cat)
        return categories
    
    def parseProducts(data):
        products = []
        for product in data['Products']:
            sku  = product['DisplaySkuAvailabilities'][0]
            sku_properties = sku["Sku"]["LocalizedProperties"][0]
            sku_title = sku_properties["SkuTitle"]
            sku_description = sku_properties["SkuDescription"]
            newProduct = {
                'identifier': product['ProductId'],
                'name': sku_title,
                'description': sku_description,
                'type': product['ProductKind'],
                'creator': product['LocalizedProperties'][0]['DeveloperName'],
                'api_name': "",
                'marketplace': 'microsoft',
                'url': "",
                'categories': "",
                'keywords': ""
            }
            products.append(newProduct)
        return products
    
    def getIds(data):
        ids = ""
        for item in data['Data']:
            ids = ids + item['PackageIdentifier'] + "," 
        print(ids)
        return {'productIds': ids}
    


 