# Author:       Adam Anderson
# Date:         Mar 15, 2016
# Module:       parser.py
# Python:       3.4.2

import tools
import string
from enum import Enum


class WordType(Enum):
    VERB = 0
    ADJECTIVE = 1
    NOUN = 2
    PREPOSITION = 3


class ParserContext(object):
    """
    A class representing any sort of state required for proper parser operation.  The desire is to keep the entire
    parser stateless with the exception of this class - and also to keep this class as simple as possible.

    The ParserContext is not planned to be persisted between application runs, however ,if this state proves to be
    valuable enough to keep between runs of the game, it could be persisted.
    """
    def __init__(self,adjectives=[], nouns=[], prepositions=[], verbs=[]):
        self.last_noun = None
        self.verbs = verbs
        self.nouns = nouns
        self.prepositions = prepositions
        self.adjectives = adjectives


class StatementStructure(object):
    def __init__(self, structure, unrecognized_words=[]):
        self.structure = structure
        self.unrecognizd_words = unrecognized_words

    def get_structure(self):
        """
        Returns a Tuple of the WordTypes that make up the statement structure.
        :return: a Tuple of instances of WordType which define this statement structure's statement's structure.
        """
        s = []
        for word in self.structure:
            s.append(word[0])
        return tuple(s)


class InputParser(object):

    def __init__(self):
        self.valid_structures = [(WordType.VERB, WordType.NOUN), (WordType.VERB, WordType.NOUN, WordType.PREPOSITION, WordType.NOUN)]

        # Initialize Parser Context
        a, n, p, v = self.__load_data()
        self.parser_context = ParserContext(a, n, p, v)


    def __load_data(self):
        """
        Read in the known words from files and return lists of words.
        :return: A tuple of lists of words.
        """
        adjectives = tools.read_word_file("data/adjectives.txt")
        nouns = tools.read_word_file("data/nouns.txt")
        prepositions = tools.read_word_file("data/prepositions.txt")
        verbs = tools.read_word_file("data/verbs.txt")

        return adjectives, nouns, prepositions, verbs


    def sanitize_input(self, input_string):
        """
        Remove all whitespace, punctuation and other non-essential characters and returns the input string as a list,
        split into words.

        :param input_string: the user's input string to be sanitized.

        :return: a list of clean words.  No punctuation, all lower case.
        """

        # Remove any punctuation characters from the input string.
        # probably shouldn't reconstruct this map every time we sanitize input, but for now, its cool.
        remove_punct_map = dict.fromkeys(map(ord, string.punctuation))
        input_string = input_string.translate(remove_punct_map)

        # Force to lower case.
        input_string = input_string.lower()

        # Split the string into words.
        words = input_string.split(" ")

        return words


    def __determine_structure(self, input_string):
        """
        Determines the structure of an input string, and returns a StatementStructure object describing it.
        :param input_string: the ser input string to parse to generate the StatementStructure object.
        :return:
        """
        words = self.sanitize_input(input_string)
        unrecognized = []
        structure = []
        nouns_found = 0

        for word in words:
            word = word.lower()
            # VERB
            if word in self.parser_context.verbs:
                structure.append((WordType.VERB, word))

            # NOUN
            elif word in self.parser_context.nouns:
                structure.append((WordType.NOUN, word))

                # Update Parser context with most recently referenced noun.
                nouns_found += 1
                self.parser_context.last_noun = word

            # PREP
            elif word in self.parser_context.prepositions:
                structure.append((WordType.PREPOSITION, word))

            # ADJ
            elif word in self.parser_context.adjectives:
                structure.append((WordType.ADJECTIVE, word))

            # If we didnt recognize the word as a Verb, Noun or Preposition, add it to the unrecognized word list.
            else:
                if word not in unrecognized:
                    unrecognized.append(word)

        # if more than one noun was found in this sentence, follow-on sentences can't just
        # refer to a noun indirectly, so clear the referenced noun.
        if nouns_found > 1:
            self.parser_context.last_noun = None

        return StatementStructure(tuple(structure), unrecognized)


    def parse_input(self, input_string):
        """
        This method takes an input string, sanitizes it, performs checks to ensure it is valid, and generates a
        StatementStructure object.

         Using the supplied game_state and adenture objects, the parser is able to update the game state with any relevant
         changes that have occured as a result of the supplied input..

        :param input_string: the string to parse.
        :return: None
        """

        # Generate Statement Structure
        statement = self.__determine_structure(input_string)

        print("Unrecognized Words", statement.unrecognizd_words)
        print("Structure", statement.structure)

        if statement.get_structure() in self.valid_structures:
            print("Structure supported:", statement.get_structure())
        else:
            print("Structure not supported:", statement.get_structure())