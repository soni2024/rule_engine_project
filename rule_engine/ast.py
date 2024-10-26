import re

class InvalidRuleException(Exception):
    """Custom exception for invalid rules."""
    pass

class Node:
    def __init__(self, node_type, value=None, left=None, right=None):
        self.type = node_type  # "operand" or "operator"
        self.value = value      # operator or operand value
        self.left = left        # left child Node
        self.right = right      # right child Node

    def __repr__(self):
        if self.type == "operand":
            return f"({self.value})"
        return f"({self.left} {self.value} {self.right})"

    
    @classmethod
    def from_string(cls, string):
        string = string.strip()
        if string.startswith('(') and string.endswith(')'):
            string = string[1:-1]  # Remove outer parentheses
            tokens = re.split(r'\s+', string, 2)
            if len(tokens) == 3:
                left = cls.from_string(tokens[0])
                value = tokens[1]
                right = cls.from_string(tokens[2])
                return cls("operator", value, left, right)
            return cls("operand", string)
        return cls("operand", string)


def tokenize_rule(rule_string):
    """Tokenizes the rule string into operators and operands."""
    tokens = re.findall(r"\w+|[><=]+|'[^']*'|\(|\)|AND|OR", rule_string)
    return tokens


def parse_expression(tokens):
    """Parses tokens into an AST."""
    if not tokens:
        return None

    token = tokens.pop(0)

    if token == "(":
        left_node = parse_expression(tokens)
        operator = tokens.pop(0)  # Should be an operator
        right_node = parse_expression(tokens)
        tokens.pop(0)  # Pop the closing ")"
        return Node("operator", operator, left_node, right_node)

    elif token in ["AND", "OR"]:
        # Handle left node for AND/OR
        left_node = parse_expression(tokens)
        right_node = parse_expression(tokens) if tokens else None
        return Node("operator", token, left_node, right_node)

    else:
        # This must be an operand or a complete comparison expression
        if token in ["age", "department"]:  # Check for specific fields
            if tokens[0] in [">", "<", "="]:  # If the next token is an operator
                operator = tokens.pop(0)
                value = tokens.pop(0) if tokens[0].startswith("'") else tokens.pop(0)
                return Node("operator", operator, Node("operand", token), Node("operand", value))
        return Node("operand", token)






def create_rule(rule_string):
    """Creates a rule AST from the given rule string."""
    if not isinstance(rule_string, str) or not rule_string.strip():
        raise InvalidRuleException("Rule string is not valid or empty")
    if not re.match(r"^[\w\s><=ANDOR'\"()]+$", rule_string):
        raise InvalidRuleException("Rule contains invalid characters or format")
    
    tokens = tokenize_rule(rule_string)
    print("Tokens:", tokens)  # Debug: Print tokens
    return parse_expression(tokens)



def combine_rules(rules):
    """Combines multiple rules into a single AST with AND operators."""
    combined_rule = None
    for rule_string in rules:
        current_ast = create_rule(rule_string)
        if combined_rule is None:
            combined_rule = current_ast
        else:
            combined_rule = Node("operator", "AND", combined_rule, current_ast)
    return combined_rule

def evaluate_rule(node, data):
    """Evaluates the AST against provided data."""
    if node is None:
        return False

    if node.type == "operand":
        return evaluate_operand(node.value, data)

    elif node.type == "operator":
        left_value = evaluate_rule(node.left, data)
        if node.right is not None:
            right_value = evaluate_rule(node.right, data)
        else:
            right_value = True  # Treat absence of right as true for ANDs

        if node.value == "AND":
            return left_value and right_value
        elif node.value == "OR":
            return left_value or right_value

    return False

def evaluate_operand(condition, data):
    """Evaluates a single condition against provided data."""
    match = re.match(r"(\w+)\s*([><=]+)\s*([\w']+)", condition)
    if match:
        field, operator, value = match.groups()
        field = field.strip()
        value = value.strip().strip("'")

        if field in data:
            # Convert value to int if it's numeric
            if value.isdigit():
                value = int(value)

            # Evaluate based on the operator
            if operator == ">":
                return data[field] > value
            elif operator == "<":
                return data[field] < value
            elif operator == "=":
                return data[field] == value
    return False  # Default for invalid conditions
