#!/usr/bin/env python3

import unittest

import pytest

from daltonlens import generate, simulate


pytest.importorskip("Geometry3D", reason="Geometry3D is optional for Ishihara plates")


class TestIshiharaPlate(unittest.TestCase):
    def test_protanopia(self):
        im = generate.ishihara_plate_dichromacy(
            simulate.Deficiency.PROTAN, "Protan Severity 1.0"
        )
        self.assertEqual(im.shape[-1], 3)

    def test_protanomaly(self):
        im = generate.ishihara_plate_dichromacy(simulate.Deficiency.PROTAN)
        self.assertEqual(im.shape[-1], 3)

    def test_deuteranopia(self):
        im = generate.ishihara_plate_dichromacy(simulate.Deficiency.DEUTAN)
        self.assertEqual(im.shape[-1], 3)

    def test_tritanopia(self):
        im = generate.ishihara_plate_dichromacy(simulate.Deficiency.TRITAN)
        self.assertEqual(im.shape[-1], 3)


if __name__ == "__main__":
    unittest.main()
