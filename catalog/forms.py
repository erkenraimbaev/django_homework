from django import forms

from catalog.models import Product, Version


class StyleFormMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ProductForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name_product', 'description', 'image', 'category', 'price', 'is_published')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        self.fields["is_published"].widget.attrs['class'] = 'form-check-input'

    def clean_name_product(self):
        error_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']
        cleaned_data = self.cleaned_data.get('name_product')
        if cleaned_data in error_words:
            raise forms.ValidationError('Такой продукт добавить нельзя!')
        return cleaned_data

    def clean_description(self):
        error_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']
        cleaned_data = self.cleaned_data.get('description')
        for word in error_words:
            if word in cleaned_data:
                raise forms.ValidationError('Такого слова в описании быть не может!')
        return cleaned_data


class VersionForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Version
        fields = ('version', 'name_version', 'product', 'current_version')
        # fields = '__all__'
