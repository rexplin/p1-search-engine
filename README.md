# p1-search-engine
## Statistics on DC

## Text Processing
We used the nltk word tokenizer, and the nltk snowball stemmer, set to english words. We used a custom stopword list
that was compiled of all the suggested stopword lists. We used the nltk one as a starting point and extended it to also
use the lists found at: 
https://gist.github.com/sebleier/554280  
http://www.lemurproject.org/stopwords/stoplist.dft   
https://github.com/stanfordnlp/CoreNLP/blob/master/data/edu/stanford/nlp/patterns/surface/stopwords.txt   
https://www.ranks.nl/stopwords  
https://drive.google.com/file/d/1GgXVQg11M2h0RMftEH_-o1HPcJgsdWSw/view?usp=sharing  

#### How we Processed
Initially we we combine the title and content of the document, then we tokenize it. We then make all the tokens lowercase
and check if they are in the stop word list. If they aren't we add them to our list of filtered tokens. We then take
this list of filtered tokens, and remove tokens from it that are punctuation. Finally we stem this list to create our 
final list of tokens that is now ready to be put into our index. We then decided to check once more for stop words just 
in case anything was stemmed into one, we decided that we would get rid of it then. 
#### Text processing implementation decisions
We decided that we did want to use a stemmer for our index because we felt that the benefits from grouping similar words 
that had been stemmed to the same one, would outweigh the negatives of combining two words with similar spelling and very
different meanings. We decided to remove stopwords, because the size of the index with the stopwords left in would be 
much to large for it to be efficient. We chose to use the stopwords from several different list to try and remove as many
as we could. We felt like we were unable to add any collection specific stopwords due to the size and variety of the 
collection, so we just removed the basic sentence structure type of words. 

## Query suggestions implementation decisions

## Relevance ranking implementation decisions