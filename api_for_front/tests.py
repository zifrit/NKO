import datetime
import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from django.test import TestCase

from . import models


class CRUDLinkStep(TestCase):
    @classmethod
    def setUpClass(cls):
        super(CRUDLinkStep, cls).setUpClass()
        cls.links_1 = models.LinksStep.objects.create(start_id=1, end_id=2, description='test1', color='Black', data={})
        cls.links_2 = models.LinksStep.objects.create(start_id=3, end_id=4, description='test2', color='white', data={})
        cls.links_3 = models.LinksStep.objects.create(start_id=5, end_id=6, description='test3', color='yellow',
                                                      data={})

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
                "data": {},
            },
            {
                "id": 2,
                "start_id": 3,
                "end_id": 4,
                "data": {},
            },
            {
                "id": 3,
                "start_id": 5,
                "end_id": 6,
                "data": {},
            },
        ]
        self.assertJSONEqual(response.content, expected_data)

    def test_get_detail(self):
        response = self.client.get(reverse('linksstep-detail', kwargs={"pk": self.links_1.pk}))
        expected_data = {
            "id": 1,
            "start_id": 1,
            "end_id": 2,
            "data": {},
        }
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertJSONEqual(response.content, expected_data)

    def test_error_create(self):
        response = self.client.post(reverse('linksstep-list'),
                                    {
                                        "start_id": 2,
                                        "end_id": 2,
                                        "data": {},
                                    }
                                    )
        message_error = {'message': 'Начало и конец не могут быть одинаковыми'}
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertJSONEqual(response.content, message_error)

    def test_correct_create(self):
        response = self.client.post(reverse('linksstep-list'),
                                    {
                                        "start_id": 7,
                                        "end_id": 8,
                                        "description": 'test4',
                                        "color": 'green',
                                        "data": json.dumps({"test": "test"}),
                                    }
                                    )
        expected_data = {
            "id": 4,
            "start_id": 7,
            "end_id": 8,
            "data": {"test": "test"},
        }
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertJSONEqual(response.content, expected_data)

    def test_delete(self):
        response = self.client.delete(reverse('linksstep-detail', kwargs={"pk": self.links_1.pk}))
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)


class CRUDProject(TestCase):
    @classmethod
    def setUpClass(cls):
        super(CRUDProject, cls).setUpClass()
        cls.user = User.objects.create_user(username='test', password='test')
        cls.today = str(datetime.date.today())
        cls.pro_1 = models.MainProject.objects.create(name='test1',
                                                      user=cls.user,
                                                      date_start="2022-10-17",
                                                      date_end="2022-10-18")
        cls.pro_2 = models.MainProject.objects.create(name='test2',
                                                      user=cls.user,
                                                      date_start="2022-10-17",
                                                      date_end="2022-10-18")
        cls.pro_3 = models.MainProject.objects.create(name='test3',
                                                      user=cls.user,
                                                      date_start="2022-10-17",
                                                      date_end="2022-10-18")

    @classmethod
    def tearDownClass(cls):
        super(CRUDProject, cls).tearDownClass()
        cls.pro_1.delete()
        cls.pro_2.delete()
        cls.pro_3.delete()

    def test_get_list(self):
        response = self.client.get(reverse('mainproject-list'))
        expected_data = [
            {
                "id": 1,
                "user": "test",
                "name": "test1",
                "date_create": self.today,
                "date_start": "2022-10-17",
                "date_end": "2022-10-18",
                "last_change": self.today,
            },
            {
                "id": 2,
                "user": "test",
                "name": "test2",
                "date_create": self.today,
                "date_start": "2022-10-17",
                "date_end": "2022-10-18",
                "last_change": self.today,
            },
            {
                "id": 3,
                "user": "test",
                "name": "test3",
                "date_create": self.today,
                "date_start": "2022-10-17",
                "date_end": "2022-10-18",
                "last_change": self.today,
            },
        ]
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertJSONEqual(response.content, expected_data)

    def test_get_detail(self):
        response = self.client.get(reverse('mainproject-detail', kwargs={"pk": self.pro_1.pk}))
        expected_data = {
            "id": 1,
            "name": "test1",
            "steps": [],
            "links": []
        }
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertJSONEqual(response.content, expected_data)

    def test_create(self):
        response = self.client.post(reverse('mainproject-list'),
                                    {
                                        "name": "test4",
                                        "date_start": "2022-10-17",
                                        "date_end": "2022-10-18",
                                    }
                                    )
        expected_data = {
            "id": 4,
            "name": "test4",
            "date_create": self.today,
            "date_start": "2022-10-17",
            "date_end": "2022-10-18",
            "last_change": self.today,
        }
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertJSONEqual(response.content, expected_data)

    def test_delete(self):
        response = self.client.delete(reverse('mainproject-detail', kwargs={"pk": self.pro_1.pk}))
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
