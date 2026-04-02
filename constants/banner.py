"""FastX Startup Banner Constants.

This module contains ASCII art banners and startup messages.
"""

from __future__ import annotations


class BannerConfig:
    """Configuration class for FastX startup banner.

    This class contains all banner-related constants including
    ASCII art, headers, and formatting options.
    """

    # ASCII Art Banner - FastX Logo (compact)
    FASTX_BANNER: str = r"""
╔═════════════════════════════════════════════╗
║                                             ║
║  ███████╗ █████╗ ███████╗████████╗██╗  ██╗  ║
║  ██╔════╝██╔══██╗██╔════╝╚══██╔══╝╚██╗██╔╝  ║
║  █████╗  ███████║███████╗   ██║    ╚███╔╝   ║
║  ██╔══╝  ██╔══██║╚════██║   ██║    ██╔██╗   ║
║  ██║     ██║  ██║███████║   ██║   ██╔╝ ██╗  ║
║  ╚═╝     ╚═╝  ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝  ║
║                                             ║
║      Production-grade FastAPI Framework     ║
╚═════════════════════════════════════════════╝
"""

    # Section Headers
    SERVER_INFO_HEADER: str = "Server Information:"
    API_DOCS_HEADER: str = "API Documentation:"
    HEALTH_ENDPOINTS_HEADER: str = "Health Endpoints:"
    ENVIRONMENT_HEADER: str = "Environment:"
    FEATURES_HEADER: str = "Features:"

    # Feature Indicators
    FEATURE_ENABLED: str = "[+]"
    FEATURE_DISABLED: str = "[-]"

    # Ready Message
    READY_MESSAGE: str = "FastX is ready! Press Ctrl+C to stop."

    # Label Widths (for alignment)
    LABEL_WIDTH: int = 12

    @classmethod
    def get_banner(cls) -> str:
        """Get the full banner string."""
        return cls.FASTX_BANNER

    @classmethod
    def get_feature_indicator(cls, enabled: bool) -> str:
        """Get feature indicator based on enabled state.

        Args:
            enabled: Whether the feature is enabled

        Returns:
            [+] if enabled, [-] if disabled
        """
        return cls.FEATURE_ENABLED if enabled else cls.FEATURE_DISABLED

__all__ = [
    "BannerConfig"
]
