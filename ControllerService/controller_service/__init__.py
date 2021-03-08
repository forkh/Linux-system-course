import json
from flask import Flask, jsonify
from flask_restful import reqparse, Resource, Api
import sqlite3
import sys

app = Flask(__name__)
api = Api(app)

#TIMER_FILEPATH = './timers.json'
TIMER_FILEPATH = './timers.db'

#TIMERS = dict()

parser = reqparse.RequestParser()
parser.add_argument('alias')
parser.add_argument('uuid')
parser.add_argument('is_online')
parser.add_argument('tid')
parser.add_argument('time')
parser.add_argument('date')
parser.add_argument('status')
parser.add_argument('comment')
parser.add_argument('deletable')

def sqlite_query(sql, tuple_args):
    conn = sqlite3.connect(TIMER_FILEPATH)
    conn.cursor().execute(sql, tuple_args)
    conn.commit()
    conn.close()
    return None

class Controller:
    timers = dict()
    def __init__(self):
        self.timer_filepath = TIMER_FILEPATH
        #with open(TIMER_FILEPATH, 'r') as fh:
        #    self.timers = json.loads(fh.read())
        #print(self.timers)

    def get_timers(self):
        conn = sqlite3.connect(TIMER_FILEPATH)
        c = conn.cursor()
        c.execute("SELECT devices.alias, uuid, is_online, tid, time, date, status, comment, deletable FROM devices INNER JOIN timers on timers.alias = devices.alias")
        #c.execute("SELECT devices.alias, uuid, is_online, tid, time, date, status FROM devices INNER JOIN timers on timers.alias = devices.alias")
        fetched_values = c.fetchall()
        conn.close()
        ret = dict()
        for tmpl in fetched_values:
            ret[tmpl[3]] = {'alias': tmpl[0], 'uuid': tmpl[1], 'is_online': tmpl[2], 'tid': tmpl[3], 'time': tmpl[4], 'date': tmpl[5], 'status': tmpl[6], 'comment': tmpl[7], 'deletable': tmpl[8]}
            #ret[tmpl[3]] = {'alias': tmpl[0], 'uuid': tmpl[1], 'is_online': tmpl[2], 'tid': tmpl[3], 'time': tmpl[4], 'date': tmpl[5], 'status': tmpl[6]}
        return ret

    def get_timer(self, alias):
        try:
            conn = sqlite3.connect(TIMER_FILEPATH)
            c = conn.cursor()
            t = (alias,)
            req = c.execute("SELECT devices.alias, uuid, is_online, tid, time, date, status, comment, deletable FROM devices INNER JOIN timers on timers.alias = devices.alias WHERE timers.alias=?", t)
            temporary_list = req.fetchall()[0]
            ret = dict()
            ret['alias']     = temporary_list[0]
            ret['uuid']      = temporary_list[1]
            ret['is_online'] = temporary_list[2]
            ret['tid']       = temporary_list[3]
            ret['time']      = temporary_list[4]
            ret['date']      = temporary_list[5]
            ret['status']    = temporary_list[6]
            ret['comment']   = temporary_list[7]
            ret['deletable'] = temporary_list[8]
            conn.close()
            return ret, 200
        except IndexError:
            return 404

    def create_timer(self, arguments):
        if arguments['date'] == '':
            date = '.'
        else:
            date = arguments['date']
        
        t = (arguments['alias'], arguments['time'], date, arguments['status'], arguments['comment'], arguments['deletable'])
        conn = sqlite3.connect(TIMER_FILEPATH)
        sql = "INSERT INTO timers (alias,time,date,status,comment,deletable) VALUES(?,?,?,?,?,?)"
        conn.cursor().execute(sql, t)
        conn.commit()
        conn.close()
        return 200

    def remove_timer(self, tid):
        t = (tid, )
        print(80 * '-')
        print(t)
        sys.stdout.flush()
        sql = "DELETE FROM timers WHERE tid = ?"
        sqlite_query(sql, t)

controller = Controller()

class GetTimer(Resource):
    def get(self, alias):
        return controller.get_timer(alias)

class GetTimers(Resource):
    def get(self):
        return controller.get_timers()

class CreateTimer(Resource):
    def post(self):
        args = parser.parse_args()
        return controller.create_timer(args)

class RemoveTimer(Resource):
    def get(self, tid):
        return controller.remove_timer(tid)

api.add_resource(GetTimer, '/alias/<alias>')
api.add_resource(GetTimers, '/timers')
api.add_resource(CreateTimer, '/create')
api.add_resource(RemoveTimer, '/remove/<tid>')
