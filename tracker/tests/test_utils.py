import django

django.setup()


from asgiref.sync import async_to_sync
from django.test import TestCase
from faker import Faker

from tracker.choices import Roles
from tracker.models import CustomUser, Repository, TelegramUser
from tracker.utils import get_all_repostitories

fake = Faker()


class TestGetAllRepositories(TestCase):
    def setUp(self):
        self.custom_user = CustomUser.objects.create(
            email=fake.email, role=Roles.CONTRIBUTOR
        )

        self.user = TelegramUser.objects.create(
            telegram_id="123456789", user_id=self.custom_user.id
        )

        self.repo1 = Repository.objects.create(user=self.custom_user, name="TestRepo1")
        self.repo2 = Repository.objects.create(user=self.custom_user, name="TestRepo2")

    def test_get_all_repositories_valid_user(self):
        """Test valid telegram ID fetching repositories."""
        result = async_to_sync(get_all_repostitories)(tele_id="123456789")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["name"], "TestRepo1")
        self.assertEqual(result[1]["name"], "TestRepo2")

    def test_get_all_repositories_invalid_user(self):
        """Test invalid telegram ID raises exception."""
        with self.assertRaises(TelegramUser.DoesNotExist):
            async_to_sync(get_all_repostitories)(tele_id="987654321")
