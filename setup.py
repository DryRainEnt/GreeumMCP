#!/usr/bin/env python
"""
GreeumMCP: Greeum Memory Engine as MCP Server
"""
from setuptools import setup, find_packages
import os

# Read version from __init__.py
with open(os.path.join('greeummcp', '__init__.py'), 'r') as f:
    for line in f:
        if line.startswith('__version__'):
            version = line.split('=')[1].strip().strip('"\'')
            break
    else:
        version = '0.1.0'

# Read long description from README.md
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="greeummcp",
    version=version,
    description="Greeum Memory Engine as MCP Server",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="GreeumAI",
    author_email="contact@greeum.ai",
    url="https://github.com/GreeumAI/GreeumMCP",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.10",
    install_requires=[
        "greeum>=0.6.1",  # Greeum core package
        "mcp>=1.0.0",     # MCP Python SDK
        "fastapi>=0.100.0",  # API server (HTTP transport)
        "pydantic>=2.0.0",  # Data validation
        "uvicorn>=0.15.0",  # ASGI server
        "typer>=0.9.0",   # CLI interface
    ],
    entry_points={
        "console_scripts": [
            "greeum_mcp=greeummcp.server:main",
            "greeummcp=greeummcp.cli:app",
        ],
    },
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=23.0.0",
            "mypy>=1.0.0",
        ],
    },
) 