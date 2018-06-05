from django.db import models

class Bestpic(models.Model):
    title = models.CharField(max_length=200)
    year = models.IntegerField()
    length = models.IntegerField()
    genre = models.CharField(max_length=100, blank=True, null=True)
    winner = models.IntegerField()
    streaming = models.IntegerField()

    def __str__(self):
        return self.title + ', ' + str(self.year) + ', ' + str(self.length) + ', ' + self.genre + ', ' + str(self.winner) + ', ' + str(self.streaming)

    class Meta:
        managed = False
        db_table = 'BestPic'
        unique_together = (('title', 'year'),)

class Streamlinks(models.Model):
    title= models.CharField(max_length=200)
    netflix = models.CharField(max_length = 200)
    hulu = models.CharField(max_length = 200)
    hbo = models.CharField(max_length = 200)
    amazonprime = models.CharField(max_length = 200)

    def __str__(self):
        return self.title + ', ' + self.netflix + ', ' + self.hulu + ', ' + self.hbo + ', ' + self.amazonprime



class Genre(models.Model):
    GENRE_CHOICES = (
        ('',''),
        ('ACT', 'Action'),
        ('ADV','Adventure'),
        ('ANI', 'Animated'),
        ('BIO', 'Biography'),
        ('COM', 'Comedy'),
        ('CRM', 'Crime'),
        ('DOC', 'Documentary'),
        ('DRA', 'Drama'),
        ('EPIC', 'Epic'),
        ('FAM', 'Family'),
        ('FANT', 'Fantasy'),
        ('HIS', 'Historical'),
        ('HOR', 'Horror'),
        ('INDY', 'Independent'),
        ('MUS', 'Musical'),
        ('MYS', 'Mystery'),
        ('POL', 'Political'),
        ('ROM', 'Romance'),
        ('SCIFI', 'Sci-Fi'),
        ('SIL', 'Silent'),
        ('SPR', 'Sport'),
        ('THR', 'Thriller'),
        ('WAR', 'War'),
        ('WEST', 'Western'),
    )

# Create your models here.
