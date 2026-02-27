from datetime import datetime, time, timedelta
from urllib.parse import quote

from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from django.db import transaction
from django.http import HttpResponseBadRequest

from professionals.models import Professional
from services.models import Service
from schedule.models import WeeklyAvailability
from bookings.models import Booking
from django.shortcuts import render
from django.urls import reverse

def about(request):
    return render(request, "core/about.html")


def home(request):
    return render(request, "core/home.html")


def choose_professional(request):
    professionals = Professional.objects.filter(is_active=True).order_by("name")
    return render(
        request,
        "core/choose_professional.html",
        {"professionals": professionals},
    )


def choose_service(request, professional_slug):
    professional = get_object_or_404(
        Professional, slug=professional_slug, is_active=True
    )
    services = Service.objects.filter(
        is_active=True, professionals=professional
    ).order_by("name")

    return render(
        request,
        "core/choose_service.html",
        {
            "professional": professional,
            "services": services,
        },
    )


def _generate_slots(professional, service_duration_minutes, day_date):
    weekday = day_date.weekday()  # 0=Mon..6=Sun
    windows = WeeklyAvailability.objects.filter(
        professional=professional,
        weekday=weekday,
    )

    slots = []
    step = timedelta(minutes=30)
    duration = timedelta(minutes=service_duration_minutes)

    for w in windows:
        window_start = timezone.make_aware(
            datetime.combine(day_date, w.start_time)
        )
        window_end = timezone.make_aware(
            datetime.combine(day_date, w.end_time)
        )

        cur = window_start
        while cur + duration <= window_end:
            conflict = Booking.objects.filter(
                professional=professional,
                start__lt=cur + duration,
                end__gt=cur,
                status__in=["pending", "confirmed"],
            ).exists()

            if not conflict and cur >= timezone.now():
                slots.append(cur)

            cur += step

    return slots


def choose_slot(request, professional_slug, service_id):
    professional = get_object_or_404(
        Professional, slug=professional_slug, is_active=True
    )
    service = get_object_or_404(
        Service,
        id=service_id,
        is_active=True,
        professionals=professional,
    )

    today = timezone.localdate()
    days = [today + timedelta(days=i) for i in range(0, 7)]

    selected_day = request.GET.get("day")
    slots = []

    if selected_day:
        day_date = datetime.strptime(selected_day, "%Y-%m-%d").date()
        slots = _generate_slots(
            professional, service.duration_minutes, day_date
        )

    return render(
        request,
        "core/choose_slot.html",
        {
            "professional": professional,
            "service": service,
            "days": days,
            "selected_day": selected_day,
            "slots": slots,
        },
    )


@require_http_methods(["POST"])
def confirm_booking(request):
    professional_slug = request.POST["professional_slug"]
    service_id = int(request.POST["service_id"])
    slot_iso = request.POST["slot_iso"]

    customer_name = request.POST["customer_name"].strip()
    customer_whatsapp = request.POST["customer_whatsapp"].strip()

    professional = get_object_or_404(
        Professional, slug=professional_slug, is_active=True
    )
    service = get_object_or_404(
        Service,
        id=service_id,
        is_active=True,
        professionals=professional,
    )

    start = datetime.fromisoformat(slot_iso)
    if timezone.is_naive(start):
        start = timezone.make_aware(start)

    end = start + timedelta(minutes=service.duration_minutes)

    # 🔒 Trava de concorrência real
    with transaction.atomic():
        conflict = Booking.objects.select_for_update().filter(
            professional=professional,
            start__lt=end,
            end__gt=start,
            status__in=["pending", "confirmed"],
        ).exists()

        if conflict:
            return HttpResponseBadRequest(
                "Este horário acabou de ser reservado. Volte e escolha outro."
            )

        booking = Booking.objects.create(
            professional=professional,
            service=service,
            customer_name=customer_name,
            customer_whatsapp=customer_whatsapp,
            start=start,
            end=end,
            status="confirmed",
        )
        cancel_link = request.build_absolute_uri(reverse("cancel_booking", args=[booking.cancel_token]))

    # 📲 WhatsApp
    number = "".join(
        ch for ch in professional.whatsapp_number if ch.isdigit()
    )

    msg = (
    f"Novo agendamento confirmado ✅\n\n"
    f"Profissional: {professional.name}\n"
    f"Serviço: {service.name}\n"
    f"Data/Hora: {booking.start:%d/%m/%Y %H:%M}\n"
    f"Cliente: {booking.customer_name}\n"
    f"WhatsApp do cliente: {booking.customer_whatsapp}\n\n"
    f"---\n\n"
    f"Caso o cliente precise cancelar ou reagendar,\n"
    f"ele pode fazer isso pelo link abaixo:\n\n"
    f"{cancel_link}\n\n"
    f"Cancelamentos devem ser feitos com no mínimo 6 horas de antecedência."
)

    url = f"https://wa.me/{number}?text={quote(msg)}"
    return redirect(url)


def cancel_booking(request, token):
    booking = get_object_or_404(Booking, cancel_token=token)

    #se já estiver cancelado
    if booking.status == "cancelled":
        return render(request, "core/ja_cancelado.html")
    
    #verifica regra das 6 horas
    if not booking.can_cancel():
        return render(request, "core/prazo_expirado.html",{"booking": booking })
    
    #cancela
    booking.status = "cancelled"
    booking.save()

    return render (request, "core/sucesso.html", {"booking": booking })
