from django.shortcuts import redirect
from django.urls import reverse


class FirstLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if (request.user.is_authenticated and
                not request.user.profile.setup_complete and
                request.path != reverse('profile_setup')):
            return redirect('profile_setup')

        return response