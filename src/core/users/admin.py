from django.contrib import admin
from .models import CustomUser
from django.core.exceptions import ValidationError
from .validators import validate_brickyard_and_institution


class CustomUserAdmin(admin.ModelAdmin):
    model = CustomUser
    list_display = [
        "username",
        "email",
        "role",
        "brickyard",
        "institution",
        "is_staff",
        "is_superuser",
    ]
    list_filter = ["role", "brickyard", "institution", "is_staff", "is_superuser"]
    search_fields = ["username", "email"]

    def save_model(self, request, obj, form, change):
        try:
            validate_brickyard_and_institution(obj)
        except ValidationError as e:
            self.message_user(request, str(e), level="ERROR")
            return

        if not obj.brickyard and not obj.institution:
            obj.is_staff = True
            obj.is_superuser = True

        super().save_model(request, obj, form, change)


admin.site.register(CustomUser, CustomUserAdmin)
