from django.test import TestCase
from django.urls import reverse
from wrecks.models import Wrecks
from . import views

# from django.test.runner import DiscoverRunner
#
#
# class ManagedModelTestRunner(DiscoverRunner):
#     """
#     Test runner that automatically makes all unmanaged models in your Django
#     project managed for the duration of the test run, so that one doesn't need
#     to execute the SQL manually to create them.
#     """
#
#     def setup_test_environment(self, *args, **kwargs):
#         from django.apps import apps
#         for model in apps.get_models():
#             model._meta.managed = True
#         super(ManagedModelTestRunner, self).setup_test_environment(*args, **kwargs)
#
#     def teardown_test_environment(self, *args, **kwargs):
#         super(ManagedModelTestRunner, self).teardown_test_environment(*args, **kwargs)
#         # reset unmanaged models
#         for m in self.unmanaged_models:
#             m._meta.managed = False


# Create your tests here.
class TestHomepageView(TestCase):
    def setUp(self):
        # Setup run before every test method.
        pass

    def tearDown(self):
        # Clean up run after every test method.
        pass

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse(views.homepage))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wrecks/template.html')
        self.assertTemplateUsed(response, 'wrecks/homepage.html')


class TestShipListView(TestCase):
    def setUp(self):
        # Setup run before every test method.
        pass

    def tearDown(self):
        # Clean up run after every test method.
        pass

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/ships/")
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse(views.listofships))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wrecks/template.html')
        self.assertTemplateUsed(response, 'wrecks/listofships.html')


# class TestMarkersView(TestCase):
#     number_of_ships = 17
#
#     def setUp(self):
#         for ship_num in range(self.number_of_ships):
#             Wrecks.objects.create(
#                 ship_num=ship_num,
#                 ship_name="S.S. {}".format(ship_num)
#             )
#         pass
#
#     def tearDown(self):
#         # Clean up run after every test method.
#         pass
#
#     def test_view_url_exists_at_desired_location(self):
#         response = self.client.get("/wrecks/markers.json")
#         self.assertEqual(response.status_code, 200)
#
#     def test_view_uses_correct_template(self):
#         response = self.client.get(reverse(views.markers))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateNotUsed(response, 'wrecks/*.html')
#
#     def test_lists_all_authors(self):
#         # Get json and confirm it has (exactly) 17 items
#         response = self.client.get(reverse('markers'))
#         self.assertEqual(response.status_code, 200)
#         self.assertTrue(len(response.context['data']) == self.number_of_ships)
