from django import forms
from gge_proxy_manager.models import NonPlayerCastle


class NonPlayerCastleForm(forms.ModelForm):

    class Meta:
        model = NonPlayerCastle