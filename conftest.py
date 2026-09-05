"""
Pytest configuration for Nephrolithiasis Metabolic Agent test suite.
Sets required environment variables for secure test execution.
"""
import os
import secrets


def pytest_configure(config):
    """Configure test environment with secure defaults."""
    # Generate a secure test key if not provided
    if not os.getenv("AUDIT_SECRET_KEY"):
        os.environ["AUDIT_SECRET_KEY"] = f"test-audit-key-{secrets.token_hex(16)}-secure-random-32plus-chars"
