import uuid
from decimal import Decimal
from django.db import models
from django.db.models import Sum
from django.conf import settings

from django_countries.fields import CountryField

from products.models import Product
from profiles.models import UserProfile


class Order(models.Model):
    order_number = models.CharField(max_length=32, null=False, editable=False)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = CountryField(blank_label='(select your country)', null=False, blank=False)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    postcode = models.CharField(max_length=20, null=False, blank=False)
    street_address = models.CharField(max_length=80, null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)
    delivery_cost = models.DecimalField(max_digits=6, decimal_places=2, null=False, default=0)
    order_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    original_cart = models.TextField(null=False, blank=False, default='')
    stripe_pid = models.CharField(max_length=254, null=False, blank=False, default='')
    loyalty_points = models.DecimalField(max_digits=10, decimal_places=0, null=False, default=0)

    def _generate_order_number(self):
        """
        Generate a random, unique order number using UUID
        """
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """
        Update grand total each time a line item is added,
        accounting for delivery costs.
        """
        self.order_total = self.lineitems.aggregate(Sum('lineitem_total'))['lineitem_total__sum'] or 0
        if self.order_total < settings.FREE_DELIVERY_THRESHOLD:
            self.delivery_cost = settings.STANDARD_DELIVERY_COSTS
        else:
            self.delivery_cost = 0
        self.grand_total = self.order_total + self.delivery_cost
        self.save()

    def update_loyalty_points(self):
        """
        Update loyalty points based on order_total.
        """
        self.order_total = self.lineitems.aggregate(Sum('lineitem_total'))['lineitem_total__sum'] or 0
        if self.order_total < 10:
            self.loyalty_points = 0
        else:
            self.loyalty_points = int(self.order_total / 10)
        self.save()

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the order number
        if it hasn't been set already.
        """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        """
        Override the original save method to set the order total
        with 10% discount if first purchase per account
        """
        if self.user_profile:
            if self.user_profile.total_loyalty_points == 0:
                self.order_total = round(self.order_total - (self.order_total * Decimal(0.10)), 2)
                # recalculate loyalty points based on discounted costs
                if self.order_total < 10:
                    self.loyalty_points = 0
                else:
                    self.loyalty_points = int(self.order_total / 10)
                # revise standard order delivery costs based on discounted costs
                if self.order_total < settings.FREE_DELIVERY_THRESHOLD:
                    self.delivery_cost = settings.STANDARD_DELIVERY_COSTS
                else:
                    self.delivery_cost = 0
                # save the new costs
                self.grand_total = self.order_total + self.delivery_cost
        """
        Override the original save method to set the delivery cost
        to 0 if user has level 2 or 3 loyalty status
        """
        if self.user_profile:
            if self.user_profile.total_loyalty_points > 60:
                self.delivery_cost = 0
                self.grand_total = self.order_total + self.delivery_cost
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number


class OrderLineItem(models.Model):
    order = models.ForeignKey(Order, null=False, blank=False, on_delete=models.CASCADE, related_name='lineitems')
    product = models.ForeignKey(Product, null=False, blank=False, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False, editable=False)

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the lineitem total
        and update the order total.
        """
        self.lineitem_total = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'SKU {self.product.sku} on order {self.order.order_number}'
