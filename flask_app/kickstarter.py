import requests
from .models import DB
from bs4 import BeautifulSoup
import re


def request_data(url):
    """
    Requests data from a html page
    :param url:
    :return:
    """
    slug = re.search('/projects/(.*)\?', url).group(1)

    session = requests.Session()
    request = session.get(url)
    soup = BeautifulSoup(request.text, 'html.parser')
    xcsrf = soup.find("meta", {"name": "csrf-token"})["content"]

    query = """
    query GetEndedToLive($slug: String!) {
      project(slug: $slug) {
          id
          name
          creator {
            name
            location {
                displayableName  
            }
            launchedProjects {
                totalCount
            }
          }
          isProjectWeLove
          category {
                name
          }
          location {
                displayableName  
            }
          isSharingProjectBudget
          backersCount
          percentFunded 
          goal {
                currency
                amount
          }
          pledged {
                currency
                amount
          }
          deadlineAt
          duration
          stateChangedAt
          commentsCount
          state
          currency
          deadlineAt
          showCtaToLiveProjects
          state
          description
          url
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

    return r.json()
