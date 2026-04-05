"""InputParser - auto-detect input type (folder vs file vs Zentao ID)."""
import re
from enum import Enum
from pathlib import Path
from typing import Literal


class InputType(Enum):
    ZENTAO = "zentao"
    FILE = "file"
    FOLDER = "folder"
    UNKNOWN = "unknown"


class InputParser:
    """Auto-detects input type from identifier string.

    Implements INPUT-09 per D-01:
    - Path.exists() → file/folder detection
    - Zentao ID regex: story-\d+, task-\d+, bug-\d+
    - Also handles bare numeric IDs (treated as story)
    """

    # Zentao ID patterns
    ZENTAO_PATTERN = re.compile(
        r'^(story|task|bug)[-_](\d+)$', re.IGNORECASE
    )
    BARE_NUMERIC_PATTERN = re.compile(r'^(\d+)$')

    @classmethod
    def detect(cls, identifier: str) -> InputType:
        """Detect input type from identifier string.

        Args:
            identifier: User-provided input (path, Zentao ID, or bare number)

        Returns:
            InputType enum value

        Detection order per D-01:
        1. Path.exists() → is_file() → FILE
        2. Path.exists() → is_dir() → FOLDER
        3. Zentao ID regex match → ZENTAO
        4. Bare numeric (e.g. "38817") → ZENTAO (default to story)
        5. Otherwise → UNKNOWN
        """
        identifier = identifier.strip()
        if not identifier:
            return InputType.UNKNOWN

        # Check if it's a file or folder path
        path = Path(identifier)
        if path.exists():
            if path.is_file():
                return InputType.FILE
            elif path.is_dir():
                return InputType.FOLDER

        # Check Zentao ID with prefix (story-123, task-456, bug-789)
        if cls.ZENTAO_PATTERN.match(identifier):
            return InputType.ZENTAO

        # Check bare numeric ID (e.g. "38817") — default to story
        if cls.BARE_NUMERIC_PATTERN.match(identifier):
            return InputType.ZENTAO

        return InputType.UNKNOWN

    @classmethod
    def parse_zentao_id(cls, identifier: str) -> tuple[str, int] | None:
        """Parse Zentao ID into (type, numeric_id) tuple.

        Args:
            identifier: Zentao ID string like "story-38817" or "38817"

        Returns:
            Tuple of (type, id) or None if not a valid Zentao ID
        """
        identifier = identifier.strip()

        # With prefix
        match = cls.ZENTAO_PATTERN.match(identifier)
        if match:
            return (match.group(1).lower(), int(match.group(2)))

        # Bare numeric — default to story
        match = cls.BARE_NUMERIC_PATTERN.match(identifier)
        if match:
            return ("story", int(match.group(1)))

        return None