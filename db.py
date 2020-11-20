import peewee as pw
from playhouse.sqlite_ext import JSONField
import datetime


db = pw.SqliteDatabase('clan_members.db')

class Player(pw.Model):
    tag = pw.CharField()
    firstTime = pw.DateTimeField()
    json = JSONField()
    class Meta:
        database = db

def handle_memberList(current_players):
    time_start = None
    time_now  = datetime.datetime.now()
    with db:
        for p in current_players:
            entry = Player.get_or_none(Player.tag == p['tag'])
            if not entry:
                entry = Player(tag=p['tag'], firstTime=time_now, json={})
                entry.save()
            p['firstTime'] = entry.firstTime
    for p in current_players:
        if time_start == None:
            time_start = p['firstTime']
            print("TIME START:::", time_start)
        if p['firstTime'] == time_start:
            p['delta'] = 'с начала отчета'
        else:
            p['delta'] = time_now - p['firstTime']


if __name__ == "__main__":
    print("test db")