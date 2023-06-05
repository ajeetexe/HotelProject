from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
import uuid
# from django.utils.translation import ugettext_lazy as _
# Create your models here.

class UserManager(BaseUserManager):
    
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email not found")
        email = self.normalize_email(email)
        user = self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
    
    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser',False)
        extra_fields.setdefault('is_staff',False)
        return self._create_user(email,password,**extra_fields)
    

    def create_superuser(self,email,password,**extra_fields):
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_staff',True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True")
        return self._create_user(email,password,**extra_fields)
    

class User(AbstractUser):
    
    username = None
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=10,default='')
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    gender = models.CharField(max_length=10,choices=(
        ('male','Male'),
        ('female','Female'),
        ('other','Other')
    ))
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

class ForgetPasswordVarify(models.Model):
    user = models.OneToOneField(User,models.CASCADE,primary_key=True)
    data = models.CharField(max_length=1000)
    is_varified = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)
    
class Room(models.Model):
    room_detail = models.CharField(max_length=1000)
    city = models.CharField(max_length=1000)
    star = models.CharField(max_length=1000)
    room_image = models.ImageField(upload_to='room')
    room_price = models.PositiveIntegerField()
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return str(self.pk)


class Booking(models.Model):
    
    booking_id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4,unique=True)
    email = models.ForeignKey(User,models.CASCADE)
    room = models.ForeignKey(Room,models.CASCADE) 
    first_name = models.CharField(max_length=1000)
    last_name = models.CharField(max_length=1000)
    phone_number = models.CharField(max_length=10)
    check_in = models.DateField()
    check_out = models.DateField()
    guests = models.CharField(max_length=1000)
    room_type = models.CharField(max_length=1000)

    def __str__(self):
        return str(self.booking_id)



class UserMessage(models.Model):
    full_name = models.CharField(max_length=1000)
    email = models.EmailField()
    message = models.TextField(max_length=10000)
    is_registerd = models.BooleanField(default=False)

    def __str__(self):
        return str(self.full_name)
    
class PaymentDetail(models.Model):
    payment_id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4,unique=True)
    booking_id = models.OneToOneField(Booking,models.CASCADE)
    card_holder_name = models.CharField(max_length=1000)
    card_type = models.CharField(max_length=1000)
    card_name = models.CharField(max_length=1000)
    card_number = models.CharField(max_length=20)
    expiry_date = models.CharField(max_length=5)
    cvv = models.CharField(max_length=3)
    payment_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.payment_id)
    