"""
Okumpi core models — everything the site renders is editable in /admin.
Django 5.x / 6.x compatible. No Pillow required (logos/covers are
static paths or CSS gradients, not ImageFields).
"""
from django.conf import settings
from django.db import models
from django.utils.text import slugify


class TimeStampedModel(models.Model):
    """Abstract base model with created/updated timestamps."""
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SlugModelMixin(models.Model):
    """Auto-slugs from a `name` or `title` field."""

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if hasattr(self, 'slug') and not self.slug:
            source = getattr(self, 'name', None) or getattr(self, 'title', '')
            self.slug = slugify(source)[:180]
        super().save(*args, **kwargs)


class SiteSettings(TimeStampedModel):
    """Site configuration key-value pairs."""
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField(blank=True)
    description = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = 'Site Setting'
        verbose_name_plural = 'Site Settings'

    def __str__(self):
        return self.key


class ServiceCategory(SlugModelMixin, TimeStampedModel):
    """Practice areas — Okumpi Build, Integrate, Cloud & AI, Secure, Connect, Care."""
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    icon = models.CharField(
        max_length=40, default='code',
        help_text="SVG icon key: code, plug, cloud, shield, network, headset, chip, chart")
    tagline = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    accent = models.CharField(
        max_length=20, default='violet',
        help_text="Accent hue: violet, iris, magenta, cyan, lime, amber")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name_plural = 'Service Categories'

    def __str__(self):
        return self.name


class Service(SlugModelMixin, TimeStampedModel):
    """Individual services under a practice area."""
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150)
    category = models.ForeignKey(
        ServiceCategory, on_delete=models.CASCADE, related_name='services')
    description = models.TextField()
    features = models.TextField(
        blank=True, help_text="Comma-separated list of features")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        unique_together = ['slug', 'category']

    def __str__(self):
        return self.name

    def get_features_list(self):
        return [f.strip() for f in self.features.split(',') if f.strip()]


class Industry(SlugModelMixin, TimeStampedModel):
    """Vertical solutions — HRMS, Hospital, Property, Judicial, Government…"""
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=120, unique=True)
    icon = models.CharField(max_length=40, default='building')
    headline = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    features = models.TextField(blank=True, help_text="Comma-separated highlights")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name_plural = 'Industries'

    def __str__(self):
        return self.name

    def get_features_list(self):
        return [f.strip() for f in self.features.split(',') if f.strip()]


class Testimonial(TimeStampedModel):
    """Client testimonials shown in the home-page carousel."""
    PLATFORM_CHOICES = [
        ('google', 'Google'),
        ('clutch', 'Clutch'),
        ('trustpilot', 'Trustpilot'),
        ('linkedin', 'LinkedIn'),
        ('direct', 'Direct Client'),
    ]

    quote = models.TextField()
    author = models.CharField(max_length=100)
    role = models.CharField(max_length=120, blank=True)
    company = models.CharField(max_length=120, blank=True)
    platform = models.CharField(
        max_length=20, choices=PLATFORM_CHOICES, default='direct')
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=5.0)
    avatar_hue = models.PositiveIntegerField(
        default=260, help_text="0-360 hue for the generated avatar")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.author} ({self.platform})"

    @property
    def initials(self):
        parts = self.author.replace('.', '').split()
        return ''.join(p[0] for p in parts[:2]).upper()

    @property
    def stars_full(self):
        return range(int(self.rating))

    @property
    def stars_empty(self):
        return range(5 - int(self.rating))


class Partner(TimeStampedModel):
    """Technology / payments / banking partners (logo marquee)."""
    KIND_CHOICES = [
        ('payments', 'Mobile Money & Banking'),
        ('cloud', 'Cloud & Technology'),
        ('client', 'Client'),
    ]

    name = models.CharField(max_length=120)
    kind = models.CharField(max_length=20, choices=KIND_CHOICES, default='cloud')
    logo = models.CharField(
        max_length=255,
        help_text="Static path, e.g. img/partners/aws.png")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class Country(TimeStampedModel):
    """African countries Okumpi serves."""
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=2, help_text="ISO 2-letter code")
    flag = models.CharField(max_length=10, default='🌍')
    phone_code = models.CharField(max_length=10, blank=True)
    phone_number = models.CharField(max_length=30, blank=True)
    office_location = models.CharField(max_length=100, blank=True)
    is_hq = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name_plural = 'Countries'

    def __str__(self):
        return f"{self.flag} {self.name}"


class FAQ(TimeStampedModel):
    """Frequently asked questions (home page accordion)."""
    question = models.CharField(max_length=250)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'

    def __str__(self):
        return self.question


class JobPosition(SlugModelMixin, TimeStampedModel):
    """Open roles listed on the careers page."""
    JOB_TYPE_CHOICES = [
        ('full_time', 'Full-Time'),
        ('part_time', 'Part-Time'),
        ('contract', 'Contract'),
        ('intern', 'Internship'),
    ]

    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150)
    location = models.CharField(max_length=100)
    job_type = models.CharField(
        max_length=20, choices=JOB_TYPE_CHOICES, default='full_time')
    description = models.TextField()
    requirements = models.TextField(blank=True)
    tags = models.CharField(
        max_length=255, blank=True, help_text="Comma-separated tags")
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title

    def get_tags_list(self):
        return [t.strip() for t in self.tags.split(',') if t.strip()]


class News(SlugModelMixin, TimeStampedModel):
    """News and press releases."""
    NEWS_TYPE_CHOICES = [
        ('announcement', 'Announcement'),
        ('partnership', 'Partnership'),
        ('expansion', 'Expansion'),
        ('award', 'Award'),
        ('insight', 'Insight'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    news_type = models.CharField(
        max_length=20, choices=NEWS_TYPE_CHOICES, default='announcement')
    excerpt = models.CharField(max_length=300, blank=True)
    content = models.TextField()
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created']
        verbose_name_plural = 'News'

    def __str__(self):
        return self.title


class BlogCategory(SlugModelMixin, TimeStampedModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name_plural = 'Blog Categories'

    def __str__(self):
        return self.name


class BlogPost(SlugModelMixin, TimeStampedModel):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    category = models.ForeignKey(
        BlogCategory, on_delete=models.SET_NULL, null=True,
        blank=True, related_name='posts')
    excerpt = models.CharField(max_length=300, blank=True)
    content = models.TextField()
    author_name = models.CharField(max_length=100, default='Okumpi Team')
    read_minutes = models.PositiveIntegerField(default=5)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title


class KBArticle(SlugModelMixin, TimeStampedModel):
    """Knowledge base articles."""
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    category = models.ForeignKey(
        ServiceCategory, on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField()
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['title']
        verbose_name = 'KB Article'

    def __str__(self):
        return self.title


class ForumCategory(SlugModelMixin, TimeStampedModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    icon = models.CharField(max_length=40, default='chat')
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name_plural = 'Forum Categories'

    def __str__(self):
        return self.name


class ForumPost(TimeStampedModel):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(
        ForumCategory, on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True)
    content = models.TextField()
    is_published = models.BooleanField(default=True)
    views = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title


class ContactMessage(TimeStampedModel):
    """Contact form submissions."""
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    company = models.CharField(max_length=150, blank=True)
    country = models.CharField(max_length=50, blank=True)
    service_interest = models.CharField(max_length=80, blank=True)
    message = models.TextField()
    is_resolved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f"{self.name} - {self.email}"


class Newsletter(TimeStampedModel):
    """Newsletter subscribers (hero email capture)."""
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email
