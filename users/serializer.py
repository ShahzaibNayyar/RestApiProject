from rest_framework import serializers
from RestApiProject import settings
from .models import User, UserProfile,Vehicles

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, write_only=True)
    class Meta:
        model = User
        fields = ['email','first_name','last_name','password','is_staff','is_active','is_superuser']

    def create(self, validated_data):
        return User.objects._create_user(**validated_data)

    def update(self, instance, validated_data):
        print("instance check", instance, "validated_data", validated_data)
        return super().update(instance, validated_data)


class UpdateUserSerializer(serializers.ModelSerializer):
    # model = User
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    is_staff = serializers.BooleanField()
    is_active = serializers.BooleanField()
    is_superuser = serializers.BooleanField()

    class Meta:
        model = User
        fields = ['first_name','last_name','is_staff','is_active','is_superuser']


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)
    class Meta:
        model = UserProfile
        related_fields = ['user']
        fields = ['user','phone_number','age','gender']
        extra_kwargs = {
            'email': {'validators': []},
        }

    def create(self, validated_data):
        user_data = validated_data.pop('user')

        user = User.objects._create_user(email=user_data['email'],
                                         password=user_data['password'],
                                         first_name=user_data['first_name'],
                                         last_name=user_data['last_name'],
                                         is_active =user_data['is_active'],
                                         is_superuser=user_data['is_superuser'],
                                         is_staff=user_data['is_staff'],
                                         )

        userProfile = UserProfile.objects.create(
                                                 user=user,
                                                 phone_number=validated_data['phone_number'],
                                                 age=validated_data['age'],
                                                 gender=validated_data['gender']
                                                 )

        return userProfile

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')

        print("UserData" , user_data['first_name'])

        user_serializer = UpdateUserSerializer(data={

                "first_name": user_data['first_name'],
                "last_name": user_data['last_name'],
                "is_staff": user_data['is_staff'],
                "is_active": user_data['is_active'],
                "is_superuser": user_data['is_superuser']

        })
        if user_serializer.is_valid():
            print(user_serializer.validated_data)
            user = user_serializer.update(instance= instance.user, validated_data=user_serializer.validated_data)
            print('USER SERIALIZER' , user_serializer)
            validated_data['user'] = user
            profile_serializer = UserProfileSerializer(data=validated_data)
            if profile_serializer.is_valid():
                profile = profile_serializer.update(instance=instance,
                                                    validated_data=profile_serializer.validated_data)
                validated_data = profile
                print("validated_data", validated_data)
            else:
                print(profile_serializer.errors)
        else:
            print("ERROR" , user_serializer.errors)
        return super().update(instance, validated_data)

class VehicleSerializer(serializers.ModelSerializer):
    # user = UserSerializer(read_only=True)
    # user = UserSerializer(read_only=True,many=False)
    # user = UserSerializer(read_only=False, many=True)

    # user = UserSerializer.PrimaryKeyRelatedField(
    #     queryset=User.objects.all(),  # Or User.objects.filter(active=True)
    #     required=False,
    #     allow_null=True,
    #     default=None
    # )

    user = serializers.PrimaryKeyRelatedField(queryset = User.objects.all(),many = False)


    # user = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Vehicles
        fields = ['user', 'vehicle_type', 'make', 'model', 'color','reg_year']
        # read_only_fields = ('user')


        #
        # def create(self, validated_data):
        #     user_data = self.request.user
        #     print("user_data", user_data)
        #     vehicle = Vehicles.objects.create(user=user_data['email'],
        #                                          type=validated_data['vehicle_type'],
        #                                          make=validated_data['make'],
        #                                          model=validated_data['model'],
        #                                          color=validated_data['color'],
        #                                          reg_year=validated_data['reg_year'],
        #                                          )
        #     return vehicle
