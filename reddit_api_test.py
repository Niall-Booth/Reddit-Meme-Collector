import requests
import pandas as pd
import time

reddit_secret_key = ''#My redidit secret key goes here
reddit_personal_key = ''#My reddit personal key goes here

auth = requests.auth.HTTPBasicAuth(reddit_personal_key, reddit_secret_key)

data = {
    'grant_type' : 'password',
    'username' : '',#My username goes here
    'password' : ''#My password goes here
}

api_headers = {'User-Agent' : 'MyAPI/0.0.1'}

res = requests.post('https://www.reddit.com/api/v1/access_token', auth=auth, data=data, headers=api_headers)

TOKEN = res.json()['access_token']

api_headers['Authorization'] = f'bearer {TOKEN}'

response = requests.get('https://oauth.reddit.com/r/memes/hot', headers=api_headers, params={'limit' : '100'}).json()

all_posts = []

for post in response['data']['children']:
    if len(post['data']['link_flair_richtext']) > 0: continue

    all_posts.append([post['data']['title'], post['data']['url']])

memes_csv = pd.read_csv('memes.csv')

for x in range(0, len(all_posts)):
    memes_csv.loc[len(memes_csv.index)] = [[x+1], all_posts[x][0], all_posts[x][1]]

memes_csv.to_csv("memes.csv", index=False)

time.sleep(5)
print('deleting')
time.sleep(1)

for x in range(0, len(all_posts)):
    memes_csv = pd.read_csv('memes.csv')
    memes_csv.drop(memes_csv[memes_csv['Title'] == all_posts[x][0]].index, inplace = True)
    print(f'{all_posts[x][0]}: deleted')
    memes_csv.to_csv("memes.csv", index=False)
    time.sleep(1)