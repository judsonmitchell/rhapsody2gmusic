from gmusicapi import Mobileclient, Musicmanager
from operator import itemgetter
import pprint
import json
import urllib2
import string
from bs4 import BeautifulSoup
from getpass import getpass
import sys

email = raw_input('email:')
password = getpass()
android_device_id = raw_input('your android device id:')
page = urllib2.urlopen('http://www.rhapsody.com/playlist/mp.153515987').read()
soup = BeautifulSoup(page, 'html.parser')
name = soup.find('h1', {'id': 'page-name'}).text
playlist_name = name.strip("\r\n")

links = soup.select('ul#playlist-tracks li')
queries = []
for link in links:
    #attempt to remove crap like (2007 Remastered LP Version)
    bad_parens = link['track_name'].rfind('(')
    if bad_parens > 1: #so, at least not at beginning of name
        track_name = link['track_name'][:bad_parens]
    else:
        track_name = link['track_name']

    q = link['artist_name'] + ' ' + track_name 
    queries.append(q)

print queries
#sys.exit()
#Now Google
mc = Mobileclient()
mc.login(email, password, android_device_id)

hits = 0 
misses = 0 
track_ids = []
failed_queries = []
for q in queries:
    search = mc.search_all_access(q, max_results=5)
    g_songs = search['song_hits']
    if any(g_songs):
        sort_by_score = sorted(g_songs, key=itemgetter('score'), reverse=True)
        print sort_by_score[0]['track']['storeId']
        track_ids.append(sort_by_score[0]['track']['storeId'])
        hits += 1
    else:
        misses += 1
        failed_queries.append(q)

print 'Hits: {0} Misses: {1}'.format(hits,misses)
print failed_queries

playlist_id = mc.create_playlist(playlist_name)
mc.add_songs_to_playlist(playlist_id, track_ids)
print 'done'
