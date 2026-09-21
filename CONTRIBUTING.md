# Contributing to Rank Torrent Name (RTN)

Thank you for considering a contribution to RTN! This document provides guidelines and instructions for contributing to this project. By contributing, you agree to abide by our community norms and conduct.

## Getting Started

### Setup Environment

1. **Clone the Repository**: Clone the project repository and enter the project directory:

```bash
git clone https://github.com/streama-hub/rank-torrent-name.git
cd rank-torrent-name
```

2. **Install Poetry**: RTN uses Poetry for dependency management. Ensure you have Poetry installed by following the [official instructions](https://python-poetry.org/docs/#installation).

3. **Install Dependencies**: Install the project dependencies with Poetry:

```bash
poetry install --with dev
```

### Making Changes

- Create a new branch for your changes:

```bash
git switch -c <branch-name>
```

- Make your changes, ensuring you adhere to the project's coding standards and practices.

### Testing and Linting

Before submitting your changes, run the tests and ensure your code passes all lint checks:

- **Run Tests**:

```bash
make test
```

- **Check Code Style**:

```bash
make lint
```

- **Check Coverage**
```bash
make coverage
```

### Performance Benchmarking

RTN uses `pyperf` for performance benchmarking. If your changes could impact performance, please run the benchmarks:

```bash
make benchmark
```

Include the benchmark results in your pull request if relevant.

### Committing Your Changes

- We try to follow [Conventional Commits](https://www.conventionalcommits.org/) specs.
- Commit your changes with a clear and descriptive commit message.
- Push your changes to your fork:

```bash
git push origin <branch-name>
```

### Submitting a Pull Request

- Go to the [RTN GitHub repository](https://github.com/streama-hub/rank-torrent-name).
- Click on the "Pull requests" tab and then the "New pull request" button.
- Choose your fork and branch with the changes, then click "Create pull request".
- Provide a clear and detailed description of the changes and the reasons behind them.

## Community and Conduct

Keep contributions and discussions respectful and focused on the project.

## Questions and Support

Read the [FAQ](docs/users/faq.md) for configuration guidance and check the [repository](https://github.com/streama-hub/rank-torrent-name) for updates.

---

Thank you for contributing to RTN! Your efforts help make this project better for everyone.
