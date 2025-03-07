import pytest
from django.utils.timezone import now, timedelta
from users.models.daily_messages import DailyMessage
from users.models.daily_message_limit import DailyMessageLimit


@pytest.fixture
def setup_daily_limit(db) -> DailyMessageLimit:
    """Creates and returns a DailyMessageLimit instance."""

    return DailyMessageLimit.objects.create(
        limit=3, 
        expiration_time=timedelta(minutes=3), 
        reset_time=timedelta(hours=24)
    )


@pytest.fixture
def email() -> str:
    """Returns a test email address."""

    return "test@example.com"


@pytest.mark.django_db
def test_send_message_success(setup_daily_limit: DailyMessageLimit, email: str) -> None:
    """Tests if a message is sent successfully when under the limit."""

    response = DailyMessage.send_message(email)

    assert response == "Message sent successfully!"
    assert DailyMessage.objects.filter(email=email).count() == 1


@pytest.mark.django_db
def test_daily_limit_exceeded(setup_daily_limit: DailyMessageLimit, email: str) -> None:
    """Tests if the daily limit prevents additional messages from being sent."""

    for _ in range(setup_daily_limit.limit):
        DailyMessage.send_message(email)

    response = DailyMessage.send_message(email)

    assert any(
        msg in response
        for msg in ["You have reached your daily message limit", "Please, try again in"]
    ), f"Expected response to contain limit message but got: {response}"


@pytest.mark.django_db
def test_check_daily_limit(setup_daily_limit: DailyMessageLimit, email: str) -> None:
    """Tests if check_daily_limit correctly detects limit reached."""

    for _ in range(setup_daily_limit.limit):
        DailyMessage.objects.create(
            email=email, 
            message_sent_at=now()
        )

    limit_message = DailyMessage.check_daily_limit(
                        email, 
                        setup_daily_limit.limit, 
                        setup_daily_limit.reset_time
                    )
    
    assert limit_message is not None
    assert "You have reached your daily message limit" in limit_message


@pytest.mark.django_db
def test_message_expiration_time(setup_daily_limit: DailyMessageLimit, email: str) -> None:
    """Tests if the expiration time prevents messages from being sent too frequently."""
    
    DailyMessage.objects.create(
        email=email, 
        message_sent_at=now()
    )
    
    response = DailyMessage.send_message(email)
    assert "Please, try again in" in response