# Django Rule Engine with AST

## Overview

This project is a simple 3-tier rule engine application (Simple UI, API, and Backend, Data) developed to determine user eligibility based on attributes like age, department, income, spend, etc. The system uses an Abstract Syntax Tree (AST) to represent conditional rules and allows for dynamic creation, combination, and modification of these rules.

## Features

- **Create Rule**: Define new eligibility rules.
- **Combine Rules**: Merge multiple rules into a single rule.
- **Evaluate Rule**: Test rules against user attributes to determine eligibility.
- **REST API**: Expose rule operations via API endpoints.

## Project Structure

my_rule_engine_project/ │ ├── manage.py # Django management script ├── db.sqlite3 # SQLite database (if using SQLite) │ ├── my_rule_engine/ # Main project directory │ ├── init.py │ ├── settings.py # Project settings │ ├── urls.py # Project URLs │ ├── wsgi.py # WSGI entry point for deployment │ ├── rule_engine/ # Application directory for the rule engine │ ├── init.py │ ├── admin.py # Admin interface for models │ ├── apps.py # Application configuration │ ├── migrations/ # Directory for migration files │ ├── models.py # Database models │ ├── tests.py # Unit tests for the application │ ├── urls.py # Application-specific URLs │ ├── views.py # View functions for handling requests │ ├── serializers.py # Serializers for converting data to/from JSON │ ├── ast.py # AST logic for rule parsing and evaluation │ ├── forms.py # Forms for user input (if needed) │ └── templates/ # Directory for HTML templates │ ├── base.html # Base template │ ├── index.html # Homepage template │ ├── rule_form.html # Template for rule input form │ ├── combine_rules.html # Template for combining rules │ ├── evaluation_result.html # Template for displaying evaluation results │ └── requirements.txt # Required packages for the project


## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/soni2024/rule_engine_project.git
    cd my_rule_engine_project
    ```

2. Create a virtual environment and activate it:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Run migrations:
    ```bash
    python manage.py migrate
    ```

5. Start the development server:
    ```bash
    python manage.py runserver
    ```

## Usage

### Web Interface

1. Navigate to `http://127.0.0.1:8000/` to access the homepage.
2. Use the navigation links to create rules, combine rules, and evaluate rules.

### REST API

#### Create Rule
- **Endpoint**: `/api/create_rule/`
- **Method**: POST
- **Request**:
    ```json
    {
        "name": "Rule1",
        "rule": "(age > 30 AND department = 'Sales')"
    }
    ```
- **Response**:
    ```json
    {
        "status": "success",
        "ast": "((age) > (30) AND (department) = ('Sales'))"
    }
    ```

#### Combine Rules
- **Endpoint**: `/api/combine_rules/`
- **Method**: POST
- **Request**:
    ```json
    {
        "rules": ["(age > 30 AND department = 'Sales')", "(age < 25 AND department = 'Marketing')"]
    }
    ```
- **Response**:
    ```json
    {
        "status": "success",
        "combined_ast": "(((age) > (30) AND (department) = ('Sales')) AND ((age) < (25) AND (department) = ('Marketing')))"
    }
    ```

#### Evaluate Rule
- **Endpoint**: `/api/evaluate_rule/`
- **Method**: POST
- **Request**:
    ```json
    {
        "rule": "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing'))",
        "attributes": {
            "age": 35,
            "department": "Sales",
            "salary": 60000,
            "experience": 3
        }
    }
    ```
- **Response**:
    ```json
    {
        "status": "success",
        "result": true
    }
    ```

## Tests

Run unit tests:
```bash
python manage.py test
