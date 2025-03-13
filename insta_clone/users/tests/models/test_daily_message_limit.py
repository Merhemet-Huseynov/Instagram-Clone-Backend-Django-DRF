import pytest
from datetime import timedelta
from users.models.daily_message_limit import DailyMessageLimit


@pytest.mark.django_db
class TestDailyMessageLimit:
    
    def test_default_values(self):
        """
        Test the default values for DailyMessageLimit model.
        """
        limit_obj = DailyMessageLimit.objects.create()

        assert limit_obj.limit == 3                               # Default limit value
        assert limit_obj.expiration_time == timedelta(minutes=3)  # Default expiration_time value
        assert limit_obj.reset_time == timedelta(hours=24)        # Default reset_time value
    
    def test_custom_values(self):
        """
        Test the functionality of setting custom values for DailyMessageLimit model.
        """
        custom_limit = 5
        custom_expiration_time = timedelta(minutes=5)
        custom_reset_time = timedelta(hours=12)

        limit_obj = DailyMessageLimit.objects.create(
            limit=custom_limit,
            expiration_time=custom_expiration_time,
            reset_time=custom_reset_time
        )

        assert limit_obj.limit == custom_limit
        assert limit_obj.expiration_time == custom_expiration_time
        assert limit_obj.reset_time == custom_reset_time

    def test_str_method(self):
        """
        Test the string representation of DailyMessageLimit model.
        """
        limit_obj = DailyMessageLimit.objects.create()

        expected_str = "Daily Limit: 3 Expiration Time: 0:03:00 Reset Time: 1 day, 0:00:00"
        assert str(limit_obj) == expected_str
