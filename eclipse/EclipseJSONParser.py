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
        print(response.text)
        categories = []
        root = ET.fromstring(response.text)  # Parse XML string
        for market_elem in root.findall('market'):
            for category in market_elem.findall('category'):
                category = {
                    'id': category.get('id'),
                    'count': category.get('count'),
                    'url': category.get('url'),
                    'name': category.get('name')
                }
                categories.append(category)

        return categories

    
    def extractMarkets(response):
        markets = []
        root = ET.fromstring(response.text)  # Parse XML string
        for market_elem in root.findall('market'):
            market = {
                'id': market_elem.get('id'),
                'url': market_elem.get('url'),
                'name': market_elem.get('name')
            }
            markets.append(market)

        return markets
    
    
    def extractProductsByParameter(response, typeOfSearch):
        products = []
        root = ET.fromstring(response.text)
        category= root.find(typeOfSearch)
        for product_elem in category.findall('node'):
            #Añadimos las categorias a las que pertenece
            categories = []
            for category in product_elem.find('categories').findall('category'):
                categories.append(category.get('id'))
            #Añadimos una pequeña descripcion del producto
            short_description_elem = product_elem.find('shortdescription')
            desc = ""
            if short_description_elem is not None:
                desc = short_description_elem.text.strip()

            #Añadir atributos del producto
            product = {
                'id': product_elem.get('id'),
                'url': product_elem.get('url'),
                'name': product_elem.get('name'),
                'categories': categories,
                'shortdescription': desc,
            }
            products.append(product)
        return products
    
    def extractSingleProduct(response):
        product = {}
        root = ET.fromstring(response.text)
        product_elem = root.find('node')
        #Añadimos las categorias a las que pertenece
        categories = []
        for category in product_elem.find('categories').findall('category'):
            categories.append(category.get('id'))
        #Añadimos una pequeña descripcion del producto
        short_description_elem = product_elem.find('shortdescription')
        desc = ""
        if short_description_elem is not None:
            desc = short_description_elem.text.strip()

        #Añadir atributos del producto
        product = {
            'id': product_elem.get('id'),
            'url': product_elem.get('url'),
            'name': product_elem.get('name'),
            'categories': categories,
            'shortdescription': desc,
        }
        return product