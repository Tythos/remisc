"""Unit tests for the default service operations/responses.
"""

import unittest
from remisc import service

class DefResTests(unittest.TestCase):
    def test_root(self):
        svc = service.Service()
        svc._root(None, None)
        
    def test_help(self):
        svc = service.Service()
        res = svc._help(None, None)
        
    def test_null(self):
        svc = service.Service()
        res = svc._null(None, None)
        self.assertTrue(res == '')
        
if __name__ == '__main__':
    unittest.main()
