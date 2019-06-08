from collections import defaultdict
import io
from surprise import SVDpp
from surprise import Dataset
from surprise import get_dataset_dir, accuracy
from surprise.model_selection import train_test_split


def read_item_names():
    """Read the u.item file from MovieLens 100-k dataset and return two
    mappings to convert raw ids into movie names and movie names into raw ids.
    """

    file_name = get_dataset_dir() + '/ml-100k/ml-100k/u.item'
    rid_to_name = {}
    name_to_rid = {}
    with io.open(file_name, 'r', encoding='ISO-8859-1') as f:
        for line in f:
            line = line.split('|')
            rid_to_name[line[0]] = line[1]
            name_to_rid[line[1]] = line[0]

    return rid_to_name, name_to_rid

def get_top_n(predictions, n=10):
    '''Return the top-N recommendation for each user from a set of predictions.

    Args:
        predictions(list of Prediction objects): The list of predictions, as
            returned by the test method of an algorithm.
        n(int): The number of recommendation to output for each user. Default
            is 10.

    Returns:
    A dict where keys are user (raw) ids and values are lists of tuples:
        [(raw item id, rating estimation), ...] of size n.
    '''

    # First map the predictions to each user.
    top_n = defaultdict(list)
    for uid, iid, true_r, est, _ in predictions:
        top_n[uid].append((iid, est))

    # Then sort the predictions for each user and retrieve the k highest ones.
    for uid, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_n[uid] = user_ratings[:n]

    return top_n


# First train an SVD algorithm on the movielens dataset.
data = Dataset.load_builtin('ml-100k')
trainset, testset = train_test_split(data, test_size=.25)

algo = SVDpp()
algo.fit(trainset)

rid_to_name, name_to_rid = read_item_names()

# Than predict ratings for all pairs (u, i) that are NOT in the training set.
predictions = algo.test(testset)

accuracy.rmse(predictions)


top_n = get_top_n(predictions, n=10)

# Print the recommended items for each user
# for uid, user_ratings in top_n.items():
#     print(uid, [[rid_to_name[iid], rating] for (iid, rating) in user_ratings])

user_id = str(234)

print(user_id, [[rid_to_name[iid], rating] for (iid, rating) in top_n[user_id]])