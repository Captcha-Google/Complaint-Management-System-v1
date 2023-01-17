from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    entity = models.ForeignKey("Entities",on_delete= models.SET_NULL,null=True,blank=True)
    position =  models.OneToOneField("Position",on_delete= models.SET_NULL,null=True,blank=True)

class Position(models.Model):
    position_id = models.AutoField(primary_key=True,unique=True)
    position_type = models.CharField(max_length=255,unique=True)
    date_added = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.position_type

    class Meta:
        # db_table = "position"
        verbose_name_plural = "Positions"

class Complainant(models.Model):

    complainant_id = models.AutoField(primary_key=True,unique=True)
    complainant_name = models.CharField(max_length=255)
    complainant_purok = models.ForeignKey("Purok",on_delete=models.SET_NULL, null=True, blank=True)
    complainant_barangay = models.CharField(max_length=50,default='Dalipe')
    date_added = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.complainant_name

    class Meta:
        # db_table = "complainant"
        verbose_name_plural = "Complainant"

class Entities(models.Model):

    entity_id = models.AutoField(primary_key=True,unique=True)
    entity_name = models.CharField(max_length=255)
    date_added = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.entity_name

    class Meta:
        # db_table = "entity"
        verbose_name_plural = "Entities"

class Respondents(models.Model):
    respondent_id = models.AutoField(primary_key=True,unique=True)
    respondent_name = models.CharField(max_length=255,unique=True)
    respondent_purok = models.ForeignKey("Purok",on_delete=models.SET_NULL,null=True, blank=True)
    respondent_barangay  = models.CharField(max_length=50,default='Dalipe')
    date_added = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.respondent_name

    class Meta:
        # db_table = "respondent"
        verbose_name_plural = "Respondents"

class Purok(models.Model):
    purok_id = models.AutoField(primary_key=True,unique=True)
    purok_name = models.CharField(max_length=255)
    date_added = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.purok_name

    class Meta:
        # db_table = "purok"
        verbose_name_plural = "Purok"

class Complaints(models.Model):
    STATUS_FIRST = "First Meeting"
    STATUS_SECOND = "Second Meeting"
    STATUS_THIRD = "Third Meeting"
    STATUS_SETTLED = "Settled"
    STATUS_FINAL = "Endorsed"

    COMPLAINT_TYPE_1 = "Minor Complaint"
    COMPLAINT_TYPE_2 = "Major Complaint"

    STATUS = {
        (STATUS_FIRST, 'First Meeting'),
        (STATUS_SECOND, 'Second Meeting'),
        (STATUS_THIRD, 'Third Meeting'),
        (STATUS_SETTLED, 'Settled'),
        (STATUS_FINAL, 'Endorsed'),
    }

    COMPLAINT_TYPE = {
        (COMPLAINT_TYPE_1, 'Minor Complaint'),
        (COMPLAINT_TYPE_2, 'Major Complaint'),
    }

    complaint_id      = models.AutoField(primary_key=True,unique=True)
    case_no           = models.IntegerField(default=0,unique=True)
    complainant       = models.ForeignKey(Complainant, on_delete=models.CASCADE)
    respondent        = models.ForeignKey(Respondents, on_delete=models.CASCADE)
    complaint_status  = models.CharField(max_length=50, choices=STATUS)
    complaint_type    = models.CharField(max_length=50, choices=COMPLAINT_TYPE,default=COMPLAINT_TYPE_1)
    complaint_desc    = models.TextField(max_length=300)
    settlement_desc   = models.TextField(max_length=300)
    hearing_schedule  = models.DateTimeField(default=datetime.now())
    date_complaint    = models.DateTimeField(default=datetime.now(),null=True,blank=True)

    def __str__(self):
        return str(self.complainant)

    class Meta:
        # db_table = "complaints"
        verbose_name_plural = "Complaints"
