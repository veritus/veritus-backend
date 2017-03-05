from django.db import models
from main.models import Entity
from parliament.models import ParliamentSession


class Bill(Entity):
    description_link = models.TextField()
    althingi_created = models.DateField()
    number = models.IntegerField()
    parliament_session = models.ForeignKey(ParliamentSession)


class Case(Entity):
    number = models.IntegerField()
    parliament_session = models.ForeignKey(ParliamentSession)
    case_type = models.TextField()
    case_status = models.TextField()
    # TODO:
    # related_case_numbers = models.CharField(
    #     validators=[validate_comma_separated_integer_list])
    # subject_numbers = models.CommaSeparatedIntegerField()


class Subject(Entity):
    parliament_session = models.ForeignKey(ParliamentSession)
    major_group_number = models.IntegerField()
    major_group_name = models.TextField()
    number = models.IntegerField()
    description = models.TextField()
    # TODO associated_cases
