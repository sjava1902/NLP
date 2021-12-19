from collections import defaultdict
import re
import math

    
    
def tokenize(text):
    text = text.lower()
    text = re.sub(r',', r' , ', str(text))
    text = re.sub(r'"', r' " ', str(text))
    text = re.sub(r'-', r' - ', str(text))
    text = re.sub(r'!', r' ! ', str(text))
    text = re.sub(r'\?', r' ? ', str(text))
    text = re.sub(r'\.', r' . ', str(text))
    text = re.sub(r'\(', r' ( ', str(text))
    text = re.sub(r'\)', r' ) ', str(text))
    text = re.sub(r'<br /><br />', r'', str(text))
    
    text = re.sub(r'[^a-z ^0-9 ^!?,".\(\)-]', r'', str(text))
    return text.split()
    ##P(positive | word) = P(word | positive) * P(positive) / P(word)
feedback = open("train.texts", "r", encoding = 'utf-8')
cluster = open("train.labels", "r", encoding = 'utf-8')
positive = []
negative = []
lenspos = [] #длины позитивных отзывов
lensneg = [] #длины негативных отзывов
sum_len_pos = 0
sum_len_neg = 0
while True:
    line = feedback.readline()
    if not line:
        break
    mark = cluster.readline()
    if mark == 'neg\n':
        line = line.lower()
        negative.append(line)
        lensneg.append(len(line))
        sum_len_neg += len(line)
    else:
        line = line.lower()
        positive.append(line)
        lenspos.append(len(line))
        sum_len_pos += len(line)
# Пункт а) 

max_len_pos = max(lenspos)
max_len_neg = max(lensneg)
min_len_pos = min(lenspos)
min_len_neg = min(lensneg)
avr_len_pos = sum_len_pos / len(positive)
avr_len_neg = sum_len_neg / len(negative)

lenspos = sorted(lenspos)
lensneg = sorted(lensneg)
mediana_pos = (lenspos[int(len(lenspos)/2)] + lenspos[int((len(lenspos)-1)/2)]) /2
mediana_neg = (lensneg[int(len(lensneg)/2)] + lenspos[int((len(lensneg)-1)/2)]) /2

print('Макс. длина позитивных отзывов = ', max_len_pos)
print('Мин. длина позитивных отзывов = ', min_len_pos)
print('Макс. длина негативных отзывов = ', max_len_neg)
print('Мин. длина негативных отзывов = ', min_len_neg)
print('Средняя длина позитивных отзывов = ', avr_len_pos)
print('Средняя длина негативных отзывов = ', avr_len_neg)
print('Медиана полозитивных отзывов = ', mediana_pos)
print('Медиана негативных отзывов = ', mediana_neg)
print()



# Пункт b)
split_positive = []
split_negative = []
for feed_back in negative:
    mass_of_word = tokenize(feed_back) 
    split_negative.append(mass_of_word)
for feed_back in positive:
    mass_of_word = tokenize(feed_back) 
    split_positive.append(mass_of_word)

    
# Пункт с)
count_pos = {}
count_neg = {}
n_pos_words = 0 #количество всех слов во всех  позитивных отзывах
n_neg_words = 0 #...
for feed_back in split_positive:
    for word in feed_back:
        value = count_pos.get(word)
        n_pos_words += 1
        if value == None:
            count_pos[word] = 1
        else:
            value += 1
            count_pos.update({word : value})
            
for feed_back in split_negative:
    for word in feed_back:
        value = count_neg.get(word)
        n_neg_words += 1
        if value == None:
            count_neg[word] = 1
        else:
            value += 1
            count_neg.update({word : value})
#P(WORD) = (coun word in pos + count word in neg)/count_all_words
    ####P(word | positive)
freq_pos = {}
freq_neg = {}

for feed_back in split_positive:
    for word in feed_back:
        value = count_pos.get(word)
        value /= n_pos_words
        freq_pos[word] = value
            
for feed_back in split_negative:
    for word in feed_back:
        value = count_neg.get(word)
        value /= n_neg_words
        freq_neg[word] = value

#сортировка словарей
# пункт d)
list_freq_pos = list(freq_pos.items())
list_freq_pos.sort(key=lambda i: i[1])
list_freq_neg = list(freq_neg.items())
list_freq_neg.sort(key=lambda i: i[1])
list_freq_neg.reverse()
list_freq_pos.reverse()
#считаем байесовские веса
weight_pos = freq_pos.copy()
weight_neg = freq_neg.copy()

for word in freq_pos:
    value = freq_pos.get(word)
    value /= n_pos_words
    weight_pos.update({word: value})
for word in freq_neg:
    value = freq_neg.get(word)
    value /= n_neg_words
    weight_neg.update({word: value})
weight = {}

for word in weight_neg:
    value_neg = weight_neg.get(word)
    value_pos = weight_pos.get(word)
    if (value_pos == None):
        continue
    weight.update({word: math.log(value_pos / value_neg)})
#упорядочиваем байесовские веса
list_weight = list(weight.items())
list_weight.sort(key=lambda i: i[1])
list_weight.reverse()
stop_words = []
print('Выводим самые частые НЕГАТИВНЫЕ')  
j = 0
for i in list_freq_neg:
    print(i[0], ':', i[1])
    stop_words.append(i[0])
    j += 1
    if (j == 45):
        break
print()
print()
print('Выводим самые частые ПОЗИТИВНЫЕ')

j = 0
for i in list_freq_pos:
    print(i[0], ':', i[1])
    stop_words.append(i[0])
    j += 1
    if (j == 45):
        break
print()
print()
print('Выводим байесовские веса, упорядоченные по убыванию')
k = 0
list_weight_rev = list_weight.copy()
list_weight_rev.reverse()
for i in list_weight:
    for j in list_freq_pos:
        value1 = j[1]
        if (j[0] == i[0]):
            break
        
    for j in list_freq_neg:
        value2 = j[1]
        if (j[0] == i[0]):
            break
    print(i[0], ':', i[1])
    k += 1
    if (k == 30):
        break
print()
print()
print('Выводим байесовсике веса, упорядоченные по возрастанию')

k= 0
for i in list_weight_rev:
    for j in list_freq_pos:
        value1 = j[1]
        if (j[0] == i[0]):
            break
        
    for j in list_freq_neg:
        value2 = j[1]
        if (j[0] == i[0]):
            break
    print(i[0], ':', i[1])
    k += 1
    if (k == 30):
        break

###
##пункт f
n_pos_dwords = 0
n_neg_dwords = 0
lastword = split_positive[0][0]
double_word_pos = {}
for feed_back in split_positive:
    for word in feed_back:
        if (word == lastword):
            continue
        a = lastword+word
        n_pos_dwords += 1
        value = double_word_pos.get(a)
        if (value == None):
            double_word_pos[a] = 1
        else:
            value += 1
            double_word_pos.update({a : value})
        lastword = word
        
lastword = split_negative[0][0]
double_word_neg = {}
for feed_back in split_negative:
    for word in feed_back:
        if (word == lastword):
            continue
        a = lastword+word
        n_neg_dwords += 1
        value = double_word_neg.get(a)
        if (value == None):
            double_word_neg[a] = 1
        else:
            value += 1
            double_word_neg.update({a : value})
        lastword = word
#сортируем словари двойных слов
list_dw_pos = list(double_word_pos.items())
list_dw_pos.sort(key=lambda i: i[1])
list_dw_neg = list(double_word_neg.items())
list_dw_neg.sort(key=lambda i: i[1])
list_dw_neg.reverse()
list_dw_pos.reverse()
##Считаем ЧАСТОТЫ двойных слов
freq_dw_neg = {}
freq_dw_pos = {}

last_dword = split_positive[0][0]
for feed_back in split_positive:
    for word in feed_back:
        if (word == last_dword):
            continue
        a = last_dword + word
        value = double_word_pos.get(a) # количество двойных позитивных слов
        value /= n_pos_dwords
        freq_dw_pos[a] = value
        last_dword = word
        
last_dword = split_negative[0][0]
for feed_back in split_negative:
    for word in feed_back:
        if (word == last_dword):
            continue
        a = last_dword + word
        value = double_word_neg.get(a) # количество двойных негативных слов
        value /= n_neg_dwords
        freq_dw_neg[a] = value
        last_dword = word

#закрываем обучающие файлы
feedback.close()
cluster.close()

# пункт e
predict = open("dev.texts", "r", encoding = 'utf - 8')
predict_labels = open("dev.labels", "r", encoding = 'utf - 8')
pred_pos = []
pred_neg = []
labels = []
while True:
    line = predict_labels.readline()
    if not line:
        break
    labels.append(line)
##P(positive | word) = P(word | positive) * P(positive) / P(word)
j = 0
accur = 0
count = 0
answer = []
while True:
    line = predict.readline()
    if not line:
        break
    else:
        count += 1
        line = line.lower()
        text = tokenize(line)
        negver = 0
        posver = 0
        last_word = text[0][0]
        for word in text:
            if (word in stop_words):
                last_word = word
                continue
            value1 = count_pos.get(word)
            value2 = count_neg.get(word)
            if (value1 == None):
                last_word = word
                continue
            if (value2 == None):
                last_word = word
                continue
            
            P_word_if_positive = freq_pos.get(word)
            P_positive = len(split_positive)/(len(split_positive) + len(split_negative))
            P_word = (value1 + value2)/(n_pos_words + n_neg_words)
            posver += P_word_if_positive * P_positive / P_word
            
            P_word_if_negative = freq_neg.get(word)
            P_negative = len(split_negative)/(len(split_positive) + len(split_negative))
            P_word = (value1 + value2)/(n_pos_words + n_neg_words)
            negver += P_word_if_negative * P_negative / P_word

            ### обработка двойных слов.
            a = last_word + word
            value1 = double_word_pos.get(a)
            value2 = double_word_neg.get(a)
            if (value1 == None):
                last_word = word
                continue
            if (value2 == None):
                last_word = word
                continue            
            P_dword_if_positive = freq_dw_pos.get(a)
            P_positive = len(split_positive)/(len(split_positive) + len(split_negative))
            P_dword = (value1 + value2)/(n_pos_dwords + n_neg_dwords)
            posver += math.log(P_dword_if_positive * P_positive / P_dword)

            P_dword_if_negative = freq_dw_neg.get(a)
            P_negative = len(split_negative)/(len(split_positive) + len(split_negative))
            P_dword = (value1 + value2)/(n_neg_dwords + n_neg_dwords)
            negver += math.log(P_dword_if_negative * P_negative / P_dword)
        if (posver > negver):
            answer.append('pos\n')
            if ('pos\n' == labels[j]):
                accur += 1
        else:
            answer.append('neg\n')
            if ('neg\n' == labels[j]):
                accur += 1
        j += 1
print('Точность работы на файле DEV =', end = ' ')
print(accur/count)

predict = open("train.texts", "r", encoding = 'utf - 8')
predict_labels = open("train.labels", "r", encoding = 'utf - 8')
pred_pos = []
pred_neg = []
labels = []
while True:
    line = predict_labels.readline()
    if not line:
        break
    labels.append(line)

j = 0
accur = 0
count = 0
answer = []
while True:
    line = predict.readline()
    if not line:
        break
    else:
        count += 1
        line = line.lower()
        text = tokenize(line)
        negver = 0
        posver = 0
        last_word = text[0][0]
        for word in text:
            if (word in stop_words):
                last_word = word
                continue
            value1 = count_pos.get(word)
            value2 = count_neg.get(word)
            if (value1 == None):
                last_word = word
                continue
            if (value2 == None):
                last_word = word
                continue
            
            P_word_if_positive = freq_pos.get(word)
            P_positive = len(split_positive)/(len(split_positive) + len(split_negative))
            P_word = (value1 + value2)/(n_pos_words + n_neg_words)
            posver += P_word_if_positive * P_positive / P_word
            
            P_word_if_negative = freq_neg.get(word)
            P_negative = len(split_negative)/(len(split_positive) + len(split_negative))
            P_word = (value1 + value2)/(n_pos_words + n_neg_words)
            negver += P_word_if_negative * P_negative / P_word

            ### обработка двойных слов.
            a = last_word + word
            value1 = double_word_pos.get(a)
            value2 = double_word_neg.get(a)
            if (value1 == None):
                last_word = word
                continue
            if (value2 == None):
                last_word = word
                continue            
            P_dword_if_positive = freq_dw_pos.get(a)
            P_positive = len(split_positive)/(len(split_positive) + len(split_negative))
            P_dword = (value1 + value2)/(n_pos_dwords + n_neg_dwords)
            posver += math.log(P_dword_if_positive * P_positive / P_dword)

            P_dword_if_negative = freq_dw_neg.get(a)
            P_negative = len(split_negative)/(len(split_positive) + len(split_negative))
            P_dword = (value1 + value2)/(n_neg_dwords + n_neg_dwords)
            negver += math.log(P_dword_if_negative * P_negative / P_dword)
        if (posver > negver):
            answer.append('pos\n')
            if ('pos\n' == labels[j]):
                accur += 1
        else:
            answer.append('neg\n')
            if ('neg\n' == labels[j]):
                accur += 1
        j += 1
print('Точность алгоритма на обучающей выборке =', end = ' ')
print(accur/count)

#################
"""
Я не смог разобраться, чтобы реализовать программу так, чтобы получить нужный для
автоматической проверки файл preds.tsv.
Я реализовал байесовский классификатор, в котором использует вероятности для биграмм и слов
одновременно. Также я реализовал список стоп-слов. Слова и символы, которые чаще всего
встречаются в позитивных и негативных отзывах не несут никакой пользы для нас. Можете запустить пргорамму,
она выполняется не быстро, но она не зацикливается и действительно выводит результат в виде точности алгоритма.
"""
