def read_config(config_file='config.ini'):
    import os
    import configparser

    # Get the current script directory
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Get the parent directory
    parent_dir = os.path.dirname(current_dir)

    # Construct the path to the config.ini file
    config_path = os.path.join(parent_dir, config_file)

    config = configparser.ConfigParser()
    config.read(config_path)

    return config

def transform_odds(odd: float):
    #return (1/odd) * 100
    return 1/odd

def read_data_from_csv(csv, eliminate_outlier=True):
    '''Given bulk data in CSV, Preprocess it to fit in DB'''
    import pandas as pd
    import numpy as np

    data_sample = pd.read_csv(csv)

    data_sample['prob_player1'] = data_sample['player1_odd'].apply(transform_odds)
    data_sample['prob_player2'] = data_sample['player2_odd'].apply(transform_odds)

    data_sample_dropna = data_sample.dropna(subset=['player1_odd','player2_odd'])

    game_columns = ['hg1','ag1','hg2','ag2','hg3','ag3','hg4','ag4','hg5','ag5']
    home_game_columns = [f'hg{i}' for i in range(1,6)]
    away_game_columns = [f'ag{i}' for i in range(1,6)]

    for col in game_columns:
        data_sample_dropna[col] = data_sample_dropna[col].fillna(0)

    player1_score = data_sample_dropna[home_game_columns].sum(axis=1)
    player2_score = data_sample_dropna[away_game_columns].sum(axis=1)

    data_sample_dropna['score_player1'] = np.zeros(data_sample_dropna.shape[0])
    data_sample_dropna['score_player2'] = np.zeros(data_sample_dropna.shape[0])

    for i, _ in data_sample_dropna.iterrows():
        if player1_score[i] > player2_score[i]:
            data_sample_dropna.loc[i, 'score_player1'] = 1
            data_sample_dropna.loc[i, 'score_player2'] = 0
        else:
            data_sample_dropna.loc[i, 'score_player1'] = 0
            data_sample_dropna.loc[i, 'score_player2'] = 1

    data_sample_dropna = data_sample_dropna.drop(columns=game_columns, axis=1)
    data_sample_dropna = data_sample_dropna.drop(columns='status', axis=1)

    data_features = data_sample_dropna[data_sample_dropna.columns[7:]]

    integer_columns = []
    float_columns = []

    for col in data_features.columns:
        if data_features[col].dtype == np.int64:
            integer_columns.append(col)
        elif data_features[col].dtype == np.float64:
            float_columns.append(col)

    data_players = dict()
    players = list()

    for i, row in data_features.iterrows():
        #print(data_sample_dropna.loc[i, 'player1'])
        players.append(data_sample_dropna.loc[i, 'player1'])
        players.append(data_sample_dropna.loc[i, 'player2'])

    data_players['players'] = players

    for i, row in data_features.iterrows():
        for col in data_features.columns:
            if col.endswith('player1'):
                data_players[col.replace('_player1', '')] = list()
    
    for i, row in data_features.iterrows():
        for col in data_features.columns:
            if col.endswith('player1'):
                data_players[col.replace('_player1', '')].append(data_features.loc[i, col])
            elif col.endswith('player2'):
                data_players[col.replace('_player2', '')].append(data_features.loc[i, col])

    data_players_df = pd.DataFrame(data_players)

    data_players_df['nb_games'] = 1

    for col in data_players_df.columns:
        if data_players_df[col].dtype in {np.int64, np.float64}:
            data_players_df[col] /= data_players_df['nb_games']
    
    features_df = data_players_df.drop(columns=['prob', 'nb_games'], axis=1)
    targets_df =  data_players_df['prob']

    model_input = list()

    for i in range(0,features_df.shape[0],2):
        #print(i)
        #print(features_df.iloc[i:i+2].transpose())
        _pairs = features_df.iloc[i:i+2].transpose()
        
        _input = np.array([ (i, j) for i, j in zip(_pairs[i+0].to_numpy()[1:], _pairs[i+1].to_numpy()[1:]) ])
        model_input.append(_input)

    model_input = np.array(model_input)
    model_output = np.array([ (targets_df[i], targets_df[i+1]) for i in range(0,targets_df.shape[0],2) ])

    if eliminate_outlier:
        model_input_no_outlier = model_input.copy()
        model_output_no_outlier = model_output.copy()

        index_to_remove = list()

        for i, value in enumerate(zip(model_input, model_output)):
            model, score = value
            
            print(model[-1], score)
            if model[-1][0] > model[-1][1] and score[0] < score[1]:
                print('outlier1')
                index_to_remove.append(i)
                #model_input_no_outlier = np.delete(model_input_no_outlier, i, axis=0)
                #model_output_no_outlier = np.delete(model_output_no_outlier, i, axis=0)
                #print(f'removed outlier index {i}')
            
            elif model[-1][1] > model[-1][0] and score[1] < score[0]:
                print('outlier2')
                index_to_remove.append(i)
                #model_input_no_outlier = np.delete(model_input_no_outlier, i, axis=0)
                #model_output_no_outlier = np.delete(model_output_no_outlier, i, axis=0)
                #print(f'removed outlier index {i}')

        model_input_no_outlier = np.delete(model_input, index_to_remove, axis=0)
        model_output_no_outlier = np.delete(model_output, index_to_remove, axis=0)

        return model_input_no_outlier, model_output_no_outlier
    
    else:
        
        return model_input, model_output
    
def model_input_ratio(model_input):
    import numpy as np

    _epsilon = 1e-6

    model_input_ratio = list()

    for model in model_input:
        #print(model.shape)
        _per_model = list()
        for i in range(model.shape[0]):
            #print(model[i])
            _t = (model[i][0] + _epsilon) / (model[i][1] + _epsilon)
            _per_model.append(_t)

        _per_model = np.array(_per_model)
        model_input_ratio.append(_per_model)

    model_input_ratio = np.array(model_input_ratio)

    return model_input_ratio