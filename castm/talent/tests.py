from rest_framework.test import APITestCase
from django.contrib.auth.models import User


class ProfileTests(APITestCase):
    def test_profile(self):
        user = User.objects.all().first()
        url = "/api/talents/profile/%s" % (user.id, )
        response = self.client.get(url, None, format='json')
        return response