import MySQLdb
import assymcrypt
from werkzeug.security import generate_password_hash


def hashword(word):
    """salted"""
    return generate_password_hash(word)


def opendb():
    return MySQLdb.connect(host="localhost", user="demo", passwd="demo",db="challenge", unix_socket="/var/run/mysqld/mysqld.sock")


def createtable():
    db = opendb()
    cur = db.cursor()
    cur.execute("CREATE TABLE words (wordhash VARCHAR(128), word VARCHAR(60000), freq int, PRIMARY KEY (wordhash));")
    db.close()


def addsamplerows():
    db = opendb()
    cur = db.cursor()
    try:
        cur.execute('INSERT INTO words (wordhash, word, freq) VALUES ("blah_hashed", "xxxxyyyyzzzz_enc", 2);')
        db.commit() 
    except MySQLdb.IntegrityError:
        pass
    finally:
        db.close()

def trackword(crypt, word, count):
    """
    if there update it, otherwise insert
    """
    db = opendb()
    cur = db.cursor()
    try:

        wordhash = hashword(word)
        rowcount = cur.execute('SELECT * FROM words WHERE wordhash="{}";'.format(wordhash))
        if rowcount == 0:
            encryptword = crypt.en(word)
            cur.execute('INSERT INTO words (wordhash, word, freq) VALUES ("{}", "{}", {});'.format(wordhash, encryptword, count))
        else:
            found = cur.fetchone()
            newcount = found[2] + count
            cur.execute('UPDATE words SET freq={} WHERE wordhash="{}";'.format(newcount, wordhash))
        db.commit()

    except MySQLdb.IntegrityError:
        pass
    finally:
        db.close()

def trackwords(ordered):
    """
    todo: this would be done in a transaction instead of one of a time
    """
    crypt = assymcrypt.Crypt()
    for word, count in ordered.iteritems():
        trackword(crypt, word, count)

def listwords():
    """
    returns a list of lists (word, count pair), not an ordered dict
    """
    crypt = assymcrypt.Crypt()
    db = opendb()
    cur = db.cursor()
    words = [ ]
    try:
        cur.execute('SELECT * FROM words ORDER BY freq DESC;')
        for row in cur:
            actualword = crypt.de(row[1])
            words.append([ actualword, row[2] ])

    except MySQLdb.IntegrityError:
        pass
    finally:
        db.close()

    return words
 


if __name__ == "__main__":
    #createtable()
    #addsamplerows()
    #trackword('really', 8)
    pass

