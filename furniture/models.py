from django.db import models

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('Classic', 'Classic'),
        ('Modern', 'Modern'),
        ('Decoration', 'Decoration'),
        ('Office', 'Office'),
        ('Hotel', 'Hotel'),
    ]

    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Modern')
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    main_image = models.ImageField(upload_to='products/images/')
    model_3d = models.FileField(upload_to='products/models/')

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='gallery', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/gallery/')

    def __str__(self):
        return f"Gallery Image for {self.product.name}"