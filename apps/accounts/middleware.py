from django.shortcuts import redirect
from django.urls import reverse


class ForcePasswordChangeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and getattr(request.user, 'must_change_password', False):
            current_path = request.path
            allowed_paths = {
                reverse('accounts:change_password'),
                reverse('accounts:logout'),
                reverse('accounts:login'),
            }
            if not (
                current_path in allowed_paths
                or current_path.startswith('/static/')
                or current_path.startswith('/media/')
            ):
                return redirect('accounts:change_password')
        return self.get_response(request)
