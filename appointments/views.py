from django.db import transaction
from django.http import JsonResponse
from .models import AvailabilitySlot, Appointment
from django.contrib.auth import get_user_model
from .google_calendar import create_calendar_event
import datetime
import requests
import threading

User = get_user_model()


# Send email asynchronously
def send_email_async(payload):
    try:
        requests.post(
            "http://localhost:3000/dev/send-email",
            json=payload
        )
    except Exception as e:
        print("Email service error:", e)


def book_slot(request, slot_id, patient_id):
    try:
        with transaction.atomic():

            # Lock slot row
            slot = AvailabilitySlot.objects.select_for_update().get(id=slot_id)

            # Prevent double booking
            if slot.is_booked:
                return JsonResponse({"error": "Slot already booked"}, status=400)

            # 🚨 NEW: Prevent booking past slots
            slot_datetime = datetime.datetime.combine(slot.date, slot.start_time)
            now = datetime.datetime.now()

            if slot_datetime <= now:
                return JsonResponse(
                    {"error": "This slot has already expired"},
                    status=400
                )

            patient = User.objects.get(id=patient_id)

            # Create appointment
            appointment = Appointment.objects.create(
                doctor=slot.doctor,
                patient=patient,
                slot=slot
            )

            # Mark slot booked
            slot.is_booked = True
            slot.save()

            # Create Google Calendar event
            try:
                start = datetime.datetime.combine(slot.date, slot.start_time)
                end = datetime.datetime.combine(slot.date, slot.end_time)

                create_calendar_event(
                    f"Appointment with Dr {slot.doctor.username}",
                    start,
                    end
                )

            except Exception as e:
                print("Calendar error:", e)

            # Email payload
            payload = {
                "action": "BOOKING_CONFIRMATION",
                "email": patient.email or "blackdevil0123456@gmail.com",
                "doctor": slot.doctor.username,
                "date": str(slot.date),
                "time": str(slot.start_time)
            }

            # Send email in background
            threading.Thread(
                target=send_email_async,
                args=(payload,)
            ).start()

            return JsonResponse({
                "message": "Appointment booked successfully",
                "appointment_id": appointment.id
            })

    except AvailabilitySlot.DoesNotExist:
        return JsonResponse({"error": "Slot not found"}, status=404)