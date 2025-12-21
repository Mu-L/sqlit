"""Unit tests for SQL Server adapter."""

from __future__ import annotations

import struct
import pytest

from sqlit.db.adapters.mssql import _convert_datetimeoffset


class TestConvertDatetimeOffset:
    """Tests for the datetimeoffset binary converter function.

    The datetimeoffset binary format is 20 bytes:
    - year (2 bytes, signed short)
    - month (2 bytes, signed short)
    - day (2 bytes, signed short)
    - hour (2 bytes, signed short)
    - minute (2 bytes, signed short)
    - second (2 bytes, signed short)
    - nanoseconds (4 bytes, unsigned int)
    - tz_hour (2 bytes, signed short)
    - tz_minute (2 bytes, signed short)
    """

    def _pack_datetimeoffset(
        self,
        year: int,
        month: int,
        day: int,
        hour: int,
        minute: int,
        second: int,
        nanoseconds: int,
        tz_hour: int,
        tz_minute: int,
    ) -> bytes:
        """Pack values into the datetimeoffset binary format."""
        return struct.pack(
            "<6hI2h",
            year, month, day, hour, minute, second,
            nanoseconds, tz_hour, tz_minute
        )

    def test_positive_timezone_offset(self):
        """Test conversion with positive timezone offset (+05:30 India)."""
        binary = self._pack_datetimeoffset(
            2024, 12, 21, 14, 30, 45, 123456000, 5, 30
        )
        result = _convert_datetimeoffset(binary)

        assert result == "2024-12-21 14:30:45.123456 +05:30"

    def test_negative_timezone_offset(self):
        """Test conversion with negative timezone offset (-05:00 Eastern)."""
        binary = self._pack_datetimeoffset(
            2024, 1, 15, 10, 30, 0, 500000000, -5, 0
        )
        result = _convert_datetimeoffset(binary)

        assert result == "2024-01-15 10:30:00.500000 -05:00"

    def test_utc_timezone(self):
        """Test conversion with UTC timezone (+00:00)."""
        binary = self._pack_datetimeoffset(
            2024, 6, 20, 0, 0, 0, 0, 0, 0
        )
        result = _convert_datetimeoffset(binary)

        assert result == "2024-06-20 00:00:00.000000 +00:00"

    def test_max_precision_nanoseconds(self):
        """Test conversion with maximum nanosecond precision."""
        # 999999999 nanoseconds = 999999 microseconds (truncated)
        binary = self._pack_datetimeoffset(
            2024, 12, 31, 23, 59, 59, 999999999, 0, 0
        )
        result = _convert_datetimeoffset(binary)

        assert result == "2024-12-31 23:59:59.999999 +00:00"

    def test_zero_nanoseconds(self):
        """Test conversion with zero nanoseconds."""
        binary = self._pack_datetimeoffset(
            2024, 1, 1, 0, 0, 0, 0, -8, 0
        )
        result = _convert_datetimeoffset(binary)

        assert result == "2024-01-01 00:00:00.000000 -08:00"

    def test_negative_timezone_with_minutes(self):
        """Test conversion with negative timezone that has minutes (-03:30 Newfoundland)."""
        binary = self._pack_datetimeoffset(
            2024, 7, 4, 12, 0, 0, 0, -3, -30
        )
        result = _convert_datetimeoffset(binary)

        # Note: The format shows absolute values for hours and minutes
        assert result == "2024-07-04 12:00:00.000000 -03:30"

    def test_far_future_date(self):
        """Test conversion with a far future date."""
        binary = self._pack_datetimeoffset(
            2099, 12, 31, 23, 59, 59, 0, 12, 0
        )
        result = _convert_datetimeoffset(binary)

        assert result == "2099-12-31 23:59:59.000000 +12:00"

    def test_leap_year_date(self):
        """Test conversion with a leap year date (Feb 29)."""
        binary = self._pack_datetimeoffset(
            2024, 2, 29, 12, 0, 0, 0, 0, 0
        )
        result = _convert_datetimeoffset(binary)

        assert result == "2024-02-29 12:00:00.000000 +00:00"
