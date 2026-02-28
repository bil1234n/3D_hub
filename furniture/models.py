from django.db import models
from cloudinary_storage.storage import RawMediaCloudinaryStorage

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
    
    # Images will automatically use the DEFAULT_FILE_STORAGE (Standard Media)
    main_image = models.ImageField(upload_to='products/images/')
    
    # 3D Models are explicitly forced to use Raw Storage
    model_3d = models.FileField(
        upload_to='products/models/',
        storage=RawMediaCloudinaryStorage()
    )

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='gallery', on_delete=models.CASCADE)
    
    # Gallery images also use standard Media storage
    image = models.ImageField(upload_to='products/gallery/')

    def __str__(self):
        return f"Gallery Image for {self.product.name}"
