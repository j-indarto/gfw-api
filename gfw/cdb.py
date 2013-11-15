# Global Forest Watch API
# Copyright (C) 2013 World Resource Institute
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

"""This module supports executing CartoDB queries."""

import json
import logging
import urllib
from google.appengine.api import urlfetch

# CartoDB endpoint:
ENDPOINT = 'http://wri-01.cartodb.com/api/v1/sql'


def execute(query):
    """Exectues supplied query on CartoDB and returns response body as JSON."""
    rpc = urlfetch.create_rpc(deadline=60)
    url = '%s?%s' % (ENDPOINT, urllib.urlencode(dict(q=query)))
    logging.info(url)
    urlfetch.make_fetch_call(rpc, url)
    try:
        result = rpc.get_result()
        if result.status_code == 200:
            return json.loads(result.content)
    except urlfetch.DownloadError, e:
        logging.error("CartoDB SQL API Error: %s %s" % (e, query))
