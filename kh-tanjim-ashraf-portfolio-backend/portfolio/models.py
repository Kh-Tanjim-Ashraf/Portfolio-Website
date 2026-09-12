from django.db import models
from shared.models import TimestampMixins
from django.core.validators import MinValueValidator, MaxValueValidator, URLValidator
from django.utils.text import slugify

'''
# Anatomy of TextChoices:
VARIABLE_NAME = "database_value", _("Human Readable Label")

# Note: To filter by category, always provide the database_value from the client/django-view
'''

class Skill(TimestampMixins):
    # TODO: Write a case study about why I changed the short form of category names to original form. Link to->`filter_by_search()` method of `SkillFilter` class in `filters.py` file
    class Category(models.TextChoices):
        FRONTEND = 'frontend', 'Frontend'
        BACKEND = 'backend', 'Backend'
        DATABASE = 'database', 'Database'
        DEVOPS = 'devops', 'DevOps'
        TOOLS = 'tools', 'Tools'
        SOFT_SKILL = 'soft skill', 'Soft Skill'
    
    name = models.CharField(max_length=50, unique=True)
    category = models.CharField(max_length=10, choices=Category.choices)
    proficiency = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    icon = models.ImageField(upload_to='portfolio/skill/icon/')
    display_order = models.PositiveSmallIntegerField(default=0)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name}'



class Project(TimestampMixins):
    class Category(models.TextChoices):
        WEB = 'web', 'Web'
        MOBILE = 'mobile', 'Mobile'
        API = 'api', 'API'
        ML = 'ml', 'ML'
        OTHER = 'other', 'Other'
    
    title = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True) # blank=True allows empty form submission
    skill = models.ManyToManyField(to=Skill, related_name="skills")
    summary = models.CharField(max_length=200)
    description = models.TextField()
    cover_image = models.ImageField(upload_to="portfolio/project/coverImage/")
    category = models.CharField(max_length=6, choices=Category.choices)
    live_url = models.URLField(max_length=255, blank=True, null=True, validators=[URLValidator(schemes=['https'])])
    github_url = models.URLField(max_length=255, blank=True, null=True, validators=[URLValidator(schemes=['https'])])
    is_featured = models.BooleanField(default=False)
    completed_date = models.DateTimeField(null=True, blank=True)
    display_order = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return f'{self.title} --- Display Order: {self.display_order}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)



class Experience(TimestampMixins):
    class EmploymentTypes(models.TextChoices):
        FULL_TIME = 'Ft', 'Full Time'
        PART_TIME = 'Pt', 'Part Time'
        INTERNSHIP = 'Ir', 'Internship'
        FREELANCE = 'Fl', 'Freelance'
        CONTRACT = 'Cr', 'Contract'
    
    company = models.CharField(max_length=150)
    role = models.CharField(max_length=150)
    employment_type = models.CharField(max_length=2, choices=EmploymentTypes.choices)
    location = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField()
    company_url = models.URLField(max_length=255, null=True, blank=True, validators=[URLValidator(schemes=['https','http'])])
    display_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f'{self.company}---{self.role}---Display Order: {self.display_order}'



class Education(TimestampMixins):
    instituition = models.CharField(max_length=150) 
    degree = models.CharField(max_length=30)
    field_of_study = models.CharField(max_length=30)
    start_year = models.DateTimeField()
    end_year = models.DateTimeField(null=True, blank=True)
    grade = models.CharField(max_length=30, null=True, blank=True)
    description = models.CharField(null=True, blank=True)

    def __str__(self):
        return f'{self.instituition}---{self.degree}: {self.field_of_study}'