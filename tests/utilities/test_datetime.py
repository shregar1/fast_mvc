"""Tests for datetime utilities."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import List, Optional
from unittest.mock import patch, MagicMock

import pytest

from utilities.datetime import DateTimeUtility


class TestDateTimeUtility:
    """Test class for DateTimeUtility."""

    def test_init_default_values(self):
        """Test initialization with default values."""
        util = DateTimeUtility()
        assert util.urn is None
        assert util.user_urn is None
        assert util.api_name is None
        assert util.user_id is None

    def test_init_with_context(self):
        """Test initialization with context values."""
        util = DateTimeUtility(
            urn="test-urn",
            user_urn="user-123",
            api_name="api-test",
            user_id="user-456"
        )
        assert util.urn == "test-urn"
        assert util.user_urn == "user-123"
        assert util.api_name == "api-test"
        assert util.user_id == "user-456"

    def test_now_returns_datetime(self):
        """Test now() returns a datetime object."""
        result = DateTimeUtility.now()
        assert isinstance(result, datetime)

    def test_now_returns_utc(self):
        """Test now() returns UTC datetime."""
        result = DateTimeUtility.now()
        assert result.tzinfo == timezone.utc

    def test_now_returns_recent_time(self):
        """Test now() returns time close to current time."""
        before = datetime.now(timezone.utc)
        result = DateTimeUtility.now()
        after = datetime.now(timezone.utc)
        assert before <= result <= after

    def test_utc_now_is_deprecated_alias(self):
        """Test utc_now is deprecated alias for now."""
        with pytest.warns(DeprecationWarning):
            result = DateTimeUtility.utc_now()
        assert isinstance(result, datetime)

    def test_format_iso_basic(self):
        """Test basic ISO formatting."""
        dt = datetime(2024, 1, 15, 10, 30, 0, tzinfo=timezone.utc)
        result = DateTimeUtility.format_iso(dt)
        assert "2024-01-15" in result
        assert "10:30" in result

    def test_parse_iso_valid(self):
        """Test parsing valid ISO string."""
        iso_str = "2024-01-15T10:30:00+00:00"
        result = DateTimeUtility.parse_iso(iso_str)
        assert isinstance(result, datetime)
        assert result.year == 2024
        assert result.month == 1
        assert result.day == 15

    def test_parse_iso_invalid(self):
        """Test parsing invalid ISO string returns None."""
        result = DateTimeUtility.parse_iso("not-a-date")
        assert result is None

    def test_add_days(self):
        """Test adding days to datetime."""
        dt = datetime(2024, 1, 1, tzinfo=timezone.utc)
        result = DateTimeUtility.add_days(dt, 5)
        assert result.day == 6

    def test_add_days_negative(self):
        """Test subtracting days."""
        dt = datetime(2024, 1, 10, tzinfo=timezone.utc)
        result = DateTimeUtility.add_days(dt, -5)
        assert result.day == 5

    def test_add_hours(self):
        """Test adding hours."""
        dt = datetime(2024, 1, 1, 10, 0, tzinfo=timezone.utc)
        result = DateTimeUtility.add_hours(dt, 5)
        assert result.hour == 15

    def test_add_minutes(self):
        """Test adding minutes."""
        dt = datetime(2024, 1, 1, 10, 30, tzinfo=timezone.utc)
        result = DateTimeUtility.add_minutes(dt, 45)
        assert result.hour == 11
        assert result.minute == 15

    def test_is_past_with_past_date(self):
        """Test is_past with past date."""
        past = datetime(2020, 1, 1, tzinfo=timezone.utc)
        assert DateTimeUtility.is_past(past) is True

    def test_is_past_with_future_date(self):
        """Test is_past with future date."""
        future = datetime(2030, 1, 1, tzinfo=timezone.utc)
        assert DateTimeUtility.is_past(future) is False

    def test_is_future_with_future_date(self):
        """Test is_future with future date."""
        future = datetime(2030, 1, 1, tzinfo=timezone.utc)
        assert DateTimeUtility.is_future(future) is True

    def test_is_future_with_past_date(self):
        """Test is_future with past date."""
        past = datetime(2020, 1, 1, tzinfo=timezone.utc)
        assert DateTimeUtility.is_future(past) is False

    def test_days_between(self):
        """Test calculating days between dates."""
        start = datetime(2024, 1, 1, tzinfo=timezone.utc)
        end = datetime(2024, 1, 10, tzinfo=timezone.utc)
        result = DateTimeUtility.days_between(start, end)
        assert result == 9

    def test_days_between_negative(self):
        """Test days_between with reversed dates."""
        start = datetime(2024, 1, 10, tzinfo=timezone.utc)
        end = datetime(2024, 1, 1, tzinfo=timezone.utc)
        result = DateTimeUtility.days_between(start, end)
        assert result == -9

    def test_start_of_day(self):
        """Test getting start of day."""
        dt = datetime(2024, 1, 15, 14, 30, 45, tzinfo=timezone.utc)
        result = DateTimeUtility.start_of_day(dt)
        assert result.hour == 0
        assert result.minute == 0
        assert result.second == 0

    def test_end_of_day(self):
        """Test getting end of day."""
        dt = datetime(2024, 1, 15, 14, 30, 45, tzinfo=timezone.utc)
        result = DateTimeUtility.end_of_day(dt)
        assert result.hour == 23
        assert result.minute == 59
        assert result.second == 59

    def test_to_timestamp(self):
        """Test converting to timestamp."""
        dt = datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
        result = DateTimeUtility.to_timestamp(dt)
        assert isinstance(result, (int, float))
        assert result > 0

    def test_from_timestamp(self):
        """Test converting from timestamp."""
        ts = 1704067200  # 2024-01-01 00:00:00 UTC
        result = DateTimeUtility.from_timestamp(ts)
        assert isinstance(result, datetime)
        assert result.year == 2024

    def test_format_custom(self):
        """Test custom formatting."""
        dt = datetime(2024, 1, 15, 10, 30, 0, tzinfo=timezone.utc)
        result = DateTimeUtility.format_custom(dt, "%Y/%m/%d")
        assert result == "2024/01/15"


class TestDateTimeUtilityProperties:
    """Test properties of DateTimeUtility."""

    def test_urn_getter_setter(self):
        """Test urn property."""
        util = DateTimeUtility()
        util.urn = "test"
        assert util.urn == "test"

    def test_user_urn_getter_setter(self):
        """Test user_urn property."""
        util = DateTimeUtility()
        util.user_urn = "user"
        assert util.user_urn == "user"

    def test_api_name_getter_setter(self):
        """Test api_name property."""
        util = DateTimeUtility()
        util.api_name = "api"
        assert util.api_name == "api"

    def test_user_id_getter_setter(self):
        """Test user_id property."""
        util = DateTimeUtility()
        util.user_id = "id"
        assert util.user_id == "id"

    def test_logger_access(self):
        """Test logger is accessible."""
        util = DateTimeUtility()
        assert util.logger is not None


class TestDateTimeUtilityEdgeCases:
    """Test edge cases."""

    def test_parse_iso_empty_string(self):
        """Test parsing empty string."""
        result = DateTimeUtility.parse_iso("")
        assert result is None

    def test_parse_iso_none(self):
        """Test parsing None."""
        result = DateTimeUtility.parse_iso(None)
        assert result is None

    def test_add_days_with_none(self):
        """Test add_days with None."""
        with pytest.raises((AttributeError, TypeError)):
            DateTimeUtility.add_days(None, 5)

    def test_days_between_none(self):
        """Test days_between with None."""
        dt = datetime.now(timezone.utc)
        with pytest.raises((AttributeError, TypeError)):
            DateTimeUtility.days_between(None, dt)
