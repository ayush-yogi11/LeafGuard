"""
Seeds a handful of realistic sample blog posts for local development.

Usage:
    python manage.py seed_blog
    python manage.py seed_blog --flush   # deletes existing posts first
"""
from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.accounts.models import CustomUser
from apps.blog.models import Post, Category, Tag


SAMPLE_POSTS = [
    {
        "title": "Recognizing Early Blight Before It Spreads",
        "category": "Disease Alerts",
        "tags": ["tomato", "blight", "prevention"],
        "excerpt": "Early blight often starts small — here's what to look for on lower leaves before it takes hold.",
        "content": (
            "<p>Early blight typically appears first on the oldest, lowest leaves of the plant "
            "as small brown spots with a distinctive concentric ring pattern, sometimes described "
            "as a target or bullseye.</p>"
            "<p>Left unmanaged, lesions expand and merge, causing yellowing and premature leaf drop. "
            "Because the fungus overwinters in soil and plant debris, crop rotation and removing "
            "infected foliage promptly are your first lines of defense.</p>"
            "<p>If conditions are humid and disease pressure is high, a copper-based or chlorothalonil "
            "fungicide applied early in the season can help protect new growth.</p>"
        ),
    },
    {
        "title": "Why Overhead Watering Invites Fungal Disease",
        "category": "Prevention Tips",
        "tags": ["watering", "fungus", "prevention"],
        "excerpt": "The way you water matters as much as how often — here's why drip irrigation beats sprinklers.",
        "content": (
            "<p>Many common leaf diseases — late blight, septoria leaf spot, powdery mildew — spread "
            "far more aggressively when foliage stays wet for extended periods.</p>"
            "<p>Overhead watering, especially in the evening, keeps leaves damp overnight, creating "
            "ideal conditions for fungal spores to germinate. Switching to drip irrigation or soaker "
            "hoses at the base of the plant keeps foliage dry while still delivering water to the roots.</p>"
            "<p>If overhead watering is your only option, water early in the morning so leaves have "
            "the whole day to dry out.</p>"
        ),
    },
    {
        "title": "Citrus Greening: What Growers Need to Know",
        "category": "Disease Alerts",
        "tags": ["citrus", "greening", "pests"],
        "excerpt": "There's no cure for citrus greening — early detection and vector control are everything.",
        "content": (
            "<p>Huanglongbing, commonly known as citrus greening, is one of the most destructive "
            "citrus diseases worldwide. Infected trees show blotchy, asymmetric yellowing on leaves "
            "and produce small, bitter, lopsided fruit.</p>"
            "<p>The disease is spread by the Asian citrus psyllid, a small insect that feeds on citrus "
            "foliage. Because there is currently no cure, management focuses on controlling the "
            "psyllid population with approved insecticides and removing confirmed infected trees "
            "to prevent further spread.</p>"
            "<p>Regularly inspecting new growth for the psyllid itself, not just disease symptoms, "
            "gives growers the earliest possible warning.</p>"
        ),
    },
    {
        "title": "A Simple Weekly Leaf-Check Routine",
        "category": "Seasonal Care",
        "tags": ["routine", "prevention"],
        "excerpt": "Catching disease early is mostly about looking often — here's a five-minute weekly habit.",
        "content": (
            "<p>Most home gardeners lose plants to disease not because treatment doesn't work, but "
            "because the problem isn't spotted until it's already widespread.</p>"
            "<p>A simple fix: once a week, walk your garden and turn over a few lower leaves on each "
            "plant, checking the undersides where mildew and pest eggs are hardest to spot from above. "
            "Look for discoloration, spotting, or a dusty coating.</p>"
            "<p>Pairing this habit with a quick photo scan of anything suspicious means you'll usually "
            "catch problems while they're still easy to manage.</p>"
        ),
    },
]


class Command(BaseCommand):
    help = "Seeds sample blog posts for local development."

    def add_arguments(self, parser):
        parser.add_argument(
            "--flush",
            action="store_true",
            help="Delete all existing posts before seeding new ones.",
        )

    def handle(self, *args, **options):
        if options["flush"]:
            deleted_count, _ = Post.objects.all().delete()
            self.stdout.write(self.style.WARNING(f"Deleted {deleted_count} existing post(s)."))

        # Use the first staff/superuser as the author, falling back to
        # creating one won't happen here — seeding assumes you've already
        # run createsuperuser, since posts need a real author account.
        author = CustomUser.objects.filter(is_staff=True).first()
        if author is None:
            self.stderr.write(self.style.ERROR(
                "No staff user found. Run `python manage.py createsuperuser` first."
            ))
            return

        created_count = 0
        for entry in SAMPLE_POSTS:
            if Post.objects.filter(title=entry["title"]).exists():
                continue  # avoid duplicates on repeated runs

            category, _ = Category.objects.get_or_create(name=entry["category"])

            post = Post.objects.create(
                title=entry["title"],
                author=author,
                category=category,
                excerpt=entry["excerpt"],
                content=entry["content"],
                status=Post.Status.PUBLISHED,
                published_at=timezone.now(),
            )

            for tag_name in entry["tags"]:
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                post.tags.add(tag)

            created_count += 1
            self.stdout.write(f"  Created: {post.title}")

        self.stdout.write(self.style.SUCCESS(f"\nSeeded {created_count} new post(s)."))