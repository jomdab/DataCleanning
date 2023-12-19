import csv
import random
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.linear_model import ElasticNet
from sklearn.linear_model import SGDRegressor
from sklearn.svm import SVR
from sklearn.linear_model import BayesianRidge
from sklearn.kernel_ridge import KernelRidge
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
# from sklearn.preprocessing import normalize
from sklearn.model_selection import train_test_split

def r2(output,target):
    mean = sum(output) / len(output)

    # Calculate the total sum of squares (TSS)
    tss = sum((y - mean) ** 2 for y in output)

    # Calculate the sum of squares of residuals (SSR)
    rss = sum((target[i] - output[i]) ** 2 for i in range(len(output)))

    # Calculate R-squared (R2)
    return 1 - (rss / tss)

def normalize(data):
    normalized_data = []
    min_val = min(min(row) for row in data)
    max_val = max(max(row) for row in data)
    for row in data:
        temp = []
        for element in row:
            temp.append((element-min_val)/(max_val-min_val))
        normalized_data.append(temp)
    return normalized_data

# def train_test_split(input,target,ratio):
#     num_sample = int(ratio*len(input))
    
#     #create random indices
#     indices = list(range(len(input)))
#     random.shuffle(indices)

#     #split train and test set
#     train_data = indices[:num_sample]
#     test_data = indices[num_sample:]

#     X_train = [input[i] for i in train_data]
#     y_train = [target[i] for i in train_data]
#     X_test = [input[i] for i in test_data]
#     y_test = [target[i] for i in test_data]
#     return X_train,X_test,y_train,y_test


def load_data(file):
    input = []
    target = []
    with open(file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            # Convert the input data values to floats
            input_row = [float(value) for value in row[:-1]]
            input.append(input_row)
            # Convert the target value to a float
            target_value = float(row[-1])
            target.append(target_value)

    return input, target

def main():
    file = 'dataset.csv'
    input, target = load_data(file)
    normalized_input = normalize(input)
    # for i in range(5):
    #     print(normalized_input[i])
    #     print(noramlized_target[i])
    X_train,X_test,y_train,y_test = train_test_split(normalized_input,target,test_size=0.2,shuffle=False)

    #train model
    model = RandomForestRegressor()
    model.fit(X_train, y_train)

    #evaluate
    y_pred = model.predict(X_test)
    print("r2 of model = ",r2_score(y_pred=y_pred,y_true=y_test))
    print("mse = ",mean_squared_error(y_pred=y_pred,y_true=y_test))

    #write prediction result to csv file
    write_data = list(zip(y_pred,y_test))
    with open('prediction.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Predicted', 'Desire'])
        writer.writerows(write_data)


main()