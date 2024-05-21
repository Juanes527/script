import random
import json
from django import forms
from .models import Guion, Pose


class GuionForm(forms.ModelForm):
    ubicacion_x = forms.FloatField(label="Ubicación X")
    ubicacion_y = forms.FloatField(label="Ubicación Y")
    ubicacion_z = forms.FloatField(label="Ubicación Z")
    rotacion_x = forms.FloatField(label="Rotación X", required=False)
    rotacion_y = forms.FloatField(label="Rotación Y", required=False)
    rotacion_z = forms.FloatField(label="Rotación Z", required=False)

    class Meta:
        model = Guion
        fields = [
            "titulo",
            "genero",
            "pose_actores",
            "dialogos",
            "ubicacion_x",
            "ubicacion_y",
            "ubicacion_z",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.ubicacion_actores:
            ubicacion = json.loads(self.instance.ubicacion_actores)
            self.initial["ubicacion_x"] = ubicacion.get("x", 0)
            self.initial["ubicacion_y"] = ubicacion.get("y", 0)
            self.initial["ubicacion_z"] = ubicacion.get("z", 0)
            self.initial["rotacion_x"] = ubicacion.get("rotacion_x", 0)
            self.initial["rotacion_y"] = ubicacion.get("rotacion_y", 0)
            self.initial["rotacion_z"] = ubicacion.get("rotacion_z", 0)
        else:
            self.initial["ubicacion_x"] = round(random.uniform(0, 10), 2)
            self.initial["ubicacion_y"] = round(random.uniform(0, 10), 2)
            self.initial["ubicacion_z"] = round(random.uniform(0, 10), 2)
            self.initial["rotacion_x"] = round(random.uniform(0, 360))
            self.initial["rotacion_y"] = round(random.uniform(0, 360))
            self.initial["rotacion_z"] = round(random.uniform(0, 360))

        # Add Bootstrap classes to form fields
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
        self.fields["dialogos"].widget.attrs.update(
            {"rows": "5"}
        )  # Adjust the dialog field size

    def save(self, commit=True):
        guion = super().save(commit=False)
        ubicacion_x = self.cleaned_data["ubicacion_x"]
        ubicacion_y = self.cleaned_data["ubicacion_y"]
        ubicacion_z = self.cleaned_data["ubicacion_z"]

        ubicacion_aleatoria = {
            "x": round(ubicacion_x),
            "y": round(ubicacion_y),
            "z": round(ubicacion_z),
            "rotacion_x": self.cleaned_data.get("rotacion_x", 0),
            "rotacion_y": self.cleaned_data.get("rotacion_y", 0),
            "rotacion_z": self.cleaned_data.get("rotacion_z", 0),
        }
        guion.ubicacion_actores = json.dumps(ubicacion_aleatoria)

        if commit:
            guion.save()

        return guion
