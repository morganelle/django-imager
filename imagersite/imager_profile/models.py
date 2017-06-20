"""Creates models for Imager Profile."""
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.encoding import python_2_unicode_compatible


PHOTO_STYLES = (
    ('BW', 'blackandwhite'),
    ('PAN', 'panorama'),
    ('MAC', 'macro'),
    ('COL', 'color'),
    ('FILM', 'film')
)

AGES = [(i, i) for i in range(6, 120)]

CAMERAS = (
    ('IP', 'iPhone'),
    ('AND', 'Android'),
    ('CAN', 'Canon'),
    ('NIK', 'Nikon'),
    ('LE', 'Leica')
)


class ProfileManager(models.Manager):
    """."""

    def get_queryset(self):
        """."""
        return super(ProfileManager, self).get_queryset().filter(user__is_active=True)


@python_2_unicode_compatible
class ImagerProfile(models.Model):
    """Create imager-specific user profile."""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=50)
    age = models.IntegerField(choices=AGES)
    camera = models.CharField(
        max_length=100,
        choices=CAMERAS
    )
    style = models.CharField(
        max_length=4,
        choices=PHOTO_STYLES
    )
    website = models.URLField(max_length=150)

    objects = models.Manager()
    active = ProfileManager()

    @property
    def is_active(self):
        """Return is_active status on associated user."""
        return self.user.is_active

    def __repr__(self):
        """."""
        return """
    username: {}
    photo_style: {}
    location: {}
    age: {}
    site: {}
    camera: {}
""".format(self.user.username, self.photo_style, self.location, self.age, self.website, self.camera)


@receiver(post_save, sender=User)
def make_imagerprofile(sender, **kwargs):
    """."""
    if kwargs['created']:
        new_profile = ImagerProfile(user=kwargs['instance'])
        new_profile.save()
