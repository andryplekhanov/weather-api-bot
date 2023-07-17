import json
from typing import List, Tuple, Dict

from tgbot.config import Config
from tgbot.services.api_request import request_to_api


def parse_cities_group(city: str, config: Config) -> List[Tuple]:
    url = config.misc.geocoder_url
    apikey = config.misc.geocoder_key
    querystring = {'geocode': city, 'apikey': apikey, 'format': 'json'}
    response = request_to_api(url=url, querystring=querystring)
    if response:
        cities = list()
        try:
            result = json.loads(response.text)
            for place in result.get('response').get('GeoObjectCollection').get('featureMember'):
                city = place.get('GeoObject').get('name')
                description = place.get('GeoObject').get('description')
                pos = place.get('GeoObject').get('Point').get('pos')
                cities.append((city, description, pos))
        except Exception:
            cities = None
        return cities
    return None
