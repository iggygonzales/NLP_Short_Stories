""""
file: main.py
desc: main file for nlp
uncomment things to test
"""

# Import the Textastic class
from textastic import Textastic

files = ['A_Sound_of_Thunder.pdf', 'Black_Cat.pdf', 'The_Mark_on_the_Wall.pdf',
         'The_Snows_of_Kilimanjaro.pdf', 'The_Story_of_an_Hour.pdf', 'Tell-Tale-Heart.pdf']


def main():

    # Downlod if needed
    # nltk.download()

    textastic = Textastic()

    # Load text using default parser
    cat = textastic.load_text("Black_Cat.pdf", label='The Black Cat')
    thunder = textastic.load_text(filename = "A_Sound_of_Thunder.pdf", label='A Sound of Thunder')
    wall = textastic.load_text(filename="The_Mark_on_the_Wall.pdf", label='The Mark on the Wall')
    snows = textastic.load_text(filename="The_Snows_of_Kilimanjaro.pdf", label='The Snows of Kilimanjaro')
    hour = textastic.load_text(filename="The_Story_of_an_Hour.pdf", label='The Story of an Hour')
    heart = textastic.load_text(filename="Tell-Tale-Heart.pdf", label='Tell-Tale-Heart')

    # Load stop words
    stopwords = textastic.load_stop_words("stopwords.txt")

    # Visualize word count using Sankey diagram
    textastic.wordcount_sankey(word_list=[cat, thunder, wall, snows, hour, heart], k=3, stopwords=stopwords)

    # Creates word cloud
    textastic.plot_word_clouds(files, stopwords=stopwords)

    # Creates sentiment graph
    textastic.plot_sentiment_analysis(files)



if __name__ == '__main__':
    main()



