"""
Command-line interface for the code smell detector.
"""

import argparse
import sys
import os
from pathlib import Path
from typing import List, Optional
from .smell_detector import CodeSmellDetector


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Detect code smells in Python source code",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m detector.cli smelly_code/calculator.py
  python -m detector.cli --config config.yaml smelly_code/
  python -m detector.cli --only long_method,god_class smelly_code/
  python -m detector.cli --exclude magic_numbers smelly_code/
  python -m detector.cli --output report.txt smelly_code/
        """
    )
    
    parser.add_argument(
        'target',
        help='Python file or directory to analyze'
    )
    
    parser.add_argument(
        '--config', '-c',
        help='Path to configuration YAML file'
    )
    
    parser.add_argument(
        '--only',
        help='Only detect specific code smells (comma-separated)',
        metavar='SMELLS'
    )
    
    parser.add_argument(
        '--exclude',
        help='Exclude specific code smells (comma-separated)',
        metavar='SMELLS'
    )
    
    parser.add_argument(
        '--output', '-o',
        help='Output file for the report'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )
    
    parser.add_argument(
        '--format',
        choices=['text', 'json', 'csv'],
        default='text',
        help='Output format (default: text)'
    )
    
    args = parser.parse_args()
    
    # Parse only and exclude options
    only = args.only.split(',') if args.only else None
    exclude = args.exclude.split(',') if args.exclude else None
    
    # Initialize detector
    detector = CodeSmellDetector(args.config)
    
    # Find Python files to analyze
    python_files = find_python_files(args.target)
    
    if not python_files:
        print(f"No Python files found in {args.target}")
        sys.exit(1)
    
    if args.verbose:
        print(f"Analyzing {len(python_files)} Python files...")
    
    # Analyze each file
    all_smells = []
    for file_path in python_files:
        if args.verbose:
            print(f"Analyzing {file_path}...")
        
        smells = detector.detect_smells(file_path, only, exclude)
        all_smells.extend(smells)
    
    # Generate report
    if args.format == 'text':
        report = detector.generate_report()
    elif args.format == 'json':
        report = generate_json_report(all_smells)
    elif args.format == 'csv':
        report = generate_csv_report(all_smells)
    else:
        report = detector.generate_report()
    
    # Output report
    if args.output:
        with open(args.output, 'w') as f:
            f.write(report)
        print(f"Report saved to {args.output}")
    else:
        print(report)
    
    # Exit with appropriate code
    if all_smells:
        high_severity_count = len([s for s in all_smells if s.severity == 'high'])
        if high_severity_count > 0:
            sys.exit(2)  # High severity smells found
        else:
            sys.exit(1)  # Smells found but not high severity
    else:
        sys.exit(0)  # No smells found


def find_python_files(target: str) -> List[str]:
    """Find all Python files in the target path."""
    python_files = []
    target_path = Path(target)
    
    if target_path.is_file():
        if target_path.suffix == '.py':
            python_files.append(str(target_path))
    elif target_path.is_dir():
        for py_file in target_path.rglob('*.py'):
            python_files.append(str(py_file))
    
    return sorted(python_files)


def generate_json_report(smells: List) -> str:
    """Generate JSON format report."""
    import json
    
    report_data = {
        'total_smells': len(smells),
        'smells': []
    }
    
    for smell in smells:
        report_data['smells'].append({
            'type': smell.smell_type,
            'file': smell.file_path,
            'line': smell.line_number,
            'description': smell.description,
            'severity': smell.severity,
            'suggestion': smell.suggestion
        })
    
    return json.dumps(report_data, indent=2)


def generate_csv_report(smells: List) -> str:
    """Generate CSV format report."""
    import csv
    import io
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow(['Type', 'File', 'Line', 'Description', 'Severity', 'Suggestion'])
    
    # Write data
    for smell in smells:
        writer.writerow([
            smell.smell_type,
            smell.file_path,
            smell.line_number,
            smell.description,
            smell.severity,
            smell.suggestion
        ])
    
    return output.getvalue()


if __name__ == '__main__':
    main()
