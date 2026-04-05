#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Worklet - Developer workflow assistant

Fetches requirements, tasks, and bugs from Zentao and generates technical implementation plans.
"""

from .config import WorkletConfig
from .client import WorkletClient
from .models import Attachment, Bug, Story, Task
from .exporter import MarkdownExporter
from .service import WorkletService

__version__ = "2.0.0"
__all__ = [
    "WorkletConfig",
    "WorkletClient",
    "Attachment",
    "Bug",
    "Story",
    "Task",
    "MarkdownExporter",
    "WorkletService",
]
