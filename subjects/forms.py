from django import forms

from .models import Subject


class SubjectForm(forms.ModelForm):
    """Staff-facing form for the subject edit page."""

    class Meta:
        model = Subject
        fields = ("generic",)
        widgets = {
            "generic": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
