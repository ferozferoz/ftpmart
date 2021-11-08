import sys

from PIL import Image
from io import BytesIO

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify



# Create your models here.


class Warranty(models.Model):

    warranty_type = models.CharField(max_length=200)
    warranty_desc = models.CharField(max_length=400)

    def __str__(self):
        return self.warranty_type


class ReturnPolicy(models.Model):
    return_policy_type = models.CharField(max_length=200)
    return_policy_desc = models.CharField(max_length=400)

    def __str__(self):
        return self.return_policy_type


class Category(models.Model):

    name = models.CharField(max_length=200)
    slug = models.SlugField(null=True, blank=True, unique=True)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='child', on_delete=models.CASCADE)

    def __breadcrumb__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent

        return '->'.join(reversed(full_path))

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Supplier(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    home_phone = models.CharField(max_length=15)
    office_phone = models.CharField(max_length=15)
    joined_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Item(models.Model):

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,related_name='category')
    sub_category = models.ForeignKey(Category, on_delete=models.CASCADE,related_name='sub_category')
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    sell_quantity = models.CharField(max_length=200)
    cost_price = models.DecimalField( max_digits=10, decimal_places=2)
    display_original_selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    display_new_selling_price = models.DecimalField(max_digits=10,  decimal_places=2)
    description = models.TextField()
    warranty = models.ForeignKey(Warranty, on_delete=models.DO_NOTHING)
    return_policy = models.ForeignKey(ReturnPolicy, on_delete=models.DO_NOTHING)

    image_1 = models.FileField()
    image_2 = models.FileField(null=True,blank=True)
    image_3 = models.FileField(null=True,blank=True)
    image_4 = models.FileField(null=True,blank=True)
    image_5 = models.FileField(null=True,blank=True)

    view_count = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    availability = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):  # new
        # creating slug automatically
        if not self.slug:
            self.slug = slugify(self.name)

        # resizing image to 340 x 340 before saving it
        if self.image_1:
            im = Image.open(self.image_1)
            # Resize/modify the image
            im = im.resize((340,340))
            # after modifications, save it to the output
            im.save(self.image_1.path, format='JPEG', quality=90)

        if self.image_2:
            im = Image.open(self.image_2)
            # Resize/modify the image
            im = im.resize((340, 340))
            # after modifications, save it to the output
            im.save(self.image_2.path, format='JPEG', quality=90)

        if self.image_3:
            im = Image.open(self.image_3)
            # Resize/modify the image
            im = im.resize((340, 340))
            # after modifications, save it to the output
            im.save(self.image_3.path, format='JPEG', quality=90)

        if self.image_4:
            im = Image.open(self.image_4)
            # Resize/modify the image
            im = im.resize((340, 340))
            # after modifications, save it to the output
            im.save(self.image_4.path, format='JPEG', quality=90)

        if self.image_5:
            im = Image.open(self.image_5)
            # Resize/modify the image
            im = im.resize((340, 340))
            # after modifications, save it to the output
            im.save(self.image_5.path, format='JPEG', quality=90)

        return super().save(*args, **kwargs)


class InventoryManager(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="admins")
    mobile = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username


