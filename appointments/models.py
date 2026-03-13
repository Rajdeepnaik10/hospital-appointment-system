from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class AvailabilitySlot(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.doctor} {self.date} {self.start_time}"
    
class Appointment(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="doctor_appointments")
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="patient_appointments")

    slot = models.OneToOneField(AvailabilitySlot, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient} with {self.doctor}"