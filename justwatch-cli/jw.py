#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import argparse

from simplejustwatchapi.justwatch import search
from rich import print
from rich.table import Table
from imdb import Cinemagoer

USE_IMDB = True
VERBOSE = False

# Edit this to add the services you have available
AVAILABLE_SERVICES = [ "netflix", "max", "amazon prime video", "filmin", "movistar plus" ]

ia = Cinemagoer()

def vprint(data):
    if VERBOSE:
        print(data)

def colorize_services(offers):
    ret = []
    for offer in offers:
        if any([offer.lower() == i.lower() for i in AVAILABLE_SERVICES]):
            ret.append(f"[bright_green]{offer}[/bright_green]")
        else:
            ret.append(f"{offer}")
    return ", ".join(ret)


def do_query(query, use_imdb=False, lang="ES", country="es", limit=5, year=None, renting=False):
    vprint(f"Searching for \"{query}\"")
    results = search(query, lang, country, limit, True)
    if not results:
        print("No results found")
        return

    table = Table(title="Results")
    table.add_column("Title", style="cyan")

    ## It is done like that because rich tables cannot be sorted or columns move
    if VERBOSE:
        table.add_column("ID", style="magenta")

    table.add_column("released", style="green")

    if use_imdb:
        table.add_column("score", style="red")

    table.add_column("streaming", style="grey66")

    if renting:
        table.add_column("renting", style="grey66")

    for c, result in enumerate(results):
        vprint(f"Parsing result {c}")
        if result.release_year and year and result.release_year not in range(year-5, year+5):
            vprint(f"Skipping [b]\"{result.title}\" ({result.release_year})[/b] because it's not in the year range.")
            continue
        offers= []
        rent = []
        #print(json.dumps(result, indent=4))

        for i in result.offers:
            if i.monetization_type.lower() == "flatrate":
                offers.append(f"{i.package.name}")
            if i.monetization_type.lower() == "rent":
                rent.append(f"{i.package.name}")
        score = "N/A"
        if use_imdb and result.imdb_id:
            try:
                score_q = ia.get_movie(result.imdb_id[2:])
                if score_q:
                    score = score_q['rating']
            except Expception as e:
                vprint(f"Error getting IMDB score: {e}")
                score = "Error"

        items = [result.title, str(result.entry_id) if VERBOSE else None, str(result.release_year), str(score) if use_imdb else None, colorize_services(offers) if offers else "Not available for streaming", (colorize_services(rent) if rent else "Not available for rent") if renting else None]

        table.add_row(*[i for i in items if i is not None])

    if table.row_count:
        print(table)
    else:
        print("No results found")

def main():
    parser = argparse.ArgumentParser(description="JustWatch CLI")
    parser.add_argument("query", nargs='?', type=str, help="Search query")
    parser.add_argument("--imdb", action="store_true", help="Use IMDB to get ratings")
    parser.add_argument("--lang", type=str, default="ES", help="Language to use. Defaults to 'es'")
    parser.add_argument("--country", type=str, default="es", help="Country to use. Defaults to 'ES'. ")
    parser.add_argument("--limit", type=int, default=5, help="Limit results to this number")
    parser.add_argument("--year", type=int, help="Year when you think it was release. It will automatically add +5 and -5 years to the number.")
    parser.add_argument("--rent", action="store_true", help="Show also renting options")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")

    args = parser.parse_args()

    VERBOSE = args.verbose

    if args.query:
        do_query(args.query, use_imdb=args.imdb, lang=args.lang, country=args.country, limit=args.limit, year=args.year, renting=args.rent)
        sys.exit()

    try:
        while True:
            query = input("Enter a search query: ")

            if query.lower() == "exit":
                break
            do_query(query, use_imdb=args.imdb, lang=args.lang, country=args.country, limit=args.limit, year=args.year, renting=args.rent)
    except KeyboardInterrupt:
        print("Exiting...")
        sys.exit()

if __name__ == "__main__":
    main()

