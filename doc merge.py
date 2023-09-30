
from book_reader import TextProcessor

import spacy
from spacy.tokens import Doc


nlp = spacy.blank('en')
doc1 = nlp(u'This is the doc number one.')
doc2 = nlp(u'And this is the doc number two.')

# Will work for few Docs, but see further recommendations below
docs=[doc1, doc2]

# `c_doc` is your "merged" doc
c_doc = Doc.from_docs(docs)
print("Merged text: ", c_doc.text)

# Some quick checks: should not trigger any error.
assert len(list(c_doc.sents)) == len(docs)
assert [str(ent) for ent in c_doc.ents] == [str(ent) for doc in docs for ent in doc.ents]
