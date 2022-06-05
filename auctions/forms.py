from django.forms import ModelForm
from auctions.models import Item


class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ["title", "description", "start_price", "category", "image"]
