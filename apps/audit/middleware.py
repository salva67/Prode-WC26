from .models import AuditLog

class RequestAuditMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.path.startswith("/static/") or request.path.startswith("/media/"):
            return response
        user = request.user if getattr(request, "user", None) and request.user.is_authenticated else None
        AuditLog.objects.create(
            actor=user,
            method=request.method,
            path=request.path[:255],
            status_code=getattr(response, "status_code", 200),
            meta={"htmx": request.headers.get("HX-Request") == "true"},
        )
        return response
