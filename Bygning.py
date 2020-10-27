import psycopg2
import argparse

# -          Få ut en liste over alle bygningstyper i json-format
# -          Angi en bygningstype og få ut en oversikt i json-format over bygninger (med id, geometri og bygningstype) som har den bygningstypen.
# -          Legge til en ny bygningstype

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Hent fra, eller gi input til database")
    parser.add_argument("-userInput", help="Din hovedinput")
    parser.add_argument("--optionalUserInput", help="Ditt valgfrie navn paa bygningstype, for aa hente ut eller lage ny")
    parser.add_argument("--optionalUserIDInput", type=int, help="Din valgte ID, for aa lage ny bygningstype")
    args = parser.parse_args()

    con = psycopg2.connect(host="localhost", database="kartverket", port="5432",
                           user="postgres", password="furuheia15")
    cur = con.cursor()

    if args.userInput == "list-bygningstyper":
        cur.execute("SELECT json_build_object("
                          "'id', bt.id,"
                          "'bygningstype', bt.bygningstype) "
                          "FROM bygningstype as bt")

        rows = cur.fetchall()
        print(rows)

    if args.userInput == "vis-bygninger-med-type":
        print ("\nBygninger med type " + args.optionalUserInput + ": \n")
        cur.execute("SELECT json_build_object("
                          "'id', b.id, "
                          "'geometriNord', b.geometrinord, "
                          "'geometriOst', b.geometriost, "
                          "'bygningstype',bt.bygningstype) "
                          "FROM "
                          "bygning as b INNER JOIN bygningstype as bt "
                          "ON b.id = bt.id "
                          "WHERE bt.bygningstype = " + "'" + args.optionalUserInput + "'") #remember quotation marks to "concatenate" the args-string

        rows = cur.fetchall()
        print(rows)

    elif args.userInput == "lagre-bygningstype":
        cur.execute("INSERT INTO bygningstype(id, bygningstype) "
                    "VALUES(%s, %s)", (args.optionalUserIDInput, args.optionalUserInput))
        con.commit()

        cur.execute("SELECT * FROM bygningstype as bt "
                    "WHERE bt.bygningstype = " + "'" + args.optionalUserInput + "'")

        print("Lagt til foelgende bygningstype (id + type): \n")
        rows = cur.fetchall()
        print(rows)

    cur.close()
    con.close()#final
