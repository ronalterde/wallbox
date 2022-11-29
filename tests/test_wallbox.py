#!/usr/bin/env python3

from .context import wallbox
import unittest
from unittest.mock import MagicMock


class WallboxTest(unittest.TestCase):
    """Wallbox register read/write tests."""

    def test_is_register_readable(self):
        self.assertTrue(wallbox.core.is_register_readable(4))
        self.assertTrue(wallbox.core.is_register_readable(257))
        self.assertFalse(wallbox.core.is_register_readable(258))

    def test_is_register_writeable(self):
        self.assertFalse(wallbox.core.is_register_writeable(4))
        self.assertTrue(wallbox.core.is_register_writeable(257))
        self.assertTrue(wallbox.core.is_register_writeable(258))

    def test_read_register(self):
        mock = MagicMock()
        mock.read_register.return_value = 42
        wb = wallbox.core.Wallbox(mock, wallbox.core.registers)

        self.assertEqual(wb.read_register(4), 42)
        mock.read_register.assert_called_once_with(4, functioncode=4)

        mock.reset_mock()
        self.assertEqual(wb.read_register(257), 42)
        mock.read_register.assert_called_once_with(257, functioncode=3)

    def test_disable_watchdog(self):
        mock = MagicMock()
        wb = wallbox.core.Wallbox(mock, wallbox.core.registers)

        wb.disable_watchdog()
        mock.write_register.assert_called_once_with(257, 0, functioncode=6)

    def test_enable_standby(self):
        mock = MagicMock()
        wb = wallbox.core.Wallbox(mock, wallbox.core.registers)

        wb.enable_standby(True)
        mock.write_register.assert_called_once_with(258, 0, functioncode=6)

        mock.reset_mock()
        wb.enable_standby(False)
        mock.write_register.assert_called_once_with(258, 4, functioncode=6)

    def test_set_max_current(self):
        mock = MagicMock()
        wb = wallbox.core.Wallbox(mock, wallbox.core.registers)

        wb.set_max_current(60)
        mock.write_register.assert_called_once_with(261, 60, functioncode=6)

        mock.reset_mock()
        wb.set_max_current(160)
        mock.write_register.assert_called_once_with(261, 160, functioncode=6)


if __name__ == '__main__':
    unittest.main()
