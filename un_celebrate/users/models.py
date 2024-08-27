from django.db import models


class TgUser(models.Model):
    first_name = models.CharField(max_length=100, db_column='first_name')
    last_name = models.CharField(max_length=100, db_column='last_name')
    tg_id = models.IntegerField(unique=True, db_column='tg_id')
    date_birth = models.DateTimeField(db_column='birthday')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        db_table = 'TgUser'
