# Chess Tournament Manager

A Python application for managing chess tournaments with player registration, match pairing, and tournament reporting.

## Requirements

- Python 3.13 or higher
- One of the following package managers:
  - **uv** (recommended - faster and modern)
  - **pip-tools** (traditional approach)

## Installation

### Method 1: Using uv (Recommended)

1. **Install uv** (if not already installed):
   ```bash
   pip install uv
   ```

2. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd ocpy04
   ```

3. **Install dependencies**:
   ```bash
   # Install production dependencies only
   uv sync
   
   # Install with development dependencies (for development/testing)
   uv sync --group dev
   ```

### Method 2: Using pip-tools (Traditional)

1. **Install pip-tools**:
   ```bash
   pip install pip-tools
   ```

2. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd ocpy04
   ```

3. **Create virtual environment**:
   ```bash
   python -m venv .venv
   
   # Activate virtual environment
   # On Windows:
   .venv\Scripts\activate
   # On macOS/Linux:
   source .venv/bin/activate
   ```

4. **Install dependencies**:
   ```bash
   # For production
   pip-sync requirements.txt
   
   # For development (includes testing tools)
   pip-sync requirements-dev.txt
   ```

## Running the Application

### With uv:
   ```bash
  uv run chess
  # Alternative way to run
  uv run python -m chess_tournament_manager 
   ```
### With pip/pip-tools:
   ```bash
   # with venv activated
  python -m chess_tournament_manager
  # Alternative way to run
  python chess_tournament_manager/**main**.py
   ```
## Development

### Code Quality Tools

This project uses several code quality tools:
- **flake8**: Code linting and style checking
- **black**: Code formatting
- **flake8-pyproject**: Integration between flake8 and pyproject.toml

### Running Code Quality Checks

#### With uv:
   ```bash
  # Run flake8
  uv run flake8 .
  # Run black formatting check
  uv run black --check .
  # Auto-format code with black
  uv run black .
   ```
#### With pip-tools:
   ```bash
  # Run flake8
  flake8 .
  # Run black formatting check
  black --check .
  # Auto-format code with black
  black .
   ```
### Generating flake8 Reports

#### With uv:
   ```bash
  # in html format
  uv run flake8 .
  # in .txt format
  uv run flake8 --output-file=flake8-report.txt .
   ```
#### With pip-tools:
   ```bash
  # in html format
  flake8 --format=html --htmldir=flake8-report .
  # in .txt format
  flake8 --output-file=flake8-report.txt .
   ```
