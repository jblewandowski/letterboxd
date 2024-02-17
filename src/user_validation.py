def user_validation(user):
    from bs4 import BeautifulSoup
    import requests
    try:
        user_name = BeautifulSoup(requests.session().get(f'https://letterboxd.com/{user}').content, 'html.parser').find('span', {'class':'displayname tooltip'}).text
    except:
        user_name = False
    return user_name