from rest_framework import status
from rest_framework.exceptions import ValidationError
from django.test import TestCase
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from api.serializers import ApiSerializer


class ApiTest(TestCase):
    def test_serializer_valid_input(self):
        data = {'tree': '(S (NP (DT The) (NN cat)) (VP (VBD sat) (PP (IN on) (NP (DT the) (NN mat)))))'}
        serializer = ApiSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data, data)

    def test_serializer_missing_field(self):
        data = {}
        serializer = ApiSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors, {'tree': ['This field is required.']})

    def test_tree_view(self):
        url = reverse('tree-view')
        data = {'tree': '(S (NP (DT The) (NN cat)) (VP (VBD sat) (PP (IN on) (NP (DT the) (NN mat)))))'}
        response = self.client.get(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_schema_view(self):
        url = reverse('api-schema')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_docs_view(self):
        url = reverse('api-docs')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_missing_parameter(self):
        url = reverse('tree-view')
        # If the 'tree' parameter is missing, a 400 Bad Request response should be returned
        data = {}
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_extra_parameter(self):
        url = reverse('tree-view')
        # If an unknown parameter is passed, it should be ignored
        data = {'tree': '(S (NP (DT The) (NN cat)) (VP (VBD sat) (PP (IN on) (NP (DT a) (NN mat)))))', 'foo': 'bar'}
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
