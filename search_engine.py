"""Maxwell Banks
Search Engine
CPE202
"""

import sys
import os
from linear_hash import *
import math

class SearchEngine:
    """A search engine class that builds and maintains an inverted
       index of documents stored in a specified directory and 
       provides a functionality to search documents with query terms

    Attribues:
        directory(str): a directory name
        stopwords(HashMap):a hash table containing stopwords
        doc_length(HashMap): a hash table containing the total 
            number of words in each document
        doc_freqs(HashMap): a hash table containing the number of 
            documents containing the term for each term
        term_freqs(HashMap): a hash table of hash tables for each 
            term. Each hash table contains the frequency of the 
            term in documents (document names are the keys and 
            the frequencies are the values)
    """
    def __init__(self, directory, stopwords):
        self.doc_length = HashTableLinear()
        self.doc_freqs = HashTableLinear() #this will not be used in this assignment
        self.term_freqs = HashTableLinear()
        self.stopwords = stopwords
        self.index_files(directory)

    def read_file(self, file_name):
        
        """A helper function to read a file
        Args:
            infile(str): the path to a file

        Returns:
            list: a list of str read from a file
        """
        #print('reading' + file_name)
        file = open(file_name, 'r')
        contents = file.read()
        file.close()
        return contents

    def parse_words(self, lines):
        
        """split strings into words
        Converts words to lower cases and remove new line chars.
        Excludes stopwords.
        Args:
            lines(list): a list of strings 
        Returns:
            list: a list of words
        """
        #print('\nparsing...' + str(lines))
        word_string = lines.split()
        no_stops_word_list = []
        for word in word_string:
            if word not in self.stopwords and word != '\n':
                no_stops_word_list.append(repr(word.lower()))
        return no_stops_word_list

    def count_words(self, filename, words):

        """counts words in a file and stores the frequency of each
        word in the term_freqs hash table.
        words should do not contain stopwords.
        Also stores the total count of words contained in the file
        in the doc_length hash table.
        Args:
            filename(str): the file name
            words(list): a list of words
        Returns:
            None
        """
        #print('counting...' + filename)
        count = 0
        for word in words:
            #print(word)
            count += 1
            if self.term_freqs.contains(word):
                hash_word = self.term_freqs.get(word)[1]
                hash_word.put(filename, 1)
            else:
                self.term_freqs.put(word, HashTableLinear())
                hash_word = self.term_freqs.get(word)[1]
                hash_word.put(filename, 1)

        self.doc_length.put(filename, count)


        #self.doc_length.put(filename, file_hash)




    def index_files(self, directory):

        """index all text files in a given directory 
        Args:
            directory (str) : the path of a directory
        """
        #print('indexing...' + directory)
        all_list = os.listdir(directory)
        #print(all_list)
        file_list = []
        #checking if a file is a file
        for file in all_list:
            #print(file)
            text = os.path.splitext(file)[1] == '.txt'
            #print(os.path.splitext(file))
            file_path = (os.path.join(directory, file))
            if os.path.isfile(file_path) and text:
                file_list.append(file_path)
                #print(file_path)
        #print('====================')
        #print(file_list)
        #print('====================')
        for file in file_list:
            #print(os.path.split(file))

            contents = self.read_file(file)
            word_list = self.parse_words(contents)
            self.count_words(file, word_list)


    def get_wf(self, tf):
        
        """comptes the weighted frequency 
        Args:
            tf(float): term frequency 
        Returns:
            float: the weighted frequency
        """
        #print('getting wf...' + str(tf))
        if tf > 0:
            wf = 1 + math.log(tf)
        else:
            wf = 0
        return wf

    def biggest_tuple(self, tuples):
        """Takes a list of tuples and returns the largest value and the list
        with out that value in it
        Args:
            list(list): A list of tuples with values (ANY,int)
        returns:
            tuple: The tuple with the largest [1]
            list: The remaining list
        """
        mx = tuples[0]
        del tuples[0]
        for i in range(len(tuples)):
            if tuples[i][1] > mx[1]:
                temp = tuples[i]
                tuples[i] = mx
                mx = temp
        return mx, tuples


    def get_scores(self, terms):
        """creates a list of scores for each file in corpus
        "The Score" is the weighted frequency/the total word count in the file
        our program computes this score for each term in a query and sum all the scores
        Args:
            terms (list) : a list of str
        Returns:
            list : a list of tuples, each containing the filename and its relevancy score
        """
        #scores = HashMap()
        #print('getting scores...' + str(terms))
        scores = HashTableLinear()

        #For each query term terms
        for query in terms:
            try:
                files_table = self.term_freqs.get(query)[1]
                for file_score in files_table.table:
                    if file_score is not None:
                        scores.put(file_score[0], self.get_wf(file_score[1]))
            except:
                pass
        score_list = []
        for val in scores.table:
            if val is not None and val[1] > 0:
                score_list.append((val[0], val[1]))

        ordered_score_list = []
        big = None
        while len(score_list) > 1:
            big, score_list = self.biggest_tuple(score_list)
            ordered_score_list.append(big)

        ordered_score_list.append(score_list[0])
        
        return ordered_score_list


                
            #Fetch a hash table of t from self.term_freqs
            
        #For each file in the hash table, add wf to scores[file]
        #For each file in scores, do scores[file] /= self.doc_length[file]
        #Return scores


def main():
    """The main beef of the function. Requests a user input from the
    terminal screen and uses the search engine class the find all 
    relevent documents

    Args:
        None

    Returns:
        None
    """
    file = open('stop_words.txt', 'r')
    stop_words_str = file.read()
    file.close()
    stop_words = stop_words_str.split()

    path = sys.argv[-1]
    engine = SearchEngine(path, stop_words)
    user_in = None
    while True:
        #input('Press any key to print the term frequencies')
        #print(engine.term_freqs)
        user_in = input('input: ')

        if user_in == 'q':
            break

        elif user_in == 'f':
            for word in engine.term_freqs.table:
                if word:
                    for freq in word[1].table:
                        if freq:
                            print((word[0])+ "\t:\t" + str(freq[0])\
                            + "\t" + str(freq[1]))

        elif len(user_in) < 2:
            print('Please use the "s:" followed by a path to search\
            , "f" to display the frequencies of \nthe words or the \
            "q" function to quit')
        else:
            
            parsed_input = engine.parse_words(user_in[2:])
            scores = engine.get_scores(parsed_input)
            for file in scores:
                split_file = file[0].split('/')
                print((split_file[-1], file[1]))


if __name__ == '__main__':
    main()