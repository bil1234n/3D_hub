from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, ProductImage, ProductVariant
from django import forms

# Custom widget to handle multiple file selection professionally
class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

# views.py

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        # REMOVED model_3d and model_3d_link from here
        fields = ['category', 'name', 'price', 'description', 'main_image']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control mb-3'}),
            'name': forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Product Name'}),
            'price': forms.NumberInput(attrs={'class': 'form-control mb-3'}),
            'description': forms.Textarea(attrs={'class': 'form-control mb-3', 'rows': 3}),
            'main_image': forms.FileInput(attrs={'class': 'form-control mb-3'}),
        }

def product_add(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()

            # Handle Gallery Images
            gallery_files = request.FILES.getlist('gallery_images')
            for f in gallery_files:
                ProductImage.objects.create(product=product, image=f)

            # Handle 3D Variants (Type & Color)
            v_names = request.POST.getlist('variant_name[]')
            v_files = request.FILES.getlist('variant_file[]')
            v_links = request.POST.getlist('variant_link[]')

            for i in range(len(v_names)):
                if v_names[i]: # Only if a name was entered
                    # Check if file exists at this index, else None
                    file_to_upload = v_files[i] if i < len(v_files) else None
                    link_to_save = v_links[i] if i < len(v_links) else ""
                    
                    ProductVariant.objects.create(
                        product=product,
                        variant_name=v_names[i],
                        model_3d=file_to_upload,
                        model_3d_link=link_to_save
                    )

            return redirect('product_list')
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
    products = Product.objects.all().prefetch_related('variants')
    return render(request, 'product_management.html', {'products': products})

def product_delete(request, pk):
    """Remove a product from the collection"""
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product.delete()
        return redirect('product_list')
    return render(request, 'product_confirm_delete.html', {'product': product})

def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save()
            
            # Handle Gallery
            gallery_files = request.FILES.getlist('gallery_images')
            for f in gallery_files:
                ProductImage.objects.create(product=product, image=f)

            # Handle Variants (This will ADD new ones)
            v_names = request.POST.getlist('variant_name[]')
            v_files = request.FILES.getlist('variant_file[]')
            v_links = request.POST.getlist('variant_link[]')

            for i in range(len(v_names)):
                if v_names[i]:
                    file_to_upload = v_files[i] if i < len(v_files) else None
                    link_to_save = v_links[i] if i < len(v_links) else ""
                    
                    ProductVariant.objects.create(
                        product=product,
                        variant_name=v_names[i],
                        model_3d=file_to_upload,
                        model_3d_link=link_to_save
                    )
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'product_form.html', {
        'form': form, 
        'edit_mode': True, 
        'product': product
    })
