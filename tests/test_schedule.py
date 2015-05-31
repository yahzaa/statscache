import time
import unittest

import freezegun
import nose.tools
import datetime


from statscache.schedule import Schedule, Frequency


class TestSchedule(unittest.TestCase):

    @freezegun.freeze_time('2012-01-14 00:00:00')
    def test_basic(self):
        s = Schedule(minute=[15], hour=[5])
        self.assertEquals(float(s), 5 * 60 * 60 + 15 * 60 + 1)

    @freezegun.freeze_time('2012-01-14 00:00:00')
    def test_one_second(self):
        s = Schedule()
        self.assertEquals(float(s), 1)

    @freezegun.freeze_time('2012-01-14 00:00:01')
    def test_one_second_ahead(self):
        s = Schedule()
        self.assertEquals(float(s), 1)

    @freezegun.freeze_time('2012-01-14 00:00:00')
    def test_two_seconds(self):
        s = Schedule(second=[2])
        self.assertEquals(float(s), 2)

    @freezegun.freeze_time('2012-01-14 12:00:00')
    def test_wrap_day(self):
        s = Schedule(minute=[15], hour=[5])
        self.assertEquals(float(s), 17 * 60 * 60 + 15 * 60 + 1)

    @freezegun.freeze_time('2012-01-14 12:15:00')
    def test_wrap_day_match_minute(self):
        s = Schedule(minute=[15], hour=[5])
        self.assertEquals(float(s), 17 * 60 * 60 + 1)

    @freezegun.freeze_time('2012-01-14 12:16:00')
    def test_wrap_day_wrap_minute(self):
        s = Schedule(minute=[15], hour=[5])
        self.assertEquals(float(s), 16 * 60 * 60 + 59 * 60 + 1)

    @freezegun.freeze_time('2012-01-14 00:00:00')
    def test_working_with_time_sleep(self):
        s = Schedule(second=[1])
        time.sleep(s)  # Let's just make sure this doesn't crash

    @freezegun.freeze_time('2012-01-14 04:00:00')
    def test_prev_day_wrap_with_hour_minute_second_roundup(self):
        s = Schedule(minute=[15], hour=[5])
        self.assertEquals(
            float(
                (s.prev() - datetime.datetime.strptime(
                    '2012-01-13', '%Y-%m-%d')).total_seconds()),
            5 * 60 * 60 + 15 * 60 + 59)

    @freezegun.freeze_time('2012-01-14 05:19:27')
    def test_prev_second_roundup(self):
        s = Schedule(hour=[5], minute=[10, 20], second=[0, 15, 30, 45])
        self.assertEquals(
            float(
                (s.prev() - datetime.datetime.strptime(
                    '2012-01-14', '%Y-%m-%d')).total_seconds()),
            5 * 60 * 60 + 10 * 60 + 45)

    @freezegun.freeze_time('2012-01-14 04:19:27')
    def test_prev_minute_second_roundup(self):
        s = Schedule(hour=[3, 5], minute=[10, 20], second=[0, 15, 30, 45])
        self.assertEquals(
            float(
                (s.prev() - datetime.datetime.strptime(
                    '2012-01-14', '%Y-%m-%d')).total_seconds()),
            3 * 60 * 60 + 20 * 60 + 45)

    @nose.tools.raises(ValueError)
    def test_wrap_invalid_item(self):
        Schedule(minute=['lol'])

    @nose.tools.raises(TypeError)
    def test_wrap_invalid_item_int(self):
        Schedule(minute=1)


class TestFrequecny(unittest.TestCase):

    def test_second_init_success(self):
        f = Frequency('10s')
        self.assertEqual(str(f), '10s')
        f = Frequency('60s')
        self.assertEqual(str(f), '60s')

    def test_minute_init_success(self):
        f = Frequency('10m')
        self.assertEqual(str(f), '10m')
        f = Frequency('60m')
        self.assertEqual(str(f), '60m')

    def test_hour_init_success(self):
        f = Frequency('24h')
        self.assertEqual(str(f), '24h')

    def test_second_init_error(self):
        self.assertRaises(ValueError, Frequency, '0s')
        self.assertRaises(ValueError, Frequency, '70s')

    def test_minute_init_error(self):
        self.assertRaises(ValueError, Frequency, '0m')
        self.assertRaises(ValueError, Frequency, '70m')

    def test_hour_init_error(self):
        self.assertRaises(ValueError, Frequency, '0h')
        self.assertRaises(ValueError, Frequency, '25h')

    def test_init_error_with_bad_values(self):
        self.assertRaises(ValueError, Frequency, 'lol')
        self.assertRaises(ValueError, Frequency, '-10s')
        self.assertRaises(ValueError, Frequency, '10d')
        self.assertRaises(ValueError, Frequency, '10h20m')
        self.assertRaises(ValueError, Frequency, '1.3s')


if __name__ == '__main__':
    unittest.main()
