'''

@author: Miguel Maldonado
'''

template_sentence={}
template_sentence["My favourite emoji is "]=1
template_sentence["What is my favourite emoji?"]=2

QUESTION_TEMP = "What is my favourite emoji?"


def detectSentenceType(sentence):    
    for template in template_sentence.keys():
        if sentence.startswith(template):
            return template_sentence[template]
    return 0

def storeEmoji(sentence,name,users):
    users[name]["emoji"]=sentence[-1:]
    return "OK!"
    
def favoriteEmoji(name,users):
    return "Your favourite emoji is "+users[name]["emoji"]


def controller(sentence,name,users,model):
    sentence_type = detectSentenceType(sentence)
    if sentence_type == 1:
        return storeEmoji(sentence,name, users)
    elif sentence_type == 2:
        return favoriteEmoji(name,users)
    else:
        prediction = model.prediction(sentence)
        if prediction < 0.5:
            return '😥'
        else:
            return "😁"
            
            