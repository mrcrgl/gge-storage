from django import forms


class CastlesByDistanceForm(forms.Form):

    castle = forms.ChoiceField(choices=[])
    distance = forms.DecimalField(decimal_places=1, localize=True)