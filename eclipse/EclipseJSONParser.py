from MonitoringSoftwareMarketplaces.JSONParser import JSONParser
import xml.etree.ElementTree as ET

class EclipseJSONParser(JSONParser):
    """Extract text from a PDF"""
    def load_data_source(self, path: str, file_name: str):
        """Overrides InformalInterface.load_data_source()"""
        pass

    def read_data(self, full_file_path: str):
        """Overrides InformalInterface.read_data()"""
        pass

    def extractCategories(response):
        categories = []
        root = ET.fromstring(response.text)  # Parse XML string
        for market_elem in root.findall('market'):
            for category in market_elem.findall('category'):
                category = {
                    'identifier': category.get('id'),
                    'url': category.get('url'),
                    'name': category.get('name'),
                    'market': market_elem.get('id'),
                    'marketplace': 'eclipse'
                }
                categories.append(category)

        return categories

    
    def extractMarkets(response):
        markets = []
        root = ET.fromstring(response.text)  # Parse XML string
        for market_elem in root.findall('market'):
            market = {
                'identifier': market_elem.get('id'),
                'url': market_elem.get('url'),
                'name': market_elem.get('name'),
                'marketplace': 'eclipse'
            }
            markets.append(market)

        return markets
    
    
    def extractProductsByParameter(response, typeOfSearch):
        products = []
        root = ET.fromstring(response.text)
        element = root.find(typeOfSearch)
        for product_elem in element.findall('node'):
            #Añadimos las categorias a las que pertenece
            #Añadimos las categorias a las que pertenece
            categories = []
            if(product_elem.find('categories')):
                for category in product_elem.find('categories').findall('category'):
                    categories.append(category.get('name'))
        
            #Añadimos las categorias a las que pertenece
            tags = []
            if(product_elem.find('tags')):
                for tag in product_elem.find('tags').findall('tag'):
                    tags.append(tag.get('name'))
            
            #Añadimos una pequeña descripcion del producto
            description_elem = product_elem.find('body')
            desc = ""
            if description_elem is not None:
                desc = description_elem.text.strip()
            #Añadir atributos del producto
            product = {
            'identifier': product_elem.get('id'),
            'url': product_elem.get('url'),
            'name': product_elem.get('name'),
            'categories': categories,
            'keywords': tags,
            'description': desc,
            'type': product_elem.find('type').text,
            'creator': product_elem.find('owner').text,
            'api_name': "",
            'marketplace': 'eclipse'
        }
            products.append(product)
        print("Conjunto productos", products)
        return products
    
    def extractSingleProduct(response):
        product = {}
        root = ET.fromstring(response.text)
        product_elem = root.find('node')
       
        #Añadimos las categorias a las que pertenece
        categories = []
        for category in product_elem.find('categories').findall('category'):
            print(category.get('name'))
            categories.append(category.get('name'))
       
        #Añadimos las categorias a las que pertenece
        tags = []
        for tag in product_elem.find('tags').findall('tag'):
            print("tag" ,tag.get('name'))
            tags.append(tag.get('name'))
        
        #Añadimos una pequeña descripcion del producto
        description_elem = product_elem.find('body')
        desc = ""
        if description_elem is not None:
            desc = description_elem.text.strip()

        #Añadir atributos del producto
        product = {
            'identifier': product_elem.get('id'),
            'url': product_elem.get('url'),
            'name': product_elem.get('name'),
            'categories': categories,
            'keywords': tags,
            'description': desc,
            'type': product_elem.find('type').text,
            'creator': product_elem.find('owner').text,
            'api_name': "",
            'marketplace': 'eclipse'
        }
        return product