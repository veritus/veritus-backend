def getSoupFromLink(link):
    return BeautifulSoup(requests.get(link).content, features="xml")
