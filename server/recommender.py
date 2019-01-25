import turicreate as tc
import sys
import mysql.connector

model_1 = tc.load_model("../recommender.model")

mydb = mysql.connector.connect( host="localhost", user="root", passwd="delgado_0077", database="films" )

def listFilms(numFilm, Film ):
        my_list = tc.SArray([int(Film)])
        similar_items = model_1.get_similar_items(my_list, k=int(numFilm))
	list = []
        #similar_items.print_rows(num_rows=int(sys.argv[2]))
	mycursor = mydb.cursor()
	for movie in similar_items:
		sql = "SELECT id, title, year FROM films WHERE id = %i" % int(movie['similar'])
		mycursor.execute(sql)
		myresult = mycursor.fetchall()
		list.append(str(unicode(myresult[0][0])))
                list.append(str(unicode(myresult[0][1])))
                list.append(str(unicode(myresult[0][2])))
		list.append(movie['score'])
	return list

def manuallyRecommendation(id_movie):
        my_list = tc.SArray([int(id_movie)])
        similar_items = model_1.recommend(my_list, k=5)
        similar_items.print_rows(num_rows=5) 

#manuallyRecommendation(sys.argv[1])
