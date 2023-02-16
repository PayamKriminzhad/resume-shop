from django import forms

class UserNewOrderForm(forms.Form):
    product_id = forms.IntegerField(
        widget=forms.HiddenInput(),
    )

    count = forms.IntegerField(
        widget=forms.NumberInput(),
        initial=1
    )

class UserNewOrderFormForComponent(forms.Form):
    product_id = forms.IntegerField(
        widget=forms.HiddenInput(),
    )

    count = forms.IntegerField(
        widget=forms.HiddenInput(),
    )
