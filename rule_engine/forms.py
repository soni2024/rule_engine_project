from django import forms
from .models import Rule

class RuleForm(forms.ModelForm):
    class Meta:
        model = Rule
        fields = ['name', 'rule_string']  # Included 'name' field too
        labels = {
            'rule_string': 'Enter Rule',
            'name': 'Rule Name'
        }

class CombineRulesForm(forms.Form):
    rule_ids = forms.ModelMultipleChoiceField(
        queryset=Rule.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label='Select Rules to Combine'
    )

class EvaluateRuleForm(forms.Form):
    age = forms.IntegerField(label='Age')
    department = forms.CharField(label='Department')
    salary = forms.IntegerField(label='Salary')
    experience = forms.IntegerField(label='Experience')
