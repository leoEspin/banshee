#!/usr/bin/python

"""
Copyright (c) 2009 Wolfgang Steitz
Additional adaptations by Karl Voit
https://askubuntu.com/a/127199
https://karl-voit.at/2020/05/08/Migration-Bashee-to-Rhythmbox/

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software Foundation,
Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA
"""

import sys
import sqlite3
from lxml import etree

RB_DB = 'rhythmdb.xml'
BA_DB = 'banshee.db'

class banshee_db():
    def __init__(self, file):
        self.con = sqlite3.connect(file)

    def get_song_info(self, url):
        try:
            res = self.con.execute(
                'select Rating, Playcount, DateAddedStamp, LastPlayedStamp, Comment from CoreTracks where uri = ?',
                (url,) ).fetchone() # https://docs.python.org/3/library/sqlite3.html#sqlite3-placeholders
            if res is None:         # the tuple is sqlite3 weirdness. see doc above   
                return None, None, None, None, None
            else:
                return res
        except:
            return None, None, None, None, None


banshee = banshee_db(BA_DB)

tree = etree.parse(RB_DB)
root = tree.getroot()
for song in root:
    if song.get("type") == 'song':
        #print('song: ' + str(song))

        rating = None
        playcount = None
        dateadded = None   ## Rhythmbox: first-seen
        lastplayed = None  ## Rhythmbox: last-played
        comment = None     ## Rhythmbox: comment

        for attr in song:
            if attr.tag == 'location':
                location = attr.text
            if attr.tag == 'rating':
                rating = attr.text
            if attr.tag == 'play-count':
                playcount = int(attr.text)
                song.remove(attr)
            if attr.tag == 'first-seen':
                dateadded = attr.text
                song.remove(attr)
            if attr.tag == 'last-played':
                lastplayed = attr.text
                song.remove(attr)
            if attr.tag == 'comment':
                comment = attr.text
                song.remove(attr)


        rating_banshee, playcount_banshee, \
            dateadded_banshee, lastplayed_banshee, \
            comment_banshee = banshee.get_song_info(location)

        if rating is None: # no rating in rhythmbox XML
            if not (rating_banshee == 0 or rating_banshee is None):
                rating = rating_banshee
                #print('set rating to ' + str(rating_banshee))

        if not (playcount_banshee == 0 or playcount_banshee is None):
            if playcount is None:
                playcount = playcount_banshee
                #print('set playcount to ' + str(playcount_banshee))
            else:
                playcount += playcount_banshee

        # insert rating into rb db
        if rating is not None:
            element = etree.Element('rating')
            element.text = str(rating)
            song.append(element)

        # update playcount of rb db
        if playcount is not None:
            element = etree.Element('play-count')
            element.text = str(playcount)
            song.append(element)

        if dateadded_banshee is not None:
            #print('set dateadded to ' + str(dateadded_banshee))
            element = etree.Element('first-seen')
            element.text = str(dateadded_banshee)
            song.append(element)

        if lastplayed_banshee is not None:
            #print('set last-played to ' + str(lastplayed_banshee))
            element = etree.Element('last-played')
            element.text = str(lastplayed_banshee)
            song.append(element)

        if comment_banshee is not None:
            #print('set comment to ' + str(comment_banshee))
            element = etree.Element('comment')
            element.text = str(comment_banshee)
            song.append(element)

tree.write(RB_DB)