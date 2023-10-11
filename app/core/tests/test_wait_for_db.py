from unittest.mock import patch
from django.core.management import call_command
from django.test import SimpleTestCase
from psycopg2 import OperationalError as Psycopg2Error
from django.db.utils import OperationalError


@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """
    A test class for the 'wait_for_db' management command.
    This class contains unit tests for checking the behavior of the 'wait_for_db' command.
    Attributes:
        patched_check (MagicMock): A mock object for simulating Command.check.
    """
    def test_wait_for_db_ready(self, patched_check):
        """
        Test the 'wait_for_db' command when the database is immediately ready.
        This test ensures that the command works correctly when the database is available right away.
        Parameters:
            patched_check (MagicMock): A mock object for simulating Command.check.
        """
        patched_check.return_value = True
        call_command('wait_for_db')
        patched_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """
        Test the 'wait_for_db' command with a simulated delay in database availability.
        This test checks how the command handles a scenario where the database is initially unavailable
        and becomes available after a certain number of retries.
        Parameters:
            patched_sleep (MagicMock): A mock object for simulating time.sleep.
            patched_check (MagicMock): A mock object for simulating Command.check.
        """
        patched_check.side_effect = [Psycopg2Error] * 1 + \
                                    [OperationalError] * 2 + [True]
        call_command('wait_for_db')
        self.assertEqual(patched_check.call_count, 4)
        patched_check.assert_called_with(databases=['default'])




