from django.test import TestCase
import json
from rest_framework.test import APIRequestFactory, APITransactionTestCase
from django.urls import reverse
from rest_framework import status

from .models import *
from .views import SubmitDataViewset
from .serializers import PeakSerializer


class TestSimple(APITransactionTestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = SubmitDataViewset.as_view({'post': 'create',
                                               'get': 'list',
                                               'patch': 'partial_update'})
        self.url = '/submitData/'
        data_1 = {
            "country": "РФ",
            "category": "перевал",
            "title": "Озерный",
            "other_titles": "",
            "connect": "соединяет две горы",
            "status": "new",
            "method_of_passage": "пешком",
            "user": {
                "surname": "Бабкин",
                "name": "Андрей",
                "patronymic": "Юрьевич",
                "email": "kir2845@mail.ru",
                "telephone": "+79518001704"
            },
            "coords": {
                "latitude": 15.3842,
                "longitude": 87.15201,
                "height": 3200
            },
            "level": {
                "winter": "1b",
                "spring": "",
                "summer": "1a",
                "autumn": "1a"
            },
            "images": [
                {"title": "перевал",
                 "photo": "https://dicovage.com/image/data/journal2/blog/cikavinki/Dorohu/190.jpg"}]
        }

        data_2 = {
            "country": "РФ",
            "category": "горная вершина",
            "title": "Зюраткуль",
            "other_titles": "",
            "connect": "нет",
            "status": "new",
            "method_of_passage": "пешая прогулка",
            "user": {
                "surname": "Бабкина",
                "name": "Лариса",
                "patronymic": "Вячеславовна",
                "email": "elena.alena1275@yandex.ru",
                "telephone": "+79518001704"
            },
            "coords": {
                "latitude": 65.3842,
                "longitude": 25.15251,
                "height": 1640
            },
            "level": {
                "winter": "2a",
                "spring": "",
                "summer": "1a",
                "autumn": ""
            },
            "images": [{"title": "вершина",
                        "photo": " https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT9ht5Brvr4t_Ky66-pYaAvIY1rN8qEAmbwWhDjgRRtcilNqeTL0eKicMuirwiqymk0epM&usqp=CAU"},
                       {"title": "озеро",
                        "photo": " https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT9ht5Brvr4t_Ky66-pYaAvIY1rN8qEAmbwWhDjgRRtcilNqeTL0eKicMuirwiqymk0epM&usqp=CAU"}]
        }

        request_1 = self.factory.post(self.url, data_1, format='json')
        request_2 = self.factory.post(self.url, data_2, format='json')
        response_1 = self.view(request_1)
        response_2 = self.view(request_2)

        self.assertEqual(response_1.status_code, status.HTTP_200_OK)
        self.assertEqual(response_2.status_code, status.HTTP_200_OK)
        self.assertEquals(Peak.objects.count(), 2)

    def test_add(self):
        data = {
            "country": "РФ",
            "category": "Перевал",
            "title": "Тестовый перевал",
            "other_titles": "",
            "connect": "соединяет две горы",
            "status": "new",
            "method_of_passage": "пешком",
            "user": {
                "surname": "Петров",
                "name": "Иван",
                "patronymic": "Васильевич",
                "email": "petrov123@yandex.ru",
                "telephone": "+79511111111"
            },
            "coords": {
                "latitude": 11.2222,
                "longitude": 11.2222,
                "height": 1111
            },
            "level": {
                "winter": "",
                "spring": "",
                "summer": "",
                "autumn": ""
            },
            "images": [
                {"title": "Тестовый перевал",
                 "photo": "https://dicovage.com/image/data/journal2/blog/cikavinki/Dorohu/190.jpg"}]
        }

        request = self.factory.post(self.url, data, format='json')
        response = self.view(request)

        peak = Peak.objects.last()
        self.assertEqual(peak.category, 'Перевал')
        self.assertEqual(peak.title, 'Тестовый перевал')
        self.assertEqual(peak.method_of_passage, 'пешком')
        self.assertEqual(peak.status, 'new')

    def test_get_list(self):
        request = self.factory.get(self.url)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_id(self):
        peak = Peak.objects.last()
        self.assertEquals(Peak.objects.count(), 2)
        response = self.client.get(f'{self.url}{peak.id}/')
        serializer_data = PeakSerializer(peak).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer_data, response.data)

    def test_patch(self):
        peak = Peak.objects.last()
        self.assertEquals(Peak.objects.count(), 2)
        response = self.client.get(f'{self.url}{peak.id}/')

        data = {
                "country": "РФ",
                "category": "горная вершина",
                "title": "Зюраткуль",
                "other_titles": "",
                "connect": "нет",
                "add_time": "2023-10-04T14:53:38.003690Z",
                "status": "new",
                "method_of_passage": "пешая прогулка",
                "user": {
                    "id": 2,
                    "surname": "Бабкина",
                    "name": "Лариса",
                    "patronymic": "Вячеславовна",
                    "email": "elena.alena1275@yandex.ru",
                    "telephone": "+79518001704"
                },
                "coords": {
                    "latitude": 65.3842,
                    "longitude": 25.15251,
                    "height": 1640
                },
                "level": {
                    "winter": "2b",
                    "spring": "1b",
                    "summer": "1a",
                    "autumn": "1a"
                },
                "images": [
                    {
                        "title": "вершина",
                        "photo": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT9ht5Brvr4t_Ky66-pYaAvIY1rN8qEAmbwWhDjgRRtcilNqeTL0eKicMuirwiqymk0epM&usqp=CAU"
                    },
                    {
                        "title": "озеро",
                        "photo": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT9ht5Brvr4t_Ky66-pYaAvIY1rN8qEAmbwWhDjgRRtcilNqeTL0eKicMuirwiqymk0epM&usqp=CAU"
                    }
                ]
            }

        request = self.factory.patch(f'{self.url}{peak.id}/', data, format='json')
        response = self.view(request, pk=peak.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        peak = Peak.objects.last()
        self.assertEqual(peak.level.winter, '2b')
        self.assertEqual(peak.level.spring, '1b')
        self.assertEqual(peak.level.summer, '1a')
        self.assertEqual(peak.level.autumn, '1a')

    def test_error_add(self):
        data = {
            "title": "Тестовый перевал",
            "other_titles": "",
            "connect": "соединяет две горы",
            "status": "new1",
            "method_of_passage": "пешком",
            "user": {
                "surname": "Петров",
                "name": "Иван",
                "patronymic": "Васильевич",
                "email": "petrov123@yandex.ru",
                "telephone": "+79511111111"
            },
            "coords": {
                "latitude": 11.2222,
                "longitude": 11.2222,
                "height": 1111
            },
            "level": {
                "winter": "",
                "spring": "",
                "summer": "",
                "autumn": ""
            },
            "images": [
                {"title": "Тестовый перевал",
                 "photo": "https://dicovage.com/image/data/journal2/blog/cikavinki/Dorohu/190.jpg"}]
        }

        request = self.factory.post(self.url, data, format='json')
        response = self.view(request)
        self.assertEquals(Peak.objects.count(), 2)

    def test_error_patch(self):
        peak = Peak.objects.last()
        self.assertEquals(Peak.objects.count(), 2)
        response = self.client.get(f'{self.url}{peak.id}/')

        data = {
            "user": {
                "surname": "Иванов",
                "name": "Петр",
                "patronymic": "Васильевич",
                "email": "petrov123@yandex.ru",
                "telephone": "+79511111111"
            },
        }

        request = self.factory.patch(f'{self.url}{peak.id}/', data, format='json')
        response = self.view(request, pk=peak.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        peak = Peak.objects.last()
        self.assertEqual(peak.user.surname, "Бабкина")
        self.assertEqual(peak.user.name, "Лариса")
        self.assertEqual(peak.user.patronymic, "Вячеславовна")
        self.assertEqual(peak.user.email, "elena.alena1275@yandex.ru")
        self.assertEqual(peak.user.telephone, "+79518001704")
