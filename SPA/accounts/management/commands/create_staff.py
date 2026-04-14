from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from accounts.models import UserProfile

class Command(BaseCommand):
    help = 'Tao tai khoan nhan vien/chu spa'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str, help='Email cua nhan vien')
        parser.add_argument('password', type=str, help='Mat khau')
        parser.add_argument('--role', type=str, default='staff', help='staff hoac customer (mac dinh: staff)')
        parser.add_argument('--name', type=str, help='Ten nhan vien')

    def handle(self, *args, **options):
        email = options['email']
        password = options['password']
        role = options['role']
        name = options.get('name') or email.split('@')[0]

        # Disconnect signals temporarily
        from accounts import signals as acc_signals
        post_save.disconnect(acc_signals.create_user_profile, sender=User)

        try:
            user = User.objects.get(email=email)
            self.stdout.write(self.style.ERROR(f'Email {email} da ton tai!'))
            return
        except User.DoesNotExist:
            pass

        try:
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=name
            )

            profile = UserProfile.objects.create(user=user, role=role)

            self.stdout.write(self.style.SUCCESS(
                f'Success! Tao tai khoan thanh cong!\n'
                f'Email: {email}\n'
                f'Role: {profile.get_role_display()}\n'
                f'Ten: {name}'
            ))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Loi: {str(e)}'))
        finally:
            # Reconnect signals
            post_save.connect(acc_signals.create_user_profile, sender=User)



