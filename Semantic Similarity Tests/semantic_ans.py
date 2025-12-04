import gensim
model = gensim.models.KeyedVectors.load_word2vec_format("train.bin", binary=True)

yellow = []
green = []
blue = []
purple = []

file = open("editable_connect_list.txt")
for line in file:
    line = line.split(",")
    word_cosine = []
    counter = 1
    if line[0] == "yellow":
        for i in range(3):
            while (counter + (2 + i)) != 6:
                if line[2 + i].strip() in model and line[counter + (2 + i)].strip() in model:
                    word_cosine.append(1 - model.distance(line[(2 + i)].strip(), line[counter + (2 + i)].strip()))
                    counter += 1
                elif line[(2 + i)] not in model:
                    print(line[(2 + i)])
                    counter += 1
                elif line[counter + (2 + i)] not in model:
                    print(line[counter + (2 + i)])
                    counter += 1
            counter = 1
    
        if len(word_cosine) > 0 and len(yellow) > 0:
            yellow[0] = (yellow[0] + max(word_cosine))/2
            word_cosine.clear()
        elif len(word_cosine) > 0 and len(yellow) == 0:
            yellow.append(max(word_cosine))
            word_cosine.clear()
        else:
            word_cosine.clear()
            

    if line[0] == "green":
        for i in range(3):
            while (counter + (2 + i)) != 6:
                if line[2 + i].strip() in model and line[counter + (2 + i)].strip() in model:
                    word_cosine.append(1 - model.distance(line[(2 + i)].strip(), line[counter + (2 + i)].strip()))
                    counter += 1
                elif line[(2 + i)] not in model:
                    print(line[(2 + i)])
                    counter += 1
                elif line[counter + (2 + i)] not in model:
                    print(line[counter + (2 + i)])
                    counter += 1
            counter = 1
    
        if len(word_cosine) > 0 and len(green) > 0:
            green[0] = (green[0] + max(word_cosine))/2
            word_cosine.clear()
        elif len(word_cosine) > 0 and len(green) == 0:
            green.append(max(word_cosine))
            word_cosine.clear()
        else:
            word_cosine.clear()

    
    if line[0] == "blue":
        for i in range(3):
            while (counter + (2 + i)) != 6:
                if line[2 + i].strip() in model and line[counter + (2 + i)].strip() in model:
                    word_cosine.append(1 - model.distance(line[(2 + i)].strip(), line[counter + (2 + i)].strip()))
                    counter += 1
                elif line[(2 + i)] not in model:
                    print(line[(2 + i)])
                    counter += 1
                elif line[counter + (2 + i)] not in model:
                    print(line[counter + (2 + i)])
                    counter += 1
            counter = 1
    
        if len(word_cosine) > 0 and len(blue) > 0:
            blue[0] = (blue[0] + max(word_cosine))/2
            word_cosine.clear()
        elif len(word_cosine) > 0 and len(blue) == 0:
            blue.append(max(word_cosine))
            word_cosine.clear()
        else:
            word_cosine.clear()


    if line[0] == "purple":
        for i in range(3):
            while (counter + (2 + i)) != 6:
                if line[2 + i].strip() in model and line[counter + (2 + i)].strip() in model:
                    word_cosine.append(1 - model.distance(line[(2 + i)].strip(), line[counter + (2 + i)].strip()))
                    counter += 1
                elif line[(2 + i)] not in model:
                    print(line[(2 + i)])
                    counter += 1
                elif line[counter + (2 + i)] not in model:
                    print(line[counter + (2 + i)])
                    counter += 1
            counter = 1
    
        if len(word_cosine) > 0 and len(purple) > 0:
            purple[0] = (purple[0] + max(word_cosine))/2
            word_cosine.clear()
        elif len(word_cosine) > 0 and len(purple) == 0:
            purple.append(max(word_cosine))
            word_cosine.clear()
        else:
            word_cosine.clear()


print(yellow)
print(green)
print(blue)
print(purple)

