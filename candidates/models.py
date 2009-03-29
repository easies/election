from django.db import models
from django import forms
from django.conf import settings
from ..util.resizepic import resize_pic, rename_image
from django.core.files import File
import os

## -------------- Models ----------------------------------------------------##

class Candidate(models.Model):
    """ Class for representing a person running for an office in an election."""

    ## ---------- Attributes ------------------------------------------------##
    username    = models.CharField(max_length=20,unique=True)
    username.verbose_name   = 'CCIS Username'

    fname       = models.CharField(max_length=20)
    fname.verbose_name      = 'First Name'

    lname       = models.CharField(verbose_name='Last Name',max_length=40)
    lname.verbose_name      = 'Last Name'

    stance      = models.TextField(max_length=400,blank=True)

    pic         = models.ImageField(upload_to='election_profiles',
                                    null=True,blank=True)
    pic.verbose_name        = 'Profile Picture'

    offices     = models.ManyToManyField('Office',blank=True)
    offices.verbose_name    = 'Running For'

    ## ---------- Methods ------------------------------------------------##
    def __unicode__(self):
        return self.username

    def __str__(self):
        return self.__unicode__()

    def fullname(self):
        return self.fname + ' ' + self.lname

    def save(self, *args, **kwargs):
        cleanup = False
        if not self.pic.name == '':
            src = self.pic.path
            dst = rename_image(src, self.username)
            dst_root = settings.MEDIA_ROOT + dst
            try:
                os.remove(dst_root)
            except:
                pass
            dst_temp = rename_image(src, self.username + '-temp')
            dst_temp_root = settings.MEDIA_ROOT + dst_temp
            if resize_pic(src, dst_temp_root, [200,400]):
                try:
                    fd = open(dst_temp_root, 'r')
                    self.pic.save(dst, File(fd), save=False)
                    cleanup = True
                except:
                    pass
        
        super(Candidate, self).save(args, kwargs)
        if cleanup:
            try:
                os.chmod(src, 0777)
                os.remove(src)
                os.chmod(dst_temp_root, 0777)
                os.remove(dst_temp_root)
            except:
                pass



    class Meta:
        ordering = ['lname']

class Office(models.Model):
    """ Class for representing an officer position in ACM."""

    ## ---------- Attributes ------------------------------------------------##
    sort        = models.IntegerField(max_length=20)
    sort.verbose_name       = 'Sort Order'

    ## TODO: Change this limit to 30
    title       = models.CharField(max_length=30)
    title.verbose_name      = 'Office Title'

    SEMESTERS   = ( (1, 'Fall'), (2, 'Spring') )
    semester    = models.IntegerField(choices=SEMESTERS,default=1)
    semester.verbose_name   = 'Semester'

    desc        = models.TextField(max_length=400)
    desc.verbose_name       = 'Office Description'

    ## ---------- Methods ------------------------------------------------##
    def __unicode__(self):
        return "%s (%s)" % (self.title, self.SEMESTERS[self.semester - 1][1])

    def fulltitle(self):
        return str(self)

    class Meta:
        ordering = ['sort','title']
        unique_together = ("title", "semester")

## -------------- Forms ----------------------------------------------------##

class CandidateForm(forms.ModelForm):
    class Meta:
        model   = Candidate
        exclude = ['username']

class OfficeForm(forms.ModelForm):
    class Meta:
        model = Office
