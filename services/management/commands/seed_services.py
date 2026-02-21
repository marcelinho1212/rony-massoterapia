from django.core.management.base import BaseCommand
from professionals.models import Professional
from services.models import Service


class Command(BaseCommand):
    help = "Seed services and associate them with active professionals"

    def handle(self, *args, **options):
        services_data = [
            "Acupuntura",
            "Ventosaterapia",
            "Massoterapia",
            "Liberação Miofascial",
            "Quiropraxia",
            "Pedra Quente",
            "Fisiotrainer",
            "Shiatsu",
            "Massagem Relaxante",
            "Crochetagem",
            "Corrente Russa",
            "Cone Chinês",
            "Lomi Lomi Sensorial",
            "Shiatsu Drenante",
            "Banho Turco",
            "Esfoliação Corporal",
            "Hidratação",
        ]

        DEFAULT_PRICE_CENTS = 15000  # R$ 150,00
        DEFAULT_DURATION_MINUTES = 60

        professionals = Professional.objects.filter(is_active=True)

        if not professionals.exists():
            self.stdout.write(
                self.style.ERROR("Nenhum profissional ativo encontrado.")
            )
            return

        created_count = 0

        for service_name in services_data:
            service, created = Service.objects.get_or_create(
                name=service_name,
                defaults={
                    "price_cents": DEFAULT_PRICE_CENTS,
                    "duration_minutes": DEFAULT_DURATION_MINUTES,
                    "is_active": True,
                },
            )

            # associa a todos os profissionais ativos
            service.professionals.set(professionals)

            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f"Serviço criado: {service.name}")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"Serviço já existe: {service.name}")
                )

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                f"Seed concluído. {created_count} novo(s) serviço(s) criado(s)."
            )
        )
