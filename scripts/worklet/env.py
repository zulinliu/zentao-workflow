"""Environment detection with try-first strategy and caching."""
import json
import os
import subprocess
import time
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path

# Cache file location
CACHE_FILE = Path.home() / ".worklet" / "env_cache.json"
CACHE_TTL_SECONDS = 24 * 60 * 60  # 24 hours


@dataclass
class EnvResult:
    """Environment detection result."""
    backend: str  # "python"
    python_version: str  # e.g. "3.10.0"
    superpowers_available: bool
    superpowers_version: str | None
    cached_at: float  # Unix timestamp

    def is_fresh(self) -> bool:
        """Check if cache is still valid (within TTL)."""
        age = time.time() - self.cached_at
        return age < CACHE_TTL_SECONDS

    def to_dict(self) -> dict:
        return {
            "backend": self.backend,
            "python_version": self.python_version,
            "superpowers_available": self.superpowers_available,
            "superpowers_version": self.superpowers_version,
            "cached_at": self.cached_at,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "EnvResult":
        return cls(
            backend=d["backend"],
            python_version=d["python_version"],
            superpowers_available=d["superpowers_available"],
            superpowers_version=d.get("superpowers_version"),
            cached_at=d["cached_at"],
        )


class EnvDetector:
    """Environment detector with try-first strategy and caching.

    Implements ENV-01 (try-first), ENV-02 (24h cache), ENV-03 (npx detection).
    """

    def __init__(self):
        self._cache_file = CACHE_FILE
        self._ensure_cache_dir()

    def _ensure_cache_dir(self):
        """Ensure cache directory exists."""
        self._cache_file.parent.mkdir(parents=True, exist_ok=True)

    def _read_cache(self) -> EnvResult | None:
        """Read cached environment result if fresh."""
        if not self._cache_file.exists():
            return None
        try:
            with open(self._cache_file) as f:
                data = json.load(f)
            result = EnvResult.from_dict(data)
            if result.is_fresh():
                return result
            return None
        except (json.JSONDecodeError, KeyError, ValueError):
            return None

    def _write_cache(self, result: EnvResult):
        """Write environment result to cache."""
        with open(self._cache_file, 'w') as f:
            json.dump(result.to_dict(), f, indent=2)

    def _detect_superpowers(self) -> tuple[bool, str | None]:
        """Detect superpowers via npx.

        Per D-03:
        - which npx -> npx -y superpowers --version
        Returns (available, version_string)
        """
        try:
            # Check npx exists
            npx_path = subprocess.run(
                ["which", "npx"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            if npx_path.returncode != 0:
                return False, None

            # Try npx -y superpowers --version
            result = subprocess.run(
                ["npx", "-y", "superpowers", "--version"],
                capture_output=True,
                text=True,
                timeout=30,
            )
            if result.returncode == 0:
                version = result.stdout.strip() or "unknown"
                return True, version
            return False, None
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False, None

    def _detect_python_version(self) -> str:
        """Get Python version string."""
        import sys
        return f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"

    def detect(self, force: bool = False) -> EnvResult:
        """Detect environment, using cache if available and fresh.

        Per ENV-01: try-first strategy
        1. Check cache first (if not force)
        2. If cache miss or stale, do fresh detection
        3. Cache the result

        Args:
            force: If True, skip cache and do fresh detection

        Returns:
            EnvResult with detected environment info
        """
        # Try cache first (unless force)
        if not force:
            cached = self._read_cache()
            if cached is not None:
                return cached

        # Fresh detection
        python_version = self._detect_python_version()
        superpowers_available, superpowers_version = self._detect_superpowers()

        result = EnvResult(
            backend="python",
            python_version=python_version,
            superpowers_available=superpowers_available,
            superpowers_version=superpowers_version,
            cached_at=time.time(),
        )

        # Cache the result
        self._write_cache(result)
        return result

    def clear_cache(self):
        """Clear the environment cache."""
        if self._cache_file.exists():
            self._cache_file.unlink()