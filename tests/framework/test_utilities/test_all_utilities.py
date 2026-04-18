"""Comprehensive tests for all utilities."""

from __future__ import annotations

import pytest
from typing import Any, Optional


class TestUtilityImports:
    """Test that all utilities can be imported."""

    def test_import_env_utility(self):
        """Test EnvironmentParserUtility can be imported."""
        from utilities.env import EnvironmentParserUtility
        assert EnvironmentParserUtility is not None

    def test_import_datetime_utility(self):
        """Test DateTimeUtility can be imported."""
        from utilities.datetime import DateTimeUtility
        assert DateTimeUtility is not None

    def test_import_string_utility(self):
        """Test StringUtility can be imported."""
        from utilities.string import StringUtility
        assert StringUtility is not None

    def test_import_auth_helpers(self):
        """Test utilities.auth module-level helpers can be imported."""
        from utilities.auth import constant_time_compare, parse_basic_authorization
        assert constant_time_compare is not None
        assert parse_basic_authorization is not None

    def test_import_cors_utility(self):
        """Test CorsConfigUtility can be imported."""
        from utilities.cors import CorsConfigUtility
        assert CorsConfigUtility is not None

    def test_import_security_headers_utility(self):
        """Test SecurityHeadersUtility can be imported."""
        from utilities.security_headers import SecurityHeadersUtility
        assert SecurityHeadersUtility is not None

    def test_import_system_utility(self):
        """Test SystemUtility can be imported."""
        from utilities.system import SystemUtility
        assert SystemUtility is not None

    def test_import_validator_utility(self):
        """Test ConfigValidatorUtility can be imported."""
        from utilities.validator import ConfigValidatorUtility
        assert ConfigValidatorUtility is not None


class TestUtilityInheritance:
    """Test that all utilities inherit from IUtility."""

    def test_env_utility_inheritance(self):
        """Test EnvironmentParserUtility inherits from IUtility."""
        from utilities.env import EnvironmentParserUtility
        from abstractions.utility import IUtility
        assert issubclass(EnvironmentParserUtility, IUtility)

    def test_datetime_utility_inheritance(self):
        """Test DateTimeUtility inherits from IUtility."""
        from utilities.datetime import DateTimeUtility
        from abstractions.utility import IUtility
        assert issubclass(DateTimeUtility, IUtility)

    def test_string_utility_inheritance(self):
        """Test StringUtility inherits from IUtility."""
        from utilities.string import StringUtility
        from abstractions.utility import IUtility
        assert issubclass(StringUtility, IUtility)

    def test_cors_utility_inheritance(self):
        """Test CorsConfigUtility inherits from IUtility."""
        from utilities.cors import CorsConfigUtility
        from abstractions.utility import IUtility
        assert issubclass(CorsConfigUtility, IUtility)

    def test_security_headers_utility_inheritance(self):
        """Test SecurityHeadersUtility inherits from IUtility."""
        from utilities.security_headers import SecurityHeadersUtility
        from abstractions.utility import IUtility
        assert issubclass(SecurityHeadersUtility, IUtility)

    def test_system_utility_inheritance(self):
        """Test SystemUtility inherits from IUtility."""
        from utilities.system import SystemUtility
        from abstractions.utility import IUtility
        assert issubclass(SystemUtility, IUtility)

    def test_validator_utility_inheritance(self):
        """Test ConfigValidatorUtility inherits from IUtility."""
        from utilities.validator import ConfigValidatorUtility
        from abstractions.utility import IUtility
        assert issubclass(ConfigValidatorUtility, IUtility)


class TestUtilityInstantiation:
    """Test that all utilities can be instantiated."""

    def test_env_utility_instantiation(self):
        """Test EnvironmentParserUtility can be instantiated."""
        from utilities.env import EnvironmentParserUtility
        util = EnvironmentParserUtility()
        assert util is not None

    def test_datetime_utility_instantiation(self):
        """Test DateTimeUtility can be instantiated."""
        from utilities.datetime import DateTimeUtility
        util = DateTimeUtility()
        assert util is not None

    def test_string_utility_instantiation(self):
        """Test StringUtility can be instantiated."""
        from utilities.string import StringUtility
        util = StringUtility()
        assert util is not None

    def test_cors_utility_instantiation(self):
        """Test CorsConfigUtility can be instantiated."""
        from utilities.cors import CorsConfigUtility
        util = CorsConfigUtility()
        assert util is not None

    def test_security_headers_utility_instantiation(self):
        """Test SecurityHeadersUtility can be instantiated."""
        from utilities.security_headers import SecurityHeadersUtility
        util = SecurityHeadersUtility()
        assert util is not None

    def test_system_utility_instantiation(self):
        """Test SystemUtility can be instantiated."""
        from utilities.system import SystemUtility
        util = SystemUtility()
        assert util is not None

    def test_validator_utility_instantiation(self):
        """Test ConfigValidatorUtility can be instantiated."""
        from utilities.validator import ConfigValidatorUtility
        util = ConfigValidatorUtility()
        assert util is not None


class TestUtilityContext:
    """Test that all utilities support context attributes."""

    @pytest.mark.parametrize("util_class,util_name", [
        ("utilities.env.EnvironmentParserUtility", "env"),
        ("utilities.datetime.DateTimeUtility", "datetime"),
        ("utilities.string.StringUtility", "string"),
        ("utilities.cors.CorsConfigUtility", "cors"),
        ("utilities.security_headers.SecurityHeadersUtility", "security_headers"),
        ("utilities.system.SystemUtility", "system"),
        ("utilities.validator.ConfigValidatorUtility", "validator"),
    ])
    def test_utility_has_urn_property(self, util_class, util_name):
        """Test utility has urn property."""
        module_name, class_name = util_class.rsplit(".", 1)
        module = __import__(module_name, fromlist=[class_name])
        util_class_obj = getattr(module, class_name)
        util = util_class_obj()
        assert hasattr(util, "urn")

    @pytest.mark.parametrize("util_class,util_name", [
        ("utilities.env.EnvironmentParserUtility", "env"),
        ("utilities.datetime.DateTimeUtility", "datetime"),
        ("utilities.string.StringUtility", "string"),
        ("utilities.cors.CorsConfigUtility", "cors"),
        ("utilities.security_headers.SecurityHeadersUtility", "security_headers"),
        ("utilities.system.SystemUtility", "system"),
        ("utilities.validator.ConfigValidatorUtility", "validator"),
    ])
    def test_utility_has_user_urn_property(self, util_class, util_name):
        """Test utility has user_urn property."""
        module_name, class_name = util_class.rsplit(".", 1)
        module = __import__(module_name, fromlist=[class_name])
        util_class_obj = getattr(module, class_name)
        util = util_class_obj()
        assert hasattr(util, "user_urn")

    @pytest.mark.parametrize("util_class,util_name", [
        ("utilities.env.EnvironmentParserUtility", "env"),
        ("utilities.datetime.DateTimeUtility", "datetime"),
        ("utilities.string.StringUtility", "string"),
        ("utilities.cors.CorsConfigUtility", "cors"),
        ("utilities.security_headers.SecurityHeadersUtility", "security_headers"),
        ("utilities.system.SystemUtility", "system"),
        ("utilities.validator.ConfigValidatorUtility", "validator"),
    ])
    def test_utility_has_api_name_property(self, util_class, util_name):
        """Test utility has api_name property."""
        module_name, class_name = util_class.rsplit(".", 1)
        module = __import__(module_name, fromlist=[class_name])
        util_class_obj = getattr(module, class_name)
        util = util_class_obj()
        assert hasattr(util, "api_name")

    @pytest.mark.parametrize("util_class,util_name", [
        ("utilities.env.EnvironmentParserUtility", "env"),
        ("utilities.datetime.DateTimeUtility", "datetime"),
        ("utilities.string.StringUtility", "string"),
        ("utilities.cors.CorsConfigUtility", "cors"),
        ("utilities.security_headers.SecurityHeadersUtility", "security_headers"),
        ("utilities.system.SystemUtility", "system"),
        ("utilities.validator.ConfigValidatorUtility", "validator"),
    ])
    def test_utility_has_user_id_property(self, util_class, util_name):
        """Test utility has user_id property."""
        module_name, class_name = util_class.rsplit(".", 1)
        module = __import__(module_name, fromlist=[class_name])
        util_class_obj = getattr(module, class_name)
        util = util_class_obj()
        assert hasattr(util, "user_id")

    @pytest.mark.parametrize("util_class,util_name", [
        ("utilities.env.EnvironmentParserUtility", "env"),
        ("utilities.datetime.DateTimeUtility", "datetime"),
        ("utilities.string.StringUtility", "string"),
        ("utilities.cors.CorsConfigUtility", "cors"),
        ("utilities.security_headers.SecurityHeadersUtility", "security_headers"),
        ("utilities.system.SystemUtility", "system"),
        ("utilities.validator.ConfigValidatorUtility", "validator"),
    ])
    def test_utility_has_logger_property(self, util_class, util_name):
        """Test utility has logger property."""
        module_name, class_name = util_class.rsplit(".", 1)
        module = __import__(module_name, fromlist=[class_name])
        util_class_obj = getattr(module, class_name)
        util = util_class_obj()
        assert hasattr(util, "logger")
