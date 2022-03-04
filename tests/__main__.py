import unittest
from tests.test_code_format import CodeFormatTestCase
from tests.test_data_converted import ConvertSapDocumentTestCase


__all__ = [
    "CodeFormatTestCase",
    "ConvertSapDocumentTestCase"
]
if __name__ == "__main__":
    unittest.main(verbosity=2)
