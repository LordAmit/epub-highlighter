'''
Assumption: words are taken from memrise.com

The words are in a file in this format:

word (parts of speech)
meaning


for example:

aberrant (adjective)
markedly different from an accepted norm
aberration (noun)
a deviation from what is normal or expected
abstain (verb)
choose not to consume or take part in (particularly something enjoyable)

this will be extracted in following format:
word,-,(parts of speech) meaning
For example,

aberrant,-,(adjective) markedly different from an accepted norm
aberration,-,(noun) a deviation from what is normal or expected
abstain,-,(verb) choose not to consume or take part in (particularly something enjoyable)


'''

content = open("gre1000").readlines()

words = content[0::2]
meanings = content[1::2]

if len(words) != len(meanings):
    raise ValueError(
        "Lengths of word and meaning are supposed to be equal. Aborting.", len(words), len(meanings))

words_only = []
parts_of_speech = []

for word in words:
    split_word = str(word).split(' ', 1)
    words_only.append(split_word[0])
    parts_of_speech.append(split_word[1].strip())

aFile = open("gre1000_formatted", "w")
for i in range(0, len(words)):
    line = words_only[i] + ",-," + parts_of_speech[
        i] + " " + meanings[i].strip() + "\n"
    aFile.write(line)

aFile.close()
