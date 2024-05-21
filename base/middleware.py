from django.http import HttpResponseForbidden


class RoleBasedAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if (
            request.path.startswith("/crear_guion/")
            or request.path.startswith("/lista_guion_historial/")
            or request.path.startswith("/lista_guiones/")
        ) and request.session.get("role") != "guionista":
            return HttpResponseForbidden(
                "No tienes permisos para ingresar a esta página."
            )
        return response
