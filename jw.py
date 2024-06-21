import sys
from simplejustwatchapi.justwatch import search
from rich import print
from rich.table import Table
from imdb import Cinemagoer
USE_IMDB = True

ia = Cinemagoer()

def do_query(query):
    results = search(query, "ES", "es", 5, True)
    if not results:
        print("No results found")
        return

    table = Table(title="Results")
    table.add_column("Title", style="cyan")
    table.add_column("ID", style="magenta")
    table.add_column("released", style="green")
    table.add_column("score", style="red")
    table.add_column("offers", style="blue")

    for result in results:
        offers= []
        for i in result.offers:
            if i.monetization_type.lower() == "flatrate":
                offers.append(f"{i.package.name}")
        score = "N/A"
        if USE_IMDB:
            score_q = ia.get_movie(result.imdb_id[2:])
            if score_q:
                score = score_q['rating']
        table.add_row(result.title, str(result.entry_id), str(result.release_year), str(score), ", ".join(offers))

    if table:
        print(table)

if len(sys.argv) >= 2:
    do_query(sys.argv[1])
    sys.exit()

while True:
    query = input("Enter a search query: ")

    if query.lower() == "exit":
        break
    do_query(query)
