"""
A calculator application with intentional code smells for educational purposes.
This module demonstrates various code smells while maintaining functionality.
"""

import math
import os
import sys
from typing import List, Dict, Any


class Calculator:
    """A calculator class that demonstrates the God Class code smell."""
    
    def __init__(self):
        self.history = []
        self.user_preferences = {}
        self.cache = {}
        self.config = {}
        self.stats = {}
        self.last_result = 0
        
    def add(self, a: float, b: float) -> float:
        """Add two numbers."""
        result = a + b
        self.history.append(f"add({a}, {b}) = {result}")
        self.last_result = result
        return result
    
    def subtract(self, a: float, b: float) -> float:
        """Subtract two numbers."""
        result = a - b
        self.history.append(f"subtract({a}, {b}) = {result}")
        self.last_result = result
        return result
    
    def multiply(self, a: float, b: float) -> float:
        """Multiply two numbers."""
        result = a * b
        self.history.append(f"multiply({a}, {b}) = {result}")
        self.last_result = result
        return result
    
    def divide(self, a: float, b: float) -> float:
        """Divide two numbers."""
        if b == 0:
            raise ValueError("Cannot divide by zero")
        result = a / b
        self.history.append(f"divide({a}, {b}) = {result}")
        self.last_result = result
        return result
    
    def power(self, base: float, exponent: float) -> float:
        """Calculate base raised to the power of exponent."""
        result = base ** exponent
        self.history.append(f"power({base}, {exponent}) = {result}")
        self.last_result = result
        return result
    
    def sqrt(self, number: float) -> float:
        """Calculate square root."""
        if number < 0:
            raise ValueError("Cannot calculate square root of negative number")
        result = math.sqrt(number)
        self.history.append(f"sqrt({number}) = {result}")
        self.last_result = result
        return result
    
    def calculate_complex_expression(self, a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t):
        """Demonstrates Large Parameter List code smell."""
        # This method has too many parameters (20 parameters)
        result = (a + b + c + d + e + f + g + h + i + j + k + l + m + n + o + p + q + r + s + t) / 20
        self.history.append(f"complex_expression result = {result}")
        self.last_result = result
        return result
    
    def process_large_dataset(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Demonstrates Long Method code smell."""
        # This method is too long and does too many things
        total = 0
        count = 0
        max_val = float('-inf')
        min_val = float('inf')
        even_count = 0
        odd_count = 0
        positive_count = 0
        negative_count = 0
        zero_count = 0
        sum_squares = 0
        sum_cubes = 0
        geometric_mean = 1
        harmonic_mean = 0
        
        # Process each item in the dataset
        for item in data:
            if 'value' in item:
                value = item['value']
                total += value
                count += 1
                
                if value > max_val:
                    max_val = value
                if value < min_val:
                    min_val = value
                
                if value % 2 == 0:
                    even_count += 1
                else:
                    odd_count += 1
                
                if value > 0:
                    positive_count += 1
                elif value < 0:
                    negative_count += 1
                else:
                    zero_count += 1
                
                sum_squares += value * value
                sum_cubes += value * value * value
                geometric_mean *= abs(value) if value != 0 else 1
                harmonic_mean += 1 / value if value != 0 else 0
        
        # Calculate statistics
        mean = total / count if count > 0 else 0
        variance = 0
        for item in data:
            if 'value' in item:
                variance += (item['value'] - mean) ** 2
        variance = variance / count if count > 0 else 0
        std_dev = math.sqrt(variance)
        
        geometric_mean = geometric_mean ** (1 / count) if count > 0 else 0
        harmonic_mean = count / harmonic_mean if harmonic_mean > 0 else 0
        
        # Create result dictionary
        result = {
            'total': total,
            'count': count,
            'mean': mean,
            'max': max_val,
            'min': min_val,
            'variance': variance,
            'std_dev': std_dev,
            'even_count': even_count,
            'odd_count': odd_count,
            'positive_count': positive_count,
            'negative_count': negative_count,
            'zero_count': zero_count,
            'sum_squares': sum_squares,
            'sum_cubes': sum_cubes,
            'geometric_mean': geometric_mean,
            'harmonic_mean': harmonic_mean
        }
        
        self.history.append(f"process_large_dataset processed {count} items")
        return result
    
    def save_to_file(self, filename: str):
        """Save calculator state to file."""
        with open(filename, 'w') as f:
            f.write(f"Calculator History:\n")
            for entry in self.history:
                f.write(f"{entry}\n")
            f.write(f"Last Result: {self.last_result}\n")
    
    def load_from_file(self, filename: str):
        """Load calculator state from file."""
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    if line.startswith("Last Result:"):
                        self.last_result = float(line.split(":")[1].strip())
    
    def get_history(self) -> List[str]:
        """Get calculation history."""
        return self.history.copy()
    
    def clear_history(self):
        """Clear calculation history."""
        self.history.clear()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get calculator statistics."""
        return {
            'total_calculations': len(self.history),
            'last_result': self.last_result,
            'cache_size': len(self.cache)
        }


class MathUtils:
    """Utility class for mathematical operations."""
    
    @staticmethod
    def factorial(n: int) -> int:
        """Calculate factorial of n."""
        if n < 0:
            raise ValueError("Factorial not defined for negative numbers")
        if n == 0 or n == 1:
            return 1
        return n * MathUtils.factorial(n - 1)
    
    @staticmethod
    def fibonacci(n: int) -> int:
        """Calculate nth Fibonacci number."""
        if n < 0:
            raise ValueError("Fibonacci not defined for negative numbers")
        if n <= 1:
            return n
        return MathUtils.fibonacci(n - 1) + MathUtils.fibonacci(n - 2)


def calculate_tax(income: float, rate: float) -> float:
    """Calculate tax amount."""
    # Magic numbers: 100, 0.01, 50000, 0.15, 100000, 0.25
    if income < 100:
        return 0
    elif income < 50000:
        return income * 0.01
    elif income < 100000:
        return income * 0.15
    else:
        return income * 0.25


def process_payment(amount: float, currency: str) -> Dict[str, Any]:
    """Process payment with magic numbers."""
    # Magic numbers: 0.03, 0.5, 1000, 0.02
    processing_fee = amount * 0.03
    if currency == "USD":
        conversion_rate = 1.0
    elif currency == "EUR":
        conversion_rate = 0.85
    else:
        conversion_rate = 0.5
    
    total_amount = amount + processing_fee
    if total_amount > 1000:
        discount = total_amount * 0.02
        total_amount -= discount
    
    return {
        'amount': amount,
        'processing_fee': processing_fee,
        'conversion_rate': conversion_rate,
        'total_amount': total_amount
    }


def validate_email(email: str) -> bool:
    """Validate email address."""
    # Duplicated code: email validation logic repeated
    if not email or '@' not in email:
        return False
    
    parts = email.split('@')
    if len(parts) != 2:
        return False
    
    local, domain = parts
    if not local or not domain:
        return False
    
    if '.' not in domain:
        return False
    
    return True


def validate_phone(phone: str) -> bool:
    """Validate phone number."""
    # Duplicated code: similar validation logic as email
    if not phone or len(phone) < 10:
        return False
    
    if not phone.isdigit():
        return False
    
    if len(phone) > 15:
        return False
    
    return True


def send_notification(message: str, recipient: str):
    """Send notification - demonstrates Feature Envy."""
    # This method is more interested in the EmailService class than its own
    email_service = EmailService()
    email_service.send_email(recipient, "Notification", message)
    email_service.log_sent_email(recipient, message)
    email_service.update_email_stats(recipient)


class EmailService:
    """Email service class."""
    
    def __init__(self):
        self.sent_emails = []
        self.email_stats = {}
    
    def send_email(self, to: str, subject: str, body: str):
        """Send email."""
        print(f"Email sent to {to}: {subject}")
        self.sent_emails.append({'to': to, 'subject': subject, 'body': body})
    
    def log_sent_email(self, to: str, body: str):
        """Log sent email."""
        print(f"Logged email to {to}")
    
    def update_email_stats(self, to: str):
        """Update email statistics."""
        if to not in self.email_stats:
            self.email_stats[to] = 0
        self.email_stats[to] += 1


def main():
    """Main function to demonstrate the calculator."""
    calc = Calculator()
    
    # Basic operations
    print("Basic Calculator Operations:")
    print(f"2 + 3 = {calc.add(2, 3)}")
    print(f"10 - 4 = {calc.subtract(10, 4)}")
    print(f"5 * 6 = {calc.multiply(5, 6)}")
    print(f"15 / 3 = {calc.divide(15, 3)}")
    print(f"2^3 = {calc.power(2, 3)}")
    print(f"√16 = {calc.sqrt(16)}")
    
    # Complex expression with many parameters
    result = calc.calculate_complex_expression(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 
                                              11, 12, 13, 14, 15, 16, 17, 18, 19, 20)
    print(f"Complex expression result: {result}")
    
    # Process large dataset
    data = [{'value': i} for i in range(1, 101)]
    stats = calc.process_large_dataset(data)
    print(f"Dataset statistics: {stats}")
    
    # Tax calculation with magic numbers
    tax = calculate_tax(75000, 0.15)
    print(f"Tax for $75,000: ${tax}")
    
    # Payment processing
    payment = process_payment(500, "USD")
    print(f"Payment processing: {payment}")
    
    # Validation functions
    print(f"Email validation: {validate_email('test@example.com')}")
    print(f"Phone validation: {validate_phone('1234567890')}")
    
    # Feature envy demonstration
    send_notification("Hello World", "user@example.com")
    
    print(f"Calculator history: {len(calc.get_history())} operations")


if __name__ == "__main__":
    main()
