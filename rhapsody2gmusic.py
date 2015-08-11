from gmusicapi import Mobileclient, Musicmanager
from operator import itemgetter
import json
import urllib2
import string
from bs4 import BeautifulSoup
from getpass import getpass
import sys

def parse_config():
    config = {} 
    try:
        with open(".config") as f:
            lines = f.readlines()
            for i in lines:
                words = i.split()
                if words[0] == 'email':
                    config['email'] = words[1]
                elif words[0] == 'password':
                    config['password'] = i.split(' ',1)[1]
                elif words[0] == 'android_device_id':
                    config['android_device_id'] = i.split(' ',1)[1].strip()
            if 'password' not in config:
                # If Password not in Config, ask for it
                config['password'] = getpass()
    except IOError:
        print "Can't find .config file"
        return False
    return config

config = parse_config()
if not config:
    config = {}
    config['email'] = raw_input('email:')
    config['password'] = getpass()
    config['android_device_id'] = raw_input('your android device id:')

# Ask for shareable URL of playlist, e.g.http://www.rhapsody.com/playlist/mp.145164964
rhapsody_url = raw_input('URL of your rhapsody playlist:')

page = urllib2.urlopen(rhapsody_url).read()
soup = BeautifulSoup(page, 'html.parser')
if not soup.find('h1', {'id': 'page-name'}):
    print 'Playlist not found'
    sys.exit()

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

#Now Google
mc = Mobileclient()
mc.login(config['email'], config['password'], config['android_device_id'])

hits = 0 
misses = 0 
track_ids = []
failed_queries = []
for q in queries:
    search = mc.search_all_access(q, max_results=5)
    g_songs = search['song_hits']
    if any(g_songs):
        sort_by_score = sorted(g_songs, key=itemgetter('score'), reverse=True)
        #print sort_by_score[0]['track']['storeId']
        track_ids.append(sort_by_score[0]['track']['storeId'])
        hits += 1
    else:
        misses += 1
        failed_queries.append(q)

print 'Hits: {0} Misses: {1}'.format(hits,misses)
if misses > 0:
    print 'Unable to find a Google Music match for these tracks:'
    print failed_queries

playlist_id = mc.create_playlist(playlist_name)
mc.add_songs_to_playlist(playlist_id, track_ids)
print 'Playlist "{}" successfully added to Google Music with {} songs'.format(playlist_name, hits)
