from mediawiki import MediaWiki
from flair.data import Sentence
from flair.models import SequenceTagger
from transformers import pipeline
import logging



class WikiFinder:
    def __init__(self) -> None:
        self.tagger = SequenceTagger.load('flair/ner-english')
        self.wikipedia = MediaWiki()
    
    def ner_predict(self, question):
        sentence = Sentence(question)
        self.tagger.predict(sentence)
        entities = [entity for entity in sentence.get_spans('ner')]
        return entities

    def find_wikis(self, word):
        if not isinstance(word, str):
            word = word.to_original_text()
        return self.wikipedia.search(word)

    def read_content(self, page):
        return self.wikipedia.page(page).content

    def get_url(self, page):
        return self.wikipedia.page(page).url

class FindAnswers:
    def __init__(self):
        self.nlp = pipeline("question-answering")
        self.wf = WikiFinder()

    def ExtractText(self, question, context):
        return self.nlp(question=question, context=context)

    def AnswerQuestion(self, question):
        logging.info(f"Answering qn :{question}")
        #TODO: find out why having question marks gives whacky results
        question = question.replace("?", "")
        question = question.strip()
        entities = self.wf.ner_predict(question)
        wikis = []
        answers = []
        for entity in entities:
            wikis += self.wf.find_wikis(entity)[0:1]
        for wiki in wikis:
            logging.info(f"searching wiki: {wiki}")
            context = self.wf.read_content(wiki)
            if context:
                answer = self.ExtractText(question, context)
                logging.info(answer)
                answer["wiki"] = self.wf.get_url(wiki)
                answers.append(answer)
        return self.format_output(answers)

    def format_output(self, answers):
        if answers:
            final_answer = sorted(answers, key=lambda k: k['score'], reverse=True)[0]
        else:
            return "No answers found, please try a different question"
        return f"Answer: {final_answer['answer']}, based on the wiki: {final_answer['wiki']}"
