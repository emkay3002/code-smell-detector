# Software Reengineering Assignment: Code Smell Detection

This project demonstrates code smell detection in Python applications. It includes a sample program with intentional code smells and a detector application that can identify these smells using AST analysis.

## Project Structure

```
CodeScan/
├── smelly_code/           # Sample program with intentional code smells
│   ├── calculator.py      # Main calculator application
│   └── test_calculator.py # Unit tests for the calculator
├── detector/              # Code smell detection application
│   ├── __init__.py
│   ├── smell_detector.py  # Main detection logic
│   ├── cli.py            # Command-line interface
│   └── __main__.py       # Module entry point
├── docs/                 # Documentation
│   └── smells.md         # Code smells documentation
├── report/               # Placeholder for final report
├── config.yaml           # Detector configuration
├── requirements.txt      # Python dependencies
├── .gitignore           # Git ignore file
└── README.md            # This file
```

## Code Smells Demonstrated

The `smelly_code/calculator.py` file contains six intentional code smells:

1. **Long Method** - `process_large_dataset()` method is too long
2. **God Class** - `Calculator` class has too many responsibilities
3. **Duplicated Code** - Similar validation logic in `validate_email()` and `validate_phone()`
4. **Large Parameter List** - `calculate_complex_expression()` has 20 parameters
5. **Magic Numbers** - Hardcoded values in `calculate_tax()` function
6. **Feature Envy** - `send_notification()` method is too dependent on `EmailService`

## Installation

1. Clone or download this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Running the Sample Program

To run the calculator with code smells:

```bash
cd smelly_code
python calculator.py
```

### Running the Unit Tests

To run the unit tests:

```bash
cd smelly_code
python -m pytest test_calculator.py -v
```

### Using the Code Smell Detector

#### Basic Usage

```bash
# Analyze a single file
python -m detector smelly_code/calculator.py

# Analyze a directory
python -m detector smelly_code/

# Use custom configuration
python -m detector --config config.yaml smelly_code/
```

#### Advanced Options

```bash
# Only detect specific smells
python -m detector --only long_method,god_class smelly_code/

# Exclude specific smells
python -m detector --exclude magic_numbers smelly_code/

# Generate different output formats
python -m detector --format json smelly_code/
python -m detector --format csv smelly_code/

# Save report to file
python -m detector --output report.txt smelly_code/
```

#### Command Line Options

- `--config, -c`: Path to configuration YAML file
- `--only`: Only detect specific code smells (comma-separated)
- `--exclude`: Exclude specific code smells (comma-separated)
- `--output, -o`: Output file for the report
- `--verbose, -v`: Enable verbose output
- `--format`: Output format (text, json, csv)

## Configuration

The detector can be configured using the `config.yaml` file. You can:

- Enable/disable specific code smell detectors
- Adjust detection parameters (e.g., maximum method length)
- Set severity levels for different smells
- Customize similarity thresholds for duplicated code detection

## Detector Features

The code smell detector includes:

- **AST-based analysis** for accurate Python code parsing
- **Configurable detection rules** via YAML configuration
- **Multiple output formats** (text, JSON, CSV)
- **Command-line interface** with filtering options
- **Severity-based reporting** (high, medium, low)
- **Detailed suggestions** for refactoring

## Supported Code Smells

1. **Long Method**: Detects methods that exceed a configurable line count
2. **God Class**: Identifies classes with too many methods or attributes
3. **Duplicated Code**: Finds similar code blocks using similarity analysis
4. **Large Parameter List**: Detects methods with too many parameters
5. **Magic Numbers**: Identifies hardcoded numeric literals
6. **Feature Envy**: Finds methods that are overly dependent on other classes

## Development

### Adding New Code Smells

To add a new code smell detector:

1. Add the detector method to `CodeSmellDetector` class
2. Update the configuration schema in `config.yaml`
3. Add the detector to the `_get_enabled_detectors()` method
4. Update the CLI help text

### Running Tests

```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=detector

# Run specific test file
python -m pytest smelly_code/test_calculator.py
```

## Report Generation

The project includes a placeholder `report/` directory for the final 4-6 page report. The report should cover:

- Introduction to code smells and their impact
- Analysis of the detected smells in the sample code
- Discussion of refactoring strategies
- Evaluation of the detector's effectiveness
- Conclusions and recommendations

## Dependencies

- Python 3.7+
- PyYAML for configuration parsing
- Standard library modules (ast, re, argparse, etc.)

## License

This project is created for educational purposes as part of a Software Reengineering assignment.

## Author

Software Reengineering Assignment - Code Smell Detection Project
