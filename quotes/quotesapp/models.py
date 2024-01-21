from django.db import models

# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=35, null=False, unique=True)

    def __str__(self):
        return f"{self.name}"


class Author(models.Model):
    fullname = models.CharField(max_length=25, null=False)
    born_date = models.CharField(max_length=25, null=False)
    born_location = models.CharField(null=False)
    description= models.TextField()

    # def __str__(self):
    #     return f"{self.fullname}"


class Quote(models.Model):
    tags = models.ManyToManyField(Tag)
    # author = models.CharField(max_length=150, null=False)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    quote = models.TextField()

    # def __str__(self):
        # return f"{self.name}"

