from django.test import TestCase
from django.urls import reverse
from django.db import models

class YourViewTestCase(TestCase):
    def test_your_view(self):
        url = reverse('models')  # 替换为你的视图名称
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Expected Content")
# Create your tests here.


#class Info(models.Model):
    #info_email = models.EmailField(max_length=254)
    #info_phone = models.CharField(max_length=15)

    #def __str__(self):
        #return self.info_email