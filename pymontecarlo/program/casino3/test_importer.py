#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Philippe T. Pinard"
__email__ = "philippe.pinard@gmail.com"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2012 Philippe T. Pinard"
__license__ = "GPL v3"

# Standard library modules.
import unittest
import logging
import os

# Third party modules.

# Local modules.
from pymontecarlo.testcase import TestCase

from pymontecarlo.options.options import Options
from pymontecarlo.options.detector import TrajectoryDetector, ElectronFractionDetector
from pymontecarlo.program.casino3.importer import Importer

# Globals and constants variables.
from pymontecarlo.options.particle import ELECTRON
from pymontecarlo.options.collision import NO_COLLISION
from pymontecarlo.results.result import EXIT_STATE_ABSORBED

class TestImporter(TestCase):

    def setUp(self):
        TestCase.setUp(self)

        self.testdata = os.path.join(os.path.dirname(__file__),
                                     'testdata', 'test1')

        self.i = Importer()

    def tearDown(self):
        TestCase.tearDown(self)

    def testskeleton(self):
        self.assertTrue(True)

    def test_detector_trajectory(self):
        # Create
        ops = Options(name='test1')
        ops.beam.energy_eV = 20e3
        ops.detectors['trajectories'] = TrajectoryDetector(50)

        # Import
        filepath = os.path.join(self.testdata, 'gold_15kev.cas')
        results = self.i.import_cas(ops, filepath)

        # Test
        result = results['trajectories']
        self.assertEqual(14689, len(result))

        trajectory = list(result)[0]
        self.assertTrue(trajectory.is_primary())
        self.assertFalse(trajectory.is_secondary())
        self.assertIs(ELECTRON, trajectory.particle)
        self.assertIs(NO_COLLISION, trajectory.collision)
        self.assertEqual(EXIT_STATE_ABSORBED, trajectory.exit_state)
        self.assertEqual(851, len(trajectory.interactions))
        self.assertEqual(5, trajectory.interactions.shape[1])

    def test_detector_electron_fraction(self):
        # Create
        ops = Options(name='test1')
        ops.beam.energy_eV = 20e3
        ops.detectors['electron-fraction'] = ElectronFractionDetector()

        # Import
        filepath = os.path.join(self.testdata, 'gold_15kev.cas')
        results = self.i.import_cas(ops, filepath)

        # Test
        result = results['electron-fraction']

        self.assertAlmostEqual(0.46, result.absorbed[0], 4)
        self.assertAlmostEqual(0.0, result.absorbed[1], 4)

        self.assertAlmostEqual(0.54, result.backscattered[0], 4)
        self.assertAlmostEqual(0.0, result.backscattered[1], 4)

        self.assertAlmostEqual(0.0, result.transmitted[0], 4)
        self.assertAlmostEqual(0.0, result.transmitted[1], 4)

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
