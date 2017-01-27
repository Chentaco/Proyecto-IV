from django import forms
from teams.models import Team, Jugador

class TeamForm(forms.ModelForm):
    nombre = forms.CharField(max_length=30, help_text="Introduce el nombre del equipo.")
    ciudad = forms.CharField(max_length=30, help_text="Introduce la ciudad del equipo.")
    visitas = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Team
        fields = ('nombre','ciudad')

class JugadorForm(forms.ModelForm):
    nick = forms.CharField(max_length=40, help_text="Nick del jugador.")
    name = forms.CharField(max_length=60, help_text="Nombre del jugador.")

    class Meta:
        # Provide an association between the ModelForm and a model
        model = Jugador

        # What fields do we want to include in our form?
        # This way we don't need every field in the model present.
        # Some fields may allow NULL values, so we may not want to include them...
        # Here, we are hiding the foreign key.
        # we can either exclude the category field from the form,
        exclude = ('team','slug')
        #or specify the fields to include (i.e. not include the category field)
        #fields = ('title', 'url', 'views')             
