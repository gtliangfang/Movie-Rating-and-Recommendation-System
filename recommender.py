import graphlab
from graphlab import SFrame
import MySQLdb
from config import *

def create_rec_list():
	conn = MySQLdb.connect(host=db_config["db_host"],port=db_config["db_port"],user=db_config["db_user"],passwd=db_config["db_passwd"],db=db_config["db_name"],charset="utf8")
	#cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
	user_rate = graphlab.SFrame.from_sql(conn, "select user_id,group_id,title from bulletin;")
	#cursor.execute("select * from user where user_id='" + str(self.user_id) + "';")
	#data = cursor.fetchall()
	#conn.close()
	#print user_rate

	#print user_rate[0]

	#renameSF
	user_rate.rename({'group_id': 'item_id', 'title':'rating'})

	#FactorizationRecommender
	m = graphlab.recommender.create(user_rate, target='rating')
	recs = m.recommend()
	recs.to_sql(conn, "recommender")
	conn.close()

	#recs.print_rows(num_rows=10, num_columns=4)

	#ItemSimilarityRecommender
	#sf2 = graphlab.SFrame({'user_id': ['0', '0', '0', '1', '1', '2', '2', '2'],'item_id': ['a', 'b', 'c', 'a', 'b', 'b', 'c', 'd'],'rating': [1, 3, 2, 5, 4, 1, 4, 3]})
	#m2 = graphlab.item_similarity_recommender.create(user_rate, target="rating", similarity_type='pearson')
	#m2.predict(sf)
	#recs2 = m2.recommend()
	#recs2.to_sql(conn, "recommender")
	#conn.close()










#sf = graphlab.SFrame({'user_id': ["0", "0", "0", "1", "1", "2", "2", "2"], 'item_id': ["a", "b", "c", "a", "b", "b", "c", "d"],'rating': [1, 3, 2, 5, 4, 1, 4, 3]})
#m = graphlab.recommender.create(sf, target='rating')
#recs = m.recommend()
#print recs

#sf = graphlab.SFrame({'user_id': ['0', '0', '0', '1', '1', '2', '2', '2'], 'item_id': ['a', 'b', 'c', 'a', 'b', 'b', 'c', 'd']})
#m = graphlab.recommender.create(sf)
#recs = m.recommend()
#print recs
#print type(recs)