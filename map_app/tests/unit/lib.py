from __future__ import unicode_literals, absolute_import

from mock import MagicMock, call, Mock

from django.test import TestCase

from ...lib import FusionTableMixin
from ...models import Address

class FusionTableMixinTestCase(TestCase):

    def setUp(self):
        self.fusion_table_mixin = FusionTableMixin
        self.table_id = 'test-table-id'
        self.service = MagicMock(name='Service')
        self.service.query.return_value = MagicMock(name='Query')
        self.service.query().sql.return_value = MagicMock(name='sql')
        self.execute_mock = MagicMock(name='execute')
        self.address_1 = Address(address='Test 1')
        self.address_2 = Address(address='Test 2')

    @property
    def addresses(self):
        return [self.address_1, self.address_2]

    @property
    def get_next_query(self):
        for address in self.addresses:
            yield ("INSERT INTO {table_id} "
             "(address, latitude, longitude,"
             " computed_address) VALUES "
             "\"('{address}', , , '')\""
             .format(table_id=self.table_id, address=address))

    def test_bulk_save(self):
        expected_queries = list(self.get_next_query)
        def query_side_effect(sql):
            self.assertIn(sql, expected_queries)
            return self.execute_mock

        self.service.query().sql.side_effect = query_side_effect
        self.fusion_table_mixin.bulk_save(self.addresses, self.service,
                                          self.table_id)

        self.service.query.assert_called()
        self.service.query().sql.assert_has_calls([
            call(sql=expected_queries[0]),
            call(sql=expected_queries[1])
        ])






