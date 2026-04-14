from django.conf import settings
from django.db import models
from django.utils.text import slugify


class Service(models.Model):
    CATEGORY_FACE = "face"
    CATEGORY_BODY = "body"
    CATEGORY_HAIR = "hair"

    CATEGORY_CHOICES = [
        (CATEGORY_FACE, "Da mặt"),
        (CATEGORY_BODY, "Body"),
        (CATEGORY_HAIR, "Triệt lông"),
    ]

    STATUS_ACTIVE = "active"
    STATUS_INACTIVE = "inactive"

    STATUS_CHOICES = [
        (STATUS_ACTIVE, "Hoạt động"),
        (STATUS_INACTIVE, "Tạm dừng"),
    ]

    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    short_description = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    duration_minutes = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=4.5)
    image_url = models.URLField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_ACTIVE)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["display_order", "id"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class CustomerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="customer_profile")
    full_name = models.CharField(max_length=150, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)
    loyalty_points = models.PositiveIntegerField(default=0)
    avatar_url = models.URLField(blank=True)
    member_since = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["user__username"]

    def __str__(self):
        return self.display_name

    @property
    def display_name(self):
        if self.full_name:
            return self.full_name
        fallback = f"{self.user.last_name} {self.user.first_name}".strip()
        return fallback or self.user.username
