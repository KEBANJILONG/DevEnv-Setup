#!/usr/bin/env python3
"""
DevEnv-Setup Launcher
One-Click Development Environment Setup Tool
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import and run
from devenv import main

if __name__ == "__main__":
    main()