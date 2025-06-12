# Robots Instructions

## Best Practices

- Keep commits focused and small. Include clear commit messages.
- Format Python code with tools like `black` and `isort`.
- Include type hints where reasonable.
- Provide docstrings for public modules, classes, and functions.
- Run the test suite with `pytest` (or `python -m unittest`) before committing.

## Project Specific Guidelines

- **Prompt Logging**: Save the user prompt that led to each commit in the `docs/prompts/` directory. Name the file using the commit hash or a short description.
- **Unit Tests**: When implementing new functionality, accompany it with unit tests under `tests/`.
- **Documentation**: Document new concepts and implementations in the `docs/` directory or update existing documentation accordingly.

