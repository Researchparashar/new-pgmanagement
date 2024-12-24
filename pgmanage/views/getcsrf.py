from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie

@ensure_csrf_cookie
def get_csrf_token(request):
    # This will ensure the CSRF cookie is set and return the token to the frontend
    csrf_token = get_token(request)
    
    # Return the CSRF token with a status
    return JsonResponse({'csrfToken': csrf_token, 'status': 'success'})
