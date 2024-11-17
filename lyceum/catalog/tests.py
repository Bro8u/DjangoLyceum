from http import HTTPStatus

import django.core.exceptions
from django.test import Client, TestCase
from django.urls import reverse
from parameterized import parameterized

import catalog.models

__all__ = []


class ItemModelTest(TestCase):

    def setUp(self):
        self.category_one = catalog.models.Category.objects.create(
            name="Категория 1",
            slug="category-1",
            weight=150,
        )
        self.tag_one = catalog.models.Tag.objects.create(
            is_published=True,
            name="Тэг 1",
            slug="tag-1",
        )
        super(ItemModelTest, self).setUp()

    def test_unable_create_text_without_key_words(self):

        item_count = catalog.models.Item.objects.count()

        with self.assertRaises(django.core.exceptions.ValidationError):
            self.item = catalog.models.Item(
                name="Тестовый товар",
                category=self.category_one,
                text="без ключевого слова",
            )
            self.item.full_clean()
            self.item.save()
            self.item.tags.add(self.tag_one)

        self.assertEqual(
            catalog.models.Item.objects.count(),
            item_count,
        )

    def tearDown(self):
        catalog.models.Item.objects.all().delete()
        catalog.models.Tag.objects.all().delete()
        catalog.models.Category.objects.all().delete()
        super().tearDown()

    def test_create(self):
        item_count = catalog.models.Item.objects.count()
        self.item = catalog.models.Item(
            name="Тестовый товар",
            category=self.category_one,
            text="Роскошно!",
        )
        self.item.full_clean()
        self.item.save()
        self.item.tags.add(self.tag_one)
        self.assertEqual(
            catalog.models.Item.objects.count(),
            item_count + 1,
        )


class TagModelTest(TestCase):

    def setUp(self):
        self.tag1 = catalog.models.Tag.objects.create(
            name="Тестовый тег",
            slug="test-tag-slug",
        )

        super(TagModelTest, self).setUp()

    def test_tag_create(self):
        tags_count = catalog.models.Tag.objects.count()

        self.tag2 = catalog.models.Tag(
            name="Тестовый тег2",
            slug="test-tag-slug2",
        )
        self.tag2.full_clean()
        self.tag2.save()

        self.assertEqual(
            catalog.models.Tag.objects.count(),
            tags_count + 1,
        )

    def test_tag_unique_slug(self):
        tags_count = catalog.models.Tag.objects.count()
        with self.assertRaises(django.core.exceptions.ValidationError):
            self.tag_duplicate = catalog.models.Tag(
                name="Тестовый тег дубликат",
                slug="test-tag-slug",
            )
            self.tag_duplicate.full_clean()
            self.tag_duplicate.save()
        self.assertEqual(
            catalog.models.Tag.objects.count(),
            tags_count,
        )

    def test_tag_permitted_symbols(self):
        tags_count = catalog.models.Tag.objects.count()
        with self.assertRaises(django.core.exceptions.ValidationError):
            self.tag2 = catalog.models.Tag(
                name="тег 2",
                slug="test-tag-slug#",
            )
            self.tag2.full_clean()
            self.tag2.save()
        self.assertEqual(
            catalog.models.Tag.objects.count(),
            tags_count,
        )


class CategoryModelTest(TestCase):

    def setUp(self):
        self.cat1 = catalog.models.Category.objects.create(
            name="Тестовая категория",
            slug="test-slug",
            weight=150,
        )

        super(CategoryModelTest, self).setUp()

    def test_category_create(self):
        cats_count = catalog.models.Category.objects.count()

        self.cat2 = catalog.models.Category(
            name="Коша 2",
            slug="test-slug-new",
        )
        self.cat2.full_clean()
        self.cat2.save()

        self.assertEqual(
            catalog.models.Category.objects.count(),
            cats_count + 1,
        )

    def test_category_unique_slug(self):
        cats_count = catalog.models.Category.objects.count()
        with self.assertRaises(django.core.exceptions.ValidationError):
            self.cat_duplicate = catalog.models.Category(
                name="Тестовая",
                slug="test-slug",
                weight=150,
            )
            self.cat_duplicate.full_clean()
            self.cat_duplicate.save()
        self.assertEqual(
            catalog.models.Category.objects.count(),
            cats_count,
        )

    def test_category_permitted_symbols(self):
        cats_count = catalog.models.Category.objects.count()
        with self.assertRaises(django.core.exceptions.ValidationError):
            self.cat2 = catalog.models.Category(
                name="Кошка 2",
                slug="test-slug#",
                weight=150,
            )
            self.cat2.full_clean()
            self.cat2.save()
        self.assertEqual(
            catalog.models.Category.objects.count(),
            cats_count,
        )


class CatalogMain(TestCase):
    @parameterized.expand(
        [
            ("/catalog/", HTTPStatus.OK,),
            (reverse("catalog:item_list"), HTTPStatus.OK,),
        ],
    )
    def test_status_and_rendered_file(
        self,
        url,
        status,
    ):
        response = Client().get(url)
        self.assertEqual(
            response.status_code,
            status,
        )
        self.assertTemplateUsed(
            response,
            "catalog/item_list.html",
        )


class ItemDetail(TestCase):
    fixtures = ["data.json"]
    @parameterized.expand(
        [
            ("/catalog/9/", HTTPStatus.OK,),
            (reverse("catalog:item_detail", args=[10]), HTTPStatus.OK,),
        ],
    )
    def test_status_and_rendered_file(
        self,
        url,
        status,
    ):
        response = Client().get(url)
        self.assertEqual(response.status_code, status)
        self.assertTemplateUsed(
            response,
            "catalog/item.html",
        )

class Checker(TestCase):
    def check(
        self,
        item,
        exist,
        prefetched,
        not_loaded,
    ):
        item_dict = item.__dict__
        for value in exist:
            self.assertIn(value, item_dict)
        for value in prefetched:
            self.assertIn(value, item_dict['_prefetched_objects_cache'])
        for value in not_loaded:
            self.assertNotIn(value, item_dict)

class ItemMainContext(Checker):
    fixtures = ["data.json"]

    def test_type(self):
        response = Client().get("/catalog/")
        for item in response.context["items"]:
            self.assertIsInstance(item, catalog.models.Item)
    
    def test_item_size(self):
        response = Client().get("/catalog/")
        self.assertEqual(len(response.context["items"]), 5)

    def test_loaded_value(self):
        response = Client().get("/catalog/")
        for item in response.context["items"]:
            self.check(
                item,
                (
                    "name",
                    "text",
                    "category_id",
                ),
                ("tags",),
                (
                    "is_on_main",
                    "image",
                    "is_published",
                )
            )
            
            self.check(
                item.tags.all()[0],
                ("name",),
                (),
                ("is_published"),
            )

class ItemDetailContext(Checker):
    fixtures = ["data.json"]
    def test_loaded_value(self):
        response = Client().get("/catalog/8/")
        self.check(
            response.context["item"],
            (
                "name",
                "text",
                "category_id",
            ),
            ("tags",),
            (
                "is_on_main",
                "image",
                "is_published",
            )
        )

        self.check(
            response.context["item"].tags.all()[0],
            ("name",),
            (),
            ("is_published"),
        )