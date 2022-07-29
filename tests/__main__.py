import unittest
from tests.test_code_format import CodeFormatTestCase
from tests.test_data_converted import ConvertSapDocumentTestCase
from tests.test_credit_note import SapCreditNoteTestCase
from tests.test_api import SapApiTestCase


__all__ = [
    "CodeFormatTestCase",
    "ConvertSapDocumentTestCase",
    "SapCreditNoteTestCase",
    "SapApiTestCase"
]
if __name__ == "__main__":
    unittest.main(verbosity=2)
