from rest_framework import serializers
from .models import Skill, Experience, Education, Project


class SkillSerializer(serializers.ModelSerializer):

    class Meta:
        model = Skill
        fields = ['name','category','proficiency','icon','display_order','is_featured']



class ExperienceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Experience
        fields = ['company','role','employment_type','location','start_date','end_date','is_current','description','company_url','display_order']



class EducationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Education
        fields = ['instituition','degree','field_of_study','start_year','end_year','grade','description']



class SkillMinimalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Skill
        fields = ['id','name']



class ProjectSerializer(serializers.ModelSerializer):

    # Note: Only skill ids & names are enough for the list of projects, instead of the entire object of skillset. Hence it will reduce the bandwidth. And as the `GET` request is the public API endpoint, reducing bandwidth consumtion is a crucial enhancement in performance.

    # Tips: but to mitigate the `N+1 Query` issue, inside it's associated View (`Projects`) class, while making the query to the parent-table, use the `prefetch_related()` ORM method.

    # Note: Returns the primary keys (`id`) of skills associated with each projects; Since it's an M2M field, thus defining `many=True` is mandatory; This field definition is required here to execute POST, PUT, PATCH, DELETE method

    # Note: This field is used in both One-To-Many & Many-To-Many fields for serialization
    skill = serializers.PrimaryKeyRelatedField(
        queryset = Skill.objects.all(),
        many = True
    )

    class Meta:
        model = Project
        fields = ['title', 'slug', 'skill', 'summary', 'description', 'cover_image', 'category', 'live_url', 'github_url', 'is_featured', 'completed_date', 'display_order']

    # Only executes on `GET` request
    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Since `SkillMinimalSerializer` returns a `ListSerializer` class object, thus I invoked the `data` attribute on the serializer class, in order to assign the id & name of skill as objects in the `skill` field of each `Project` record.
        representation['skill'] = SkillMinimalSerializer(instance=instance.skill.all(), many=True).data
        
        return representation

    # The skill is expected to come as [2,3,6,9], but if the API recieves a multipart/form-data rather than a JSON formatted data, then it beacomes a querydict with weird behavior like wrapping the list of integers as a raw string like "2,3,6,9" or ["2,3,6,9"]. We should intercept the incoming data stream & convert the string of integer (PK) values into a native Python list of integer values by using the `to_internal_value()` method.

    # It's the best gatekeeping/translation hook in this scenario provided by DRF. If the data is messy or formatted incorrectly then utilizing this method is a best practice to transform/format any messy data or mismatched data types. 

    # In Django REST Framework (DRF), the to_internal_value() method is the entryway for deserialization and data validation.

    def to_internal_value(self, data):
        # Check if the data contains the `_mutable` attribute within itself; then consider it a querydict which is usually sent by the multipart/form-data or any frontend framework like axios/form-data API
        if hasattr(data, '_mutable'):
            data = data.copy()  # Making a shallow copy toggles the mutability of the object

            # Check if 'skill' key exists in the data obejct
            if 'skill' in data:
                skill_data = data['skill']

                # If skill-data comes in as '2,3,6,9' then handle it as string of IDs
                if isinstance(skill_data, str):
                    data.setlist('skill', [int(x.strip()) for x in skill_data.split(',') if x.strip()])

                # TODO: If skill data comes in as ['2','3','6','9'], then handle it as list of string element                
        
        return super().to_internal_value(data)