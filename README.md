# NLP Short Stories

A Northeastern University advanced programming project for text analysis and comparison of classic short stories using Natural Language Processing (NLP) techniques.

## Project Overview

This project implements an extensible NLP framework called **Textastic** that provides a suite of tools for analyzing and visualizing text data from PDF documents. The analysis includes word frequency analysis, sentiment analysis, and comparative visualizations across multiple short stories.

## Team

- Desiree DeGennaro
- Zoe Chapman
- Gabrielle Bambalan
- Miguel (Iggy) Gonzales

## Features

### Core Analysis Capabilities

1. **Text Parsing** - Extract and process text from PDF files
   - Default parser: Basic word counting and frequency analysis
   - Custom parser: Advanced tokenization with stopword filtering

2. **Word Analysis**
   - Word frequency counting
   - Stopword filtering
   - Sankey diagram visualization of word distributions

3. **Sentiment Analysis**
   - Sentence-level sentiment scoring
   - Comparative sentiment analysis across multiple texts
   - Bar chart visualization of sentiment scores

4. **Visualization**
   - Word clouds for individual documents
   - Sankey diagrams for word frequency flow
   - Sentiment comparison charts

## Project Structure

```
NLP_Short_Stories/
├── main.py                           # Main entry point
├── textastic.py                      # Textastic NLP framework class
├── metadata.yml                      # Project metadata
├── A_Sound_of_Thunder.pdf           # Sample text: "A Sound of Thunder" by Ray Bradbury
├── Black_Cat.pdf                    # Sample text: "The Black Cat" by Edgar Allan Poe
├── Tell-Tale-Heart.pdf              # Sample text: "The Tell-Tale Heart" by Edgar Allan Poe
├── The_Mark_on_the_Wall.pdf         # Sample text: "The Mark on the Wall" by Virginia Woolf
├── The_Snows_of_Kilimanjaro.pdf    # Sample text: "The Snows of Kilimanjaro" by Ernest Hemingway
├── The_Story_of_an_Hour.pdf         # Sample text: "The Story of an Hour" by Kate Chopin
├── RISE_Poster_Template_Modified_Group 24.pptx  # Project presentation
└── stopwords.txt                    # Common English stopwords (required for filtering)
```

## Installation & Dependencies

### Requirements
- Python 3.x
- nltk
- matplotlib
- plotly
- PyMuPDF (fitz)
- wordcloud
- numpy

### Setup

1. Clone the repository:
```bash
git clone https://github.com/iggygonzales/NLP_Short_Stories.git
cd NLP_Short_Stories
```

2. Install dependencies:
```bash
pip install nltk matplotlib plotly PyMuPDF wordcloud numpy
```

3. Download NLTK data (run once):
```python
import nltk
nltk.download()  # Downloads required NLTK datasets
```

4. Ensure `stopwords.txt` is in the project directory

## Usage

### Basic Usage

Run the main script to perform all analyses on the included short stories:

```bash
python main.py
```

This will:
1. Load all PDF files with custom labels
2. Load English stopwords
3. Generate a Sankey diagram showing word frequency flow
4. Create word clouds for each story
5. Perform and visualize sentiment analysis

### Using the Textastic Library

```python
from textastic import Textastic

# Initialize
textastic = Textastic()

# Load a text file
text_data = textastic.load_text("story.pdf", label="My Story")

# Load stopwords
stopwords = textastic.load_stop_words("stopwords.txt")

# Generate visualizations
textastic.wordcount_sankey(word_list=[text_data], k=5, stopwords=stopwords)
textastic.plot_word_clouds(["story.pdf"], stopwords=stopwords)
textastic.plot_sentiment_analysis(["story.pdf"])
```

## Textastic Class Reference

### Overview

The `Textastic` class is the core of the NLP framework, providing methods for text processing, analysis, and visualization. It uses a defaultdict structure to store word counts and other metrics for multiple texts.

### Class Initialization

```python
textastic = Textastic()
```

### Methods

#### `load_text(filename, label=None, default_parser=True, custom_parser=None)`

Loads and processes a text file from a PDF.

**Parameters:**
- `filename` (str): Path to the PDF file
- `label` (str, optional): Custom label for the text. Defaults to filename if not provided
- `default_parser` (bool): If True, uses the default parser for basic word counting
- `custom_parser` (bool, optional): If True, uses custom parser with tokenization

**Returns:** 
- Dictionary containing:
  - `'word_count'`: Counter object with word frequencies
  - `'numwords'`: Total number of words (after parsing)

**Example:**
```python
cat = textastic.load_text("Black_Cat.pdf", label='The Black Cat')
```

#### `load_stop_words(stopfile)`

Loads a list of stopwords from a file (one word per line).

**Parameters:**
- `stopfile` (str): Path to the stopwords file

**Returns:** List of stopwords (strings)

**Example:**
```python
stopwords = textastic.load_stop_words("stopwords.txt")
```

#### `wordcount_sankey(word_list=None, k=5, stopwords=None)`

Creates an interactive Sankey diagram showing word distribution flow across multiple texts.

**Parameters:**
- `word_list` (list, optional): List of text data dictionaries to visualize
- `k` (int): Number of top words to display per text (default: 5)
- `stopwords` (list, optional): List of words to filter out before visualization

**Returns:** None (displays interactive Plotly visualization)

**Example:**
```python
textastic.wordcount_sankey(word_list=[cat, thunder], k=3, stopwords=stopwords)
```

#### `word_cloud(filename, stopwords=None)`

Generates a word cloud for a single text file.

**Parameters:**
- `filename` (str): Path to the PDF file
- `stopwords` (list, optional): List of words to filter out

**Returns:** WordCloud object

**Example:**
```python
cloud = textastic.word_cloud("Black_Cat.pdf", stopwords=stopwords)
```

#### `plot_word_clouds(files, stopwords=None)`

Generates and displays word clouds for multiple PDF files in a subplot grid.

**Parameters:**
- `files` (list): List of PDF filenames
- `stopwords` (list, optional): List of words to filter out

**Returns:** None (displays matplotlib figure with subplots)

**Example:**
```python
textastic.plot_word_clouds(
    ["Black_Cat.pdf", "Tell-Tale-Heart.pdf"], 
    stopwords=stopwords
)
```

#### `perform_sentiment_analysis(filename)`

Calculates the average sentiment score for a single file using NLTK's Sentiment Intensity Analyzer.

**Parameters:**
- `filename` (str): Path to the PDF file

**Returns:** Float representing the compound sentiment score (-1.0 to 1.0)
- -1.0: Most negative
- 0.0: Neutral
- 1.0: Most positive

**Example:**
```python
score = textastic.perform_sentiment_analysis("Black_Cat.pdf")
print(f"Sentiment score: {score}")
```

#### `plot_sentiment_analysis(files)`

Performs sentiment analysis on multiple files and creates a comparative bar chart.

**Parameters:**
- `files` (list): List of PDF filenames

**Returns:** None (displays matplotlib bar chart)

**Example:**
```python
textastic.plot_sentiment_analysis([
    "Black_Cat.pdf", 
    "Tell-Tale-Heart.pdf",
    "A_Sound_of_Thunder.pdf"
])
```

### Internal Methods

#### `_default_parser(filename)` [Static Method]

Default parser for basic text processing without advanced tokenization.

**Process:**
1. Opens PDF file using fitz
2. Extracts text from all pages
3. Counts word frequency (case-insensitive)
4. Removes punctuation

**Returns:** Dictionary with `'word_count'` and `'numwords'`

#### `custom_parser(filename)`

Advanced parser with NLTK tokenization and stopword filtering.

**Process:**
1. Opens PDF file
2. Extracts and tokenizes text
3. Loads stopwords
4. Filters out stopwords and counts remaining words

**Returns:** Dictionary with `'word_count'` and `'numwords'`

## Sample Stories Included

1. **A Sound of Thunder** - Ray Bradbury
   - Science fiction story about time travel and consequences
   
2. **The Black Cat** - Edgar Allan Poe
   - Gothic psychological horror story
   
3. **The Tell-Tale Heart** - Edgar Allan Poe
   - Psychological thriller told from narrator's perspective
   
4. **The Mark on the Wall** - Virginia Woolf
   - Modernist stream-of-consciousness narrative
   
5. **The Snows of Kilimanjaro** - Ernest Hemingway
   - Literary fiction exploring mortality and regret
   
6. **The Story of an Hour** - Kate Chopin
   - Short story about a woman's reaction to her husband's death

## Technologies & Libraries Used

### Core Libraries
- **NLTK (Natural Language Toolkit)** - Text processing and sentiment analysis
  - `nltk.sentiment.SentimentIntensityAnalyzer` - Sentiment scoring
  - `nltk.tokenize.word_tokenize` - Text tokenization
  - `nltk.sent_tokenize` - Sentence tokenization

- **PyMuPDF (fitz)** - PDF text extraction
  - `fitz.open()` - Open and read PDF files
  - `page.get_text()` - Extract text from pages

- **Matplotlib** - Static data visualization
  - Word cloud display
  - Sentiment analysis bar charts
  - Subplot management

- **Plotly** - Interactive data visualization
  - `plotly.graph_objects.Sankey` - Interactive Sankey diagrams

- **WordCloud** - Word frequency visualization
  - `WordCloud.generate_from_frequencies()` - Cloud generation

- **Python Standard Library**
  - `collections.Counter` - Word frequency counting
  - `collections.defaultdict` - Multi-level data storage
  - `statistics.mean` - Average calculations
  - `string.punctuation` - Punctuation removal

## Important Notes

- **Stopwords File Required:** The `stopwords.txt` file must be present in the project directory for proper word filtering
- **PDF Processing:** Ensure all PDF files are in the same directory as the scripts
- **NLTK Data:** First-time usage requires downloading NLTK datasets via `nltk.download()`
- **Visualization Display:** Word cloud and sentiment charts require interactive display capability (Jupyter notebooks, IDE, or terminal with display support)
- **Optional Uncommented Features:** The `main.py` file has optional code that can be uncommented for selective testing

## Future Enhancement Possibilities

- Support for additional file formats (TXT, DOCX, HTML, etc.)
- Named Entity Recognition (NER) for identifying people, places, and things
- Topic modeling using Latent Dirichlet Allocation (LDA)
- Advanced keyword extraction with TF-IDF
- Comparative text analysis (similarity scoring between texts)
- Export functionality for analysis results (CSV, JSON, PDF reports)
- Interactive dashboard for real-time analysis
- Support for multiple languages
- Text summarization capabilities
- Author style analysis

## Troubleshooting

### Common Issues

**Issue:** `ModuleNotFoundError: No module named 'fitz'`
- **Solution:** Install PyMuPDF: `pip install PyMuPDF`

**Issue:** `FileNotFoundError: stopwords.txt not found`
- **Solution:** Create a stopwords.txt file in the project directory with common English stopwords (one per line)

**Issue:** NLTK data errors
- **Solution:** Run `nltk.download()` to download required datasets

**Issue:** No visualization display
- **Solution:** Ensure you have matplotlib backend configured or use Jupyter notebook for better visualization support

## How to Extend the Framework

### Adding a New Visualization

```python
def plot_custom_visualization(self, files):
    """Custom visualization method"""
    # Your implementation here
    pass
```

### Adding a New Parser

```python
def my_custom_parser(self, filename):
    """Custom parsing logic"""
    # Your implementation here
    return {'word_count': counter_obj, 'numwords': total}
```

## Contributing

This is an academic project. For questions or improvements, please contact Miguel Gonzales.
 
**Language:** Python 3  
**License:** Educational Use
