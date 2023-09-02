from django.urls import reverse
from rest_framework import status
from django.test import TestCase

# from rest_framework.test import APITestCase
from . import models


# Create your tests here.
class CRUDLinkStep(TestCase):
    @classmethod
    def setUpClass(cls):
        super(CRUDLinkStep, cls).setUpClass()
        cls.links_1 = models.LinksStep.objects.create(start_id=1, end_id=2, description='test1', color='Black')
        cls.links_2 = models.LinksStep.objects.create(start_id=3, end_id=4, description='test2', color='white')
        cls.links_3 = models.LinksStep.objects.create(start_id=5, end_id=6, description='test3', color='yellow')

    @classmethod
    def tearDownClass(cls):
        super(CRUDLinkStep, cls).tearDownClass()
        cls.links_1.delete()
        cls.links_2.delete()
        cls.links_3.delete()

    def test_get_list(self):
        response = self.client.get(reverse('linksstep-list'))
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        expected_data = [
            {
                "id": 1,
                "start_id": 1,
                "end_id": 2,
                "description": "test1",
                "color": "Black"
            },
            {
                "id": 2,
                "start_id": 3,
                "end_id": 4,
                "description": "test2",
                "color": "white"
            },
            {
                "id": 3,
                "start_id": 5,
                "end_id": 6,
                "description": "test3",
                "color": "yellow"
            },
        ]
        self.assertJSONEqual(response.content, expected_data)

    def test_get_detail(self):
        response = self.client.get(reverse('linksstep-detail', kwargs={"pk": self.links_1.pk}))
        expected_data = {
            "id": 1,
            "start_id": 1,
            "end_id": 2,
            "description": "test1",
            "color": "Black"
        }
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertJSONEqual(response.content, expected_data)

    def test_error_create(self):
        response = self.client.post(reverse('linksstep-list'),
                                    {
                                        "start_id": 2,
                                        "end_id": 2,
                                        "description": 'test4',
                                        "color": 'green',
                                    }
                                    )
        message_error = {'message': 'Начало и конец не могут быть одинаковыми'}
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertJSONEqual(response.content, message_error)

        # print(response.content)

    def test_correct_create(self):
        response = self.client.post(reverse('linksstep-list'),
                                    {
                                        "start_id": 7,
                                        "end_id": 8,
                                        "description": 'test4',
                                        "color": 'green',
                                    }
                                    )
        expected_data = {'status': 'ok'}
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertJSONEqual(response.content, expected_data)

    def test_delete(self):
        # response = self.client.delete(reverse('linksstep-detail', kwargs={"pk": self.links_1.pk}))
        response_2 = self.client.get(reverse('linksstep-detail', kwargs={"pk": self.links_1.pk}))

        # print(response)
        print(response_2)
