from datetime import date

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from services.models import CustomerProfile, Service


SERVICE_SEED = [
    {
        "name": "Cham soc da mat Collagen",
        "slug": "cham-soc-da-mat-collagen",
        "short_description": "Lam sach sau, duong am va tai tao da.",
        "description": "Lieu trinh cham soc da mat chuyen sau ket hop collagen giup phuc hoi do am va cai thien do dan hoi.",
        "category": Service.CATEGORY_FACE,
        "duration_minutes": 90,
        "price": 1200000,
        "rating": "4.8",
        "image_url": "https://images.unsplash.com/photo-1515377905703-c4788e51af15?auto=format&fit=crop&w=1200&q=80",
        "status": Service.STATUS_ACTIVE,
        "display_order": 1,
    },
    {
        "name": "Tri mun chuyen sau",
        "slug": "tri-mun-chuyen-sau",
        "short_description": "Dieu tri mun an toan, hieu qua.",
        "description": "Lieu trinh lam sach, hut ba nhon, lay nhan mun va phuc hoi hang rao bao ve da.",
        "category": Service.CATEGORY_FACE,
        "duration_minutes": 60,
        "price": 800000,
        "rating": "4.5",
        "image_url": "https://images.unsplash.com/photo-1570172619644-dfd03ed5d881?auto=format&fit=crop&w=1200&q=80",
        "status": Service.STATUS_ACTIVE,
        "display_order": 2,
    },
    {
        "name": "Massage body thu gian",
        "slug": "massage-body-thu-gian",
        "short_description": "Massage toan than giup thu gian.",
        "description": "Goi massage body voi tinh dau thien nhien, giai toa cang thang va giam moi vai gay.",
        "category": Service.CATEGORY_BODY,
        "duration_minutes": 60,
        "price": 500000,
        "rating": "4.6",
        "image_url": "https://images.unsplash.com/photo-1519823551278-64ac92734fb1?auto=format&fit=crop&w=1200&q=80",
        "status": Service.STATUS_ACTIVE,
        "display_order": 3,
    },
    {
        "name": "Triet long laser IPL",
        "slug": "triet-long-laser-ipl",
        "short_description": "Cong nghe triet long hien dai, an toan.",
        "description": "Cong nghe IPL giup giam long moc lai va toi uu trai nghiem dieu tri.",
        "category": Service.CATEGORY_HAIR,
        "duration_minutes": 90,
        "price": 2000000,
        "rating": "4.8",
        "image_url": "https://images.unsplash.com/photo-1527799820374-dcf8d9d4a388?auto=format&fit=crop&w=1200&q=80",
        "status": Service.STATUS_ACTIVE,
        "display_order": 4,
    },
    {
        "name": "Goi dau duong sinh",
        "slug": "goi-dau-duong-sinh",
        "short_description": "Lam sach da dau va thu gian.",
        "description": "Lieu trinh ket hop massage da dau giup giam cang thang va cham soc toc.",
        "category": Service.CATEGORY_BODY,
        "duration_minutes": 45,
        "price": 300000,
        "rating": "4.7",
        "image_url": "https://images.unsplash.com/photo-1521590832167-7bcbfaa6381f?auto=format&fit=crop&w=1200&q=80",
        "status": Service.STATUS_ACTIVE,
        "display_order": 5,
    },
    {
        "name": "Xong hoi sauna",
        "slug": "xong-hoi-sauna",
        "short_description": "Gian no lo chan long va dao thai doc to.",
        "description": "Xong hoi ket hop huong lieu giup thu gian co bap va dao thai doc to cho co the.",
        "category": Service.CATEGORY_BODY,
        "duration_minutes": 90,
        "price": 700000,
        "rating": "4.9",
        "image_url": "https://images.unsplash.com/photo-1544161515-4ab6ce6db874?auto=format&fit=crop&w=1200&q=80",
        "status": Service.STATUS_ACTIVE,
        "display_order": 6,
    },
]


USER_SEED = [
    {
        "username": "manager",
        "email": "manager@example.com",
        "password": "pass12345",
        "first_name": "Quan ly",
        "last_name": "Mai Tram",
        "is_staff": True,
        "is_superuser": False,
    },
    {
        "username": "customer",
        "email": "customer@example.com",
        "password": "pass12345",
        "first_name": "Khach",
        "last_name": "Hang",
        "is_staff": False,
        "is_superuser": False,
    },
]


class Command(BaseCommand):
    help = "Seed demo users, customer profile, and services data (idempotent)."

    def handle(self, *args, **options):
        created_services = 0
        for payload in SERVICE_SEED:
            service, created = Service.objects.update_or_create(
                slug=payload["slug"], defaults=payload
            )
            if created:
                created_services += 1
            self.stdout.write(f"Service OK: {service.name}")

        for payload in USER_SEED:
            user_payload = payload.copy()
            password = user_payload.pop("password")
            user, _ = User.objects.update_or_create(
                username=user_payload["username"], defaults=user_payload
            )
            user.set_password(password)
            user.save()

            if not user.is_staff:
                CustomerProfile.objects.update_or_create(
                    user=user,
                    defaults={
                        "full_name": f"{user.last_name} {user.first_name}".strip(),
                        "member_since": date.today(),
                        "loyalty_points": 120,
                        "phone": "0901234567",
                        "address": "Da Nang",
                    },
                )

            self.stdout.write(
                f"User OK: {user.email} (staff={user.is_staff})"
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Seed completed. Services: {Service.objects.count()} total ({created_services} new)."
            )
        )


