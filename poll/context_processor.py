
from poll.models import Questions


def polls_count(request):
    count = Questions.objects.count()
    return {'polls_count':count}
