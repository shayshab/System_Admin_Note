# Contributing to System Administration Scripts

Thank you for your interest in contributing to this project! This document provides guidelines and instructions for contributing.

## Code of Conduct

Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md).

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in the Issues section
2. Use the bug report template
3. Include detailed steps to reproduce
4. Include expected and actual behavior
5. Include system information and logs

### Suggesting Enhancements

1. Check if the enhancement has already been suggested
2. Use the feature request template
3. Describe the enhancement clearly
4. Explain why it would be useful
5. Include any relevant examples

### Pull Requests

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Add tests for new functionality
5. Update documentation
6. Submit a pull request

## Development Process

### Setting Up Development Environment

1. Clone the repository:
```bash
git clone https://github.com/yourusername/system-admin-scripts.git
cd system-admin-scripts
```

2. Create a virtual environment (optional):
```bash
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Code Style

- Follow the [Shell Style Guide](https://google.github.io/styleguide/shellguide.html)
- Use meaningful variable names
- Add comments for complex logic
- Keep functions small and focused
- Use proper error handling

### Testing

1. Write tests for new functionality
2. Run existing tests:
```bash
./tests/run_tests.sh
```

3. Ensure all tests pass before submitting

### Documentation

1. Update README.md if needed
2. Add or update script documentation
3. Include usage examples
4. Document configuration options

## Commit Guidelines

- Use clear and descriptive commit messages
- Reference issues and pull requests
- Keep commits focused and atomic
- Follow the [Conventional Commits](https://www.conventionalcommits.org/) format

## Review Process

1. All submissions require review
2. Address review comments
3. Keep the discussion focused
4. Be responsive to feedback

## Release Process

1. Version numbers follow [Semantic Versioning](https://semver.org/)
2. Create release notes
3. Tag releases appropriately
4. Update documentation

## Getting Help

- Check the documentation
- Search existing issues
- Ask in discussions
- Contact maintainers

## License

By contributing, you agree that your contributions will be licensed under the project's [MIT License](LICENSE). 