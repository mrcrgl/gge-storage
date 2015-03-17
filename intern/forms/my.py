from django import forms
from gge_proxy_manager.models import Unit, LogisticJob, Castle, Alliance
from pushover.models import Client, Notify, MESSAGE_PRIORITY
import re


class PushoverClientForm(forms.ModelForm):

    class Meta:
        model = Client


class PushoverNotificationForm(forms.Form):
    RETRY = (
        (30, '30 Sek.'),
        (60, '60 Sek.'),
        (120, '2 Min.'),
        (300, '5 Min.'),
    )
    EXPIRE = (
        (60, 'nach 1 Min.'),
        (5*60, 'nach 5 Min.'),
        (10*60, 'nach 10 Min.'),
        (15*60, 'nach 15 Min.'),
    )

    match_alliance = forms.ModelChoiceField(queryset=Alliance.objects.all(), required=False)
    match_my_players = forms.BooleanField(required=False)
    priority = forms.ChoiceField(choices=MESSAGE_PRIORITY, required=True)
    retry = forms.ChoiceField(choices=RETRY, label='Intervall', help_text='Bei Prio=Emergency wird im angegebenen Intervall geklingelt bis man bestaetigt.', required=False)
    expire = forms.ChoiceField(choices=EXPIRE, label='Verfall', help_text='Ende des obigen Intervalls wenn man nicht reagiert.', required=False)

    class Meta:
        model = Notify

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(PushoverNotificationForm, self).__init__(*args, **kwargs)

        if user:
            self.fields['match_alliance'].queryset = Alliance.objects.filter(players__user=user).distinct()


class MyProductionJobForm(forms.Form):

    castle = forms.ModelChoiceField(queryset=Castle.objects.all(), required=True)
    unit = forms.ModelChoiceField(queryset=Unit.objects.all(), required=True)
    valid_until = forms.IntegerField(required=False, help_text="Max. Menge des Werkzeugs (optional)")
    gold_limit = forms.IntegerField(required=False)
    wood_limit = forms.IntegerField(required=False)
    stone_limit = forms.IntegerField(required=False)
    is_active = forms.BooleanField(required=False)
    burst_mode = forms.BooleanField(required=False, help_text="Ignoriert alle Limits und verringert das Abfrageintervall.")

    def __init__(self, *args, **kwargs):
        player = kwargs.pop('player', None)
        unit_type = kwargs.pop('unit_type', None)
        super(MyProductionJobForm, self).__init__(*args, **kwargs)

        if player:
            self.fields['castle'].queryset = Castle.objects.filter(player=player, type__in=Castle.TYPE_WITH_WARRIORS).order_by('kingdom', 'type', 'resource_type')
            self.fields['unit'].queryset = Unit.objects.filter(game=player.game, type=unit_type).order_by('gge_id')


class MyRecruitmentJobForm(forms.Form):

    castle = forms.ModelChoiceField(queryset=Castle.objects.all(), required=True)
    unit = forms.ModelChoiceField(queryset=Unit.objects.all(), required=True)
    valid_until = forms.IntegerField(required=False, help_text="Max. Menge der Einheit (optional)")
    food_balance_limit = forms.IntegerField(required=False, help_text="Min. Futter-Bilanz (optional) z.B. -50 oder 300 (leer = min. +/-0)")
    gold_limit = forms.IntegerField(required=False)
    wood_limit = forms.IntegerField(required=False)
    stone_limit = forms.IntegerField(required=False)
    is_active = forms.BooleanField(required=False)
    burst_mode = forms.BooleanField(required=False, help_text="Ignoriert alle Limits und verringert das Abfrageintervall. Gut bei Feste feiern.")

    def __init__(self, *args, **kwargs):
        player = kwargs.pop('player', None)
        unit_type = kwargs.pop('unit_type', None)
        super(MyRecruitmentJobForm, self).__init__(*args, **kwargs)

        if player:
            self.fields['castle'].queryset = Castle.objects.filter(player=player, type__in=Castle.TYPE_WITH_WARRIORS).order_by('kingdom', 'type', 'resource_type')
            self.fields['unit'].queryset = Unit.objects.filter(game=player.game, type=unit_type).order_by('gge_id')


class MyLogisticJobForm(forms.Form):

    castle = forms.ModelChoiceField(queryset=Castle.objects.all(), required=True)
    receiver_name = forms.CharField(required=True)
    speed = forms.ChoiceField(choices=LogisticJob.SPEED, help_text="Vorsicht, nicht vollends getestet - teils unschluessig.")
    resource = forms.ChoiceField(choices=LogisticJob.RESOURCE)
    resource_limit = forms.IntegerField()
    gold_limit = forms.IntegerField(required=False)
    lock_for = forms.ChoiceField(choices=LogisticJob.LOCK_FOR, help_text="Sperrzeit, wie oft der Job abgefragt werden darf.")
    is_active = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        player = kwargs.pop('player', None)
        super(MyLogisticJobForm, self).__init__(*args, **kwargs)

        self._player = player

        if player:
            self.fields['castle'].queryset = Castle.objects.filter(player=player, type__in=Castle.TYPE_WITH_WARRIORS).order_by('kingdom', 'type', 'resource_type')

    def clean_receiver(self):
        receiver_name = self.cleaned_data.get('receiver_name')

        match = re.search(r'\[(\d+)\]', receiver_name)
        if not match:
            raise forms.ValidationError("Invalid receiver")

        pk = int(match.group(1))

        try:
            receiver = Castle.objects.get(game=self._player.game, pk=pk)
        except Castle.DoesNotExist:
            raise forms.ValidationError("Invalid receiver")

        return receiver

    def clean_receiver_name(self):
        castle = self.cleaned_data.get('castle')
        receiver_name = self.cleaned_data.get('receiver_name')

        match = re.search(r'\[(\d+)\]', receiver_name)
        if not match:
            raise forms.ValidationError("Invalid receiver")

        pk = int(match.group(1))

        try:
            receiver = Castle.objects.get(game=self._player.game, pk=pk)
        except Castle.DoesNotExist:
            raise forms.ValidationError("Invalid receiver")

        if isinstance(castle, Castle) and isinstance(receiver, Castle):
            if castle.kingdom_id != receiver.kingdom_id:
                raise forms.ValidationError("Receiver is in another Kingdom.")

        return receiver_name