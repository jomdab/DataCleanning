import csv
import random
from sklearn.linear_model import LinearRegression

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
    for row in data:
        temp = []
        for element in row:
            temp.append((element-min(row))/(max(row)-min(row)))
        normalized_data.append(temp)
    return normalized_data

def train_test_split(input,target,ratio):
    num_sample = int(ratio*len(input))
    
    #create random indices
    indices = list(range(len(input)))
    random.shuffle(indices)

    #split train and test set
    train_data = indices[:num_sample]
    test_data = indices[num_sample:]

    X_train = [input[i] for i in train_data]
    y_train = [target[i] for i in train_data]
    X_test = [input[i] for i in test_data]
    y_test = [target[i] for i in test_data]
    return X_train,X_test,y_train,y_test


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
    noramlized_target = [i/100 for i in target]
    for i in range(5):
        print(normalized_input[i])
        print(noramlized_target[i])
    X_train,X_test,y_train,y_test = train_test_split(normalized_input,target,0.8)

    #train model
    model = LinearRegression()
    model.fit(X_train, y_train)

    #evaluate
    y_pred = model.predict(X_test)
    print("r2 of model = ",r2(y_pred,y_test))

    #write prediction result to csv file
    write_data = list(zip(y_pred,y_test))
    with open('prediction.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Predicted', 'Desire'])
        writer.writerows(write_data)


main()