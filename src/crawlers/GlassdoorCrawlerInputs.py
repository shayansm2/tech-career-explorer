class GlassdorrCrawlerInputs(object):
    def __init__(self, keyword: str, location: str, page: int = 1) -> None:
        self.keyword = keyword
        location_data = self._get_location_data(location)
        self.location_id = location_data['location_id']
        self.location_type = location_data['location_type']
        self.page = page

    # todo
    @staticmethod
    def _get_location_data(location_name: str):
        return {
            'location_id': 178,
            'location_type': 'COUNTRY',
        }