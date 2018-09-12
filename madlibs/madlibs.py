from random import *

#Default prompts for words
adj_prompt = "Input adjective: "
verb_prompt = "Input verb: "
noun_prompt = "Input noun: "

#Default stories if user does not want to make their own
default_story = "One day, while *VERB my way down the street, I ran across a *ADJE *NOUN. I was very surprised, but I kept going. I then saw a *ADJE *NOUN who was *VERB. Must have been a weird day. But finally the oddest of all, I saw a *ADJE, *ADJE *NOUN *VERB a *NOUN at me, so I decided it was time to leave.\n"
#Unused default order for default story
default_order = ["verb","adj","noun", "adj","noun","verb","adj","adj","noun","verb","noun"]

#Gets user input based on type of word
def user_input(prompt, num_left):
    user_input = input(str(num_left)+" words of this type left to enter, "+prompt)
    return user_input

#Gets words from user
def get_words(number_adj,number_noun,number_verb):

    words = list()
    for x in range(number_adj):
        words.append(user_input(adj_prompt,number_adj-x))

    for x in range(number_noun):
        words.append(user_input(noun_prompt,number_noun-x))

    for x in range(number_verb):
        words.append(user_input(verb_prompt,number_verb-x))

    return words

#To create a story object
class Story:
    def __init__(self,number_adj,number_noun,number_verb,text,order):
        self.number_noun=number_noun
        self.number_adj=number_adj
        self.number_verb=number_verb
        self.text=text
        self.order=order

#Creates an ordered list for the words to be added to the story
def order_words(words,order,number_adj,number_noun,number_verb):
    adj_words=words[0:number_adj]
    noun_words=words[number_adj:number_noun+number_adj]
    verb_words=words[number_noun+number_adj:number_noun+number_adj+number_verb]
    index = 0
    for word in words:
        if(order[index] == "adj"):
            words[index] = adj_words[0]
            adj_words.pop(0)

        elif(order[index] == "noun"):
            words[index] = noun_words[0]
            noun_words.pop(0)

        elif(order[index] == "verb"):
            words[index] = verb_words[0]
            verb_words.pop(0)
        index += 1

    return words

#Takes a user story and cleans it so it works with other helper functions
def clean_user_story(text):
    clean_story=text
    num_adj=0
    num_noun=0
    num_verb=0
    order = list()
    x=0
    while x >= 0:

        x = clean_story.find("*",x)
        if(x>=0):
            if(clean_story[x+1:x+5] == "ADJE"):
                num_adj+= 1
                order.append("adj")

            elif(clean_story[x+1:x+5] == "NOUN"):
                num_noun+= 1
                order.append("noun")

            elif(clean_story[x+1:x+5] == "VERB"):
                num_verb+= 1
                order.append("verb")

            else:
                print("Input Error, * is not followed by type of word")
                selection()

            clean_story=clean_story[0:x+1]+clean_story[x+5:]
            x += 1

    story = Story(num_adj,num_noun,num_verb,clean_story,order)
    return story

#Displays story to user, either with blanks on command or after inputting words as the complete story
def display_story(story,words):
    sectioned_story=story.split('*')
    final_story = list()

    for x in range(len(words)):
        final_story.append(sectioned_story[x])
        final_story.append(words[x])

    if(len(sectioned_story)>len(words)):
        final_story.append(sectioned_story[len(sectioned_story)-1])

    for word in final_story:
        print(word,end='')

    print("\n\n")

def randomize_words(story,words):

    random_adj = list()
    random_noun = list()
    random_verb = list()
    index = 0
    for x in range (0,story.number_adj):
        index = int(random() * (story.number_adj-x))
        random_adj.append(words[index])
        words.pop(index)


    for x in range (0,story.number_noun):
        index = int(random() * (story.number_noun-x))
        random_noun.append(words[index])
        words.pop(index)


    for x in range (0,story.number_verb):
        index = int(random() * (story.number_verb-x))
        random_verb.append(words[index])
        words.pop(index)

    random_words = random_adj + random_noun + random_verb
    return random_words


#Menu for user
def selection():
    text = 0
    print("1: Use default story")
    print("2: Use own story")
    print("3: Display default story with blanks: ")
    print("4: Quit")
    choice = int(input("Input choice: "))
    print(choice)

    if choice == 1:
        print("Using default story")
        text=default_story

    elif choice == 2:
        text = input("Write your story. Write *ADJE, *NOUN or *VERB to replace later. Press RETURN when finished: ")
        if(text.find('*') == -1):
            print("Story has no words to replace!")
            return True

    elif choice == 3:
        print(default_story)
        return True

    elif choice == 4:
        raise SystemExit

    else:
        print("Error, input is not within valid range")
        return True

    story = clean_user_story(text)
    words=get_words(story.number_adj,story.number_noun,story.number_verb)
    #Test words for default story
    #words=['blue', 'polka-dotted', 'hairy', 'ugly', 'turtle', 'bear', 'hot-dog', 'king', 'talking', 'swimming', 'throwing']

    choice = 0
    while(choice == 0):
        choice = input("Would you like to randomize the words that appear in the story? (y/n): ")
        if(choice == "Y" or choice == "y"):
            words=randomize_words(story,words)
        elif(choice == "N" or choice == "n"):
            print("Replaced words will not be randomized")
        else:
            print("Error, choice is not y or n, please try again.")
            choice=0

    words=order_words(words,story.order,story.number_adj,story.number_noun,story.number_verb)
    display_story(story.text,words)
    return True

running=True
while(running):
    running = selection()
