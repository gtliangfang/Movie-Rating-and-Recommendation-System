#coding:utf-8-*-
import MySQLdb
from config import *
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User:
    def __init__(self, name='', email='', user_id=0):
        if(name=='' and email==''):
            self.user_id = user_id
            # print 'user_id:', user_id
            try:
                data = self.get_data_by_id()
                self.username = data['username']
                self.email = data['email']
                self.role = data['role'] #admin or user?
            except Exception, e:
                print 'initUser', e
        else:
            self.username = name
            self.email = email
            if self.check_e():
                data = self.get_data_by_email()
                # print data
                self.role = data['role']

    def get_data_by_id(self):
        #if(self.check_id()):
        #    return {}
        conn = MySQLdb.connect(host=db_config["db_host"],port=db_config["db_port"],user=db_config["db_user"],passwd=db_config["db_passwd"],db=db_config["db_name"],charset="utf8")
        cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        cursor.execute("select * from user where user_id='" + str(self.user_id) + "';")
        data = cursor.fetchall()
        conn.close()

        return data[0]

    def get_data_by_email(self):
        if not self.check_e():
            return {}
        conn = MySQLdb.connect(host=db_config["db_host"],port=db_config["db_port"],user=db_config["db_user"],passwd=db_config["db_passwd"],db=db_config["db_name"],charset="utf8")
        cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        cursor.execute("select * from user where email='" + self.email + "';")
        data = cursor.fetchall()
        conn.close()
        return data[0]

    def get_data_by_name(self):
        if not self.check_u():
            return {}
        conn = MySQLdb.connect(host=db_config["db_host"],port=db_config["db_port"],user=db_config["db_user"],passwd=db_config["db_passwd"],db=db_config["db_name"],charset="utf8")
        cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        sql = 'select * from user where user_id = %d;' % self.user_id
        cursor.execute(sql)
        data = cursor.fetchall()
        conn.close()
        return data[0]

    def get_messages(self):
        conn = MySQLdb.connect(host=db_config["db_host"],port=db_config["db_port"],user=db_config["db_user"],passwd=db_config["db_passwd"],db=db_config["db_name"],charset="utf8")
        cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        
        receiver = self.user_id
        sql = "select * from message \
               where receiver = %d and viewed = 0 \
               order by time desc;" % (receiver)
        cursor.execute(sql)
        data = cursor.fetchall()
        # print "message data is:", data
        conn.close()
        return data;

    def create_group(self, groupname, topic, desc,confirmMessage):
        conn=MySQLdb.connect(host=db_config["db_host"],port=db_config["db_port"],user=db_config["db_user"],passwd=db_config["db_passwd"],db=db_config["db_name"],charset="utf8")
        cursor=conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        groupname = groupname.encode('utf8')
        #判断是否存在
        cursor.execute("select name from groups where name='" + groupname + "';")
        exist=cursor.fetchall()
        if(exist):
            print 'failed to create group :', groupname
            return 'exist'

        cursor.execute("insert into groups(name,topic,description,confirmMessage,leader_id) values(%s,%s,%s,%s,%s);",\
            (groupname, topic,desc, confirmMessage, self.user_id))
        conn.commit()

        cursor.execute("select group_id from groups where name='"+groupname+"';")
        group_id=cursor.fetchone()['group_id']

        create_message = "Have a look at new bulletin(s) in Group %s!" % groupname
        sql = 'insert into message(type, group_id, receiver, content) \
               values(%d, %d, %d, "%s");' % (1, group_id, self.user_id, create_message)
        cursor.execute(sql)
        conn.commit()

        create_message = "Have a look at new discussion(s) in Group %s!" % groupname
        sql = 'insert into message(type, group_id, receiver, content) \
               values(%d, %d, %d, "%s");' % (3, group_id, self.user_id, create_message)
        cursor.execute(sql)
        conn.commit()

        create_message = "Have a look at new vote(s) in Group %s!" % groupname
        sql = 'insert into message(type, group_id, receiver, content) \
               values(%d, %d, %d, "%s");' % (2, group_id, self.user_id, create_message)
        cursor.execute(sql)
        conn.commit()

        cursor.execute("insert into groupMemberAssosiation(group_id,member_id) values(%s,%s);",(group_id,self.user_id))
        conn.commit()
        conn.close()
        print 'created group successfully:', groupname
        return 'success'

#Keep!
    def delete_group(self,group_id):
        group_id=str(group_id)
        conn=MySQLdb.connect(host=db_config["db_host"],port=db_config["db_port"],user=db_config["db_user"],passwd=db_config["db_passwd"],db=db_config["db_name"],charset="utf8")
        cursor=conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        try:
            cursor.execute("delete from bulletin where group_id='"+group_id+"' and user_id='"+str(self.user_id)+"';")
            conn.commit()
            conn.close()
            return True
        except Exception, e:
            print 'initUser', e
            return False
#keep!

#keep!
    def get_groups(self):
        conn=MySQLdb.connect(host=db_config["db_host"],port=db_config["db_port"],user=db_config["db_user"],passwd=db_config["db_passwd"],db=db_config["db_name"],charset="utf8")
        cursor=conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        #cursor.execute("select group_id from groupMemberAssosiation where member_id='"+str(self.user_id)+"';")
        # print "user_id is", self.user_id
        # attendedGroups=cursor.fetchall()
        cursor.execute("select group_id from bulletin where user_id='"+str(self.user_id)+"';")
        #rating history
        ownGroups=cursor.fetchall()
        #conn.close()
        attendedGroupsName = []
        ownGroupsName = []
        #for i in attendedGroups:
            #attendedGroupsName += [i['group_id']]
        for i in ownGroups:
            ownGroupsName += [i['group_id']]
        print ownGroupsName

        cursor.execute("select item_id from recommender where user_id='"+str(self.user_id)+"';")
        recId=cursor.fetchall()
        for i in recId:
            attendedGroupsName += [i['item_id']]
        print attendedGroupsName

        conn.close()
        # print ownGroups
        return attendedGroupsName, ownGroupsName
    #注意！！这里的返回值是所有的小组id组成的list，不是字典的list！！！
#keep!!

#new
    def get_groups_content_search(self, search_content):
        conn=MySQLdb.connect(host=db_config["db_host"],port=db_config["db_port"],user=db_config["db_user"],passwd=db_config["db_passwd"],db=db_config["db_name"],charset="utf8")
        cursor=conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        sql = "select * from groups where name like '%"+search_content+"%' or topic like '%"+search_content+"%' or description like '%"+search_content+"%';"
        cursor.execute(sql)
        data = cursor.fetchall()
        conn.close()
        return data
        # data is a tuple with many elements, data[i] is a {} dict
        # print is the only way to debug
#new


    def join_group(self, group_id, confirm):
        group_id=str(group_id)
        group = Group(group_id=group_id)
        conn = MySQLdb.connect(host=db_config["db_host"],port=db_config["db_port"],user=db_config["db_user"],passwd=db_config["db_passwd"],db=db_config["db_name"],charset="utf8")
        cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        if(group.exist_group()):
            cursor.execute("select member_id from groupMemberAssosiation where group_id='"+str(group_id)+"';")
            member_list = cursor.fetchall()
            if(str(self.user_id) in member_list):
                return 'joined'
            if(confirm == group.confirmMessage):

                create_message = "Have a look at new bulletin(s) in Group %s!" % group.name
                sql = 'insert into message(type, group_id, receiver, content) \
                       values(%d, %s, %d, "%s");' % (1, group_id, self.user_id, create_message)
                cursor.execute(sql)
                conn.commit()

                create_message = "Have a look at new discussion(s) in Group %s!" % group.name
                sql = 'insert into message(type, group_id, receiver, content) \
                       values(%d, %s, %d, "%s");' % (3, group_id, self.user_id, create_message)
                cursor.execute(sql)
                conn.commit()

                create_message = "Have a look at new vote(s) in Group %s!" % group.name
                sql = 'insert into message(type, group_id, receiver, content) \
                       values(%d, %s, %d, "%s");' % (2, group_id, self.user_id, create_message)
                cursor.execute(sql)
                conn.commit()

                cursor.execute("insert into groupMemberAssosiation(group_id,member_id) values(%s,%s) ;", (group_id, self.user_id) )
                conn.commit()
                conn.close()
                return 'success'
            else:
                conn.close()
                return 'fail'
        conn.close()
        return 'non-ex'

    def quit_group(self,group_id):
        group = Group(group_id = group_id)
        group_id=str(group_id)
        conn = MySQLdb.connect(host=db_config["db_host"],port=db_config["db_port"],user=db_config["db_user"],passwd=db_config["db_passwd"],db=db_config["db_name"],charset="utf8")
        cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        cursor.execute("select * from groupMemberAssosiation where member_id='"+str(self.user_id)+"' and group_id='"+group_id+"';")
        exist = cursor.fetchall()
        if(exist):

            quit_message = "The member %s quitted our group." % (self.username)
            sql = "insert into news(type, group_id, receiver, content)\
                   values(%d, %s, %s, '%s');" % (6, group_id, 0, quit_message)
            cursor.execute(sql)

            quit_message = "The member %s quitted your group %s." % (self.username, group.name)
            sql = "insert into message(type, group_id, receiver, content)\
                   values(%d, %s, %s, '%s');" % (8, group_id, group.leader_id, quit_message)
            cursor.execute(sql)

            cursor.execute("delete from message where receiver='"+str(self.user_id)+"' and group_id='"+group_id+"';")

            cursor.execute("delete from groupMemberAssosiation where member_id='"+str(self.user_id)+"' and group_id='"+group_id+"';")
            conn.commit()
            #whether he's leader
            cursor.execute("select name from groups where group_id='"+group_id+"' and leader_id='"+str(self.user_id)+"';")
            isLeader=cursor.fetchall()  
            if(isLeader):
                print "the user trying to quit is LEADER!"
                cursor.execute("delete from groups where group_id='"+group_id+"';")
                conn.commit()


            conn.close()
            print 'quit group successfully :',group_id
            return 1
        print 'failed to quit group :',group_id
        conn.close()
        return 0

    def search_group(self, group_id):
        group_id=str(group_id)
        conn=MySQLdb.connect(host=db_config["db_host"],port=db_config["db_port"],user=db_config["db_user"],passwd=db_config["db_passwd"],db=db_config["db_name"],charset="utf8")
        cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        #判断是否存在
        cursor.execute("select name from groups where group_id='"+group_id+"';")
        exist=cursor.fetchall()
        if(exist):
            Group1=Group(group_id)
            return Group1
        return None

    def kick_member(self,group_id,user_id):
        group_id=str(group_id)
        user_id=str(user_id)
        conn=MySQLdb.connect(host=db_config["db_host"],port=db_config["db_port"],user=db_config["db_user"],passwd=db_config["db_passwd"],db=db_config["db_name"],charset="utf8")
        cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        cursor.execute("select name from groups where group_id='%s' and leader_id='%s';"),(group_id,self.user_id)
        exist=cursor.fetchall()
        if(exist):
            cursor.execute("select * from groupMemberAssosiation where group_id='%s' and member_id='%s';"),(group_id,user_id)
            exist=cursor.fetchall()
            if(exist):

                user = User(user_id = user_id)
                delete_message = "Group member %s is removed from our group." % user.username
                sql = "insert into news(type, group_id, receiver, content)\
                       values(%d, %s, %s, '%s');" % (5, group_id, user_id, delete_message)
                cursor.execute(sql)

                delete_message = "The leader of group %s has removed you from the group." % exist.name
                sql = "insert into message(type, group_id, receiver, content)\
                       values(%d, %s, %s, '%s');" % (4, group_id, user_id, delete_message)
                cursor.execute(sql)

                sql = "delete from message where group_id = %s and receiver = %d;" % (group_id, user_id)
                cursor.execute(sql)

                cursor.execute("delete from groupMemberAssosiation where group_id='%s' and member_id='%s';"),(group_id,user_id)
                conn.commit()

                return True
            print "Cannot find user_id in the group"
            return False

        print "Not leader"
        return False

    def message_confirm(self,message_id):
        conn = MySQLdb.connect(host=db_config["db_host"],port=db_config["db_port"],user=db_config["db_user"],passwd=db_config["db_passwd"],db=db_config["db_name"],charset="utf8")
        cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        sql = "update message set viewed = 1 where message.message_id = %s;" % message_id
        cursor.execute(sql)
        conn.commit()
        conn.close()
        return True

    def check_u(self):
        conn = MySQLdb.connect(host=db_config["db_host"],port=db_config["db_port"],user=db_config["db_user"],passwd=db_config["db_passwd"],db=db_config["db_name"],charset="utf8")
        cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        cursor.execute("select * from user where username='" + unicode(self.username) + "';")
        exist = cursor.fetchall()
        if exist:
            return 1
        return 0

    def check_e(self):
        conn = MySQLdb.connect(host=db_config["db_host"],port=db_config["db_port"],user=db_config["db_user"],passwd=db_config["db_passwd"],db=db_config["db_name"],charset="utf8")
        cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        cursor.execute("select * from user where email='" + str(self.email) + "';")
        exist = cursor.fetchall()
        if exist:
            return 1
        return 0

    def check_id(self):
        conn = MySQLdb.connect(host=db_config["db_host"],port=db_config["db_port"],user=db_config["db_user"],passwd=db_config["db_passwd"],db=db_config["db_name"],charset="utf8")
        cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        cursor.execute("select * from user where user_id='" + str(self.user_id) + "';")
        exist = cursor.fetchall()
        if exist:
            return 1
        return 0

    def login(self, pw):
        conn = MySQLdb.connect(host=db_config["db_host"],port=db_config["db_port"],user=db_config["db_user"],passwd=db_config["db_passwd"],db=db_config["db_name"],charset="utf8")
        cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        cursor.execute("select * from user where email='" + str(self.email) + "';")
        exist = cursor.fetchall()
        print exist
        if exist:
            if exist[0]['password'] == pw:
                return 1    #匹配成功
            else:
                return 0    #密码错误
        return -1               #邮箱不存在

    def register(self, password):
        conn = MySQLdb.connect(host=db_config["db_host"],port=db_config["db_port"],user=db_config["db_user"],passwd=db_config["db_passwd"],db=db_config["db_name"],charset="utf8")
        cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        #password = generate_password_hash(password)
        password = password
        sql = 'insert into user(username, password, email) values("%s","%s","%s")' % (self.username, password, self.email)
        cursor.execute(sql)
        conn.commit()
        sql = 'select * from user where email="%s"' % self.email
        cursor.execute(sql)
        user = cursor.fetchone()

        #welcome_content = "welcome to our Grape system, %s!" % user['username']
        #sql = 'insert into message(type, group_id, receiver, content, viewed) \
               #values(%d, %d, %d, "%s",0);' % (0, 0, user['user_id'], welcome_content)
        #cursor.execute(sql)
        #conn.commit()

        conn.close()
        return user

    def delete_vote(self,vote_id):
        conn=MySQLdb.connect(host=db_config["db_host"],port=db_config["db_port"],\
                             user=db_config["db_user"],passwd=db_config["db_passwd"],\
                             db=db_config["db_name"],charset="utf8")
        vote = Vote(vote_id,self.user_id)
        cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        cursor.execute("select * from groups where group_id = %d and leader_id = %d" % (vote.group_id,self.user_id))
        # only leader can delete vote
        right = cursor.fetchall()
        if (right):
            cursor.execute("delete from votes where vote_id = %d" % int(vote_id))
            conn.commit()
            conn.close()
            return True
        conn.close()
        return False

    def end_vote(self,vote_id):
        conn=MySQLdb.connect(host=db_config["db_host"],port=db_config["db_port"],\
                             user=db_config["db_user"],passwd=db_config["db_passwd"],\
                             db=db_config["db_name"],charset="utf8")
        vote = Vote(vote_id,self.user_id)
        cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        cursor.execute("select * from groups where group_id = %d and leader_id = %d" % (vote.group_id,self.user_id))
        # only leader can delete vote
        right = cursor.fetchall()
        if (right):
            cursor.execute("update votes set voting=0 and endtime=CURRENT_TIMESTAMP where vote_id=%s" % vote_id);
            conn.commit();
            conn.close();
            return True
        conn.close()
        return False

    def delete_discussion(self,discuss_id):
        conn=MySQLdb.connect(host=db_config["db_host"],port=db_config["db_port"],\
                             user=db_config["db_user"],passwd=db_config["db_passwd"],\
                             db=db_config["db_name"],charset="utf8")
        cursor=conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        discuss = Discussion(discuss_id)
        group = Group(discuss.group_id)
        valid = (discuss.user_id == self.user_id) or (group.leader_id == self.user_id)
        if(valid):
            delete_message = "Your discussion %s in group %s has been deleted by leader."\
                              % (discuss.title,group.name)
            sql = "insert into news(type, group_id, receiver, content)\
                   values(%d, %s, %s, '%s');" % (6, group.group_id, discuss.user_id, delete_message)
            cursor.execute(sql)

            sql = "delete from discussion where discuss_id = %s;" % discuss_id
            cursor.execute(sql)
            conn.commit()
            conn.close()
            return True
        conn.close()
        return False

    def delete_reply(self,reply_id):
        conn=MySQLdb.connect(host=db_config["db_host"],port=db_config["db_port"],\
                             user=db_config["db_user"],passwd=db_config["db_passwd"],\
                             db=db_config["db_name"],charset="utf8")
        cursor=conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        reply = Reply(reply_id)
        discuss = Discussion(reply.discuss_id)
        group = Group(discuss.group_id)
        valid = (reply.user_id == self.user_id) or (group.leader_id == self.user_id)
        if(valid):
            delete_message = 'Your reply: "%s" on discussion %s has been deleted by leader.'\
                              % (reply.content, discuss.title)
            sql = "insert into news(type, group_id, receiver, content)\
                   values(%d, %s, %s, '%s');" % (7, group.group_id, reply.user_id, delete_message)
            cursor.execute(sql)

            sql = "delete from reply_discuss where reply_id = %s;" % reply_id
            cursor.execute(sql)
            sql = "update discussion set reply_num = reply_num - 1\
                   where discussion.discuss_id = %d;" % reply.discuss_id
            cursor.execute(sql)
            conn.commit()
            conn.close()
            return True
        conn.close()
        return False
#keep!
    def delete_bulletin(self, bulletin_id):
        conn=MySQLdb.connect(host=db_config["db_host"],port=db_config["db_port"],\
                             user=db_config["db_user"],passwd=db_config["db_passwd"],\
                             db=db_config["db_name"],charset="utf8")
        cursor=conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        bulletin = Bulletin(bulletin_id)
        if (bulletin.user_id == self.user_id):
            print "Arrive here", bulletin.user_id
            sql = "delete from bulletin where bulletin_id = %s;" % bulletin_id
            cursor.execute(sql)
            conn.commit()
            conn.close()
            return True
        conn.close()
        return False
#keep!



class Group:

    def __init__(self, group_id):
        ##名字与数据库中相同
        self.group_id = str(group_id)
        if(self.exist_group()):
            data = self.get_data()
            self.name = data['name']
            self.topic = data['topic']
            self.confirmMessage = data['confirmMessage']
            self.leader_id = data['leader_id']
            #NEW ITEM
            self.description=data['description']
            self.create_time=data['create_time']
        #这里leader的标识也变成id了，注意！！！

    def exist_group(self):
        conn=MySQLdb.connect(host=db_config["db_host"],port=db_config["db_port"],user=db_config["db_user"],passwd=db_config["db_passwd"],db=db_config["db_name"],charset="utf8")
        cursor=conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        cursor.execute("select name from groups where group_id='" + self.group_id + "';")
        exist=cursor.fetchall()
        return exist

#keep!
    def create_bulletin(self, user_id, title, text):
        conn=MySQLdb.connect(host=db_config["db_host"],port=db_config["db_port"],\
                             user=db_config["db_user"],passwd=db_config["db_passwd"],\
                             db=db_config["db_name"],charset="utf8")
        cursor=conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        #if self.leader_id == user_id:

        #create_message = "A new bulletin %s is created in our group!" % (title)
        #receiver = -1*(user_id)
        #sql = "insert into news(type, group_id, receiver, content)\
               #values(%d, %s, %d, '%s');" % (4, self.group_id, receiver, create_message)
        #cursor.execute(sql)

        #excluder = user_id
        #sql = "update message \
               #set viewed = 0, time = CURRENT_TIMESTAMP \
               #where type = 1 and group_id = %s and receiver != %d;" % (self.group_id, excluder)
        #cursor.execute(sql)
        #conn.commit()

        sql = "insert into bulletin(user_id, group_id, title, text) values(%d,%s,'%s','%s');"\
              % (user_id, self.group_id, title, text)
        cursor.execute(sql)
        sql = "update bulletin set title = '%s', text = '%s' \
               where user_id = %d and group_id = %s;" % (title, text, user_id, self.group_id)
        cursor.execute(sql)
        conn.commit()
        conn.close()
        return True
        #conn.close()
        #return False;
#keep!

#keep!
    def get_bulletin(self):
        conn=MySQLdb.connect(host=db_config["db_host"],port=db_config["db_port"],\
                             user=db_config["db_user"],passwd=db_config["db_passwd"],\
                             db=db_config["db_name"],charset="utf8")

        cursor=conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        sql = "select * from bulletin where group_id = %s \
               order by create_time desc;" % self.group_id
        cursor.execute(sql)
        bulletin=cursor.fetchall()

        for entry in bulletin:
            user = User(user_id=entry["user_id"])
            entry['username'] = user.username

        conn.close()
        return bulletin
#keep!

#keep!
    def get_data(self):
        conn = MySQLdb.connect(host=db_config["db_host"],port=db_config["db_port"],user=db_config["db_user"],passwd=db_config["db_passwd"],db=db_config["db_name"],charset="utf8")
        cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        sql = "select * from groups where group_id="+self.group_id+";"
        cursor.execute(sql)
        data = cursor.fetchall()
        #print data
        conn.close()
        return data[0]
        #return: {'leader_id': 0L, 'name': u'Jumanji', 'topic': u'Joe Johnston', 'create_time': datetime.datetime(2017, 12, 7, 16, 55, 32), 'group_id': 2L, 'confirmMessage': 1995L, 'description': u'Action, Adventure, Family'},
#keep!

    def news(self, type, receiver, content):
        conn = MySQLdb.connect(host=db_config["db_host"],port=db_config["db_port"],user=db_config["db_user"],passwd=db_config["db_passwd"],db=db_config["db_name"],charset="utf8")
        cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        sql = "insert into message(type, group_id, receiver, content)\
                   values(%d, %s, %d, '%s');" % (type, self.group_id, receiver, content)
        cursor.execute(sql)



class Bulletin:
    def __init__(self, bulletin_id):
        self.bulletin_id = int(bulletin_id)
        if self.exist():
            data = self.get_data()
            self.group_id = data['group_id']
            self.user_id = data['user_id']
            self.title = data['title']
            self.text = data['text']

    def get_data(self):
        conn=MySQLdb.connect(host=db_config["db_host"],port=db_config["db_port"],\
                             user=db_config["db_user"],passwd=db_config["db_passwd"],\
                             db=db_config["db_name"],charset="utf8")
        cursor=conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        sql = "select * from bulletin where bulletin_id="+str(self.bulletin_id)+";"
        cursor.execute(sql)
        item = cursor.fetchone()
        user = User(user_id=item["user_id"])
        item["username"] = user.username
        conn.close()
        return item

    def increase_read_num(self):
        conn=MySQLdb.connect(host=db_config["db_host"],port=db_config["db_port"],\
                             user=db_config["db_user"],passwd=db_config["db_passwd"],\
                             db=db_config["db_name"],charset="utf8")
        cursor=conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        sql = "update bulletin set read_num = read_num + 1 \
               where bulletin.bulletin_id = %d;" % self.bulletin_id
        cursor.execute(sql)
        conn.commit()
        conn.close()

    def exist(self):
        conn=MySQLdb.connect(host=db_config["db_host"],port=db_config["db_port"],\
                     user=db_config["db_user"],passwd=db_config["db_passwd"],\
                     db=db_config["db_name"],charset="utf8")
        cursor=conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        sql = "select * from bulletin where bulletin_id = %d;" % self.bulletin_id
        cursor.execute(sql)
        exist = cursor.fetchall()
        conn.close()
        if exist:
            return 1    #exist
        return 0 

