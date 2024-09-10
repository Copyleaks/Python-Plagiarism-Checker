'''
 The MIT License(MIT)

 Copyright(c) 2016 Copyleaks LTD (https://copyleaks.com)

 Permission is hereby granted, free of charge, to any person obtaining a copy
 of this software and associated documentation files (the "Software"), to deal
 in the Software without restriction, including without limitation the rights
 to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 copies of the Software, and to permit persons to whom the Software is
 furnished to do so, subject to the following conditions:

 The above copyright notice and this permission notice shall be included in all
 copies or substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 SOFTWARE.
'''

class ScoreWeights:
    def get_grammar_score_weight(self):
        return self.grammarScoreWeight

    def set_grammar_score_weight(self, value):
        assert value
        self.grammarScoreWeight = value

    def get_mechanics_score_weight(self):
        return self.mechanicsScoreWeight

    def set_mechanics_score_weight(self, value):
        assert value
        self.mechanicsScoreWeight = value

    def get_sentence_structure_score_weight(self):
        return self.sentenceStructureScoreWeight

    def set_sentence_structure_score_weight(self, value):
        assert value
        self.sentenceStructureScoreWeight = value

    def get_word_choice_score_weight(self):
        return self.wordChoiceScoreWeight

    def set_word_choice_score_weight(self, value):
        self.wordChoiceScoreWeight = value
        assert value
