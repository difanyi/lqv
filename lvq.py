import random
import math

def read_file():
    f = open('iris_train.txt','r')
    dataset = []
    for line in f:
        dataset.append(line.split(','))

    for k in dataset:
        for j in range(len(k)):
            if j != 4:
                k[j] = float(k[j])
    for i in dataset:
        if i[-1] == 'Iris-setosa\n':
            i[-1] = '1'
        elif i[-1] == 'Iris-versicolor\n':
            i[-1] = '2'
        else:
            i[-1] = '3'
        
    return dataset




def normalize(data):
    for i in range(len(data)):
        data[i][0] = (data[i][0]-4.3)/3.4
        data[i][1] = (data[i][1]-2.2)/2.2
        data[i][2] = (data[i][2]-1.0)/5.9
        data[i][3] = (data[i][3]-0.1)/2.4
    return data



def eculidian_distance(weight,input_vec):
    return math.sqrt(((weight[0]-input_vec[0])**2+(weight[1]-input_vec[1])**2+(weight[2]-input_vec[2])**2+(weight[3]-input_vec[3])**2))



def initialize_weights(num_class):
    w = []
    for i in range(num_class):
        w.append([random.random(),random.random(),random.random(),random.random(),str(i+1)])
    return w


        
def lvq1(num_class,dataset,learning_rate,weights):
    l = [[] for i in range(num_class)]
    
    for j in range(len(dataset)):
        a = eculidian_distance(weights[0][0:-1],dataset[j][0:-1])
        b = eculidian_distance(weights[1][0:-1],dataset[j][0:-1])
        c = eculidian_distance(weights[2][0:-1],dataset[j][0:-1])
        temp2 = [a,b,c]
        temp3 = temp2.index(min(temp2))
        l[temp3].append(dataset[j])

    print(len(l[0]),len(l[1]),len(l[2]))

    for w in range(num_class):
        for temp in range(len(l[w])):
            for s in range(len(dataset)):
                if len(l[w]) != 0 and l[w][temp][-1] == dataset[s][-1]:
                    for b in range(len(weights[w])-1):
                        weights[w][b] += learning_rate*(dataset[s][b] - weights[w][b])
                elif len(l[w]) != 0 and l[w][temp][-1] != dataset[s][-1]:
                    for b in range(len(weights[w])-1):
                        weights[w][b] -= learning_rate*(dataset[s][b] - weights[w][b])
    return weights


def predict(weights,data):
    l = []
    for i in range(len(weights)):
        l.append(eculidian_distance(weights[i],data))
    return l.index(min(l))+1

def cal_accu(weight,dataset):
    l = []
    for i in range(len(dataset)):
        l.append(str(predict(weight,dataset[i])) == dataset[i][-1])
    return l.count(True)/len(l)
    


if __name__ == "__main__":
    #dataset
    dataset = read_file()
    dataset = normalize(dataset)
    #begin lvq
    ini = initialize_weights(3)
    k = lvq1(3,dataset,0.00001,ini)
    for i in range(20):
        k = lvq1(3,dataset,0.00001,k)
    return k
            
