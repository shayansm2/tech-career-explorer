class GlassdoorCrawlerInputs(object):
    def __init__(self, keyword: str, location: str, page: int = 1) -> None:
        self.keyword = keyword
        location_data = self._get_location_data(location)
        self.location_id = location_data['location_id']
        self.location_type = location_data['location_type']
        self.page = page
        self.age = None

    def set_age_in_days(self, age: int):
        self.age = age
        return self
    
    def set_page(self, page: int):
        self.page = page
        return self

    # todo check with jobspy
    @staticmethod
    def _get_location_data(location_name: str):
        return {
            'location_id': 178,
            'location_type': 'COUNTRY',
        }