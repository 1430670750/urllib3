from __future__ import absolute_import

import mock
import sys
if sys.version >= (2, 7):
    import unittest
else:
    import unittest2 as unittest

import urllib3
from urllib3.exceptions import EmptyPoolError
from urllib3.packages.six.moves import queue

class BadError(Exception):
    """
    This should not be raised.
    """
    pass


class TestMonkeypatchResistance(unittest.TestCase):
    """
    Test that connection pool works even with a monkey patched Queue module,
    see obspy/obspy#1599, kennethreitz/requests#3742, shazow/urllib3#1061.
    """
    def test_queue_monkeypatching(self):
        with mock.patch.object(queue, 'Empty', BadError):
            http = urllib3.HTTPConnectionPool(host="localhost", block=True)
            self.addCleanup(http.close)
            first_conn = http._get_conn(timeout=1)
            self.assertRaises(EmptyPoolError, http._get_conn, timeout=1)


if __name__ == '__main__':
    unittest.main()
