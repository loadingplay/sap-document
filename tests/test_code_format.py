import os
import unittest
from pycodestyle import StyleGuide


class CodeFormatTestCase(unittest.TestCase):
    def test_conformance(self):
        """ Test that we conform to PEP-8. """
        style = StyleGuide()
        result = style.check_files([
            os.path.join(os.getcwd(), 'tests'),
        ])
        self.assertEqual(
            result.total_errors,
            0,
            (
                "Found code style errors (and warnings).\n"
                "ejecuta pycodestyle src "
                "&& pycodestyle tests "
                " en el proyecto"
            )
        )
