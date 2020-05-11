import numpy
import pandas

class Popularity_Recommender():

	def __init__(self):
		# Data set
		self.train_data = None

		# User ID to give recs to
		self.user_id = None

		# Product ID
		self.item_id = None

		# Recommendation. 
		self.popularity_recommendataions = None

	# Create the recommendations.
	def create(self,train_data,user_id,item_id):

		# Data set
		self.train_data = train_data

		# User ID to give recs to
		self.user_id = user_id

		# Product ID
		self.item_id = item_id


		# The items are grouped by item_id aggregated with the count of the users and the index is reseted.
		train_data_grouped = train_data.groupby([self.item_id]).agg({self.user_id: 'count'}).reset_index()
		# The column named user_id is replaced by the name score.
		train_data_grouped.rename(columns = {'user_id': 'score'}, inplace = True)


		# The training data is sorted according to the score in descending order and by item_id in ascending order.
		train_data_sort = train_data_grouped.sort_values(['score', self.item_id], ascending = [0,1])
		# The new column named Rank is created by score sorted in ascending order.
		train_data_sort['Rank'] = train_data_sort['score'].rank(ascending = 0, method = 'first')


		# The first 15 items are saved into the popularity_recommendataions and it is returned. 
		self.popularity_recommendataions = train_data_sort.head(5)


	# Method to user created recommendations
	def recommend(self, user_id):

		# Init the user_recommendataion var by popularity_recommendataions since the recommendations has been saved into this column.
		user_recommendataion = self.popularity_recommendataions

		# Get the user_id
		user_recommendataion['user_id'] = user_id

		# Set the columns
		cols = user_recommendataion.columns.tolist()
		cols = cols[-1:] + cols[:-1]
		user_recommendataion = user_recommendataion[cols]

		return user_recommendataion