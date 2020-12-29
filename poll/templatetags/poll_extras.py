from  django import template
from poll.models import Questions
register = template.Library()
def upper(value,n):
    """Converts String to all uppercases"""
    return value.upper()[0:n]

register.filter('upper_str',upper)

""" or we can use like decorator"""
# simple_tag(name) if we want to pass name otherthan func name else it wil take name as func name
@register.simple_tag
def recent_polls(n=5,**kwargs):
    """ Recent polls """
    name = kwargs.get('name','argument is not passed')
    print(name)
    questions =Questions.objects.all().order_by('-created_at')
    return questions[0:n]

