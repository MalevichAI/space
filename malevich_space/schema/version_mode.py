from enum import Enum


class VersionMode(Enum):
    MAJOR = "major"
    MINOR = "minor"
    PATCH = "patch"
    DEFAULT = "default"
    OVERRIDE = "override"
