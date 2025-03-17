from django.utils.timezone import now
from django.core.mail import send_mail
from .models import Plant


def send_maintenance_reminders():
    today = now().date()
    plants = Plant.objects.all()

    for plant in plants:
        reminders = []
        if plant.next_watering() and plant.next_watering() <= today:
            reminders.append(f"- Arrosage")

        if plant.next_fertilizing() and plant.next_fertilizing() <= today:
            reminders.append(f"- Fertilisation")

        if plant.next_repotting() and plant.next_repotting() <= today:
            reminders.append(f"- Rempotage")

        if plant.next_pruning() and plant.next_pruning() <= today:
            reminders.append(f"- Taille")

        if reminders:
            send_mail(
                subject=f"Rappel d'entretien pour {
                    plant.name}",
                message=f"Il est temps de s'occuper de votre plante :\n" +
                "\n".join(reminders),
                from_email="no-reply@plantes.com",
                recipient_list=["user@example.com"],
                fail_silently=True)
