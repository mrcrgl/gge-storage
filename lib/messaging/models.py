from django.db import models


class Template(models.Model):
    slug = models.CharField(max_length=128, unique=True, db_index=True)
    title = models.CharField(max_length=64)
    subject = models.CharField(max_length=64)
    always_bcc_to = models.EmailField(null=True, blank=True, default=None)
    template = models.TextField()

    def __unicode__(self):
        return "%s [%s]" % (self.title, self.slug)


def upload_attachment(instance, filename):
    return 'messaging/%s/attachments/%s' % (instance.template.slug, filename.replace(' ', '_'))


class TemplateAttachment(models.Model):
    template = models.ForeignKey(Template, related_name='attachments')
    file_name = models.CharField(max_length=64, null=True, blank=True, default=None)
    file = models.FileField(upload_to=upload_attachment)