from sklearn.externals import joblib
from sklearn.datasets import fetch_20newsgroups
import pprint
categories = [
	'alt.atheism',
	'talk.religion.misc'
]
print type(categories)
data = fetch_20newsgroups(subset='test',categories = categories,remove=('headers','footers','quotes'))

def main():

	datatemp = [data['data'][i] for i in range(len(data['data'])) if data['target_names'][data['target'][i]] in categories]
	targettemp = [data['target'][i] for i in range(len(data['data'])) if data['target_names'][data['target'][i]] in categories]
	data['data'] = datatemp
	data['target'] = targettemp

	print (data['target'])
	grid_search = joblib.load("gridsearchdump.pkl")
	pprint.pprint((data['data'][0]))
	#print dir(grid_search)
	searchoutput = grid_search.best_estimator_.predict(data['data'])

	testset = ['I love jesus, jesus jesus jesus, anyone know where I can find a local church','These creationists are taking over the public schools']
	testoutput = grid_search.best_estimator_.predict(testset)

	print testoutput


if __name__ == "__main__":
	main()