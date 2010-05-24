#!/usr/bin/python

import getopt
import markdown
import mimetypes
import os.path
import sys

import gdata.sample_util
import gdata.sites.client
import gdata.sites.data

SOURCE_APP_NAME = 'pkeane-GoogleSites-v1'
GOOGLE_USERNAME = 'pjkeane'
GOOGLE_PASSWORD = 'change_this'
SITE = 'pkeaneprojects'
PARENT_PAGE = 'notes'

def get_feed_from_path(client,path):
    uri = '%s?path=%s' % (client.MakeContentFeedUri(), path)
    return client.GetContentFeed(uri=uri)

def get_html_from_markdown_file(filename):
    f = open(filename)
    md = markdown.Markdown()
    return md.convert(f.read())

def get_client(site,username,password):
    client = gdata.sites.client.SitesClient(source=SOURCE_APP_NAME, site=site)
    client.ssl = True  # Force API requests through HTTPS
    client.ClientLogin(username,password,client.source)
    return client

if __name__ == '__main__':
    if 'change_this' == GOOGLE_PASSWORD:
        try:
            from os.path import expanduser
            execfile(expanduser('~/.google_conf'))
        except:
            print 'invalid password'
            sys.exit()
        
    try:
        filename = sys.argv[1]
    except:
        print 'need filename'
        sys.exit()

    html = get_html_from_markdown_file(filename)

    client = get_client(SITE,GOOGLE_USERNAME,GOOGLE_PASSWORD)
  
    path = '/'+PARENT_PAGE 
    print 'Fetching parent page by its path: ' + path
    parent_feed = get_feed_from_path(client,path)

    entry = client.CreatePage('webpage',filename, html=html, parent=parent_feed.entry[0])
    print 'Posted! '+filename
  
