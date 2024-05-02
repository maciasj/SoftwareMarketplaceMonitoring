from MonitoringSoftwareMarketplaces.JSONParser import JSONParser

class JSONMozillaParser(JSONParser):
    """Extract text from a PDF"""
    def load_data_source(self, path: str, file_name: str):
        """Overrides InformalInterface.load_data_source()"""
        pass

    def read_data(self, full_file_path: str):
        """Overrides InformalInterface.read_data()"""
        pass
