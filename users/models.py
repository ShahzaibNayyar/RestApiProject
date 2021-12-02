from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class UserProfileManager(BaseUserManager):
    def ___str__(self):
        return self.make
    # def create(self,user,phone_number, age, gender):
    #     profile = self.model(
    #         user = user,
    #         phone_number = phone_number,
    #         age = age,
    #         gender = gender
    #     )
    #     profile.save(using=self._db)
    #     return profile



class VehicleManager(BaseUserManager):
    def create(self, user,v_type,make,model,color,reg_year ):
        vehicle = self.model(
            user=user,
            vehicle_type=v_type,
            make=make,
            model=model,
            color=color,
            reg_year=reg_year,

        )
        vehicle.save(using=self._db)
        return vehicle


class CustomUserManager(BaseUserManager):

    def _create_user(self,email, password, first_name, last_name, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        if not password:
            raise ValueError('Password is required')
        user = self.model(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self,email, password, first_name, last_name, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email=email,password=password,first_name=first_name,last_name=last_name,**extra_fields)

    def create_superuser(self,email, password, first_name, last_name, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email=email,password=password,first_name=first_name,last_name=last_name,**extra_fields)

class User(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(db_index=True, unique=True, max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    age = models.IntegerField()
    gender = models.CharField(max_length=30)

    objects = UserProfileManager()

class Vehicles(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user', null=True)
    vehicle_type = models.CharField(max_length=20)
    make = models.CharField(max_length=30)
    model = models.CharField(max_length=30)
    color = models.CharField(max_length=30)
    reg_year = models.IntegerField()

    objects = VehicleManager()

    objects = UserProfileManager()


