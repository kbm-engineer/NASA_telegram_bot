import requests


earth_date = '2023-06-10'
api_key = 'DnZoGGbzG4v2pa2rBT1NT2egAWTeSCakqjxVWvf7'
r = requests.get(f'https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?earth_date={earth_date}&api_key={api_key}')
json_text = r.json()
link = json_text.get('photos')[0].get('img_src')
print(link)