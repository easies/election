import os
from PIL import Image
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.files import File


class Candidate(models.Model):
    user = models.OneToOneField(User, related_name='candidate')
    stance = models.TextField(max_length=500, blank=True)
    picture = models.ImageField(upload_to='candidate_profiles',
        null=True, blank=True)
    offices = models.ManyToManyField('Office', blank=True,
        related_name='candidates')

    @property
    def full_name(self):
        return self.user.first_name + ' ' + self.user.last_name

    @property
    def username(self):
        return self.user.username

    def __unicode__(self):
        return self.user.username

    @staticmethod
    def resize_pic(src, dst, size):
        image = None
        try:
            image = Image.open(src)
            image.thumbnail(size, Image.ANTIALIAS)
            image.save(dst)
            os.chmod(dst, 0o644)
        except:
            if image:
                image.close()
            return False
        return True

    @staticmethod
    def rename_image(src, username):
        file_ext = os.path.splitext(src)[1].lower().replace('jpg', 'jpeg')
        return 'candidate_profiles/%s%s' % (username, file_ext)

    def save(self, *args, **kwargs):
        super(Candidate, self).save(*args, **kwargs)
        cleanup = False
        if self.picture.name:
            src = self.picture.path
            dst = self.rename_image(src, self.username)
            dst_full = os.path.join(settings.MEDIA_ROOT, dst)
            try:
                os.remove(dst_full)
            except:
                pass
            dst_temp = self.rename_image(src, self.username + '-temp')
            dst_temp_full = os.path.join(settings.MEDIA_ROOT, dst_temp)
            if self.resize_pic(src, dst_temp_full, [200, 400]):
                fd = open(dst_temp_full, 'r')
                self.picture.save(dst, File(fd), save=False)
                super(Candidate, self).save(*args, **kwargs)
                cleanup = True
        if cleanup:
            self._cleanup(src)
            self._cleanup(dst_temp_full)

    @staticmethod
    def _cleanup(f):
        try:
            os.chmod(f, 0o777)
            os.remove(f)
        except:
            pass


class Office(models.Model):
    sort = models.IntegerField(max_length=20)
    title = models.CharField(max_length=30)
    SEMESTERS = (
        (1, 'Fall'),
        (2, 'Spring'),
    )
    semester = models.IntegerField(choices=SEMESTERS, default=1)
    description = models.TextField(max_length=400)

    def __unicode__(self):
        return '%s (%s)' % (self.title, self.get_semester_display())

    @property
    def full_title(self):
        return str(self)

    class Meta:
        ordering = ['sort', 'title']
        unique_together = ('title', 'semester')


# Votes
class Vote(models.Model):
    office = models.ForeignKey(Office)
    cast_for = models.CharField(max_length=50)

    def __unicode__(self):
        return '%s : %s' % (self.office, self.cast_for)


class Ballot(models.Model):
    voter = models.OneToOneField(User, related_name='ballot')
    voted_at = models.DateTimeField(auto_now_add=True)
    ip = models.IPAddressField()

    def __unicode__(self):
        return self.voter.__unicode__()
