# 0x03. Unittests and Integration Tests

This project focuses on writing effective unit tests and integration tests for Python functions and classes. It is part of the ALX Backend specialization program.

## Description

In software development, tests help ensure code reliability and maintainability. This project emphasizes:

* Writing unit tests that validate the correctness of individual functions.
* Writing integration tests to ensure the entire system works as expected.
* Using `unittest` and `unittest.mock` for testing and mocking.
* Applying the `parameterized` library for multiple input testing.
* Mocking I/O operations such as HTTP requests.

## Learning Objectives

At the end of this project, you will be able to:

* Distinguish between unit and integration tests.
* Use `unittest` for writing test cases.
* Use `mock` to isolate tests from external systems.
* Use `parameterized.expand()` to test multiple input sets.
* Test memoized properties.

## Requirements

* All files are interpreted/compiled on Ubuntu 18.04 LTS using Python 3.7
* PEP8 style (`pycodestyle==2.5`) is followed.
* All Python files are executable and documented.
* Use of type annotations in all functions and methods.

## File Structure

```
0x03-Unittests_and_integration_tests/
├── README.md
├── client.py
├── fixtures.py
├── test_client.py
├── test_utils.py
└── utils.py
```

## How to Run Tests

To run the unit and integration tests:

```bash
python3 -m unittest test_utils.py
python3 -m unittest test_client.py
```

## Tools Used

* Python 3.7
* `unittest`
* `unittest.mock`
* `parameterized`

## Author

Mohameddeq Ahmed
