import ast
import re
import yaml
import os
from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass


@dataclass
class CodeSmell:
    """Represents a detected code smell."""
    smell_type: str
    file_path: str
    line_number: int
    description: str
    severity: str = "medium"
    suggestion: str = ""


class CodeSmellDetector:
    """Main class for detecting code smells in Python code."""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize the detector with configuration."""
        self.config = self._load_config(config_path)
        self.smells = []
    
    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        default_config = {
            'long_method': {
                'enabled': True,
                'max_lines': 20,
                'severity': 'high'
            },
            'god_class': {
                'enabled': True,
                'max_methods': 10,
                'max_attributes': 15,
                'severity': 'high'
            },
            'duplicated_code': {
                'enabled': True,
                'min_similarity': 0.8,
                'min_lines': 5,
                'severity': 'medium'
            },
            'large_parameter_list': {
                'enabled': True,
                'max_parameters': 5,
                'severity': 'medium'
            },
            'magic_numbers': {
                'enabled': True,
                'severity': 'low'
            },
            'feature_envy': {
                'enabled': True,
                'max_external_calls': 3,
                'severity': 'medium'
            }
        }
        
        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    user_config = yaml.safe_load(f)
                    # Merge user config with defaults
                    for key, value in user_config.items():
                        if key in default_config:
                            default_config[key].update(value)
            except Exception as e:
                print(f"Warning: Could not load config file {config_path}: {e}")
        
        return default_config
    
    def detect_smells(self, file_path: str, only: Optional[List[str]] = None, 
                     exclude: Optional[List[str]] = None) -> List[CodeSmell]:
        """Detect code smells in a Python file."""
        self.smells = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                source_code = f.read()
            
            tree = ast.parse(source_code, filename=file_path)
            
            # Determine which detectors to run
            detectors_to_run = self._get_enabled_detectors(only, exclude)
            
            # Run each detector
            for detector_name in detectors_to_run:
                if detector_name == 'long_method':
                    self._detect_long_methods(tree, file_path)
                elif detector_name == 'god_class':
                    self._detect_god_classes(tree, file_path)
                elif detector_name == 'duplicated_code':
                    self._detect_duplicated_code(source_code, file_path)
                elif detector_name == 'large_parameter_list':
                    self._detect_large_parameter_lists(tree, file_path)
                elif detector_name == 'magic_numbers':
                    self._detect_magic_numbers(tree, file_path)
                elif detector_name == 'feature_envy':
                    self._detect_feature_envy(tree, file_path)
        
        except Exception as e:
            print(f"Error analyzing {file_path}: {e}")
        
        return self.smells
    
    def _get_enabled_detectors(self, only: Optional[List[str]], 
                              exclude: Optional[List[str]]) -> List[str]:
        """Get list of detectors to run based on only/exclude options."""
        all_detectors = ['long_method', 'god_class', 'duplicated_code', 
                        'large_parameter_list', 'magic_numbers', 'feature_envy']
        
        if only:
            return [d for d in only if d in all_detectors and self.config.get(d, {}).get('enabled', True)]
        
        enabled_detectors = [d for d in all_detectors if self.config.get(d, {}).get('enabled', True)]
        
        if exclude:
            return [d for d in enabled_detectors if d not in exclude]
        
        return enabled_detectors
    
    def _detect_long_methods(self, tree: ast.AST, file_path: str):
        """Detect methods that are too long."""
        max_lines = self.config['long_method']['max_lines']
        severity = self.config['long_method']['severity']
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Count lines in the method
                method_lines = self._count_method_lines(node)
                if method_lines > max_lines:
                    self.smells.append(CodeSmell(
                        smell_type="Long Method",
                        file_path=file_path,
                        line_number=node.lineno,
                        description=f"Method '{node.name}' has {method_lines} lines (max: {max_lines})",
                        severity=severity,
                        suggestion="Consider breaking this method into smaller, more focused methods."
                    ))
    
    def _count_method_lines(self, method_node: ast.FunctionDef) -> int:
        """Count the number of lines in a method."""
        if not method_node.body:
            return 0
        
        # Get the line range of the method
        start_line = method_node.lineno
        end_line = start_line
        
        for node in ast.walk(method_node):
            if hasattr(node, 'lineno') and node.lineno > end_line:
                end_line = node.lineno
        
        return end_line - start_line + 1
    
    def _detect_god_classes(self, tree: ast.AST, file_path: str):
        """Detect classes that are too large (God Class)."""
        max_methods = self.config['god_class']['max_methods']
        max_attributes = self.config['god_class']['max_attributes']
        severity = self.config['god_class']['severity']
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                method_count = len([n for n in node.body if isinstance(n, ast.FunctionDef)])
                attribute_count = len([n for n in node.body if isinstance(n, ast.Assign)])
                
                if method_count > max_methods or attribute_count > max_attributes:
                    self.smells.append(CodeSmell(
                        smell_type="God Class",
                        file_path=file_path,
                        line_number=node.lineno,
                        description=f"Class '{node.name}' has {method_count} methods and {attribute_count} attributes (max: {max_methods} methods, {max_attributes} attributes)",
                        severity=severity,
                        suggestion="Consider splitting this class into smaller, more focused classes."
                    ))
    
    def _detect_duplicated_code(self, source_code: str, file_path: str):
        """Detect duplicated code using regex patterns."""
        min_similarity = self.config['duplicated_code']['min_similarity']
        min_lines = self.config['duplicated_code']['min_lines']
        severity = self.config['duplicated_code']['severity']
        
        lines = source_code.split('\n')
        
        # Simple duplication detection by looking for repeated code blocks
        for i in range(len(lines) - min_lines):
            block = lines[i:i + min_lines]
            block_text = '\n'.join(block)
            
            # Look for this block elsewhere in the code
            occurrences = []
            for j in range(i + min_lines, len(lines) - min_lines + 1):
                other_block = lines[j:j + min_lines]
                other_text = '\n'.join(other_block)
                
                if self._calculate_similarity(block_text, other_text) >= min_similarity:
                    occurrences.append(j)
            
            if occurrences:
                self.smells.append(CodeSmell(
                    smell_type="Duplicated Code",
                    file_path=file_path,
                    line_number=i + 1,
                    description=f"Code block starting at line {i + 1} appears {len(occurrences) + 1} times",
                    severity=severity,
                    suggestion="Extract this code into a separate function to avoid duplication."
                ))
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two text blocks."""
        if not text1 or not text2:
            return 0.0
        
        # Simple similarity calculation based on common words
        words1 = set(text1.split())
        words2 = set(text2.split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0
    
    def _detect_large_parameter_lists(self, tree: ast.AST, file_path: str):
        """Detect methods with too many parameters."""
        max_parameters = self.config['large_parameter_list']['max_parameters']
        severity = self.config['large_parameter_list']['severity']
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                param_count = len(node.args.args)
                if param_count > max_parameters:
                    self.smells.append(CodeSmell(
                        smell_type="Large Parameter List",
                        file_path=file_path,
                        line_number=node.lineno,
                        description=f"Method '{node.name}' has {param_count} parameters (max: {max_parameters})",
                        severity=severity,
                        suggestion="Consider using a parameter object or data class to group related parameters."
                    ))
    
    def _detect_magic_numbers(self, tree: ast.AST, file_path: str):
        """Detect magic numbers in the code."""
        severity = self.config['magic_numbers']['severity']
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
                # Check if it's a magic number (not 0, 1, or common values)
                value = node.value
                if value not in [0, 1, -1, 2, 10, 100, 1000]:
                    # Skip magic numbers in import statements or other safe contexts
                    parent = getattr(node, 'parent', None)
                    if parent and isinstance(parent, ast.Import):
                        continue
                    
                    self.smells.append(CodeSmell(
                        smell_type="Magic Number",
                        file_path=file_path,
                        line_number=node.lineno,
                        description=f"Magic number {value} found",
                        severity=severity,
                        suggestion="Replace with a named constant to improve readability."
                    ))
    
    def _detect_feature_envy(self, tree: ast.AST, file_path: str):
        """Detect methods that are more interested in other classes."""
        max_external_calls = self.config['feature_envy']['max_external_calls']
        severity = self.config['feature_envy']['severity']
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                external_calls = 0
                for child in ast.walk(node):
                    if isinstance(child, ast.Call):
                        if isinstance(child.func, ast.Attribute):
                            # Check if it's calling a method on another object
                            if hasattr(child.func, 'value') and isinstance(child.func.value, ast.Name):
                                external_calls += 1
                
                if external_calls > max_external_calls:
                    self.smells.append(CodeSmell(
                        smell_type="Feature Envy",
                        file_path=file_path,
                        line_number=node.lineno,
                        description=f"Method '{node.name}' makes {external_calls} external calls (max: {max_external_calls})",
                        severity=severity,
                        suggestion="Consider moving this method to the class it's most interested in."
                    ))
    
    def generate_report(self, output_file: Optional[str] = None) -> str:
        """Generate a report of detected code smells."""
        if not self.smells:
            return "No code smells detected."
        
        report_lines = []
        report_lines.append("Code Smell Detection Report")
        report_lines.append("=" * 50)
        report_lines.append("")
        
        # Group by smell type
        by_type = {}
        for smell in self.smells:
            if smell.smell_type not in by_type:
                by_type[smell.smell_type] = []
            by_type[smell.smell_type].append(smell)
        
        for smell_type, smells in by_type.items():
            report_lines.append(f"{smell_type} ({len(smells)} instances):")
            report_lines.append("-" * 30)
            
            for smell in smells:
                report_lines.append(f"  File: {smell.file_path}")
                report_lines.append(f"  Line: {smell.line_number}")
                report_lines.append(f"  Description: {smell.description}")
                report_lines.append(f"  Severity: {smell.severity}")
                report_lines.append(f"  Suggestion: {smell.suggestion}")
                report_lines.append("")
        
        report_text = "\n".join(report_lines)
        
        if output_file:
            with open(output_file, 'w') as f:
                f.write(report_text)
        
        return report_text
