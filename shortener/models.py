from django.db import models


class ShortUrl(models.Model):
    full_url = models.URLField(max_length=2000, unique=True, verbose_name='Full Url')
    short_url = models.CharField(max_length=6, unique=True, verbose_name='Short Url')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Date Created')
    visit_count = models.PositiveIntegerField(default=0, verbose_name='Visit Count')

    def __str__(self):
        return self.full_url    #   String representation of ShortUrl object
    
    def increase_count(self):
        #   Increase visit_count by 1
        self.visit_count += 1
        self.save()
    
    class Meta:
        verbose_name = 'Short Url'
        verbose_name_plural = 'Short Urls'
        ordering = ['-date_created', 'visit_count'] #   How to order ShortUrl objects
