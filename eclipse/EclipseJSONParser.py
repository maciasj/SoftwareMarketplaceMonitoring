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
        print(root)
        for market_elem in root.findall('market'):
            print(market_elem)
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
 