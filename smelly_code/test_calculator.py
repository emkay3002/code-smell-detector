import unittest
import tempfile
import os
from calculator import Calculator, MathUtils, calculate_tax, process_payment, validate_email, validate_phone


class TestCalculator(unittest.TestCase):
    """Test cases for Calculator class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.calc = Calculator()
    
    def test_add(self):
        """Test addition operation."""
        result = self.calc.add(2, 3)
        self.assertEqual(result, 5)
        self.assertEqual(self.calc.last_result, 5)
    
    def test_subtract(self):
        """Test subtraction operation."""
        result = self.calc.subtract(10, 4)
        self.assertEqual(result, 6)
        self.assertEqual(self.calc.last_result, 6)
    
    def test_multiply(self):
        """Test multiplication operation."""
        result = self.calc.multiply(5, 6)
        self.assertEqual(result, 30)
        self.assertEqual(self.calc.last_result, 30)
    
    def test_divide(self):
        """Test division operation."""
        result = self.calc.divide(15, 3)
        self.assertEqual(result, 5)
        self.assertEqual(self.calc.last_result, 5)
    
    def test_divide_by_zero(self):
        """Test division by zero raises ValueError."""
        with self.assertRaises(ValueError):
            self.calc.divide(10, 0)
    
    def test_power(self):
        """Test power operation."""
        result = self.calc.power(2, 3)
        self.assertEqual(result, 8)
        self.assertEqual(self.calc.last_result, 8)
    
    def test_sqrt(self):
        """Test square root operation."""
        result = self.calc.sqrt(16)
        self.assertEqual(result, 4)
        self.assertEqual(self.calc.last_result, 4)
    
    def test_sqrt_negative(self):
        """Test square root of negative number raises ValueError."""
        with self.assertRaises(ValueError):
            self.calc.sqrt(-1)
    
    def test_complex_expression(self):
        """Test complex expression with many parameters."""
        result = self.calc.calculate_complex_expression(1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                                                       1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
        self.assertEqual(result, 1.0)
    
    def test_process_large_dataset(self):
        """Test processing large dataset."""
        data = [{'value': i} for i in range(1, 11)]
        result = self.calc.process_large_dataset(data)
        
        self.assertEqual(result['count'], 10)
        self.assertEqual(result['total'], 55)  # Sum of 1 to 10
        self.assertEqual(result['max'], 10)
        self.assertEqual(result['min'], 1)
    
    def test_history(self):
        """Test calculation history."""
        self.calc.add(1, 2)
        self.calc.multiply(3, 4)
        
        history = self.calc.get_history()
        self.assertEqual(len(history), 2)
        self.assertIn("add(1, 2) = 3", history)
        self.assertIn("multiply(3, 4) = 12", history)
    
    def test_clear_history(self):
        """Test clearing history."""
        self.calc.add(1, 2)
        self.calc.clear_history()
        self.assertEqual(len(self.calc.get_history()), 0)
    
    def test_save_and_load(self):
        """Test saving and loading calculator state."""
        self.calc.add(5, 3)
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            temp_file = f.name
        
        try:
            self.calc.save_to_file(temp_file)
            
            new_calc = Calculator()
            new_calc.load_from_file(temp_file)
            self.assertEqual(new_calc.last_result, 8)
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)


class TestMathUtils(unittest.TestCase):
    """Test cases for MathUtils class."""
    
    def test_factorial(self):
        """Test factorial calculation."""
        self.assertEqual(MathUtils.factorial(0), 1)
        self.assertEqual(MathUtils.factorial(1), 1)
        self.assertEqual(MathUtils.factorial(5), 120)
    
    def test_factorial_negative(self):
        """Test factorial of negative number raises ValueError."""
        with self.assertRaises(ValueError):
            MathUtils.factorial(-1)
    
    def test_fibonacci(self):
        """Test Fibonacci calculation."""
        self.assertEqual(MathUtils.fibonacci(0), 0)
        self.assertEqual(MathUtils.fibonacci(1), 1)
        self.assertEqual(MathUtils.fibonacci(5), 5)
        self.assertEqual(MathUtils.fibonacci(10), 55)
    
    def test_fibonacci_negative(self):
        """Test Fibonacci of negative number raises ValueError."""
        with self.assertRaises(ValueError):
            MathUtils.fibonacci(-1)


class TestTaxCalculation(unittest.TestCase):
    """Test cases for tax calculation function."""
    
    def test_tax_low_income(self):
        """Test tax for low income."""
        tax = calculate_tax(50, 0.1)
        self.assertEqual(tax, 0)
    
    def test_tax_medium_income(self):
        """Test tax for medium income."""
        tax = calculate_tax(30000, 0.1)
        self.assertEqual(tax, 300)  # 30000 * 0.01
    
    def test_tax_high_income(self):
        """Test tax for high income."""
        tax = calculate_tax(75000, 0.1)
        self.assertEqual(tax, 11250)  # 75000 * 0.15


class TestPaymentProcessing(unittest.TestCase):
    """Test cases for payment processing function."""
    
    def test_payment_usd(self):
        """Test payment processing in USD."""
        result = process_payment(100, "USD")
        self.assertEqual(result['amount'], 100)
        self.assertEqual(result['processing_fee'], 3)  # 100 * 0.03
        self.assertEqual(result['conversion_rate'], 1.0)
    
    def test_payment_eur(self):
        """Test payment processing in EUR."""
        result = process_payment(100, "EUR")
        self.assertEqual(result['amount'], 100)
        self.assertEqual(result['conversion_rate'], 0.85)


class TestValidation(unittest.TestCase):
    """Test cases for validation functions."""
    
    def test_validate_email_valid(self):
        """Test valid email addresses."""
        self.assertTrue(validate_email("test@example.com"))
        self.assertTrue(validate_email("user.name@domain.co.uk"))
    
    def test_validate_email_invalid(self):
        """Test invalid email addresses."""
        self.assertFalse(validate_email(""))
        self.assertFalse(validate_email("invalid-email"))
        self.assertFalse(validate_email("@domain.com"))
        self.assertFalse(validate_email("user@"))
    
    def test_validate_phone_valid(self):
        """Test valid phone numbers."""
        self.assertTrue(validate_phone("1234567890"))
        self.assertTrue(validate_phone("123456789012345"))
    
    def test_validate_phone_invalid(self):
        """Test invalid phone numbers."""
        self.assertFalse(validate_phone(""))
        self.assertFalse(validate_phone("123"))
        self.assertFalse(validate_phone("1234567890123456"))
        self.assertFalse(validate_phone("abc1234567"))


if __name__ == '__main__':
    unittest.main()
