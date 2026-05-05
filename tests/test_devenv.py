"""Tests for DevEnv-Setup"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from unittest.mock import patch, MagicMock

class TestDevEnv(unittest.TestCase):
    
    def test_import(self):
        """Test that devenv module can be imported"""
        try:
            import devenv
            self.assertTrue(True)
        except ImportError:
            self.fail("Failed to import devenv module")
    
    def test_color_functions(self):
        """Test color formatting functions"""
        import devenv as dv
        self.assertIn("\033[", dv.color("test", dv.GREEN))
        self.assertIn("test", dv.color("test", dv.RED))
    
    def test_print_functions(self):
        """Test print helper functions don't crash"""
        import devenv as dv
        # These should not raise exceptions
        dv.print_success("test")
        dv.print_error("test")
        dv.print_info("test")
        dv.print_progress("test")
        dv.print_warning("test")
    
    def test_get_platform(self):
        """Test platform detection"""
        import devenv as dv
        platform = dv.get_platform()
        self.assertIn(platform, ["windows", "macos", "linux"])
    
    def test_config_paths(self):
        """Test config path generation"""
        import devenv as dv
        home = dv.get_home_dir()
        self.assertTrue(os.path.isabs(home))
        self.assertTrue(os.path.exists(home))

if __name__ == '__main__':
    unittest.main()