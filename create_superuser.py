import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.accounts.models import User

# Vérifier si le superutilisateur existe déjà
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@kengan.com',
        password='admin123'  # Changer ce mot de passe en production !
    )
    print("Superutilisateur 'admin' créé avec succès")
else:
    print("Le superutilisateur 'admin' existe déjà")
