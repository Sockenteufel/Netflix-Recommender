import turicreate as tc

ratings = tc.SFrame.read_csv('./complete_data.csv')
train_data, validation_data = tc.recommender.util.random_split_by_user(ratings, 'movieId', 'userId')

model = tc.recommender.create(train_data, 'userId', 'movieId',target='rating')

predictions = model.predict(validation_data)

metrics = model.evaluate(validation_data)

model.save('../recommender.model')



