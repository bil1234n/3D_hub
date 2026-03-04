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
    
    # Images automatically use DEFAULT_FILE_STORAGE (Standard Media)
    main_image = models.ImageField(upload_to='products/images/')

    def __str__(self):
        return self.name

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE)
    variant_name = models.CharField(max_length=200, help_text="e.g., Red sofa with green corner")
    
    # 3D Models are explicitly forced to use Raw Storage (for .glb, .gltf, etc.)
    model_3d = models.FileField(
        upload_to='products/models/variants/',
        storage=RawMediaCloudinaryStorage(),
        blank=True, 
        null=True
    )
    
    model_3d_link = models.URLField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f"{self.product.name} - {self.variant_name}"

    @property
    def get_model_url(self):
        if self.model_3d:
            return self.model_3d.url
        return self.model_3d_link

class ProductImage(models.Model): # Gallery
    product = models.ForeignKey(Product, related_name='gallery', on_delete=models.CASCADE)
    
    # Gallery images automatically use DEFAULT_FILE_STORAGE
    image = models.ImageField(upload_to='products/gallery/')

    def __str__(self):
        return f"Gallery Image for {self.product.name}"
