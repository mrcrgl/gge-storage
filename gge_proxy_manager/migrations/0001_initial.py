# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import gge_proxy_manager.models.alliance
import django.utils.timezone
from django.conf import settings
import gge_proxy_manager.models.economy


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountBalanceLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('gold', models.FloatField()),
                ('ruby', models.FloatField()),
                ('collected', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AccountCollectLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('gold', models.PositiveIntegerField()),
                ('ruby', models.PositiveIntegerField()),
                ('collected', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Alliance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('gge_id', models.PositiveIntegerField(db_index=True)),
                ('level', models.SmallIntegerField(default=0, blank=True)),
                ('fame', models.PositiveIntegerField(default=0)),
                ('info', models.TextField(default=None, null=True, blank=True)),
                ('description', models.TextField(default=None, null=True, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AllianceRelation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.PositiveSmallIntegerField(choices=[(1, 'Maybe war'), (2, 'NAP'), (3, 'BND')])),
                ('alliance_a', models.ForeignKey(related_name='relation_a', to='gge_proxy_manager.Alliance')),
                ('alliance_b', models.ForeignKey(related_name='relation_b', to='gge_proxy_manager.Alliance')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AttackAssignment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AttackLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.PositiveSmallIntegerField(choices=[(1, 'Angriff'), (2, 'Eroberung'), (3, 'Schattenangriff'), (4, 'Raubritter Angriff')])),
                ('message_id', models.PositiveIntegerField(unique=True, db_index=True)),
                ('count_warriors', models.PositiveIntegerField(default=None, null=True, blank=True)),
                ('count_tools', models.PositiveIntegerField(default=None, null=True, blank=True)),
                ('total_time', models.PositiveIntegerField()),
                ('weft', models.DateTimeField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AttackPlanning',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(default=None, max_length=5000, null=True, blank=True)),
                ('is_clarified', models.BooleanField(default=False)),
                ('planned_impact', models.DateTimeField(default=None, null=True, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AttackPlanTarget',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('attack_plan', models.ForeignKey(to='gge_proxy_manager.AttackPlanning')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Castle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.PositiveIntegerField(db_index=True, choices=[(0, '?'), (1, 'Hauptburg'), (2, '?'), (3, 'Hauptstadt'), (4, 'Aussenposten'), (5, '?'), (6, '?'), (7, '?'), (8, '?'), (9, '?'), (10, 'Rohstoffdorf'), (11, '?'), (12, 'Burg'), (13, '?'), (14, '?'), (15, '?'), (16, '?'), (17, '?'), (18, '?'), (19, '?'), (20, '?'), (21, '?'), (22, 'Handelsmetropole'), (23, 'Turm')])),
                ('resource_type', models.PositiveIntegerField(default=None, null=True, blank=True, choices=[(0, 'Wood'), (1, 'Stone'), (2, 'Food'), (3, 'Castle')])),
                ('kid', models.PositiveSmallIntegerField(choices=[(0, 'Green'), (1, '?'), (2, 'Ice'), (3, '?'), (4, '?'), (5, '?'), (6, '?'), (7, '?'), (8, '?')])),
                ('gge_id', models.PositiveIntegerField(db_index=True)),
                ('name', models.CharField(default=None, max_length=128, null=True, blank=True)),
                ('pos_x', models.PositiveIntegerField()),
                ('pos_y', models.PositiveIntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CastleEconomy',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('barrows', models.PositiveSmallIntegerField(default=0)),
                ('guards', models.PositiveSmallIntegerField(default=0)),
                ('citizen', models.PositiveSmallIntegerField(default=0)),
                ('stock_size', models.PositiveIntegerField(default=0)),
                ('public_order', models.IntegerField(default=0)),
                ('defence_points', models.PositiveSmallIntegerField(default=0)),
                ('wood_production', models.PositiveIntegerField(default=0)),
                ('wood_stock', models.PositiveIntegerField(default=0)),
                ('stone_production', models.PositiveIntegerField(default=0)),
                ('stone_stock', models.PositiveIntegerField(default=0)),
                ('cole_production', models.PositiveIntegerField(default=0)),
                ('cole_stock', models.PositiveIntegerField(default=0)),
                ('food_production', models.PositiveIntegerField(default=0)),
                ('food_stock', models.PositiveIntegerField(default=0)),
                ('food_consumption', models.FloatField(default=0)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('castle', models.OneToOneField(related_name='economy', to='gge_proxy_manager.Castle')),
            ],
            options={
            },
            bases=(models.Model, gge_proxy_manager.models.economy.EconomyMixin),
        ),
        migrations.CreateModel(
            name='CollectLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('wood', models.PositiveIntegerField(default=0)),
                ('stone', models.PositiveIntegerField(default=0)),
                ('food', models.PositiveIntegerField(default=0)),
                ('gold', models.PositiveIntegerField(default=0)),
                ('cole', models.PositiveIntegerField(default=0)),
                ('collected', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Confederation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('slug', models.SlugField(max_length=128)),
                ('logo', models.FileField(default=None, null=True, upload_to='confederation_logos/', blank=True)),
                ('description', models.TextField(default=None, null=True, blank=True)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128, db_index=True)),
                ('product_key', models.CharField(max_length=32)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Kingdom',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=None, max_length=128, null=True, blank=True)),
                ('kid', models.SmallIntegerField(db_index=True)),
                ('visual_key', models.CharField(default='-', max_length=8)),
                ('game', models.ForeignKey(default=None, blank=True, to='gge_proxy_manager.Game', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LogisticJob',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('speed', models.CharField(max_length=5, choices=[('-1', 'Keine Pferde'), ('1001', 'Gold Pferde (test)'), ('1004', 'Rubi Pferde 1 (test)'), ('1007', 'Rubi Pferde 2 (test)')])),
                ('is_active', models.BooleanField(default=True)),
                ('resource', models.CharField(max_length=6, choices=[('wood', 'Wood'), ('stone', 'Stone'), ('food', 'Food')])),
                ('gold_limit', models.PositiveIntegerField(default=None, null=True, blank=True)),
                ('resource_limit', models.PositiveIntegerField()),
                ('lock_for', models.PositiveIntegerField(default=2700, choices=[(900, '15 minutes'), (1800, '30 minutes'), (2700, '45 minutes'), (3600, '1 hour'), (10800, '3 hours'), (21600, '6 hours'), (32400, '9 hours'), (43200, '12 hours'), (64800, '18 hours'), (86400, '24 hours')])),
                ('locked_till', models.DateTimeField(default=django.utils.timezone.now, db_index=True)),
                ('castle', models.ForeignKey(related_name='outgoing_logistic_jobs', to='gge_proxy_manager.Castle')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LogisticLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('resource', models.CharField(max_length=6, choices=[('wood', 'Wood'), ('stone', 'Stone'), ('food', 'Food')])),
                ('amount', models.PositiveIntegerField(default=0)),
                ('sent', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('castle', models.ForeignKey(related_name='transports_sent', to='gge_proxy_manager.Castle')),
            ],
            options={
                'ordering': ['-sent'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MapExplorer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=True)),
                ('circle_started', models.DateTimeField(default=None, null=True, blank=True)),
                ('circle_ended', models.DateTimeField(default=None, null=True, blank=True)),
                ('lock_for', models.PositiveIntegerField(default=30)),
                ('area_x1', models.PositiveIntegerField()),
                ('area_x2', models.PositiveIntegerField()),
                ('area_y1', models.PositiveIntegerField()),
                ('area_y2', models.PositiveIntegerField()),
                ('screen_width', models.PositiveIntegerField()),
                ('screen_height', models.PositiveIntegerField()),
                ('current_x1', models.PositiveIntegerField(default=None, null=True, blank=True)),
                ('current_x2', models.PositiveIntegerField(default=None, null=True, blank=True)),
                ('current_y1', models.PositiveIntegerField(default=None, null=True, blank=True)),
                ('current_y2', models.PositiveIntegerField(default=None, null=True, blank=True)),
                ('lock_circle_for', models.PositiveIntegerField(default=10800, choices=[(3600, '1 hour'), (10800, '3 hours'), (21600, '6 hours'), (43200, '12 hours'), (86400, '24 hours')])),
                ('circle_locked_until', models.DateTimeField(default=django.utils.timezone.now, db_index=True)),
                ('kingdom', models.ForeignKey(to='gge_proxy_manager.Kingdom')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NonPlayerCastle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=128)),
                ('slug', models.SlugField(max_length=128)),
                ('level', models.PositiveSmallIntegerField()),
                ('fights_left', models.PositiveSmallIntegerField(default=1)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NonPlayerCastleAttackSuggestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('losses', models.CharField(default=None, max_length=255, null=True, blank=True)),
                ('status', models.PositiveSmallIntegerField(default=1, choices=[(1, 'akzeptiert')])),
                ('castle', models.ForeignKey(related_name='attack_suggestions', to='gge_proxy_manager.NonPlayerCastle')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NonPlayerCastleType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=128)),
                ('slug', models.SlugField(max_length=128)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('alliance_rank', models.PositiveSmallIntegerField(default=None, null=True, blank=True, choices=[(None, '(unbekannt)'), (0, 'Leader'), (1, 'General'), (2, 'Sergeant'), (3, 'Member'), (4, 'Rang 4'), (5, 'Rang 5'), (6, 'Rang 6'), (7, 'Rang 7'), (8, 'Rang 8')])),
                ('name', models.CharField(max_length=128)),
                ('gge_id', models.PositiveIntegerField(db_index=True)),
                ('level', models.SmallIntegerField(default=0)),
                ('experience', models.PositiveIntegerField(default=0)),
                ('honor', models.PositiveIntegerField(default=0)),
                ('fame', models.PositiveIntegerField(default=0)),
                ('success', models.PositiveIntegerField(default=0)),
                ('is_ruin', models.BooleanField(default=False, db_index=True)),
                ('dangerously', models.FloatField(default=0.0)),
                ('proxy_connected', models.DateTimeField(default=None, null=True, db_index=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('alliance', models.ForeignKey(related_name='players', default=None, blank=True, to='gge_proxy_manager.Alliance', null=True)),
                ('game', models.ForeignKey(default=None, blank=True, to='gge_proxy_manager.Game', null=True)),
                ('user', models.ForeignKey(related_name='players', default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model, gge_proxy_manager.models.alliance.AllianceRankMixin),
        ),
        migrations.CreateModel(
            name='PlayerAllianceHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('alliance_rank', models.PositiveSmallIntegerField(default=None, null=True, blank=True, choices=[(None, '(unbekannt)'), (0, 'Leader'), (1, 'General'), (2, 'Sergeant'), (3, 'Member'), (4, 'Rang 4'), (5, 'Rang 5'), (6, 'Rang 6'), (7, 'Rang 7'), (8, 'Rang 8')])),
                ('reached', models.DateTimeField(auto_now=True, db_index=True)),
                ('alliance', models.ForeignKey(related_name='player_history', default=None, blank=True, to='gge_proxy_manager.Alliance', null=True)),
                ('player', models.ForeignKey(related_name='alliance_history', to='gge_proxy_manager.Player')),
            ],
            options={
                'ordering': ['-reached'],
            },
            bases=(models.Model, gge_proxy_manager.models.alliance.AllianceRankMixin),
        ),
        migrations.CreateModel(
            name='PlayerEconomy',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ruby', models.PositiveIntegerField()),
                ('gold', models.PositiveIntegerField()),
                ('updated', models.DateTimeField(auto_now=True)),
                ('player', models.OneToOneField(related_name='economy', to='gge_proxy_manager.Player')),
            ],
            options={
            },
            bases=(models.Model, gge_proxy_manager.models.economy.EconomyMixin),
        ),
        migrations.CreateModel(
            name='PlayerHonorHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('honor', models.PositiveIntegerField(default=0)),
                ('reached', models.DateTimeField(auto_now=True, db_index=True)),
                ('player', models.ForeignKey(related_name='honor_history', to='gge_proxy_manager.Player')),
            ],
            options={
                'ordering': ['-reached'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PlayerLevelHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('level', models.PositiveSmallIntegerField(default=0)),
                ('reached', models.DateTimeField(auto_now=True, db_index=True)),
                ('player', models.ForeignKey(related_name='level_history', to='gge_proxy_manager.Player')),
            ],
            options={
                'ordering': ['-reached'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProductionJob',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('valid_until', models.PositiveIntegerField(default=None, help_text='Bis zu welcher Menge ist der Auftrag gueltig', null=True, blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('gold_limit', models.PositiveIntegerField(default=None, null=True, blank=True)),
                ('food_balance_limit', models.IntegerField(default=None, null=True, blank=True)),
                ('wood_limit', models.PositiveIntegerField(default=None, null=True, blank=True)),
                ('stone_limit', models.PositiveIntegerField(default=None, null=True, blank=True)),
                ('burst_mode', models.BooleanField(default=False, help_text='Ignoriert Nahrungsbilanz')),
                ('locked_till', models.DateTimeField(default=django.utils.timezone.now, db_index=True)),
                ('last_fault_reason', models.CharField(default=None, max_length=128, null=True)),
                ('last_fault_date', models.DateTimeField(default=None, null=True)),
                ('castle', models.ForeignKey(related_name='production_jobs', to='gge_proxy_manager.Castle')),
                ('player', models.ForeignKey(related_name='production_jobs', to='gge_proxy_manager.Player')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProductionLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.PositiveIntegerField(default=5)),
                ('produced', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('castle', models.ForeignKey(related_name='production_logs', to='gge_proxy_manager.Castle')),
                ('player', models.ForeignKey(related_name='production_logs', to='gge_proxy_manager.Player')),
            ],
            options={
                'ordering': ['-produced'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ResourceBalanceLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('wood', models.FloatField()),
                ('stone', models.FloatField()),
                ('food', models.FloatField()),
                ('cole', models.FloatField()),
                ('collected', models.DateTimeField(auto_now_add=True)),
                ('castle', models.ForeignKey(related_name='resource_balances', to='gge_proxy_manager.Castle')),
                ('player', models.ForeignKey(related_name='resource_balances', to='gge_proxy_manager.Player')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(default=None, max_length=128, null=True, blank=True)),
                ('gge_id', models.PositiveIntegerField(default=0, db_index=True)),
                ('type', models.CharField(default=None, max_length=16, null=True, blank=True, choices=[('soldier', 'Soldat'), ('tool', 'Werkzeug')])),
                ('value_type', models.CharField(default='absolute', max_length=16, choices=[('absolute', 'Absolut'), ('percentage', 'Prozentual')])),
                ('orientation', models.CharField(default=None, max_length=8, null=True, blank=True, choices=[('off', 'Offensiv'), ('deff', 'Defensiv')])),
                ('distance', models.CharField(default=None, max_length=8, null=True, blank=True, choices=[('close', 'Nah'), ('far', 'Fern')])),
                ('offence_close', models.IntegerField(default=0)),
                ('offence_far', models.IntegerField(default=0)),
                ('defence_close', models.IntegerField(default=0)),
                ('defence_far', models.IntegerField(default=0)),
                ('food_consumption', models.IntegerField(default=0)),
                ('booty_space', models.IntegerField(default=0)),
                ('travel_speed', models.IntegerField(default=0)),
                ('game', models.ForeignKey(related_name='units', to='gge_proxy_manager.Game')),
            ],
            options={
                'ordering': ['game', 'type', 'orientation', 'distance'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UnitFormation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NonPlayerCastleFormation',
            fields=[
                ('unitformation_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='gge_proxy_manager.UnitFormation')),
                ('castle', models.ForeignKey(related_name='formations', to='gge_proxy_manager.NonPlayerCastle')),
            ],
            options={
            },
            bases=('gge_proxy_manager.unitformation',),
        ),
        migrations.CreateModel(
            name='UnitList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=128, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UnitListRelation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.PositiveIntegerField(default=0)),
                ('list', models.ForeignKey(related_name='unit_relations', to='gge_proxy_manager.UnitList')),
                ('unit', models.ForeignKey(related_name='list_relations', to='gge_proxy_manager.Unit')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='unitlist',
            name='units',
            field=models.ManyToManyField(to='gge_proxy_manager.Unit', through='gge_proxy_manager.UnitListRelation'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='unitformation',
            name='center',
            field=models.ForeignKey(related_name='formations_on_center', default=None, blank=True, to='gge_proxy_manager.UnitList', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='unitformation',
            name='inner',
            field=models.ForeignKey(related_name='formations_on_inner', default=None, blank=True, to='gge_proxy_manager.UnitList', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='unitformation',
            name='left',
            field=models.ForeignKey(related_name='formations_on_left', default=None, blank=True, to='gge_proxy_manager.UnitList', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='unitformation',
            name='right',
            field=models.ForeignKey(related_name='formations_on_right', default=None, blank=True, to='gge_proxy_manager.UnitList', null=True),
            preserve_default=True,
        ),
        migrations.AlterIndexTogether(
            name='unit',
            index_together=set([('game', 'gge_id')]),
        ),
        migrations.AddField(
            model_name='productionlog',
            name='unit',
            field=models.ForeignKey(to='gge_proxy_manager.Unit'),
            preserve_default=True,
        ),
        migrations.AlterIndexTogether(
            name='productionlog',
            index_together=set([('castle', 'unit')]),
        ),
        migrations.AddField(
            model_name='productionjob',
            name='unit',
            field=models.ForeignKey(to='gge_proxy_manager.Unit'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='nonplayercastleattacksuggestion',
            name='unit_formation',
            field=models.OneToOneField(related_name='non_player_castle_attack_suggestion', to='gge_proxy_manager.UnitFormation'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='nonplayercastle',
            name='type',
            field=models.ForeignKey(related_name='non_player_castles', to='gge_proxy_manager.NonPlayerCastleType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='logisticlog',
            name='player',
            field=models.ForeignKey(related_name='transports_sent', to='gge_proxy_manager.Player'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='logisticlog',
            name='receiver',
            field=models.ForeignKey(related_name='transports_received', to='gge_proxy_manager.Castle'),
            preserve_default=True,
        ),
        migrations.AlterIndexTogether(
            name='logisticlog',
            index_together=set([('castle', 'receiver', 'resource')]),
        ),
        migrations.AddField(
            model_name='logisticjob',
            name='player',
            field=models.ForeignKey(related_name='logistic_jobs', to='gge_proxy_manager.Player'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='logisticjob',
            name='receiver',
            field=models.ForeignKey(related_name='incoming_logistic_jobs', to='gge_proxy_manager.Castle'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='collectlog',
            name='player',
            field=models.ForeignKey(related_name='resource_collect_logs', to='gge_proxy_manager.Player'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='castleeconomy',
            name='unit_list',
            field=models.OneToOneField(null=True, default=None, blank=True, to='gge_proxy_manager.UnitList'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='castle',
            name='game',
            field=models.ForeignKey(default=None, blank=True, to='gge_proxy_manager.Game', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='castle',
            name='kingdom',
            field=models.ForeignKey(default=None, blank=True, to='gge_proxy_manager.Kingdom', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='castle',
            name='player',
            field=models.ForeignKey(related_name='castles', default=None, blank=True, to='gge_proxy_manager.Player', null=True),
            preserve_default=True,
        ),
        migrations.AlterIndexTogether(
            name='castle',
            index_together=set([('kingdom', 'pos_x', 'pos_y')]),
        ),
        migrations.AddField(
            model_name='attackplantarget',
            name='player',
            field=models.ForeignKey(to='gge_proxy_manager.Player'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='attackplanning',
            name='creator',
            field=models.ForeignKey(related_name='planned_attacks', to='gge_proxy_manager.Player'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='attackplanning',
            name='targets',
            field=models.ManyToManyField(to='gge_proxy_manager.Player', through='gge_proxy_manager.AttackPlanTarget'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='attacklog',
            name='from_castle',
            field=models.ForeignKey(related_name='sent_attacks', default=None, blank=True, to='gge_proxy_manager.Castle', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='attacklog',
            name='from_player',
            field=models.ForeignKey(related_name='sent_attacks', default=None, blank=True, to='gge_proxy_manager.Player', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='attacklog',
            name='to_castle',
            field=models.ForeignKey(related_name='got_attacks', to='gge_proxy_manager.Castle'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='attacklog',
            name='to_player',
            field=models.ForeignKey(related_name='got_attacks', default=None, blank=True, to='gge_proxy_manager.Player', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='attackassignment',
            name='source_player',
            field=models.ForeignKey(related_name='attack_assignments', to='gge_proxy_manager.Player'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='attackassignment',
            name='to_target',
            field=models.ForeignKey(related_name='assignments', to='gge_proxy_manager.AttackPlanTarget'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='attackassignment',
            name='to_target_castle',
            field=models.ForeignKey(related_name='planned_attacks', to='gge_proxy_manager.Castle'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='alliance',
            name='confederation',
            field=models.ForeignKey(related_name='alliances', default=None, blank=True, to='gge_proxy_manager.Confederation', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='alliance',
            name='game',
            field=models.ForeignKey(default=None, blank=True, to='gge_proxy_manager.Game', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='alliance',
            name='related_a',
            field=models.ManyToManyField(related_name='related_b', through='gge_proxy_manager.AllianceRelation', to='gge_proxy_manager.Alliance'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='accountcollectlog',
            name='player',
            field=models.ForeignKey(related_name='collect_logs', to='gge_proxy_manager.Player'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='accountbalancelog',
            name='player',
            field=models.ForeignKey(related_name='balance_logs', to='gge_proxy_manager.Player'),
            preserve_default=True,
        ),
    ]
