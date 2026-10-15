from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Member, Sunnah
from django.db import transaction


class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True ,min_length=8)
    
    class Meta:
        model = User
        fields = ['email', 'password']
        
    def validate_email(self, value):
        value = value.lower().strip()

        if User.objects.filter(
            username__iexact=value
        ).exists():
            raise serializers.ValidationError(
                "An account with this email already exists."
            )
        return value
    
    def create(self, validated_data):
        email = validated_data['email']
        password=validated_data['password']
        
        with transaction.atomic():
            user = User.objects.create_user(username=email, email=email, password=password)
            Member.objects.create(user=user, email=email)
            Sunnah.objects.create(user=user)
        
        return user
    
class MemberSerializer(serializers.ModelSerializer):
    city = serializers.CharField()

    madhab = serializers.ChoiceField(
        choices=[
            "hanafi",
            "shafi",
            "maliki",
            "hanbali",
            "jaffari",
        ]
    )
    
    setup_complete = serializers.BooleanField(
        read_only=True
    )
    
    class Meta:
        model = Member
        
        fields = [
            "email",
            "google_cal_email",
            "city",
            "country",
            "madhab",
            "prayer_enabled",
            "setup_complete",
        ]
        read_only_fields = [
            "email",
            "setup_complete",
        ]
        
    def update(self, instance, validated_data):
        schedule_fields = {
            "city",
            "country",
            "madhab",
        }
        
        
        member_update = any(
            field in schedule_fields
            and getattr(instance, field) != value
            for field, value in validated_data.items()
        )

        instance = super().update(instance, validated_data)

        # if not instance.setup_complete:
        #     instance.setup_complete = True
        #     instance.save(
        #         update_fields=["setup_complete"]
        #     )

        self.member_update = member_update

        return instance
    
    
            
            

class SunnahPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sunnah

        fields = [
            "sunnah_enabled",
            "tahajjud",
            "duha",
            "monday_fast",
            "thursday_fast",
            "white_days_fast",
            "arafah_fast",
            "ashura_fast",
            "first_nine_dhul_hijjah",
            "six_days_shawwal",
            "surah_kahf_fri",
            "surah_mulk_daily",
            "friday_dua",
            "friday_preparation",

            "arafah_dua",
            "morning_adhkar",
            "evening_adhkar",
        ]
        
    def update(self, instance, validated_data):
        sunnah_update = any(
            getattr(instance, field) != value
            for field, value in validated_data.items()
        )

        instance = super().update(instance, validated_data)
        
        self.sunnah_update = sunnah_update

        return instance