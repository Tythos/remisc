"""Unit tests for src operator and data exchange model decorators.
"""

import unittest
from src import dxm, service

class OperatorTests(unittest.TestCase):
    def test_isop(self):
        svc = service.Service()
        self.assertTrue(hasattr(svc._root, 'isop'))
        self.assertTrue(svc._root.isop)
        
    def test_getops(self):
        svc = service.Service()
        ops = svc.getAllOps()
        self.assertTrue(len(ops) is 3)
        self.assertTrue('_help' in ops)
        self.assertTrue('_null' in ops)
        self.assertTrue('_root' in ops)

class DxmTests(unittest.TestCase):
    def test_isdxm(self):
        e = dxm.Empty()
        self.assertTrue(hasattr(e, 'isdxm'))
        self.assertTrue(e.isdxm)
        
    def test_getdxms(self):
        svc = service.Service()
        dxms = svc.getAllDxms()
        self.assertTrue(len(dxms) is 1)
        self.assertTrue(dxms[0] is dxm.Empty)

if __name__ == '__main__':
    unittest.main()
