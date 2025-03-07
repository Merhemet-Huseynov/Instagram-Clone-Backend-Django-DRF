from django.contrib.auth import get_user_model
from django.test import TestCase


class UsersManagersTests(TestCase):
    """Tests for user creation and superuser creation."""

    def test_create_user(self) -> None:
        """Test for creating a normal user."""
        User = get_user_model()
        user = User.objects.create_user(email="normal@user.com", password="foo")
        self.assertEqual(user.email, "normal@user.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email="")
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password="foo")

    def test_create_superuser(self) -> None:
        """Test for creating a superuser."""
        User = get_user_model()
        admin_user = User.objects.create_superuser(email="super@user.com", password="foo")
        self.assertEqual(admin_user.email, "super@user.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="super@user.com", password="foo", is_superuser=False)


class CustomUserSlugTests(TestCase):
    """Tests for ensuring correct generation of user slugs."""

    def setUp(self) -> None:
        """Set up the user model before tests."""
        self.User = get_user_model()

    def test_slug_generation_from_full_name(self) -> None:
        """Slug should be generated correctly from the user's first and last name."""
        user = self.User.objects.create_user(
            email="testuser@example.com",
            password="password123",
            first_name="John",
            last_name="Doe"
        )
        self.assertEqual(user.slug, "john-doe")

    def test_slug_generation_from_email(self) -> None:
        """If first and last name are not available, slug should be generated from the email's username."""
        user = self.User.objects.create_user(
            email="no-name@example.com",
            password="password123"
        )
        expected_slug = "no-name"
        self.assertTrue(user.slug.startswith(expected_slug))

    def test_slug_uniqueness(self) -> None:
        """Slug should be unique, even if two users have the same first and last name."""
        user1 = self.User.objects.create_user(
            email="user1@example.com",
            password="password123",
            first_name="Alice",
            last_name="Smith"
        )
        user2 = self.User.objects.create_user(
            email="user2@example.com",
            password="password123",
            first_name="Alice",
            last_name="Smith"
        )
        self.assertNotEqual(user1.slug, user2.slug)
