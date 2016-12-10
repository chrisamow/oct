from .. wordcloud import words,rmstopwords,wordcount,jsify


def test_simple():
        data = "these "*5 + "are,"*3 + "uniqueunique " + "some.words!"*2
        w = words(data)
        print (w)
        print ('total words: {}'.format(len(w)))
        assert len(w) == 13
        x = rmstopwords(w)
        print (x)
        assert len(x) == 3
        assert "uniqueunique" in x
        print ('without stopwords: {}'.format(len(x)))
        counts = wordcount(x)

        print ('counts: {}'.format(counts))

        z = jsify(counts)
        print ('js format: {}'.format(z))


if __name__ == '__main__':
    test_simple()

