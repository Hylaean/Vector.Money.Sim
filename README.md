# Vector Money Simulation

Vector Money Simulation is a lightweight framework for exploring interactions between economic agents and limited bio-physical resources. It models households, firms, government, and financial intermediaries that trade resources in a market with prices responding to scarcity.

## Features

- **Agent-based design** using the [Mesa](https://mesa.readthedocs.io/) library
- **Bio-physical stocks** with optional integration via [`pysd`](https://github.com/SDXorg/pysd)
- **Resource market** that automatically adjusts prices as stocks approach ecological limits
- Simple tests demonstrating price adjustment behaviour

## Installation

Install the package and its dependencies using `pip`:

```bash
pip install -e .
```

Optional dependency `pysd` will be used if available for more accurate stock integration.

## Running Tests

Execute the test suite with [pytest](https://pytest.readthedocs.io/):

```bash
pytest
```

## Documentation

Additional documentation is available in the [`docs/`](docs/) directory. See `docs/README.md` for a brief overview of the market implementation.

## License

This project is provided for educational purposes. See the `LICENSE` file if present for license information.
