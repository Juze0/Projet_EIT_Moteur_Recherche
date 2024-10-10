import Tools
import Tools2

# Test the normalize method
link = "./wiki_split_extract_2k"
tools = Tools.Tools()
tools2 = Tools2.Tools2()


#tokens = tools.normalize_spacy(link)
#lemmas = tools.lemmatize_nltk(tokens)
#word_count = tools.count_words(lemmas)

#tokens2 = tools2.normalize_spacy(link)
#lemmas2 = tools.lemmatize_spacy(tokens2)
#word_count2 = tools.count_words(lemmas2)

#index = tools.create_index_nltk(link)
inversed_index = tools.create_inversed_index_nltk(link, True)

#print(index,'\n')
#print(lemmas,'\n')
#print(tools.count_words(lemmas),'\n')

#print(tokens2,'\n')
#print(lemmas2,'\n')
#print(tools2.count_words(lemmas2),'\n')