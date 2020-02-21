from django.db import models
# Create your models here.n

class koresponden(models.Model):  
    name = models.CharField(max_length=100)
    NIP = models.CharField(max_length=100)
    sex = models.CharField(max_length=50)
    age = models.CharField(max_length=50)
    study = models.CharField(max_length=50)
    job = models.CharField(max_length=50)
    code = models.CharField(max_length=50)
    date = models.DateTimeField('Event Date')

    def __str__(self):
        return self.NIP

class link(models.Model):
    username = models.CharField(max_length=100)
    code = models.CharField(max_length=50)
    date = models.DateTimeField('Event Date')

    def __str__(self):
        return self.code

class data(models.Model):
    NIP = models.CharField(max_length=100)
    U1 = models.IntegerField()
    U2 = models.IntegerField()
    U3 = models.IntegerField()
    U4 = models.IntegerField()
    U5 = models.IntegerField()
    U6 = models.IntegerField()
    U7 = models.IntegerField()
    U8 = models.IntegerField()
    U9 = models.IntegerField()
    U10 = models.IntegerField()
    U11 = models.IntegerField()
    U12 = models.IntegerField()
    U13 = models.IntegerField()
    U14 = models.IntegerField()
    code = models.CharField(max_length=50)
    date = models.DateTimeField('Event Date')

    def __str__(self):
        return self.NIP

class subwil(models.Model):
    kode = models.CharField(max_length=50)
    wilayah = models.CharField(max_length=50)

    def __str__(self):
        return self.wilayah

    def get_absolute_url(self):
        return reverse('survey:wilayah_edit', kwargs={'pk': self.pk})

