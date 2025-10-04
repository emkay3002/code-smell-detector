# Code Smells Documentation

This document describes the code smells detected in the `smelly_code/calculator.py` file and their locations.

## 1. Long Method

**File:** `smelly_code/calculator.py`  
**Lines:** 67-120  
**Method:** `process_large_dataset`

**Description:** The `process_large_dataset` method is excessively long, containing over 50 lines of code. It performs multiple unrelated tasks including data processing, statistical calculations, and result formatting.

**Justification:** This method violates the Single Responsibility Principle by handling too many concerns in one place. It should be broken down into smaller, more focused methods.

**Suggested Refactoring:** Split into methods like `calculate_basic_stats()`, `calculate_advanced_stats()`, and `format_results()`.

## 2. God Class

**File:** `smelly_code/calculator.py`  
**Lines:** 8-150  
**Class:** `Calculator`

**Description:** The `Calculator` class has grown too large and handles too many responsibilities. It contains 15+ methods and multiple attributes, making it difficult to understand and maintain.

**Justification:** The class violates the Single Responsibility Principle by handling calculations, history management, file I/O, statistics, and configuration all in one place.

**Suggested Refactoring:** Split into separate classes like `BasicCalculator`, `HistoryManager`, `FileManager`, and `StatisticsCalculator`.

## 3. Duplicated Code

**File:** `smelly_code/calculator.py`  
**Lines:** 200-220 (validate_email) and 225-240 (validate_phone)

**Description:** The `validate_email` and `validate_phone` functions contain similar validation logic with repeated patterns for checking input validity.

**Justification:** Both functions follow the same validation pattern: check for empty input, check format, check length constraints. This duplication makes maintenance harder.

**Suggested Refactoring:** Extract common validation logic into a `validate_input()` helper function.

## 4. Large Parameter List

**File:** `smelly_code/calculator.py`  
**Lines:** 62-66  
**Method:** `calculate_complex_expression`

**Description:** The `calculate_complex_expression` method takes 20 parameters, making it extremely difficult to call and understand.

**Justification:** Having 20 parameters makes the method signature unwieldy and error-prone. It's easy to pass parameters in the wrong order.

**Suggested Refactoring:** Use a parameter object or data class to group related parameters, or use keyword arguments with default values.

## 5. Magic Numbers

**File:** `smelly_code/calculator.py`  
**Lines:** 155-160 (calculate_tax function)

**Description:** The `calculate_tax` function contains hardcoded numeric values (100, 0.01, 50000, 0.15, 100000, 0.25) without any explanation of their meaning.

**Justification:** These magic numbers make the code difficult to understand and maintain. If tax brackets change, the code needs to be modified in multiple places.

**Suggested Refactoring:** Define named constants like `LOW_INCOME_THRESHOLD = 100`, `LOW_TAX_RATE = 0.01`, etc.

## 6. Feature Envy

**File:** `smelly_code/calculator.py`  
**Lines:** 245-250  
**Method:** `send_notification`

**Description:** The `send_notification` function is more interested in the `EmailService` class than its own functionality. It makes multiple calls to `EmailService` methods.

**Justification:** This method violates the principle of encapsulation by being overly dependent on another class's interface. It should either be moved to the `EmailService` class or the functionality should be restructured.

**Suggested Refactoring:** Move the `send_notification` method to the `EmailService` class, or create a `NotificationService` that properly encapsulates the email functionality.

## Summary

The `calculator.py` file demonstrates all six major code smells:

1. **Long Method** - `process_large_dataset` method is too long
2. **God Class** - `Calculator` class has too many responsibilities  
3. **Duplicated Code** - Similar validation logic in `validate_email` and `validate_phone`
4. **Large Parameter List** - `calculate_complex_expression` has 20 parameters
5. **Magic Numbers** - Hardcoded values in `calculate_tax` function
6. **Feature Envy** - `send_notification` method is too dependent on `EmailService`

Each smell represents a different aspect of poor code design and provides opportunities for refactoring to improve code quality, maintainability, and readability.
