from django.urls import path
from . import views

urlpatterns = [
    path("", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("dashboard/logout/", views.logout, name="logout"),
    path("crear_guion/", views.crear_guion, name="crear_guion"),
    path("ver_guiones/", views.ver_guiones, name="ver_guiones"),
    path("detalles_guion/<int:guion_id>/", views.detalles_guion, name="detalles_guion"),
    path("generar_pdf/<int:guion_id>/", views.generar_pdf, name="generar_pdf"),
    path("lista_guiones/", views.lista_guiones, name="lista_guiones"),
    path("guiones/<int:guion_id>/editar/", views.editar_guion, name="editar_guion"),
    path(
        "guiones/<int:guion_id>/historial/",
        views.historial_guion,
        name="historial_guion",
    ),
    path(
        "lista_guion_historial/",
        views.lista_guion_historial,
        name="lista_guion_historial",
    ),
]
