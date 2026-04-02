"""Tests for string utilities."""

from __future__ import annotations

from utilities.string import StringUtility


class TestStringUtility:
    """Tests for :class:`StringUtility`."""

    def test_init_default_values(self):
        """Initialization with default context."""
        util = StringUtility()
        assert util.urn is None
        assert util.user_urn is None
        assert util.api_name is None
        assert util.user_id is None

    def test_init_with_context(self):
        """Initialization with tracing context."""
        util = StringUtility(urn="test", user_urn="user-1", api_name="api", user_id="u1")
        assert util.urn == "test"
        assert util.user_urn == "user-1"
        assert util.api_name == "api"
        assert util.user_id == "u1"

    def test_split_csv_splits_and_strips(self):
        """Comma-separated values are split and stripped."""
        assert StringUtility.split_csv("a, b , c", default=()) == ["a", "b", "c"]

    def test_split_csv_empty_uses_default(self):
        """Empty or whitespace-only input returns a copy of *default*."""
        default = ("x", "y")
        assert StringUtility.split_csv("", default=default) == ["x", "y"]
        assert StringUtility.split_csv("   ", default=default) == ["x", "y"]
        assert StringUtility.split_csv(None, default=default) == ["x", "y"]

    def test_split_csv_all_blank_parts_use_default(self):
        """Commas with no non-empty parts fall back to *default*."""
        assert StringUtility.split_csv(",,,", default=("fallback",)) == ["fallback"]

    def test_normalize_path_adds_leading_slash(self):
        """With ``leading_slash=True``, a leading slash is ensured."""
        assert StringUtility.normalize_path("api/v1") == "/api/v1"

    def test_normalize_path_idempotent(self):
        """Paths that already start with ``/`` are unchanged."""
        assert StringUtility.normalize_path("/health") == "/health"

    def test_normalize_path_no_leading_when_disabled(self):
        """With ``leading_slash=False``, no slash is prepended."""
        assert StringUtility.normalize_path("relative", leading_slash=False) == "relative"


class TestStringUtilityProperties:
    """Context attributes from :class:`abstractions.utility.IUtility`."""

    def test_urn_property(self):
        util = StringUtility()
        util.urn = "test"
        assert util.urn == "test"

    def test_user_urn_property(self):
        util = StringUtility()
        util.user_urn = "user"
        assert util.user_urn == "user"

    def test_api_name_property(self):
        util = StringUtility()
        util.api_name = "api"
        assert util.api_name == "api"

    def test_user_id_property(self):
        util = StringUtility()
        util.user_id = "id"
        assert util.user_id == "id"
