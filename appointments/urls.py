from django.urls import path
from .views import book_slot

urlpatterns = [
    path("book/<int:slot_id>/<int:patient_id>/", book_slot),
]