from MonitoringSoftwareMarketplaces.JSONParser import JSONParser

class MozillaParser(JSONParser):

    def parseCategories(data):
        categories = []
        for cat in data:
            categories.append(cat)
        return categories
    def parseKeywords(data):
        keywords = []
        for keyword in data:
            keywords.append(keyword)
        return keywords
    
    def parseSingleProduct(data):
        print("PRODUCTO", data)
        categories = MozillaParser.parseCategories(data['categories'])
        keywords = MozillaParser.parseKeywords(data['tags'])
        if 'description' in data and data['description'] and 'en-US' in data['description']:
            description1 = data['description']['en-US']
        else:
            description1 = "No description"

        if 'name' in data and data['name'] and 'en-US' in data['name']:
            name1 = data['name']['en-US']
        else:
            name1 = "No name available in English"

        print("NAME", name1)
        product = {
            'identifier': data['id'],
            'name': name1,
            'slug': data['slug'],
            'description': description1,
            'type': data['type'],
            'creator': data['authors'][0]['name'],
            'api_name': data['slug'],
            'marketplace': "mozilla",
            'url': data['url'],
            'categories': categories,
            'keywords': keywords
        }
        return product   

    def parseProducts( data):
        products = []
        for product in data['results']:
            products.append(MozillaParser.parseSingleProduct(product))
        return products
    
    def parseGUIDs(data):
        guids = ""
        for product in data['results']:
            guids = guids+(',')
            guids = guids+(product['addon']['guid'])
        print("GUIDS", guids, "GUIDS")
        return guids
    
    def getLanguages(data):
        languages = []
        for language in data['languages']:
            languages.append(language)
        return languages