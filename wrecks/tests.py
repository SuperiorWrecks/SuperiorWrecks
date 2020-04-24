from django.test import TestCase
from django.urls import reverse
from wrecks.models import Wrecks
from . import views
import json


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
        response = self.client.get(reverse(views.list_of_ships))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wrecks/template.html')
        self.assertTemplateUsed(response, 'wrecks/listofships.html')


class TestMarkersView(TestCase):
    NUMBER_OF_SHIPS = 17

    def setUp(self):
        for ship_num in range(self.NUMBER_OF_SHIPS):
            Wrecks.objects.create(
                ship_num=ship_num,
                ship_name="S.S. {}".format(ship_num),
                latitude=87,
                longitude=90,
            )
        # Ships without locations should not appear as markers
        for ship_num in range(8):
            Wrecks.objects.create(
                ship_num=ship_num+self.NUMBER_OF_SHIPS,
                ship_name="S.S. {}".format(ship_num+self.NUMBER_OF_SHIPS),
            )

    def tearDown(self):
        # Clean up run after every test method.
        pass

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/wrecks/markers.json")
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse(views.markers))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateNotUsed(response, 'wrecks/*.html')

    def test_lists_all_markers(self):
        # Get json and confirm it has (exactly) 17 items
        response = self.client.get(reverse(views.markers))
        self.assertEqual(response.status_code, 200)
        j = json.loads(response.content.decode('utf-8'))
        self.assertTrue(len(j) == self.NUMBER_OF_SHIPS)


class TestMarkersViewEmpty(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        # Clean up run after every test method.
        pass

    def test_lists_all_markers(self):
        response = self.client.get(reverse(views.markers))
        self.assertEqual(response.status_code, 200)
        j = json.loads(response.content.decode('utf-8'))
        self.assertTrue(len(j) == 0)


class TestAllShipsView(TestCase):
    NUMBER_OF_SHIPS = 25

    def setUp(self):
        for ship_num in range(self.NUMBER_OF_SHIPS-8):
            Wrecks.objects.create(
                ship_num=ship_num,
                ship_name="S.S. {}".format(ship_num),
                latitude=87,
                longitude=90,
            )
        # Ships without locations should appear on all ships
        for ship_num in range(self.NUMBER_OF_SHIPS-8, self.NUMBER_OF_SHIPS):
            Wrecks.objects.create(
                ship_num=ship_num,
                ship_name="S.S. {}".format(ship_num),
                year_built=50
            )

    def tearDown(self):
        # Clean up run after every test method.
        pass

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/wrecks/allShips.json")
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse(views.all_ships))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateNotUsed(response, 'wrecks/*.html')

    def test_lists_all_markers(self):
        # Get json and confirm it has (exactly) 17 items
        response = self.client.get(reverse(views.all_ships))
        self.assertEqual(response.status_code, 200)
        j = json.loads(response.content.decode('utf-8'))
        self.assertTrue(len(j) == 2)
        self.assertTrue(len(j["ships"]) == self.NUMBER_OF_SHIPS)


class TestDetailView(TestCase):
    def setUp(self):
        Wrecks.objects.create(ship_name="Edmund Fitzgerald", ship_num="277437")

    def tearDown(self):
        # Clean up run after every test method.
        pass

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/ships/Edmund%20Fitzgerald/277437/")
        self.assertEqual(response.status_code, 200)
        response = self.client.get("/ships/Edmund_Fitzgerald/277437/")
        self.assertEqual(response.status_code, 200)
        response = self.client.get("/ships/Edmund_NOT_Fitzgerald/277437/")
        self.assertEqual(response.status_code, 404)
        response = self.client.get("/ships/Edmund Fitzgerald/NOT277437/")
        self.assertEqual(response.status_code, 404)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse(views.detail, args=["Edmund_Fitzgerald", "277437"]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wrecks/shipdetail.html')
        response = self.client.get(reverse(views.detail, args=["Edmund Fitzgerald", "277437"]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wrecks/shipdetail.html')
        response = self.client.get(reverse(views.detail, args=["Edmund_Fitzgeraldjk", "277437"]))
        self.assertEqual(response.status_code, 404)
        self.assertTemplateNotUsed(response, 'wrecks/*.html')
        response = self.client.get(reverse(views.detail, args=["Edmund_Fitzgerald", "277437jk"]))
        self.assertEqual(response.status_code, 404)
        self.assertTemplateNotUsed(response, 'wrecks/*.html')


