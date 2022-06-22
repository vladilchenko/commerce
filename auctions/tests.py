from django.test import TestCase
from .models import Item, Bid, Comment, User

# Create your tests here.

class CommerceTestCase(TestCase):

    def setUp(self):
        self.vlad = User(email="vlad@hi.com", password="11111111", username="Vlad")
        self.vlad.save()
        self.tonya = User(email="tonya@hi.com", password="11111111", username="Tonya")
        self.tonya.save()

        self.book = Item(
            title = "Love & Fantasy",
            description = "Romance book with magic",
            user = self.tonya,
            start_price = 25,
            category = "book"
        )
        self.book.save()
    
    def test_bid(self):
        bid = Bid(
            item = self.book,
            price = 27,
            user = self.vlad
        )
        bid.save()

        self.assertEqual(self.book.bids.last().price, 27)
