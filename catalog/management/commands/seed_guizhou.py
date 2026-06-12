from datetime import date

from django.core.management.base import BaseCommand

from catalog.models import Feature, Region, ScenicSpot, SpotProfile


class Command(BaseCommand):
    help = "Создать демонстрационные данные для каталога достопримечательностей Гуйчжоу"

    def handle(self, *args, **options):
        SpotProfile.objects.all().delete()
        ScenicSpot.objects.all().delete()
        Feature.objects.all().delete()
        Region.objects.all().delete()

        regions = {
            "Аньшунь": "Район известен водопадами, карстовыми ландшафтами и культурой Тунбао.",
            "Цяньдуннань-Мяо-Дунский автономный округ": "Место с яркой культурой мяо и дун, деревянными домами и террасными пейзажами.",
            "Цяньнань-Буи-Мяоский автономный округ": "Район с карстом Либо, лесами и прозрачными речными долинами.",
            "Гуйян": "Столица провинции Гуйчжоу, сочетающая городской отдых и природные парки.",
            "Цзуньи": "Район с красной историей, данься-ландшафтами и чайным туризмом.",
        }
        region_objs = {
            name: Region.objects.update_or_create(name=name, defaults={"description": desc})[0]
            for name, desc in regions.items()
        }

        features = {
            "Водопады": "💦",
            "Карст": "🪨",
            "Этническая культура": "🎪",
            "Древний городок": "🏮",
            "Для семьи": "👨‍👩‍👧",
            "Пешие маршруты": "🥾",
            "Прохладный климат": "🌿",
            "Фотографии": "📷",
        }
        feature_objs = {
            name: Feature.objects.update_or_create(name=name, defaults={"icon": icon})[0]
            for name, icon in features.items()
        }

        data = [
            {
                "name": "Водопад Хуангошу",
                "region": "Аньшунь",
                "category": ScenicSpot.Category.WATERFALL,
                "short_description": "Один из самых известных крупных водопадов Азии; мощный поток можно увидеть с разных обзорных точек.",
                "address": "Гуйчжоу, Аньшунь, уезд Чжэньнин, посёлок Хуангошу",
                "ticket_price": 160,
                "rating": 5,
                "opening_date": date(1982, 1, 1),
                "is_world_heritage": False,
                "features": ["Водопады", "Карст", "Фотографии"],
                "profile": {
                    "best_season": "Июнь–октябрь, сезон высокой воды",
                    "suggested_hours": 5,
                    "transport_tips": "Можно доехать туристическим автобусом от Аньшуня или Гуйяна.",
                    "official_phone": "0851-33592136",
                },
            },
            {
                "name": "Малый Семь Арочный мост Либо",
                "region": "Цяньнань-Буи-Мяоский автономный округ",
                "category": ScenicSpot.Category.NATURE,
                "short_description": "Живописная зона с изумрудной водой, древним мостом, лесами и водопадами.",
                "address": "Гуйчжоу, округ Цяньнань, уезд Либо, рядом с туристическим посёлком Мэнлю",
                "ticket_price": 120,
                "rating": 5,
                "opening_date": date(2007, 6, 27),
                "is_world_heritage": True,
                "features": ["Карст", "Для семьи", "Прохладный климат", "Фотографии"],
                "profile": {
                    "best_season": "Апрель–сентябрь",
                    "suggested_hours": 6,
                    "transport_tips": "От станции или аэропорта Либо удобно пересесть на местный транспорт до парка.",
                    "official_phone": "0854-3516116",
                },
            },
            {
                "name": "Мяоская деревня Сицзян Цяньху",
                "region": "Цяньдуннань-Мяо-Дунский автономный округ",
                "category": ScenicSpot.Category.ETHNIC,
                "short_description": "Большая мяоская деревня на склонах гор с ночными видами, серебряными украшениями, танцами и деревянными домами.",
                "address": "Гуйчжоу, округ Цяньдуннань, уезд Лэйшань, посёлок Сицзян",
                "ticket_price": 90,
                "rating": 4,
                "opening_date": date(2008, 1, 1),
                "is_world_heritage": False,
                "features": ["Этническая культура", "Фотографии", "Древний городок"],
                "profile": {
                    "best_season": "Весна и осень",
                    "suggested_hours": 8,
                    "transport_tips": "От станции Кайли-Южный можно воспользоваться туристическим автобусом.",
                    "official_phone": "400-153-8866",
                },
            },
            {
                "name": "Древний городок Цинъянь",
                "region": "Гуйян",
                "category": ScenicSpot.Category.CULTURE,
                "short_description": "Военный городок эпохи Мин с каменными улицами, стенами, арками и местной кухней Гуйчжоу.",
                "address": "Гуйчжоу, город Гуйян, район Хуаси, посёлок Цинъянь",
                "ticket_price": 10,
                "rating": 4,
                "opening_date": date(1378, 1, 1),
                "is_world_heritage": False,
                "features": ["Древний городок", "Для семьи", "Этническая культура"],
                "profile": {
                    "best_season": "Круглый год, особенно весной и осенью",
                    "suggested_hours": 4,
                    "transport_tips": "Из центра Гуйяна можно доехать автобусом или на автомобиле через район Хуаси.",
                    "official_phone": "0851-83200400",
                },
            },
            {
                "name": "Туристическая зона Чишуй Данься",
                "region": "Цзуньи",
                "category": ScenicSpot.Category.NATURE,
                "short_description": "Сочетание красных данься-скал, водопадов, бамбуковых лесов и древовидных папоротников.",
                "address": "Гуйчжоу, город Цзуньи, Чишуй",
                "ticket_price": 80,
                "rating": 4,
                "opening_date": date(2010, 8, 1),
                "is_world_heritage": True,
                "features": ["Водопады", "Пешие маршруты", "Фотографии", "Прохладный климат"],
                "profile": {
                    "best_season": "Май–октябрь",
                    "suggested_hours": 6,
                    "transport_tips": "Лучше ехать на автомобиле или пересесть на местный транспорт от автовокзала Чишуй.",
                    "official_phone": "",
                },
            },
        ]

        for item in data:
            feature_names = item.pop("features")
            profile = item.pop("profile")
            spot, _ = ScenicSpot.objects.update_or_create(
                name=item["name"],
                defaults={
                    **item,
                    "region": region_objs[item["region"]],
                },
            )
            spot.features.set(feature_objs[name] for name in feature_names)
            SpotProfile.objects.update_or_create(spot=spot, defaults=profile)

        self.stdout.write(self.style.SUCCESS("Демонстрационные данные Гуйчжоу созданы/обновлены."))
