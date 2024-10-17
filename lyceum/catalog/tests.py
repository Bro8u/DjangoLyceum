from http import HTTPStatus

import django.core.exceptions
from django.test import Client, TestCase
from parameterized import parameterized

import catalog.models


class CatalogItemModelTest(TestCase):
    @classmethod
    def setUp(cls):
        super().setUpClass()

        cls.category = catalog.models.CatalogCategory.objects.create(
            name="Категория 1", slug="category-1", weight=150
        )
        cls.tag = catalog.models.CatalogTag.objects.create(
            is_published=True, name="Текстовый тэг", slug="test-tag-slug"
        )

    def test_unable_create_one_letter(self):

        item_count = catalog.models.CatalogItem.objects.count()

        with self.assertRaises(django.core.exceptions.ValidationError):
            self.item = catalog.models.CatalogItem(
                name="Тестовый товар",
                category=self.category,
                text="1",  # Некорректный текст
            )
            self.item.full_clean()
            self.item.save()
            self.item.tags.add(CatalogItemModelTest.tag)

        self.assertEqual(
            catalog.models.CatalogItem.objects.count(),
            item_count,
        )

    def test_create(self):
        item_count = catalog.models.CatalogItem.objects.count()
        self.item = catalog.models.CatalogItem(
            name="Тестовый товар",
            category=self.category,
            text="Роскошно!",  # Корректный текст для теста
        )
        self.item.full_clean()
        self.item.save()
        self.item.tags.add(CatalogItemModelTest.tag)
        self.assertEqual(
            catalog.models.CatalogItem.objects.count(),
            item_count + 1,
        )


class CatalogTagModelTest(TestCase):

    def setUp(self):
        self.tag = catalog.models.CatalogTag.objects.create(
            name="Тестовый тег", slug="test-tag-slug"
        )

    def test_tag_create(self):
        tags_count = catalog.models.CatalogTag.objects.count()

        self.tag1 = catalog.models.CatalogTag(
            name="Тестовый тег1", slug="test-tag-slug1"
        )
        self.tag1.full_clean()
        self.tag1.save()

        self.assertEqual(
            catalog.models.CatalogTag.objects.count(),
            tags_count + 1,
        )

    def test_tag_unique_slug(self):
        tags_count = catalog.models.CatalogTag.objects.count()
        with self.assertRaises(django.core.exceptions.ValidationError):
            self.tag_duplicate = catalog.models.CatalogTag(
                name="Тестовый тег дубликат",
                slug="test-tag-slug",  # Такой slug уже существует
            )
            self.tag_duplicate.full_clean()
            self.tag_duplicate.save()
        self.assertEqual(
            catalog.models.CatalogTag.objects.count(),
            tags_count,
        )

    def test_tag_permitted_symbols(self):
        tags_count = catalog.models.CatalogTag.objects.count()
        with self.assertRaises(django.core.exceptions.ValidationError):
            self.tag1 = catalog.models.CatalogTag(
                name="Тестовый тег дубликат", slug="test-tag-slug#"  # no #
            )
            self.tag1.full_clean()
            self.tag1.save()
        self.assertEqual(
            catalog.models.CatalogTag.objects.count(),
            tags_count,
        )


class CatalogCategoryModelTest(TestCase):

    def setUp(self):
        self.cat = catalog.models.CatalogCategory.objects.create(
            name="Тестовая категория", slug="test-slug", weight=150
        )

    def test_category_create(self):
        cats_count = catalog.models.CatalogCategory.objects.count()

        self.cat1 = catalog.models.CatalogCategory(
            name="Тестовая", slug="test-slug-new"
        )
        self.cat1.full_clean()
        self.cat1.save()

        self.assertEqual(
            catalog.models.CatalogCategory.objects.count(),
            cats_count + 1,
        )

    def test_category_unique_slug(self):
        cats_count = catalog.models.CatalogCategory.objects.count()
        with self.assertRaises(django.core.exceptions.ValidationError):
            self.cat_duplicate = catalog.models.CatalogCategory(
                name="Тестовая",
                slug="test-slug",
                weight=150,  # Такой slug уже существует
            )
            self.cat_duplicate.full_clean()
            self.cat_duplicate.save()
        self.assertEqual(
            catalog.models.CatalogCategory.objects.count(),
            cats_count,
        )

    def test_category_permitted_symbols(self):
        cats_count = catalog.models.CatalogCategory.objects.count()
        with self.assertRaises(django.core.exceptions.ValidationError):
            self.cat1 = catalog.models.CatalogCategory(
                name="Тестовая", slug="test-slug#", weight=150  # no
            )
            self.cat1.full_clean()
            self.cat1.save()
        self.assertEqual(
            catalog.models.CatalogCategory.objects.count(),
            cats_count,
        )


class CatalogMain(TestCase):

    @parameterized.expand(
        [
            ("/catalog/", HTTPStatus.OK, "Список элементов"),
        ]
    )
    def test_status_and_content(self, url, expected_status, expected_content):
        response = Client().get(url)
        self.assertContains(
            response, expected_content, status_code=expected_status
        )


class CatalogID(TestCase):

    @parameterized.expand(
        [
            ("/catalog/5/", HTTPStatus.OK, f"Подробно элемент {5}"),
        ]
    )
    def test_status_and_content(self, url, expected_status, expected_content):
        response = Client().get(url)
        self.assertContains(
            response, expected_content, status_code=expected_status
        )


class CatalogRegularExpression(TestCase):

    @parameterized.expand(
        [
            ("/catalog/re/123/", HTTPStatus.OK, "123"),
        ]
    )
    def test_status_and_content(self, url, expected_status, expected_content):
        response = Client().get(url)
        self.assertContains(
            response, expected_content, status_code=expected_status
        )

    @parameterized.expand(
        [
            ("/catalog/re/", HTTPStatus.NOT_FOUND),
            ("/catalog/re/0/", HTTPStatus.NOT_FOUND),
            ("/catalog/re/-11/", HTTPStatus.NOT_FOUND),
        ]
    )
    def test_status(self, url, expected_status):
        response = Client().get(url)
        self.assertEqual(response.status_code, expected_status)


class CatalogConverter(TestCase):

    @parameterized.expand(
        [
            ("/catalog/converter/123/", HTTPStatus.OK, "123"),
        ]
    )
    def test_status_and_content(self, url, expected_status, expected_content):
        response = Client().get(url)
        self.assertContains(
            response, expected_content, status_code=expected_status
        )

    @parameterized.expand(
        [
            ("/catalog/converter/", HTTPStatus.NOT_FOUND),
            ("/catalog/converter/0/", HTTPStatus.NOT_FOUND),
            ("/catalog/converter/-11/", HTTPStatus.NOT_FOUND),
        ]
    )
    def test_status(self, url, expected_status):
        response = Client().get(url)
        self.assertEqual(response.status_code, expected_status)
