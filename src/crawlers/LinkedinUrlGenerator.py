from urllib.parse import urlencode, urljoin

class LinkedinUrlGenerator(object):
    def __init__(self) -> None:
        self.url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search'
        self.args = {}

    # todo
    def set_location(self):
        return self
    
    def set_offset(self, offset: int):
        self.args['start'] = offset
        return self

    def set_geo_id(self, geoid: int):
        self.args['geoId'] = geoid
        return self

    def set_keywords(self, keywords: str):
        self.args['keywords'] = keywords
        return self

    def get(self):
        return urljoin(self.url, '?' + urlencode(self.args))

