from django.db import models

class Videos(models.Model):
    title = models.CharField(max_length=255)
    raw_file = models.FileField(upload_to='transcribes/media',max_length=255)
    srt_file = models.FileField(upload_to='transcribes/srt',max_length=255)
    upload_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.raw_file} - {self.upload_time}"
