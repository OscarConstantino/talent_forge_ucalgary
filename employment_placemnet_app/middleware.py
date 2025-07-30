class CSPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        csp_policy = (
            "default-src 'self';"
            "script-src 'self' https://code.jquery.com https://stackpath.bootstrapcdn.com https://cdn.jsdelivr.net https://cdnjs.cloudflare.com;"
            "style-src 'self' 'unsafe-inline' https://stackpath.bootstrapcdn.com https://fonts.googleapis.com;"
            "img-src 'self' data:;"
            "font-src 'self' https://fonts.gstatic.com;"
            "connect-src 'self';"
            "frame-ancestors 'self';"
            "form-action 'self';" # Add this for forms
        )
        response['Content-Security-Policy'] = csp_policy
        return response