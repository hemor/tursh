from django.test import TestCase
from .models import ShortUrl


#   TODO:3 - Create comprehensive tests


class ShortUrlTestCase(TestCase):

    def test_visit_count_increase_by_1(self):
        url = ShortUrl.objects.create(full_url="http://google.com", short_url="goo0gs")
        vc1 = url.visit_count
        url.increase_count()
        vc2 = url.visit_count
        self.assertEqual(vc2-vc1, 1)
    
    
