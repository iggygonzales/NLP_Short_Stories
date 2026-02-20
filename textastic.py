"""
DS 3500 HW 7 Extensible NLP Frameworks
Gabrielle Bambalan, Desiree DeGennaro, Zoe Chapman, Miguel (Iggy) Gonzales
Description: Reusable library for text analysis and comparison
"""
from statistics import mean
import matplotlib.pyplot as plt
import random as rnd
from collections import Counter, defaultdict
import nltk
from fitz import fitz
from matplotlib.sankey import Sankey
import plotly.graph_objects as go
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
import numpy as np
import string
from wordcloud import WordCloud


class Textastic:
    def __init__(self):
        self.data = defaultdict(dict)  # default dictionary of dictionaries

    @staticmethod
    def _default_parser(filename):
        """a default text parser for processing simple unformatted text files"""
        translator = str.maketrans('', '', string.punctuation)
        with fitz.open(filename) as file:
            text = ""
            for page in file:
                text += page.get_text()

            # standardize and count words
            word_counts = Counter()
            total_num_words = 0
            for word in text.lower().split():
                word = word.translate(translator)
                word_counts[word] += 1
                total_num_words += 1

            # create dict of word counts and word length
            word_dict = {'word_count': word_counts, 'numwords': total_num_words}
            print(word_dict)
            return word_dict

    def custom_parser(self, filename):
        """custom text parser for processing text files with tokens"""
        with fitz.open(filename) as file:
            text = ""
            for page in file:
                text += page.get_text()
            tokens = word_tokenize(text)
            stopwords = self.load_stop_words('stopwords.txt')
            filtered_tokens = [word for word in tokens if word not in stopwords]
            word_counts = Counter(filtered_tokens)
            total_num_words = len(filtered_tokens)
            return {'word_count': word_counts, 'numwords': total_num_words}

    def load_text(self, filename, label=None, default_parser=True, custom_parser=None):
        # default parser should take a regular text file with no special parsing
        # result is a dictionary

        if default_parser:
            results = self._default_parser(filename)
        elif custom_parser is not None:
            results = self.custom_parser(filename)
        else:
            raise ValueError("Either use_default_parser or custom_parser must be specified.")

        if label is None:
            label = filename

        for k, v in results.items():
            self.data[k][label] = v

        return results

    def load_stop_words(self, stopfile):
        """loads in a list of stop words from a file"""
        with open(stopfile) as file:
            content = file.readlines()
            stopwords = [i.strip() for i in content]
        print(stopwords)
        return stopwords

    # Below are functions for visualization purposes:

    def wordcount_sankey(self, word_list=None, k=5, stopwords=None):
        """ Sankey diagram for word counts """
        common_words = []
        for label in self.data['word_count']:
            filtered_word_counts = {
                word: count for word, count in self.data['word_count'][label].items() if word not in stopwords
            }
            word_lists = Counter(filtered_word_counts).most_common(k)
            common_words.extend(word for word, _ in word_lists)
        print(common_words)

        # sankey
        sources = []
        targets = []
        values = []
        label_mapping = {}
        for i, label in enumerate(self.data['word_count']):
            label_mapping[label] = i
            word_count = self.data['word_count'][label]
            for word, count in word_count.items():
                if word in common_words:
                    sources.append(i)
                    targets.append(len(self.data['word_count']) + common_words.index(word))
                    values.append(count)

        # plot
        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=list(self.data['word_count']) + common_words,
            ),
            link=dict(
                source=sources,
                target=targets,
                value=values
            )
        )])
        fig.show()

    def word_cloud(self, filename, stopwords=None):
        """ creates word cloud """
        word_dict = self._default_parser(filename)
        word_count_filtered = {word: count for word, count in word_dict['word_count'].items() if
                               word not in stopwords}
        word_freq = word_count_filtered
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_freq)
        return wordcloud

    def plot_word_clouds(self, files, stopwords=None):
        """Plots word clouds for each PDF file in a subplot"""
        num_files = len(files)
        num_rows = 2
        num_cols = (num_files + 1) // num_rows  # Adjust number of columns based on number of files
        fig, axes = plt.subplots(nrows=num_rows, ncols=num_cols, figsize=(15, 8))
        if num_files == 1:
            axes = [[axes]]  # Convert to a list of a list if only one file
        for i, f in enumerate(files):
            row = i // num_cols
            col = i % num_cols
            wordcloud = self.word_cloud(f, stopwords)
            ax = axes[row][col] if num_files > 1 else axes[0][0]  # Adjust indexing for single subplot
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.set_title(f, fontsize=18)
            ax.axis('off')
        plt.tight_layout()
        plt.show()

    def perform_sentiment_analysis(self, filename):
        """ gets sentiment score along each sentence and plots graph"""
        word_dict = self.custom_parser(filename)
        text = ' '.join([word + ' ' * count for word, count in word_dict['word_count'].items()])
        sid = SentimentIntensityAnalyzer()
        sentiment_scores = [sid.polarity_scores(sentence)['compound'] for sentence in nltk.sent_tokenize(text)]
        total_sentiment_score = mean(sentiment_scores)
        print(total_sentiment_score)
        return total_sentiment_score

    def plot_sentiment_analysis(self, files):
        """ plots sentiment score across different files"""
        # Perform sentiment analysis and sum the sentiment scores for each dictionary
        sentiment_scores = []
        for pdf in files:
            total_sentiment_score = self.perform_sentiment_analysis(pdf)
            sentiment_scores.append(total_sentiment_score)

        # Plotting
        plt.figure(figsize=(10, 6))
        plt.bar(range(len(files)), sentiment_scores, align='center')  # Specify x-coordinates and heights
        plt.xticks(range(len(files)), files, rotation=45)  # Set x-tick labels to file names
        plt.xlabel('File')
        plt.ylabel('Total Sentiment Score')
        plt.title('Comparison of Total Sentiment Scores for Short Stories')
        plt.tight_layout()
        plt.show()


