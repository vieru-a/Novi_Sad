# from django import forms
#
#
# class FilterForm(forms.Form):
#     min_price = forms.IntegerField(label='Цена от', required=False, min_value=1)
#     max_price = forms.IntegerField(label='до', required=False, max_value=100000)
#     ordering = forms.ChoiceField(label='сортировка', required=False, choices=[
#         ['price', 'по увеличению цены'],
#         ['-price', 'по уменьшению цены'],
#         ['m2', 'по увеличению площади'],
#         ['-m2', 'по уменьшению площади']
#     ])
