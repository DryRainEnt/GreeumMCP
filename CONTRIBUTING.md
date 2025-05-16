# Contributing to GreeumMCP

Thank you for your interest in contributing to GreeumMCP! This document provides guidelines and instructions for contributing to this project.

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md).

## How Can I Contribute?

### Reporting Bugs

- Before creating a bug report, please check the existing issues to see if the problem has already been reported.
- When creating a bug report, include as many details as possible. Fill out the required template, as the information it asks for helps us resolve issues faster.
- Include steps to reproduce the issue.
- Describe the behavior you observed and what behavior you expected.
- Include screenshots if applicable.

### Suggesting Enhancements

- Before creating an enhancement suggestion, please check the existing issues to see if the enhancement has already been suggested.
- When creating an enhancement suggestion, include as many details as possible. Fill out the template, as the information it asks for helps us understand the suggestion.
- Clearly describe the behavior you would like to see implemented and why it would be beneficial.

### Pull Requests

- Fill in the required template.
- Follow the coding style of the project (docstrings, comments, code formatting).
- Include tests for your changes if applicable.
- Update the documentation if necessary.
- Make sure your code passes all tests before submitting the PR.
- Link any relevant issues in the PR description.

## Getting Started

### Environment Setup

1. Fork the repository on GitHub.
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR-USERNAME/GreeumMCP.git
   cd GreeumMCP
   ```
3. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```
4. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

### Development Workflow

1. Create a new branch for your feature or bugfix:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. Make your changes.
3. Run the tests to make sure everything is working:
   ```bash
   pytest
   ```
4. Commit your changes:
   ```bash
   git commit -m "Description of your changes"
   ```
5. Push your branch to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
6. Open a pull request on GitHub.

## Style Guidelines

### Python Code Style

- Follow PEP 8 style guide for Python code.
- Use docstrings for all functions and classes (following Google-style docstrings).
- Keep lines under 100 characters.
- Use meaningful variable names.
- Add comments to explain complex logic.

### Commit Messages

- Use the present tense ("Add feature" not "Added feature").
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...").
- Limit the first line to 72 characters or less.
- Reference issues and pull requests liberally after the first line.

## Additional Notes

### Documentation

- Update the README.md with details of changes to the interface.
- Update the examples if needed.
- Add or update docstrings and comments as necessary.

### Testing

- Add tests for new features.
- Make sure existing tests pass.
- Aim for high test coverage.

Thank you for contributing to GreeumMCP! 