# -*- encoding: utf-8 -*-
from django.db import models
import os
from PIL import Image
from django.conf import settings


def photo_resize(image_path, sizeMustBe=200):

    img = Image.open(image_path)
    (width, height) = img.size
    newsize = (width * sizeMustBe / height, sizeMustBe)
    img = img.resize(newsize, Image.ANTIALIAS)
    img.save(image_path)


def get_path(instance, filename):
    """
    Return full path for image contained in Person.photo
    Photo should be named photo_%id%.%extensions%
    If file with that name exist, it will delete
    """
    if not instance.id:
        return os.path.join('photo', filename)
    else:
        f_extension = filename.split('.')[1]
        newname = "photo_%i.%s" % (instance.id, f_extension)
        _path = os.path.normpath(
            os.path.join(settings.MEDIA_ROOT, 'photo'))
        full_path = os.path.join(_path, newname)
        if os.path.exists(full_path):
            os.remove(full_path)
        return os.path.join('photo', newname)


class Person(models.Model):
    first_name = models.CharField("First Name", max_length=30)
    last_name = models.CharField("Last Name", max_length=30)
    birth_date = models.DateField("Date of Birth")
    con_email = models.EmailField("Email", max_length=79)
    con_jabbber = models.EmailField("Jabber", max_length=79)
    con_skype = models.CharField("Skype", max_length=79)
    bio = models.TextField("Bio", max_length=400)
    con_other = models.TextField("Other Contacts",
                                 max_length=400, blank=True)
    photo = models.ImageField("Photo", upload_to=get_path,
                              blank=True, null=True)

    def __str__(self):
        return "%i  %s   %s" % (self.pk, self.first_name, self.last_name)

    def save(self, *args, **kwargs):
        super(Person, self).save(*args, **kwargs)
        if self.photo:
            photo_resize(image_path=self.photo.path)


class RequestCollect(models.Model):
    r_method = models.CharField(max_length=20, blank=True)
    r_path = models.CharField(max_length=50)
    r_time = models.DateTimeField(auto_now_add=True)
    r_status = models.CharField(max_length=5)
    r_viewed = models.BooleanField(default=False)

    def __str__(self):
        pretty_date = self.r_time.strftime('[%d-%m-%Y %I:%M:%S]')
        return "%s\t%s\t'%s'\t%s" % (pretty_date, self.r_method,
                                     self.r_path, self.r_status)
