import gensim
model = gensim.models.KeyedVectors.load_word2vec_format("train.bin", binary=True)

yellow = []
green = []
blue = []
purple = []

file = open("editable_connect_list.txt")
for line in file:
    line = line.split(",")
    ans_avg = []
    word_avg = []
    if line[0] == "yellow":
        line[1] = line[1].split(" ")
        for i in range(4):
            for v in line[1]:
                if line[2 + i].strip() in model and v in model:
                    word_avg.append(1 - model.distance(line[2 + i].strip(), v))
                elif line[2 + i].strip() not in model:
                    print(line[2 + i].strip())
                elif v not in model:
                    print(v)
            if len(word_avg) > 0:
                ans_avg.append(sum(word_avg)/len(word_avg))
                word_avg.clear()
            else:
                word_avg.clear()
        if len(yellow) == 1 and len(ans_avg) > 0:
            yellow[0] = (yellow[0] + (sum(ans_avg)/len(ans_avg)))/2
            ans_avg.clear()
        elif len(ans_avg) != 0:
            yellow.append(sum(ans_avg)/len(ans_avg))
            ans_avg.clear()
        else:
            ans_avg.clear()

    if line[0] == "green":
        line[1] = line[1].split(" ")
        for i in range(4):
            for v in line[1]:
                if line[2 + i].strip() in model and v in model:
                    word_avg.append(1 - model.distance(line[2 + i].strip(), v))
                elif line[2 + i].strip() not in model:
                    print(line[2 + i].strip())
                elif v not in model:
                    print(v)
            if len(word_avg) > 0:
                ans_avg.append(sum(word_avg)/len(word_avg))
                word_avg.clear()
            else:
                word_avg.clear()
        if len(green) == 1 and len(ans_avg) > 0:
            green[0] = (green[0] + (sum(ans_avg)/len(ans_avg)))/2
            ans_avg.clear()
        elif len(ans_avg) != 0:
            green.append(sum(ans_avg)/len(ans_avg))
            ans_avg.clear()
        else:
            ans_avg.clear()
    
    if line[0] == "blue":
        line[1] = line[1].split(" ")
        for i in range(4):
            for v in line[1]:
                if line[2 + i].strip() in model and v in model:
                    word_avg.append(1 - model.distance(line[2 + i].strip(), v))
                elif line[2 + i].strip() not in model:
                    print(line[2 + i].strip())
                elif v not in model:
                    print(v)
            if len(word_avg) > 0:
                ans_avg.append(sum(word_avg)/len(word_avg))
                word_avg.clear()
            else:
                word_avg.clear()
        if len(blue) == 1 and len(ans_avg) > 0:
            blue[0] = (blue[0] + (sum(ans_avg)/len(ans_avg)))/2
            ans_avg.clear()
        elif len(ans_avg) != 0:
            blue.append(sum(ans_avg)/len(ans_avg))
            ans_avg.clear()
        else:
            ans_avg.clear()

    if line[0] == "purple":
        line[1] = line[1].split(" ")
        for i in range(4):
            for v in line[1]:
                if line[2 + i].strip() in model and v in model:
                    word_avg.append(1 - model.distance(line[2 + i].strip(), v))
                elif line[2 + i].strip() not in model:
                    print(line[2 + i].strip())
                elif v not in model:
                    print(v)
            if len(word_avg) > 0:
                ans_avg.append(sum(word_avg)/len(word_avg))
                word_avg.clear()
            else:
                word_avg.clear()
        if len(purple) == 1 and len(ans_avg) > 0:
            purple[0] = (purple[0] + (sum(ans_avg)/len(ans_avg)))/2
            ans_avg.clear()
        elif len(ans_avg) != 0:
            purple.append(sum(ans_avg)/len(ans_avg))
            ans_avg.clear()
        else:
            ans_avg.clear()


print(yellow)
print(green)
print(blue)
print(purple)

