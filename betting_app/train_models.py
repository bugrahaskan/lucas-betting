from .utils import read_data_from_csv, model_input_ratio, transform_odds

class Model_DecisionTreeRegressor:
    def __init__(self, csv):
        _, _, self.model_input, self.model_output = read_data_from_csv(csv)
        self.model_input = model_input_ratio(self.model_input)

        from sklearn.model_selection import train_test_split
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.model_input, self.model_output, test_size=0.2, random_state=42)

    def train_it(self):
        from sklearn.tree import DecisionTreeRegressor

        self.regressor = DecisionTreeRegressor()
        self.regressor.fit(self.X_train, self.y_train)
        
        return self.regressor
    
    def predict_it(self):
        self.y_pred = self.regressor.predict(self.X_test)

        return self.y_pred
    
    def output_it(self):
        import pandas as pd
        from sklearn.metrics import mean_squared_error

        y_test_series = pd.DataFrame(self.y_test, columns=['odd1','odd2'])
        y_pred_series = pd.DataFrame(self.y_pred, columns=['pred1','pred2'])

        res = pd.concat([y_test_series, y_pred_series], axis=1)
        res = res.apply(transform_odds)

        mse = mean_squared_error(self.y_test, self.y_pred)

        return res, mse
    

class Model_GradientBoosting:
    def __init__(self, csv):
        _, _, self.model_input, self.model_output = read_data_from_csv(csv)
        self.model_input = model_input_ratio(self.model_input)

        from sklearn.model_selection import train_test_split
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.model_input, self.model_output, test_size=0.2, random_state=42)

    def train_it(self):
        from sklearn.ensemble import GradientBoostingRegressor
        from sklearn.multioutput import MultiOutputRegressor

        self.regressor = GradientBoostingRegressor(random_state=42)
        self.multioutput_regressor = MultiOutputRegressor(self.regressor)

        self.multioutput_regressor.fit(self.X_train, self.y_train)

        return self.multioutput_regressor

    def predict_it(self):
        self.y_pred = self.multioutput_regressor.predict(self.X_test)

        return self.y_pred

    def output_it(self):
        import pandas as pd
        from sklearn.metrics import mean_squared_error

        y_test_series = pd.DataFrame(self.y_test, columns=['odd1','odd2'])
        y_pred_series = pd.DataFrame(self.y_pred, columns=['pred1','pred2'])

        res = pd.concat([y_test_series, y_pred_series], axis=1)
        res = res.apply(transform_odds)

        mse = mean_squared_error(self.y_test, self.y_pred)

        return res, mse


class Model_KNNRegressor:
    def __init__(self, csv):
        _, _, self.model_input, self.model_output = read_data_from_csv(csv)
        self.model_input = model_input_ratio(self.model_input)

        from sklearn.model_selection import train_test_split
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.model_input, self.model_output, test_size=0.2, random_state=42)

    def train_it(self):
        from sklearn.neighbors import KNeighborsRegressor

        self.regressor = KNeighborsRegressor(n_neighbors=3)
        self.regressor.fit(self.X_train, self.y_train)

        return self.regressor

    def predict_it(self):
        self.y_pred = self.regressor.predict(self.X_test)

        return self.y_pred

    def output_it(self):
        import pandas as pd
        from sklearn.metrics import mean_squared_error

        y_test_series = pd.DataFrame(self.y_test, columns=['odd1','odd2'])
        y_pred_series = pd.DataFrame(self.y_pred, columns=['pred1','pred2'])

        res = pd.concat([y_test_series, y_pred_series], axis=1)
        res = res.apply(transform_odds)

        mse = mean_squared_error(self.y_test, self.y_pred)

        return res, mse


class Model_RandomTreeRegressor:
    def __init__(self, csv):
        _, _, self.model_input, self.model_output = read_data_from_csv(csv)
        self.model_input = model_input_ratio(self.model_input)

        from sklearn.model_selection import train_test_split
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.model_input, self.model_output, test_size=0.2, random_state=42)

    def train_it(self):
        from sklearn.ensemble import RandomForestRegressor

        self.regressor = RandomForestRegressor(random_state=42)
        self.regressor.fit(self.X_train, self.y_train)

        return self.regressor

    def predict_it(self):
        self.y_pred = self.regressor.predict(self.X_test)

        return self.y_pred

    def output_it(self):
        import pandas as pd
        from sklearn.metrics import mean_squared_error

        y_test_series = pd.DataFrame(self.y_test, columns=['odd1','odd2'])
        y_pred_series = pd.DataFrame(self.y_pred, columns=['pred1','pred2'])

        res = pd.concat([y_test_series, y_pred_series], axis=1)
        res = res.apply(transform_odds)

        mse = mean_squared_error(self.y_test, self.y_pred)

        return res, mse