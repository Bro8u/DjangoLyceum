from http import HTTPStatus

import django.core.exceptions
from django.test import Client, TestCase
from parameterized import parameterized

import catalog.models


class ItemModelTest(TestCase):
    @classmethod
    def setUp(cls):
        super().setUpClass()

        cls.category = catalog.models.Category.objects.create(
            name="Категория 1",
            slug="category-1",
            weight=150,
        )
        cls.tag = catalog.models.Tag.objects.create(
            is_published=True,
            name="Текстовый тэг",
            slug="test-tag-slug",
        )

    def test_unable_create_one_letter(self):

        item_count = catalog.models.Item.objects.count()

        with self.assertRaises(django.core.exceptions.ValidationError):
            self.item = catalog.models.Item(
                name="Тестовый товар",
                category=self.category,
                text="1",
            )
            self.item.full_clean()
            self.item.save()
            self.item.tags.add(ItemModelTest.tag)

        self.assertEqual(
            catalog.models.Item.objects.count(),
            item_count,
        )

    def test_create(self):
        item_count = catalog.models.Item.objects.count()
        self.item = catalog.models.Item(
            name="Тестовый товар",
            category=self.category,
            text="Роскошно!",
        )
        self.item.full_clean()
        self.item.save()
        self.item.tags.add(ItemModelTest.tag)
        self.assertEqual(
            catalog.models.Item.objects.count(),
            item_count + 1,
        )


class TagModelTest(TestCase):

    def setUp(self):
        self.tag = catalog.models.Tag.objects.create(
            name="Тестовый тег",
            slug="test-tag-slug",
        )

    def test_tag_create(self):
        tags_count = catalog.models.Tag.objects.count()

        self.tag1 = catalog.models.Tag(
            name="Тестовый тег1",
            slug="test-tag-slug1",
        )
        self.tag1.full_clean()
        self.tag1.save()

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
            self.tag1 = catalog.models.Tag(
                name="Тестовый тег дубликат",
                slug="test-tag-slug#",
            )
            self.tag1.full_clean()
            self.tag1.save()
        self.assertEqual(
            catalog.models.Tag.objects.count(),
            tags_count,
        )


class CategoryModelTest(TestCase):

    def setUp(self):
        self.cat = catalog.models.Category.objects.create(
            name="Тестовая категория",
            slug="test-slug",
            weight=150,
        )

    def test_category_create(self):
        cats_count = catalog.models.Category.objects.count()

        self.cat1 = catalog.models.Category(
            name="Тестовая",
            slug="test-slug-new",
        )
        self.cat1.full_clean()
        self.cat1.save()

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
            self.cat1 = catalog.models.Category(
                name="Тестовая",
                slug="test-slug#",
                weight=150,
            )
            self.cat1.full_clean()
            self.cat1.save()
        self.assertEqual(
            catalog.models.Category.objects.count(),
            cats_count,
        )


class CatalogMain(TestCase):

    @parameterized.expand(
        [
            ("/catalog/", HTTPStatus.OK, "Список элементов"),
        ],
    )
    def test_status_and_content(
        self,
        url,
        expected_status,
        expected_content,
    ):
        response = Client().get(url)
        self.assertContains(
            response, expected_content, status_code=expected_status
        )


class CatalogID(TestCase):

    @parameterized.expand(
        [
            ("/catalog/5/", HTTPStatus.OK, f"Подробно элемент {5}"),
        ],
    )
    def test_status_and_content(
        self,
        url,
        expected_status,
        expected_content,
    ):
        response = Client().get(url)
        self.assertContains(
            response,
            expected_content,
            status_code=expected_status,
        )


class CatalogRegularExpression(TestCase):

    @parameterized.expand(
        [
            ("/catalog/re/123/", HTTPStatus.OK, "123"),
        ],
    )
    def test_status_and_content(
        self,
        url,
        expected_status,
        expected_content,
    ):
        response = Client().get(url)
        self.assertContains(
            response,
            expected_content,
            status_code=expected_status,
        )

    @parameterized.expand(
        [
            ("/catalog/re/", HTTPStatus.NOT_FOUND),
            ("/catalog/re/0/", HTTPStatus.NOT_FOUND),
            ("/catalog/re/-11/", HTTPStatus.NOT_FOUND),
        ],
    )
    def test_status(
        self,
        url,
        expected_status,
    ):
        response = Client().get(url)
        self.assertEqual(
            response.status_code,
            expected_status,
        )


class CatalogConverter(TestCase):

    @parameterized.expand(
        [
            ("/catalog/converter/123/", HTTPStatus.OK, "123"),
        ],
    )
    def test_status_and_content(
        self,
        url,
        expected_status,
        expected_content,
    ):
        response = Client().get(url)
        self.assertContains(
            response,
            expected_content,
            status_code=expected_status,
        )

    @parameterized.expand(
        [
            ("/catalog/converter/", HTTPStatus.NOT_FOUND),
            ("/catalog/converter/0/", HTTPStatus.NOT_FOUND),
            ("/catalog/converter/-11/", HTTPStatus.NOT_FOUND),
        ],
    )
    def test_status(
        self,
        url,
        expected_status,
    ):
        response = Client().get(url)
        self.assertEqual(
            response.status_code,
            expected_status,
        )
