"""Helper classes for writing tests."""

import unittest

import fedmsg.config
import fedmsg.meta


class BaseUnitTestCase(unittest.TestCase):

    """
    Base test case class.

    Add fixtures and other common functionality.
    """

    def setUp(self):
        """Do setup before running each test case."""
        self.db_uri = "sqlite:////var/tmp/statscache-test.sqlite"

        config = fedmsg.config.load_config([], None)
        fedmsg.meta.make_processors(**config)
        config['statscache.sqlalchemy.uri'] = self.uri
        self.fedmsg_config = config

        self.fixtures = [{
            'username': 'apache',
            'i': 4,
            'timestamp': 1467814080,
            'msg_id': u'2016-55d13473-2e48-4b6e-9542-3bc1882152ef',
            'topic': u'org.release-monitoring.prod.anitya.distro.add',
            'msg': {
                'project': None,
                'message': {
                    'agent': 'foobar',
                    'distro': u'CentOS'
                },
                'distro': {
                    'name': 'CentOS'
                }
            }
        }]
