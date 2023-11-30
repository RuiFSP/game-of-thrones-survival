import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
import pickle

def houses_model_train():
    house = pd.read_csv('features_for_quiz/houses/classes.csv')

    outcasts = house[house['outcast'] == 1]
    not_outcasts = house[house['outcast'] == 0]

    outcasts_X = outcasts.drop(columns='class')
    outcasts_y = outcasts['class']

    not_outcasts_X = not_outcasts.drop(columns='class')
    not_outcasts_y = not_outcasts['class']

    model_outcasts = KNeighborsClassifier(n_neighbors=1)
    model_not_outcasts = KNeighborsClassifier(n_neighbors=1)

    model_outcasts.fit(outcasts_X, outcasts_y)
    model_not_outcasts.fit(not_outcasts_X, not_outcasts_y)

    with open('got_survival/models_pickle/outcasts.pkl', 'wb') as file:
        pickle.dump(model_outcasts, file)

    with open('got_survival/models_pickle/not_outcasts.pkl', 'wb') as file:
        pickle.dump(model_not_outcasts, file)


def houses_model_predict(X):
    if X['outcast'][0]:
        model_outcasts = pickle.load(open('got_survival/models_pickle/outcasts.pkl', 'rb'))
        return model_outcasts.predict(X)

    model_not_outcasts = pickle.load(open('got_survival/models_pickle/not_outcasts.pkl', 'rb'))
    return model_not_outcasts.predict(X)


def get_dict(outcast, climate, empathy, fighting, honor, connections, unyielding):
    test = {
        'outcast': [outcast],
        'climate': [climate],
        'empathy': [empathy],
        'fighting': [fighting],
        'honor': [honor],
        'connections': [connections],
        'unyielding': [unyielding]
    }
    return pd.DataFrame.from_dict(test)

############### TESTING ###############

# test = {
#     'outcast': [0],
#     'climate': [2],
#     'empathy': [5],
#     'fighting': [3],
#     'honor': [4],
#     'connections': [5],
#     'unyielding': [3]
# }
# new = pd.DataFrame.from_dict(test)

if __name__ == '__main__':
    # houses_model_train()
    # print(houses_model_predict(new))
    pass
