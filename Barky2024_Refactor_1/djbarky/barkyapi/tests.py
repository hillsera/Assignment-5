from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework import routers
from rest_framework.test import APIRequestFactory, APITestCase

from .models import Bookmark
from .views import BookmarkViewSet

from django.utils import timezone

# Create your tests here.
# test plan


class BookmarkTests(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.bookmark = Bookmark.objects.create(
            id=1,
            title="Awesome Django",
            url="https://awesomedjango.org/",
            notes="Best place on the web for Django.",
        )
        # print(f"bookmark id: {self.bookmark.id}")

        # the simple router provides the name 'bookmark-list' for the URL pattern: https://www.django-rest-framework.org/api-guide/routers/#simplerouter
        self.list_url = reverse("barkyapi:bookmark-list")
        self.detail_url = reverse(
            "barkyapi:bookmark-detail", kwargs={"pk": self.bookmark.id}
        )

    # 1. create a bookmark
    def test_create_bookmark(self):
        """
        Ensure we can create a new bookmark object.
        """

        # the full record is required for the POST
        data = {
            "id": 99,
            "title": "Django REST framework",
            "url": "https://www.django-rest-framework.org/",
            "notes": "Best place on the web for Django REST framework.",
        }
        response = self.client.post(self.list_url, data, format="json")
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(Bookmark.objects.count(), 2)
        self.assertEqual(Bookmark.objects.get(id=99).title, "Django REST framework")

    # 2. list bookmarks
    def test_list_bookmarks(self):
        """
        Ensure we can list all bookmark objects.
        """
        response = self.client.get(self.list_url)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data["results"][0]["title"], self.bookmark.title)

    # 3. retrieve a bookmark
    def test_retrieve_bookmark(self):
        """
        Ensure we can retrieve a bookmark object.
        """
        response = self.client.get(self.detail_url)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data["title"], self.bookmark.title)

    # 4. delete a bookmark
    def test_delete_bookmark(self):
        """
        Ensure we can delete a bookmark object.
        """
        response = self.client.delete(
            reverse("barkyapi:bookmark-detail", kwargs={"pk": self.bookmark.id})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Bookmark.objects.count(), 0)

    # 5. update a bookmark
    def test_update_bookmark(self):
        """
        Ensure we can update a bookmark object.
        """
        # the full record is required for the POST
        data = {
            "id": 99,
            "title": "Awesomer Django",
            "url": "https://awesomedjango.org/",
            "notes": "Best place on the web for Django just got better.",
        }
        response = self.client.put(
            reverse("barkyapi:bookmark-detail", kwargs={"pk": self.bookmark.id}),
            data,
            format="json",
        )
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data["title"], "Awesomer Django")

    # list bookmarks by title
    def test_list_bookmarks_by_title(self):
        """
        List bookmarks created by title
        """
        Bookmark.objects.create(title="Github", url="https://github.com/")
        Bookmark.objects.create(title="Google", url="https://google.com/")
        response = self.client.get(self.list_url + "?ordering=title")
        
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data["results"][0]["title"], "Awesome Django")
        self.assertEqual(response.data["results"][1]["title"], "Github")
        self.assertEqual(response.data["results"][2]["title"], "Google")

    # list bookmarks by date
    def test_list_bookmarks_by_date(self):
        """
        List bookmarks by date
        """
        Bookmark.objects.create(title="Github", url="https://github.com/", date_added=timezone.now() - timezone.timedelta(days=2))
        Bookmark.objects.create(title="Google", url="https://google.com/", date_added=timezone.now() - timezone.timedelta(days=1))

        response = self.client.get(self.list_url + "?ordering=date_added")

        self.assertTrue(status.is_success(response.status_code))

        data = response.json()

        self.assertLessEqual(data["results"][0]["date_added"], data["results"][1]["date_added"])
        self.assertLessEqual(data["results"][1]["date_added"], data["results"][2]["date_added"])

    # test bookmarks url works
    def test_bookmarks_url(self):
        """
        Ensure bookmars url is pointing to correct place
        """
        url = reverse('barkyapi:bookmark-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


# 6. create a snippet
# 7. retrieve a snippet
# 8. delete a snippet
# 9. list snippets
# 10. update a snippet
# 11. create a user
# 12. retrieve a user
# 13. delete a user
# 14. list users
# 15. update a user
# 16. highlight a snippet
# 17. list bookmarks by user
# 18. list snippets by user
# 20. list bookmarks by date
# 21. list snippets by date
# 23. list bookmarks by title
# 24. list snippets by title
# 26. list bookmarks by url
# 27. list snippets by url
