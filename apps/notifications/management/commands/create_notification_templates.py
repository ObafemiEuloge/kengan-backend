from django.core.management.base import BaseCommand
from apps.notifications.models import NotificationTemplate

class Command(BaseCommand):
    help = 'Créer les templates de notification par défaut'

    def handle(self, *args, **options):
        # Template d'email de bienvenue
        welcome_template, created = NotificationTemplate.objects.get_or_create(
            code='welcome_email',
            defaults={
                'name': 'Email de bienvenue',
                'type': 'email',
                'subject': 'Bienvenue sur KENGAN - Confirmez votre compte',
                'content': """Bonjour {{username}},

Merci de vous être inscrit sur KENGAN, la plateforme de duels de connaissances anime et manga !

Pour confirmer votre compte et commencer à participer aux duels, veuillez cliquer sur le lien suivant :
{{confirmation_link}}

Ce lien expirera dans 24 heures.

Si vous avez des questions, n'hésitez pas à contacter notre équipe de support à {{support_email}}.

À bientôt dans l'arène !

L'équipe KENGAN""",
                'variables': ['username', 'confirmation_link', 'support_email'],
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'Template d\'email de bienvenue créé: {welcome_template.code}'))
        else:
            self.stdout.write(self.style.WARNING(f'Le template d\'email de bienvenue existe déjà: {welcome_template.code}'))