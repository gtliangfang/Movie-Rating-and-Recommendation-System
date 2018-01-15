import csv
import model
import time

start_time = time.time()
'''
with open('movies.tsv') as movie_file:
	movie_tsv = csv.reader(movie_file, delimiter='\t')
	for row in movie_tsv:
		model.create_movie(int(row[0]), row[1], row[2], row[3], int(row[7][:4]))
'''
time_movie = time.time() - start_time
print "MySQL spent %.4f second to process movies.tsv"%time_movie

num = 1000
curr_user = 1
with open('ratings.csv') as rating_file:
	rating_csv = csv.DictReader(rating_file)
	for row in rating_csv:
		user = int(row['userId'])
		if user > num:
			break
		for i in range(curr_user, user):
			model.create_user('user%d'%i, 'user%d@gatech.edu'%i, 'pw')
		curr_user = user
		try:
			model.add_rating(user, int(row['movieId']), float(row['rating']))
		except:
			pass

model.create_user('user%d'%num, 'user%d@gatech.edu'%num, 'pw')

time_total = time.time() - start_time

print "MySQL spent %.4f second to process rating.csv"%(time_total-time_movie)
print "MySQL spent %.4f second to process all data"%time_total

