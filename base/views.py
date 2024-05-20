from django.shortcuts import redirect, render, get_object_or_404
from django.conf import settings
import random, string, json, copy
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.db.models import Q
from django.http import HttpResponseBadRequest
from .models import User, Guion, GuionHistorial
from .forms import GuionForm
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.utils import timezone


# Create your views here.
def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username, password=password)
        except User.DoesNotExist:
            user = None

        if user is not None:
            request.session["user_id"] = user.id
            return redirect("dashboard")
        else:
            error_message = "Usuario o contraseña incorrectos!"
            return render(request, "login.html", {"error_message": error_message})

    return render(request, "login.html")


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        role = request.POST.get("role")

        if password == confirm_password:
            User.objects.create(
                username=username, email=email, password=password, role=role
            )
            return redirect("login")
        else:
            error_message = "Las contraseñas no coinciden!"
            return render(request, "register.html", {"error_message": error_message})

    return render(request, "register.html")


def dashboard(request):
    id = request.session.get("user_id")
    if id is not None:
        try:
            data = User.objects.get(id=id)
            guiones = Guion.objects.all()
            return render(request, "dashboard.html", {"data": data, "guiones": guiones})
        except User.DoesNotExist:
            del request.session["user_id"]
    return redirect("login")


def logout(request):
    request.session.clear()

    return redirect("login")


def crear_guion(request):
    if request.method == "POST":
        form = GuionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("dashboard")
    else:
        form = GuionForm()

    return render(request, "crear_guion.html", {"form": form})


def ver_guiones(request):
    guiones = Guion.objects.all()
    return render(request, "ver_guiones.html", {"guiones": guiones})


def lista_guion_historial(request):
    guiones = Guion.objects.all()
    return render(request, "lista_guion_historial.html", {"guiones": guiones})


def lista_guiones(request):
    guiones = Guion.objects.all()
    return render(request, "lista_guiones.html", {"guiones": guiones})


def detalles_guion(request, guion_id):
    guion = get_object_or_404(Guion, pk=guion_id)
    return render(request, "detalles_guion.html", {"guion": guion})


def generar_pdf(request, guion_id):
    guion = get_object_or_404(Guion, pk=guion_id)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{guion.titulo}.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    p.drawString(100, height - 100, f"Título: {guion.titulo}")
    p.drawString(100, height - 120, f"Género: {guion.genero}")
    p.drawString(100, height - 140, f"Pose de los Actores: {guion.pose_actores.gesto}")
    p.drawString(
        100, height - 160, f"Ubicación de los Actores: {guion.ubicacion_actores}"
    )
    p.drawString(100, height - 180, "Diálogos:")
    p.drawString(100, height - 200, guion.dialogos)

    p.showPage()
    p.save()
    return response


def lista_guion_historial(request):
    guiones = Guion.objects.all()
    return render(request, "lista_guion_historial.html", {"guiones": guiones})


def editar_guion(request, guion_id):
    guion = get_object_or_404(Guion, pk=guion_id)
    if request.method == "POST":

        GuionHistorial.objects.create(
            titulo=guion.titulo,
            genero=guion.genero,
            ubicacion_actores=guion.ubicacion_actores,
            pose_actores=guion.pose_actores,
            dialogos=guion.dialogos,
            guion=guion,
        )

        form = GuionForm(request.POST, instance=guion)
        if form.is_valid():
            guion = form.save()

            return redirect("lista_guiones")
    else:
        form = GuionForm(instance=guion)
    return render(request, "editar_guion.html", {"form": form, "guion": guion})


def historial_guion(request, guion_id):
    guion = get_object_or_404(Guion, pk=guion_id)
    ultimo_cambio = (
        GuionHistorial.objects.filter(guion=guion).order_by("-fecha").first()
    )

    cambios = []
    if ultimo_cambio:
        cambio_dict = {}
        cambio_dict["fecha"] = ultimo_cambio.fecha
        cambio_dict["cambios"] = []

        cambio_dict["cambios"].append(
            {
                "campo": "Título",
                "valor_anterior": ultimo_cambio.titulo,
                "nuevo_valor": guion.titulo,
            }
        )
        cambio_dict["cambios"].append(
            {
                "campo": "Género",
                "valor_anterior": ultimo_cambio.genero,
                "nuevo_valor": guion.genero,
            }
        )
        cambio_dict["cambios"].append(
            {
                "campo": "Ubicación Actores",
                "valor_anterior": ultimo_cambio.ubicacion_actores,
                "nuevo_valor": guion.ubicacion_actores,
            }
        )
        cambio_dict["cambios"].append(
            {
                "campo": "Pose Actores",
                "valor_anterior": (
                    ultimo_cambio.pose_actores.gesto
                    if ultimo_cambio.pose_actores
                    else None
                ),
                "nuevo_valor": guion.pose_actores.gesto if guion.pose_actores else None,
            }
        )
        cambio_dict["cambios"].append(
            {
                "campo": "Diálogos",
                "valor_anterior": ultimo_cambio.dialogos,
                "nuevo_valor": guion.dialogos,
            }
        )

        cambios.append(cambio_dict)

    return render(request, "historial_guion.html", {"guion": guion, "cambios": cambios})
