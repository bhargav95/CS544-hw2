import sys
import string
import json
import time
import re


def naivebayesclassify(ipfile):
    stopwords = {"ourselves", "hers", "between", "yourself", "but", "again", "there", "about", "once", "during", "out",
                 "very", "having", "with", "they", "own", "an", "be", "some", "for", "do", "its", "yours", "such",
                 "into", "of", "most", "itself", "other", "off", "is", "s", "am", "or", "who", "as", "from", "him",
                 "each", "the", "themselves", "until", "below", "are", "we", "these", "your", "his", "through", "don",
                 "nor", "me", "were", "her", "more", "himself", "this", "down", "should", "our", "their", "while",
                 "above", "both", "up", "to", "ours", "had", "she", "all", "no", "when", "at", "any", "before", "them",
                 "same", "and", "been", "have", "in", "will", "on", "does", "yourselves", "then", "that", "because",
                 "what", "over", "why", "so", "can", "did", "not", "now", "under", "he", "you", "herself", "has",
                 "just", "where", "too", "only", "myself", "which", "those", "i", "after", "few", "whom", "t", "being",
                 "if", "theirs", "my", "against", "a", "by", "doing", "it", "how", "further", "was", "here", "than"}

    sum = 0.0
    prior = {"True": 0.0,
             "Fake": 0.0,
             "Pos": 0.0,
             "Neg": 0.0}

    count = {"True": 0.0,
             "Fake": 0.0,
             "Pos": 0.0,
             "Neg": 0.0}

    features = {"True": dict(),
                "Fake": dict(),
                "Pos": dict(),
                "Neg": dict()}

    bag_of_words = set()

    regex = re.compile('[%s]' % re.escape(string.punctuation))

    with open(ipfile) as f:
        for i in f.readlines():

            line = regex.sub(' ', i).split()

            id = line[0]
            class1 = line[1]
            class2 = line[2]
            sent = line[3:]

            for words in sent:
                lower = words.lower()

                if lower in stopwords:
                    continue

                bag_of_words.add(lower)

                count[class1] += 1
                count[class2] += 1

                if lower not in features[class1]:
                    features[class1][lower] = 1.0
                else:
                    features[class1][lower] += 1

                if lower not in features[class2]:
                    features[class2][lower] = 1.0
                else:
                    features[class2][lower] += 1

            prior[class1] += 1
            prior[class2] += 1
            sum += 1

        for i, v in prior.items():
            prior[i] /= sum

        prior['addone'] = 1.0 / sum
        print prior

        print count

        print len(bag_of_words)

        with open("nbmodel.txt", "w") as op:
            json.dump({"wordset_count": len(bag_of_words), "count": count, "prior": prior, "features": features}, op,
                      indent=1)


if __name__ == "__main__":
    assert len(sys.argv) == 2

    start = time.time()

    naivebayesclassify(sys.argv[1])

    print time.time() - start
