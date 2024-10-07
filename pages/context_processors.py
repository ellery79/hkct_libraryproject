from infos.models import Info


def global_context(request):
    info = Info.objects.all().first()
    return {
        'info': info
    }
