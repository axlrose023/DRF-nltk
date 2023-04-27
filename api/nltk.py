import nltk
import itertools

class TreeTextRetriever:
    def __init__(self, tree):
        self.tree = tree

    def get_text(self):
        tree = nltk.tree.ParentedTree.fromstring(self.tree)
        leaves = tree.leaves()
        text = ' '.join(leaf for leaf in leaves)
        return text


class NounPhraseExtractor:
    def __init__(self, text, tree):
        self.text = text
        self.tree = tree
        self.sentences = nltk.sent_tokenize(self.text)
        self.all_noun_phrases = []
        self.grammar = r"""
          NP: {<DT|PRP\$>?<JJ.*>*<NN.*>+}
          CONJ: {<,|CC>}
          MULTI_NP: {<NP>(<CONJ><NP>)+}
        """

        self.parser = nltk.RegexpParser(self.grammar)

    def extract_noun_phrases(self):
        for sentence in self.sentences:
            words = nltk.word_tokenize(sentence)
            tagged_words = nltk.pos_tag(words)
            tree = self.parser.parse(tagged_words)

            for subtree in tree.subtrees():
                if subtree.label() == 'NP':
                    noun_phrase = ' '.join(word for word, tag in subtree.leaves())
                    self.all_noun_phrases.append(noun_phrase)

        permutations = list(itertools.permutations(self.all_noun_phrases, 2))

        modified_trees = []
        for permutation in permutations:
            modified_tree = self.tree.replace(permutation[0], permutation[1])
            if modified_tree != self.tree:
                modified_trees.append({"tree": modified_tree})

        return {"paraphrases": modified_trees}
