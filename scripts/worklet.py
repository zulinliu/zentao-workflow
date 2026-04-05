#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Worklet - direct execution entry point

Usage:
    python worklet.py -t story -i 38817
    python worklet.py -t task --ids 12345,12346
    python worklet.py -t bug -i 67890 -o ~/my-output
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from worklet.__main__ import main

if __name__ == "__main__":
    main()
