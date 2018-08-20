import sys
import string
import json
import time
import re
import math


def classify(ipfile):
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
    regex = re.compile('[%s]' % re.escape(string.punctuation))

    with open(ipfile) as f, open("nbmodel.txt") as f2, open("nboutput.txt", "w") as op:

        data = json.load(f2)
        prior = data['prior']
        features = data['features']
        count = data['count']

        set_count=data['wordset_count'];

        for i in f.readlines():

            line = regex.sub(' ', i).split()
            key = line[0]
            sent = line[1:]

            class_true = math.log(prior['True'])
            class_fake = math.log(prior['Fake'])
            class_pos = math.log(prior['Pos'])
            class_neg = math.log(prior['Neg'])

            for w in sent:

                word = w.lower()

                if word in stopwords:
                    continue

                if word in features['True']:
                    class_true += math.log(features['True'][word]+1) - math.log(count['True']+set_count)
                else:
                    class_true += 0 - math.log(count['True']+set_count)

                if word in features['Fake']:
                    class_fake += math.log(features['Fake'][word]+1) - math.log(count['Fake']+set_count)
                else:
                    class_fake += 0 - math.log(count['Fake']+set_count)

                if word in features['Pos']:
                    class_pos += math.log(features['Pos'][word]+1) - math.log(count['Pos']+set_count)
                else:
                    class_pos += 0 - math.log(count['Pos']+set_count)

                if word in features['Neg']:
                    class_neg += math.log(features['Neg'][word]+1) - math.log(count['Neg']+set_count)
                else:
                    class_neg += 0 - math.log(count['Neg']+set_count)

            class1 = "True" if class_true > class_fake else "Fake"
            class2 = "Pos" if class_pos > class_neg else "Neg"

            # print class_true, class_fake
            # print class_pos, class_neg
            #
            # print key, class1,class2

            op.write(" ".join([key, class1, class2 + "\n"]))


if __name__ == "__main__":
    assert len(sys.argv) == 2

    start = time.time()

    classify(sys.argv[1])
