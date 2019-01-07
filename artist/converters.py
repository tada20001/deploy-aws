from django.urls.converters import StringConverter

class SlugUnicodeConverter(StringConverter):
    regex = r"[-\w]+"
