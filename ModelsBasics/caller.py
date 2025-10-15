import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# from main_app.models import UserProfile
#
# user = UserProfile(
#     username="dido",
#     first_name="dido",
#     last_name="dido",
#     email="dido@gmail.com",
#     bio="info",
#     profile_image_url="http://dido.com"
# )
# user.full_clean()
# user.save()