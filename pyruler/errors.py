"""Custom ruler errors."""


class RuleError(Exception):
    """Base Rule error."""


class RuleConfigError(Exception):
    """Error for Rule configuration"""


class RulerError(Exception):
    """Base Ruler error."""


class RuleSetError(Exception):
    """Base RuleSet error."""


class RulerConfigError(Exception):
    """Base error for Ruler configuration."""


class RuleSetConfigError(Exception):
    """Base error for RuleSet configuration."""
