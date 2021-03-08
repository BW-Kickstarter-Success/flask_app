import requests
from geopy.geocoders import Nominatim
from geopy.point import Point
# from geopy.geocoders import GoogleV3
from currency_converter import CurrencyConverter
from datetime import datetime, timedelta
from .models import DB, Project
from bs4 import BeautifulSoup
import re


# DB = models.DB

def add_new_project(url):
    """
    Requests data from a html page
    :param url:
    :return:
    """
    try:
        slug = re.search('/projects/(.*)\?', url).group(1)

        session = requests.Session()
        request = session.get(url)
        soup = BeautifulSoup(request.text, 'html.parser')
        xcsrf = soup.find("meta", {"name": "csrf-token"})["content"]

        query = """
        query Campaign($slug: String!) {
        project(slug: $slug) {
            id  
            name
            category {
                    name
                    parentCategory {
                        name
                    }
            }
            location {
                    displayableName  
                }
            goal {
                    currency
                    amount
            }
            deadlineAt
            duration
            state
            description
            __typename
        }
        }"""

        r = session.post("https://www.kickstarter.com/graph",
                        headers={
                            "x-csrf-token": xcsrf
                        },
                        json={
                            "query": query,
                            "variables": {
                                "slug": slug
                            }
                        })

        result = r.json()['data']['project']

        # get parameters from the data
        id = result['id']
        name = result['name']
        category = result['category']['name'].lower()
        parent_category = result['category']['parentCategory']['name'].lower()
        category_slug = parent_category + "/" + category
        town, country_code = town_country(result['location']['displayableName'])
        goal_amount = to_usd(result['goal']['amount'], result['goal']['currency'])
        deadline_at = datetime.fromtimestamp(result['deadlineAt'])
        launched_at = when_launched(result['duration'], result['deadlineAt'])
        description = result['description']

        # add new project to the database
        db_project = Project(id=id, name=name, category_name=category,
                             category_slug=category_slug, goal_amount=goal_amount,
                             description=description, launched_at=launched_at,
                             deadline_at=deadline_at, country_code=country_code,
                             town=town)
        DB.session.add(db_project)

    except Exception as e:
        print("Error processing {}: {}".format(url, e))
        raise e

    else:
        # return result['location']['displayableName']
        DB.session.commit()


def to_usd(amount, currency):
    """ Converts any sum into dollar
     :param amount : amount of money (int)
     :param currency: currency (int)
     :return: int
     """
    c = CurrencyConverter(fallback_on_missing_rate=True, fallback_on_wrong_date=True)
    dollar = c.convert(amount, currency, 'USD', date=datetime.today())
    return dollar


def when_launched(duration, deadline):
    """Calculate launchedAt based on the deadline and duration
    :param duration: duration (int)
    :param deadline: deadline (datetime)
    :return: launchedAt (datetime)
    """
    duration = timedelta(days=duration)
    deadline = datetime.fromtimestamp(deadline)
    launched_at = deadline - duration
    return launched_at


def town_country(location):
    """
    :param location:
    :return:
    """
    geolocator = Nominatim(user_agent="flask_app")
    address, (latitude, longitude) = geolocator.geocode(location, language="en")
    location = geolocator.reverse((latitude, longitude), language="en")
    if 'city' in location.raw['address']:
        country = location.raw['address']['city'] + ', ' + location.raw['address']['country']
    else:
        country = location.raw['address']['hamlet'] + ', ' + location.raw['address']['country']
    country_code = location.raw['address']['country_code'].upper()
    return country, country_code
    # return location.raw['address']



if __name__ == 'main':
    pass

