#!/usr/bin/python
#coding:utf8
from flask import Flask, render_template, url_for, request, redirect, make_response, session, abort
import MySQLdb
from flask import jsonify
from config import *
from function import *
import plotly.plotly as py  #easy_install plotly
from xml.sax.saxutils import quoteattr  # transfer ' to \' to escape error in mysql
from plotly.graph_objs import *
import string
import recommender

app = Flask(__name__)

py.sign_in('NoListen','ueixigh6gr') # API KEY

app.secret_key = '\xbc\x98B\x95\x0f\x1e\xcdr\xf8\xb0\xc1\x1a\xd3H\xdd\x86T\xff\xfdg\x80\x8b\x95\xf7'

conn = MySQLdb.connect(user=db_config["db_user"],passwd=db_config["db_passwd"],host=db_config["db_host"],db=db_config["db_name"],charset="utf8")

cursor = conn.cursor()

open_event_scheduler ="SET GLOBAL event_scheduler = 1;"
cursor.execute(open_event_scheduler)
conn.commit()
#open the event_scheduler to set time expiration event


@app.route('/', methods=['GET', 'POST'])
def index():
    islogin = session.get('islogin')
    user_id = session.get('user_id')
    message1 = session.get('message1')
    attendedGroupsList = []
    ownGroupsList = []
    messages = []
    find_content = []
    html = 'index.html'
    members = None
    leader = None

    if islogin == '1':
        html = 'index-log.html'
        #get groups
        User1 = User(user_id=user_id)
        username = User1.username
        role = User1.role
        if(role == 1):
            return redirect('/admin')
        attendedGroups, ownGroups = User1.get_groups()
        for i in ownGroups:
            ownGroupsList += [Group(i).get_data()]
        for i in attendedGroups:
            attendedGroupsList += [Group(i).get_data()]
        messages = []
        print "come to /"
        #if request.method == 'GET':
            #group_id=request.args.get('group_id')
            #if group_id and group_id.isdigit():
                #return redirect(url_for('groupDetail', group_id=group_id))
        if request.method == 'GET':
            content = request.args.get('search_content')
            if content:
                find_content = list(User1.get_groups_content_search(content))
                # tuple to list
                #tem = User1.get_groups_content_search(content)
                #for groupData in tem:
                    #find_content += [groupData]
                    # analogy is the best way to code
                


    else:
        username = u'请先登录'

    return render_template(html, user_id=user_id, username=username, islogin=islogin,\
                            message1=message1, messages=messages,\
                            attend=attendedGroupsList, own=ownGroupsList, \
                            members=members, leader=leader, find_content=find_content)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        session.clear()
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        response = make_response(redirect('/'))
        session['islogin'] = '0'
        if(username == '' or password == '' or email == ''):
            session['message1'] = 'fuck!'
            return response
        if password2 == password:
            user = User(name=username, email=email)
            if user.check_e() == 1 or user.check_u() == 1:
                session['message1'] = "User already existed!"
                return response
            result = user.register(password)
            #session['username'] = result['username']
            session['islogin'] = '1'
            session['user_id'] = result['user_id']
            #session['email'] = result['email']
            return response
        else:
            session['message1'] = "Password not the same!"
            return response
    else:
        return render_template('index.html')


@app.route('/_login/', methods=['GET', 'POST'])
def login():
    session.clear()
    email = str(request.args.get('email', 0, type=str))
    password = str(request.args.get('pw', 0, type=str))
    session['islogin'] = '0'
    # print "Come here!"
    if(email == '' or password == ''):
        status = 'Please enter email and password!'
        return jsonify(status=status)
    user = User(email=email)
    state = user.login(password)
    if state == 1:
        data = user.get_data_by_email()
        session['user_id'] = data['user_id']
        session['islogin'] = '1'
        status = 'success'
        return jsonify(status=status)
    if state == 0:
        status = "Wrong password!"
        return jsonify(status=status)
    if state == -1:
        status = "Email not used!"
        return jsonify(status=status)


@app.route('/logout')
def logout():
    session.clear()
    response = make_response(redirect('/'))
    return response


@app.route('/_check_users')
def check_users():
    username = request.args.get('username', 0, type=str)
    user = User(name=username)
    return jsonify(exist=user.check_u())


@app.route('/_check_email')
def check_email():
    email = request.args.get('email', 0, type=str)
    user = User(email=email)
    return jsonify(exist=user.check_e())

#Keep!!!!!
@app.route('/_quit_group')
def quit_group():
    user_id = session.get('user_id')
    group_id = str(request.args.get('group_id', 0, type=str))
    # group = Group(group_id=group_id)
    user = User(user_id=user_id)
    status=user.quit_group(group_id=group_id)
    return jsonify(status=status)
#Keep!!!!!

#Keep!!!!!
@app.route('/_delete_group')
def deleteGroup():
    user_id = session.get('user_id')
    group_id = str(request.args.get('group_id', 0, type=int))
    print "user_id:", session
    user = User(user_id=user_id)
    return jsonify(success=user.delete_group(group_id))
#Keep!!!!!

@app.route('/group/')
def myGroups():
    return make_response(redirect('/'))

@app.errorhandler(404)
def page_not_found(error):
    user_id = session.get('user_id')
    islogin = session.get('islogin')
    if islogin == '1':
        user = User(user_id=user_id)
        username = user.username
    else:
        username = u'请先登录'
    return render_template('page_not_found.html', user_id=user_id, islogin=islogin, username=username), 404

#keep!
@app.route('/group/gp<int:group_id>')
def groupDetail(group_id):
    is_login = session.get('islogin')
    if(is_login == '0'):                       #please login first!
        return make_response(redirect('/'))
    user_id = session.get('user_id')
    user = User(user_id=user_id)
    if(user.check_id() == 0):                #user not exist?
        session.clear()
        return make_response(redirect('/'))
    user_data = user.get_data_by_id()
    #code above checks user data
    group = Group(group_id)
    if(group.exist_group()):
        group_data = group.get_data()
        #group_data['leader_name'] = User(user_id=group.leader_id).username

        #discussions = group.get_discussions()
        discussions = []
        #votes_list_voting = group.get_votes_voting()
        votes_list_voting = []
        #votes_list_end = group.get_votes_expired()
        votes_list_end = []
        bulletin = group.get_bulletin()
        #members = group.get_members()
        #news = group.get_news(user_id)
        news = []
        memberNames=[]
        role = '0'
        #for member in members:
            #if str(member['member_id']) != str(group.leader_id):
                #user=User(user_id=member['member_id'])
                #memberNames+=[user.username]

        #if {'member_id': user_id} in members :
            #role = '1'              #member
        #if str(user_id) == str(group.leader_id):
            #role = '2'              #leader

        return render_template('group-id.html', group_id=group_id, bulletin=bulletin,\
                                group_data=group_data, discussions=discussions,\
                                votes_list_voting=votes_list_voting, newsList=news,\
                                votes_list_end=votes_list_end,username=user_data['username'],\
                                memberNames=memberNames,memberNum=len(memberNames),user_id=user_id, role=role)
    abort(404)
                           #non-exist
#keep!!

#Keep!!
@app.route('/_create_bulletin/<int:group_id>')
def create_bulletin(group_id):
    title = request.args.get('title')
    text = request.args.get('text')
    user_id = session.get('user_id')
    group = Group(group_id)
    jsonify_return = jsonify(status=group.create_bulletin(user_id, title, text))
    recommender.create_rec_list()
    return jsonify_return
#Keep!

#Keep!
@app.route('/_delete_bulletin')
def delete_bulletin():
    bulletin_id = request.args.get('bulletin_id')
    print bulletin_id
    user_id = session.get('user_id')
    user = User(user_id=user_id)
    return jsonify(status=user.delete_bulletin(bulletin_id))
#keep!
if __name__ == '__main__':
    app.run(debug=True, host=HOST, port=PORT)
    