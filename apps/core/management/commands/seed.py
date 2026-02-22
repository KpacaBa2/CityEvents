from django.contrib.auth.models import Group, Permission, User
from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

from apps.categories.models import Category
from apps.core.models import City
from apps.events.models import Event
from apps.organizers.models import Organizer, OrganizerMember
from apps.tags.models import Tag
from apps.users.models import UserProfile
from apps.venues.models import Venue


class Command(BaseCommand):
    help = 'Seed demo data for CityEvents'

    def handle(self, *args, **options):
        groups = ['User', 'Organizer', 'Staff']
        group_map = {}
        for name in groups:
            group_map[name], _ = Group.objects.get_or_create(name=name)

        def add_perms(group_name, models):
            group = group_map[group_name]
            for model in models:
                ct = ContentType.objects.get_for_model(model)
                codenames = [
                    f'add_{model._meta.model_name}',
                    f'change_{model._meta.model_name}',
                    f'delete_{model._meta.model_name}',
                    f'view_{model._meta.model_name}',
                ]
                perms = Permission.objects.filter(content_type=ct, codename__in=codenames)
                group.permissions.add(*perms)

        add_perms('Organizer', [Event, Category, Venue, Organizer, Tag])
        add_perms('Staff', [Event, Category, Venue, Organizer, Tag])

        user, _ = User.objects.get_or_create(username='demo_user', defaults={'email': 'user@example.com'})
        user.set_password('DemoPass123')
        user.save()

        organizer_user, _ = User.objects.get_or_create(username='demo_org', defaults={'email': 'org@example.com'})
        organizer_user.set_password('DemoPass123')
        organizer_user.save()
        profile, _ = UserProfile.objects.get_or_create(user=organizer_user)
        profile.role = UserProfile.ROLE_ORGANIZER
        profile.save()

        city, _ = City.objects.get_or_create(name='Almaty', slug='almaty')

        categories = [
            Category.objects.get_or_create(name='Музыка', slug='music')[0],
            Category.objects.get_or_create(name='Спорт', slug='sport')[0],
            Category.objects.get_or_create(name='Выставки', slug='expo')[0],
        ]

        tags = [
            Tag.objects.get_or_create(name='Бесплатно', slug='free')[0],
            Tag.objects.get_or_create(name='Семейное', slug='family')[0],
            Tag.objects.get_or_create(name='Вечер', slug='evening')[0],
        ]

        venue, _ = Venue.objects.get_or_create(
            name='City Hall',
            slug='city-hall',
            city=city,
            address='Abay Ave 10',
            capacity=1200,
        )

        organizer, _ = Organizer.objects.get_or_create(name='CityEvents Team', slug='cityevents-team')
        OrganizerMember.objects.get_or_create(
            organizer=organizer,
            user=organizer_user,
            defaults={'role': 'Owner', 'is_owner': True},
        )

        event, _ = Event.objects.get_or_create(
            title='Городской концерт',
            slug='city-concert',
            defaults={
                'description': 'Музыкальный вечер на открытой площадке.',
                'start_at': timezone.now() + timezone.timedelta(days=3),
                'end_at': timezone.now() + timezone.timedelta(days=3, hours=2),
                'venue': venue,
                'organizer': organizer,
                'status': Event.STATUS_PUBLISHED,
                'price_from': 0,
            },
        )
        event.categories.set(categories)
        event.tags.set(tags)

        self.stdout.write(self.style.SUCCESS('Seed data created.'))
