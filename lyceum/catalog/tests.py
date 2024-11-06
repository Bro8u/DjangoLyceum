from http import HTTPStatus

import django.core.exceptions
from django.test import Client, TestCase
from parameterized import parameterized

import catalog.models


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

    # def tearDown(self):
    #     catalog.models.Item.objects.all().delete()
    #     catalog.models.Tag.objects.all().delete()
    #     catalog.models.Category.objects.all().delete()
    #     super().tearDown()

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
            ("/catalog/", HTTPStatus.OK, "Список товаров"),
            ("/catalog/", HTTPStatus.OK, "/static/images/picture.png"),
            ("/catalog/", HTTPStatus.OK, "Название товара 1"),
            (
                "/",
                HTTPStatus.OK,
                '<nav class="navbar navbar-expand-lg"'
                'style="background-color: #f8f9fa; padding: 15px;">',
            ),
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
            ("/catalog/",),
        ],
    )
    def test_rendered_file(
        self,
        url,
    ):
        response = Client().get(url)
        self.assertTemplateUsed(
            response,
            "catalog/item_list.html",
        )


class CatalogID(TestCase):

    @parameterized.expand(
        [
            ("/catalog/0/", HTTPStatus.OK, "Пример товара"),
            ("/catalog/0/", HTTPStatus.OK, '<div class="card-body">'),
        ],
    )
    def test_status_and_content(
        self,
        url,
        expected_status,
        expected_content,
    ):
        response = Client().get(url)
        print(response.content.decode("utf-8"))
        self.assertContains(
            response,
            expected_content,
            status_code=expected_status,
        )

    @parameterized.expand(
        [
            ("/catalog/0/",),
        ],
    )
    def test_rendered_file(
        self,
        url,
    ):
        response = Client().get(url)
        self.assertTemplateUsed(
            response,
            "catalog/item.html",
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
