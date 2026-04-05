"""Shared pytest fixtures for all test modules.

Per D-02: pytest + conftest.py fixtures for config/source/exporter tests.
"""
import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest

# Add scripts to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))


@pytest.fixture
def temp_workspace(tmp_path):
    """Creates a temporary directory with .worklet subdirectory.

    Returns Path to temp directory.
    """
    worklet_dir = tmp_path / ".worklet"
    worklet_dir.mkdir()
    return tmp_path


@pytest.fixture
def mock_config(temp_workspace):
    """Creates a temporary config.toml file with test values.

    Returns Path to config file.
    """
    config_path = temp_workspace / ".worklet" / "config.toml"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text("""\
[worklet]
base_url = "https://test.example.com"
username = "testuser"
password = "testpass"
output_dir = "output"
connect_timeout = 30
read_timeout = 60
""")
    return config_path


@pytest.fixture
def sample_markdown(temp_workspace):
    """Creates a test.md file in temp_workspace.

    Returns Path to the file.
    """
    md_file = temp_workspace / "test.md"
    md_file.write_text("# Test Title\n\nTest content.")
    return md_file


@pytest.fixture
def sample_pdf(temp_workspace):
    """Creates a test.pdf placeholder file.

    Note: Real PDF testing needs markitdown installed.
    Returns Path to the file.
    """
    pdf_file = temp_workspace / "test.pdf"
    # Minimal PDF header
    pdf_file.write_bytes(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    return pdf_file


@pytest.fixture
def sample_docx(temp_workspace):
    """Creates a test.docx placeholder file.

    Note: Real DOCX testing needs markitdown installed.
    Returns Path to the file.
    """
    docx_file = temp_workspace / "test.docx"
    # Minimal DOCX (ZIP) header
    docx_file.write_bytes(b"PK\x03\x04\n")
    return docx_file


@pytest.fixture
def sample_image(temp_workspace):
    """Creates a test.png placeholder file.

    Returns Path to the file.
    """
    png_file = temp_workspace / "test.png"
    # Minimal PNG header
    png_file.write_bytes(b"\x89PNG\r\n\x1a\n")
    return png_file


@pytest.fixture
def mock_zentao_response():
    """Returns dict with mocked Zentao API response structure."""
    return {
        "id": 123,
        "title": "Test Story",
        "spec": "<p>Story content</p>",
        "status": "active",
        "stage": "developed",
        "pri": "3",
        "product": 1,
        "module": 0,
        "project": 1,
        "openedBy": "admin",
        "openedDate": "2024-01-01 00:00:00",
    }


@pytest.fixture
def mock_source_registry():
    """Returns SourceRegistry instance or mock registry with known sources.

    For Phase 3, returns a mock registry. Real implementation comes in later plans.
    """
    registry = MagicMock()
    registry.get_source.return_value = None
    registry.list_sources.return_value = []
    return registry
