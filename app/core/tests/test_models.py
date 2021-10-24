#from unittest.mock import patch

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(email='a.jeebon@gmail.com', password='testpass'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


def sample_restaurant(name="Samdard"):
    """Create a sample restaurant"""
    return models.Restaurant.objects.create(
        name=name
    )


def sample_menu(name="Dish 2", items='Rice 2, Matton 3, Beef 3, Salad 3'):
    """Create a sample restaurant"""
    return models.Menu.objects.create(
        name=name,
        restaurant=sample_restaurant(),
        items=items
    )

class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'a.jeebon@gmail.com'
        password = 'test@123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = 'a.jeebon@gmail.com'
        user = get_user_model().objects.create_user(email, 'test@1234')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test@1234')

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'a.jeebon@gmail.com',
            'test@1234'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)


    def test_restaurant_str(self):
        """Test the restaurant string representation"""
        restaurant = models.Restaurant.objects.create(
            name='Star Kabab'
        )
        self.assertEqual(str(restaurant), restaurant.name)

    def test_menu_str(self):
        """Test the menu string representation"""
        menu = models.Menu.objects.create(
            name='Dish 1',
            restaurant=sample_restaurant(),
            items= 'Rice, Matton, Beef, Salad'
        )
        self.assertEqual(str(menu), menu.name)

    def test_vote_object(self):
        """Test the vote  representation"""
        vote = models.Vote.objects.create(
            user=sample_user(),
            menu=sample_menu()
        )
        self.assertIsNotNone(vote.id)
