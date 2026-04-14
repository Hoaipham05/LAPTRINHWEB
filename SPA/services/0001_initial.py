from django.db import migrations, models


def seed_services(apps, schema_editor):
    Service = apps.get_model("services", "Service")
    Service.objects.bulk_create(
        [
            Service(
                name="Cham soc da mat Collagen",
                slug="cham-soc-da-mat-collagen",
                short_description="Lam sach sau, duong am va tai tao da.",
                description="Lieu trinh cham soc da mat chuyen sau ket hop collagen giup phuc hoi do am, lam mem da va cai thien do dan hoi.",
                category="face",
                duration_minutes=90,
                price=1200000,
                rating="4.8",
                image_url="https://images.unsplash.com/photo-1515377905703-c4788e51af15?auto=format&fit=crop&w=1200&q=80",
                status="active",
                display_order=1,
            ),
            Service(
                name="Tri mun chuyen sau",
                slug="tri-mun-chuyen-sau",
                short_description="Dieu tri mun an toan, hieu qua.",
                description="Lieu trinh lam sach, hut ba nhon, lay nhan mun va phuc hoi hang rao bao ve da cho lan da de noi mun.",
                category="face",
                duration_minutes=60,
                price=800000,
                rating="4.5",
                image_url="https://images.unsplash.com/photo-1570172619644-dfd03ed5d881?auto=format&fit=crop&w=1200&q=80",
                status="active",
                display_order=2,
            ),
            Service(
                name="Massage body thu gian",
                slug="massage-body-thu-gian",
                short_description="Massage toan than giup thu gian.",
                description="Goi massage body voi tinh dau thien nhien, giai toa cang thang, giam moi vai gay va phuc hoi nang luong.",
                category="body",
                duration_minutes=60,
                price=500000,
                rating="4.6",
                image_url="https://images.unsplash.com/photo-1519823551278-64ac92734fb1?auto=format&fit=crop&w=1200&q=80",
                status="active",
                display_order=3,
            ),
            Service(
                name="Triet long vinh vien bang laser IPL",
                slug="triet-long-vinh-vien-bang-laser-ipl",
                short_description="Cong nghe triet long hien dai, an toan.",
                description="Ung dung cong nghe IPL giup giam long moc lai, han che kich ung va toi uu trai nghiem dieu tri nhieu vung da.",
                category="hair",
                duration_minutes=90,
                price=2000000,
                rating="4.8",
                image_url="https://images.unsplash.com/photo-1527799820374-dcf8d9d4a388?auto=format&fit=crop&w=1200&q=80",
                status="active",
                display_order=4,
            ),
            Service(
                name="Tri rung toc va gau",
                slug="tri-rung-toc-va-gau",
                short_description="Lam sach da dau, giam ba nhon va kich thich moc toc.",
                description="Lieu trinh cham soc da dau chuyen sau ho tro giam gau, lam sach nang toc va cai thien suc khoe chan toc.",
                category="face",
                duration_minutes=60,
                price=1300000,
                rating="4.7",
                image_url="https://images.unsplash.com/photo-1521590832167-7bcbfaa6381f?auto=format&fit=crop&w=1200&q=80",
                status="active",
                display_order=5,
            ),
            Service(
                name="Xong hoi sauna",
                slug="xong-hoi-sauna",
                short_description="Gian no lo chan long va dao thai doc to.",
                description="Xong hoi ket hop huong lieu giup thu gian co bap, lam am duong ho hap va ho tro dao thai doc to cho co the.",
                category="body",
                duration_minutes=90,
                price=700000,
                rating="4.9",
                image_url="https://images.unsplash.com/photo-1544161515-4ab6ce6db874?auto=format&fit=crop&w=1200&q=80",
                status="active",
                display_order=6,
            ),
        ]
    )


def unseed_services(apps, schema_editor):
    Service = apps.get_model("services", "Service")
    Service.objects.filter(
        slug__in=[
            "cham-soc-da-mat-collagen",
            "tri-mun-chuyen-sau",
            "massage-body-thu-gian",
            "triet-long-vinh-vien-bang-laser-ipl",
            "tri-rung-toc-va-gau",
            "xong-hoi-sauna",
        ]
    ).delete()


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Service",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=200, unique=True)),
                ("slug", models.SlugField(blank=True, max_length=220, unique=True)),
                ("short_description", models.CharField(max_length=255)),
                ("description", models.TextField()),
                ("category", models.CharField(choices=[("face", "Da mat"), ("body", "Body"), ("hair", "Triet long")], max_length=20)),
                ("duration_minutes", models.PositiveIntegerField()),
                ("price", models.PositiveIntegerField()),
                ("rating", models.DecimalField(decimal_places=1, default=4.5, max_digits=2)),
                ("image_url", models.URLField(blank=True)),
                ("status", models.CharField(choices=[("active", "Hoat dong"), ("inactive", "Tam dung")], default="active", max_length=20)),
                ("display_order", models.PositiveIntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={"ordering": ["display_order", "id"]},
        ),
        migrations.RunPython(seed_services, unseed_services),
    ]
