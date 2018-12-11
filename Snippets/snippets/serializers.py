from rest_framework import serializers

from snippets.models import LANGUAGE_CHOICES, STYLE_CHOICES, Snippet


# Creating a Serializer class
# class SnippetSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     title = serializers.CharField(required=False, allow_blank=True, max_length=100)
#     code = serializers.CharField(style={'base_template': 'textarea.html'})
#     linenos = serializers.BooleanField(required=False)
#     language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
#     style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')
#
#     def create(self, validated_data):
#         return Snippet.objects.create(**validated_data)
#
#     def update(self, snippet_instance, validated_data):
#         snippet_instance.title = validated_data.get('title', snippet_instance.title)
#         snippet_instance.code = validated_data.get('code', snippet_instance.code)
#         snippet_instance.linenos = validated_data.get('linenos', snippet_instance.linenos)
#         snippet_instance.language = validated_data.get('language', snippet_instance.language)
#         snippet_instance.style = validated_data.get('style', snippet_instance.style)
#         snippet_instance.save()
#         return snippet_instance


# Let's look at refactoring our serializer using the ModelSerializer class.
class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = ('id', 'title', 'code', 'linenos', 'language', 'style')
