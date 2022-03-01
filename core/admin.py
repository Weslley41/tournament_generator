from django.contrib import admin

from .models import Tournament, Team, Battle


class TournamentAdmin(admin.ModelAdmin):
	list_display = ('name',)


class TeamAdmin(admin.ModelAdmin):
	list_display = ('name', 'tournament')


class BattleAdmin(admin.ModelAdmin):
	list_display = ('tournament', 'round', 'game', 'team_1', 'team_2')


admin.site.register(Tournament, TournamentAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Battle, BattleAdmin)
