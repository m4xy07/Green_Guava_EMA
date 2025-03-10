from django.db import models
from django.contrib.auth.models import User
from PIL import Image


# Extending User Model Using a One-To-One Link
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField()

    def __str__(self):
        return self.user.username

    # resizing images
    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.avatar.path)

        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)


class FarmerProfile(models.Model):
    VERIFICATION_STATUS = [
        ("not_filled", "Not Filled"),
        ("pending", "Pending Verification"),
        ("verified", "Verified"),
        ("rejected", "Rejected"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    verification_status = models.CharField(max_length=20, choices=VERIFICATION_STATUS, default="not_filled")
    rejection_reason = models.TextField(blank=True, null=True)

    # Farmer-specific fields
    land_area = models.FloatField(default=0.0, help_text="Land area in hectares")
    crop_type = models.CharField(max_length=100, null=True, blank=True)
    farming_practices = models.CharField(max_length=100, choices=[
        ("organic", "Organic"),
        ("conventional", "Conventional")
    ], null=True, blank=True)
    soil_type = models.CharField(max_length=100, null=True, blank=True)
    irrigation_method = models.CharField(max_length=100, choices=[
        ("drip", "Drip"),
        ("flood", "Flood"),
        ("sprinkler", "Sprinkler")
    ], null=True, blank=True)
    fertilizer_usage = models.CharField(max_length=100, choices=[
        ("organic", "Organic"),
        ("chemical", "Chemical")
    ], null=True, blank=True)
    cover_crops = models.BooleanField(default=False)
    tillage_practices = models.CharField(max_length=100, choices=[
        ("no-till", "No Till"),
        ("minimum-till", "Minimum Till"),
        ("conventional-till", "Conventional Till")
    ], null=True, blank=True)
    carbon_credits = models.FloatField(default=0.0)
    monetary_benefit = models.FloatField(default=0.0)  # New field
    address = models.TextField(null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    district = models.CharField(max_length=100, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)

    def calculate_monetary_benefit(self):
        min_rate = 500
        max_rate = 1000
        avg_rate = (min_rate + max_rate) / 2  # Taking an average for simplicity
        return self.carbon_credits * avg_rate

    def save(self, *args, **kwargs):
        # Update monetary benefit whenever carbon credits change
        self.monetary_benefit = self.calculate_monetary_benefit()

        # Set verification status to 'pending' once the form is filled
        if self.verification_status == "not_filled":
            self.verification_status = "pending"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.verification_status}"
