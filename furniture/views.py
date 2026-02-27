from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, ProductImage
from django import forms

# Custom widget to handle multiple file selection professionally
class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class ProductForm(forms.ModelForm):
    # REMOVE 'gallery_images' from here entirely.
    # We handle it manually in the view using request.FILES.getlist()
    
    class Meta:
        model = Product
        fields = ['category', 'name', 'price', 'description', 'main_image', 'model_3d']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control mb-3'}),
            'name': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'price': forms.NumberInput(attrs={'class': 'form-control mb-3'}),
            'description': forms.Textarea(attrs={'class': 'form-control mb-3', 'rows': 3}),
            'main_image': forms.FileInput(attrs={'class': 'form-control mb-3'}),
            'model_3d': forms.FileInput(attrs={'class': 'form-control mb-3'}),
        }

def product_add(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        
        # We manually grab the files here
        gallery_files = request.FILES.getlist('gallery_images')
        
        if form.is_valid():
            # This will now work because 'gallery_images' isn't blocking it
            product = form.save()
            
            # Save the manual gallery files
            for f in gallery_files:
                ProductImage.objects.create(product=product, image=f)
                
            return redirect('product_list')
        else:
            print(form.errors) # This will now be empty if other fields are filled
    else:
        form = ProductForm()
    return render(request, 'product_form.html', {'form': form})

# --- VIEW FUNCTIONS ---

def index(request):
    """The premium 3D showroom page"""
    # prefetch_related('gallery') optimizes the database query to get all images at once
    products = Product.objects.all().prefetch_related('gallery')
    return render(request, 'index.html', {'products': products})

def product_list(request):
    """Management dashboard table"""
    products = Product.objects.all()
    return render(request, 'product_management.html', {'products': products})

def product_delete(request, pk):
    """Remove a product from the collection"""
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product.delete()
        return redirect('product_list')
    return render(request, 'product_confirm_delete.html', {'product': product})