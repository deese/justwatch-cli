import sys
import argparse

from simplejustwatchapi.justwatch import search
from rich import print
from rich.table import Table
from imdb import Cinemagoer

USE_IMDB = True
VERBOSE = False

ia = Cinemagoer()

def vprint(data):
    if VERBOSE:
        print(data)

def do_query(query, use_imdb=False, lang="ES", country="es", limit=5, year=None):
    vprint(f"Searching for \"{query}\"")
    results = search(query, lang, country, limit, True)
    if not results:
        print("No results found")
        return

    table = Table(title="Results")
    table.add_column("Title", style="cyan")
    table.add_column("ID", style="magenta")
    table.add_column("released", style="green")
    table.add_column("score", style="red")
    table.add_column("offers", style="blue")

    for c, result in enumerate(results):
        vprint(f"Parsing result {c}")
        if result.release_year and year and result.release_year not in range(year-5, year+5):
            vprint(f"Skipping [b]\"{result.title}\" ({result.release_year})[/b] because it's not in the year range.")
            continue
        #breakpoint()
        offers= []
        #print(json.dumps(result, indent=4))
        for i in result.offers:
            if i.monetization_type.lower() == "flatrate":
                offers.append(f"{i.package.name}")
        score = "N/A"
        if use_imdb and result.imdb_id:
            try:
                score_q = ia.get_movie(result.imdb_id[2:])
                if score_q:
                    score = score_q['rating']
            except Expception as e:
                vprint(f"Error getting IMDB score: {e}")

        table.add_row(result.title, str(result.entry_id), str(result.release_year), str(score), ", ".join(offers))

    if table.row_count:
        print(table)
    else:
        print("No results found")


parser = argparse.ArgumentParser(description="JustWatch CLI")
parser.add_argument("query", type=str, help="Search query")
parser.add_argument("--imdb", action="store_true", help="Use IMDB to get ratings")
parser.add_argument("--lang", type=str, default="ES", help="Language")
parser.add_argument("--country", type=str, default="es", help="Country")
parser.add_argument("--limit", type=int, default=5, help="Limit results")
parser.add_argument("--year", type=int, help="Year")
parser.add_argument("--verbose", action="store_true", help="Verbose output")

args = parser.parse_args()

VERBOSE = args.verbose

if args.query:
    do_query(args.query, use_imdb=args.imdb, lang=args.lang, country=args.country, limit=args.limit, year=args.year)
    sys.exit()

while True:
    query = input("Enter a search query: ")

    if query.lower() == "exit":
        break
    do_query(query, use_imdb=args.imdb, lang=args.lang, country=args.country, limit=args.limit, year=args.year)

