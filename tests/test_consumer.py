"""Unit tests for statscache consumer."""

import mock
from nose.tools import eq_

import statscache.consumer
from . import BaseUnitTestCase


class TestStatsConsumer(BaseUnitTestCase):

    """
    Test stats consumer.
    """

    def setUp(self):
        """Setup consumer and session."""
        super(TestStatsConsumer, self).setUp()

        class FakeHub(object):
            config = self.fedmsg_config

            def subscribe(*args, **kwargs):
                pass

        statscache.consumer.StatsConsumer._initialized = True
        self.consumer = statscache.consumer.StatsConsumer(FakeHub())
        self.session = statscache.utils.init_model(self.db_uri)

    @mock.patch('statscache.utils.datagrep', return_value=[])
    def test_plugins(self, func):
        """Check if messages are being queued."""
        for fixture in self.fixtures:
            msg = fixture['msg']
            self.consumer.consume(msg)
            eq_(self.session.Message.query.count(), 1)

    def test_consume(self):
        """Test consume method of StatsConsumer."""
        for plugin in self.consumer.plugins:
            plugin.process = mock.Mock()

         # Check that 'process' method of all plugins was called with the
         # same message.
        for fixture in self.fixtures:
            msg = fixture['msg']
            self.consumer.consume(msg)
            for plugin in self.consumer.plugins:
                plugin.process.assert_called_with(msg)
