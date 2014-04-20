from .forms import SubscribeForm


def subscribe_form(request):
    return {'subscribe_form': SubscribeForm()}
