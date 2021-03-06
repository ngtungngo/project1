import csv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from pathlib import Path
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

print("File      Path:", Path(__file__).absolute())
print("Directory Path:", Path().absolute())


def main():
    b = Path(__file__).parent.joinpath('books.csv').open()
    reader = csv.reader(b)

    for isbn, title, author, year in reader:
        print(f"{isbn} {title} {author} {year}")

    for isbn, title, author, year in reader:
        db.execute("INSERT INTO books (isbn, title, author, publication_year) VALUES (:isbn, :title, :author, :year)",
                   {"isbn": isbn, "title": title, "author": author, "year": year})
    db.commit()


if __name__ == "__main__":
    main()
