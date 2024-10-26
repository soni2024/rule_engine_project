from django.shortcuts import render, redirect
from .forms import RuleForm, CombineRulesForm, EvaluateRuleForm
from .models import Rule
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .ast import create_rule, combine_rules, evaluate_rule,Node
from django.core.exceptions import ValidationError
import re

def home(request):
    return render(request, 'rule_engine/home.html')

def create_rule_view(request):
    if request.method == 'POST':
        form = RuleForm(request.POST)
        if form.is_valid():
            rule_string = form.cleaned_data['rule_string']
            ast = create_rule(rule_string)
            Rule.objects.create(rule_string=rule_string, name=form.cleaned_data['name'], ast_representation=ast.__repr__())
            return redirect('home')
    else:
        form = RuleForm()
    return render(request, 'rule_engine/create_rule.html', {'form': form})

def combine_rules_view(request):
    if request.method == 'POST':
        form = CombineRulesForm(request.POST)
        if form.is_valid():
            selected_rules = form.cleaned_data['rule_ids']
            rule_strings = [rule.rule_string for rule in selected_rules]
            combined_ast = combine_rules(rule_strings)
            return render(request, 'rule_engine/combined_rule.html', {'combined_ast': combined_ast})
    else:
        form = CombineRulesForm()
    return render(request, 'rule_engine/combine_rules.html', {'form': form})


def evaluate_rule_view(request):
    if request.method == 'POST':
        form = EvaluateRuleForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            rule = Rule.objects.first()  # Example rule, you can change as per your logic
            ast_str = rule.ast_representation
            ast = Node.from_string(ast_str)  # Use custom method to parse the string back to Node
            result = evaluate_rule(ast, data)
            return render(request, 'rule_engine/evaluation_result.html', {'result': result})
    else:
        form = EvaluateRuleForm()
    return render(request, 'rule_engine/evaluate_rule.html', {'form': form})



def parse_rule_to_ast(rule_string):
    tokens = re.findall(r"(\w+\s*[><=]\s*[\w']+|\(|\)|and|or)", rule_string, re.IGNORECASE)
    tokens = [token.strip() for token in tokens if token.strip()]

    def build_ast(tokens):
        if len(tokens) == 1:
            return {"type": "operand", "value": tokens[0]}
        if tokens[0] == "(" and tokens[-1] == ")":
            return build_ast(tokens[1:-1])
        op_index = None
        for i, token in enumerate(tokens):
            if token.lower() in ["and", "or"]:
                op_index = i
                break
        if op_index is not None:
            operator = tokens[op_index].lower()
            left_tokens = tokens[:op_index]
            right_tokens = tokens[op_index+1:]
            return {
                "type": "operator",
                "operator": operator,
                "left": build_ast(left_tokens),
                "right": build_ast(right_tokens)
            }
        else:
            return {"type": "operand", "value": " ".join(tokens)}
    return build_ast(tokens)

def evaluate_ast(ast_node, attributes):
    if ast_node["type"] == "operand":
        operand = ast_node["value"]
        attribute, operator, threshold = parse_operand(operand)
        if attribute in attributes:
            attr_value = attributes[attribute]
            return compare(attr_value, operator, threshold)
        else:
            return False
    elif ast_node["type"] == "operator":
        left_result = evaluate_ast(ast_node["left"], attributes)
        right_result = evaluate_ast(ast_node["right"], attributes)
        if ast_node["operator"] == "and":
            return left_result and right_result
        elif ast_node["operator"] == "or":
            return left_result or right_result
    return False

def parse_operand(operand):
    match = re.match(r"(\w+)\s*(>|<|=)\s*([\w']+)", operand)
    if match:
        attribute, operator, threshold = match.groups()
        if threshold.isdigit():
            threshold = int(threshold)
        return attribute, operator, threshold
    raise ValueError(f"Invalid operand format: {operand}")

def compare(attr_value, operator, threshold):
    if operator == ">":
        return attr_value > threshold
    elif operator == "<":
        return attr_value < threshold
    elif operator == "=":
        return attr_value == threshold
    return False

# Create Rule API
@csrf_exempt
def create_rule_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            rule_string = data.get('rule')
            rule_name = data.get('name')
            if not rule_name or not rule_string:
                return JsonResponse({'status': 'error', 'message': 'Rule name and rule string are required.'}, status=400)
            rule = Rule(name=rule_name, rule_string=rule_string)
            rule.full_clean()  # Validate rule
            rule.save()
            ast = create_rule(rule_string)
            return JsonResponse({'status': 'success', 'ast': str(ast)}, status=200)
        except ValidationError as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

# Combine Rules API
@csrf_exempt
def combine_rules_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            rules = data.get('rules', [])
            combined_ast = combine_rules(rules)
            return JsonResponse({'status': 'success', 'combined_ast': str(combined_ast)}, status=200)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

# Evaluate Rule API
@csrf_exempt
def evaluate_rule_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            rule_string = data.get('rule')
            attributes = data.get('attributes')
            ast = parse_rule_to_ast(rule_string)
            result = evaluate_ast(ast, attributes)
            return JsonResponse({'status': 'success', 'result': result}, status=200)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
