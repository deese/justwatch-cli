#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" JustWatch CLI """
import sys
import argparse
from typing import NamedTuple

from simplejustwatchapi.justwatch import search
from rich import print as r_print
from rich.table import Table
from imdb import Cinemagoer

VERBOSE = False

# Edit this to add the services you have available
AVAILABLE_SERVICES = ["netflix", "max",
                      "amazon prime video", "filmin", "movistar plus"]

DEFAULTS = {
    "lang": "ES",
    "country": "es",
    "limit": 5
}

ia = Cinemagoer()

class Config(NamedTuple):
    """ Configuration for the app """
    use_imdb: bool
    lang: str
    country: str
    limit: int
    year: int
    renting: bool

    @property
    def year_range(self):
        """ Return the year range """
        return range(self.year - 5, self.year + 5)

def vprint(data):
    """ Print if Verbose is enabled """
    if VERBOSE:
        r_print(data)


def colorize_services(offers):
    """ Colorize the services available to the user  """
    ret = []
    for offer in offers:
        if any(offer.lower() == i.lower() for i in AVAILABLE_SERVICES):
            ret.append(f"[bright_green]{offer}[/bright_green]")
        else:
            ret.append(f"{offer}")
    return ", ".join(ret)

def build_table(use_imdb, renting):
    """ Build the table """
    table = Table(title="Results")
    table.add_column("Title", style="cyan")

    # It is done like that because rich tables cannot be sorted or columns move
    if VERBOSE:
        table.add_column("ID", style="magenta")

    table.add_column("released", style="green")

    if use_imdb:
        table.add_column("score", style="red")

    table.add_column("streaming", style="grey66")

    if renting:
        table.add_column("renting", style="grey66")

    return table

def do_query(query, config):
    """ Execute the query to JW """

    vprint(f"Searching for \"{query}\"")
    results = search(query, config.lang, config.country, config.limit, True)

    if not results:
        print("No results found")
        return

    table = build_table(config.use_imdb, config.renting)

    for cnt, result in enumerate(results):
        vprint(f"Parsing result {cnt}")
        if result.release_year and config.year and result.release_year not in config.year_range:
            vprint(f"Skipping [b]\"{result.title}\""
                   "({result.release_year})[/b] because it's not in the year range.")
            continue
        offers = []
        rent = []

        for i in result.offers:
            if i.monetization_type.lower() == "flatrate":
                offers.append(f"{i.package.name}")
            if i.monetization_type.lower() == "rent":
                rent.append(f"{i.package.name}")

        score = "N/A"
        if config.use_imdb and result.imdb_id:
            try:
                score_q = ia.get_movie(result.imdb_id[2:])
                if score_q:
                    score = score_q['rating']
            except Exception as ex: #pylint: disable=broad-except
                vprint(f"Error getting IMDB score: {ex}")
                score = "Error"

        items = [result.title, str(result.entry_id) if VERBOSE else None,
                 str(result.release_year), str(score) if config.use_imdb else None,
                 colorize_services(offers) if offers
                 else "Not available for streaming",
                 (colorize_services(rent) if rent
                  else "Not available for rent")
                 if config.renting else None]

        table.add_row(*[i for i in items if i is not None])

    if table.row_count:
        r_print(table)
    else:
        r_print("No results found")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="JustWatch CLI")
    parser.add_argument("query", nargs='?', type=str,
                        help="Search query")
    parser.add_argument("--imdb", action="store_true",
                        help="Use IMDB to get ratings")
    parser.add_argument("--lang", type=str, default=DEFAULTS["lang"],
                        help=f"Language to use. Defaults to '{DEFAULTS['lang']}'")
    parser.add_argument("--country", type=str, default=DEFAULTS["country"],
                        help=f"Country to use. Defaults to '{DEFAULTS['country']}'. ")
    parser.add_argument("--limit", type=int, default=DEFAULTS["limit"],
                        help="Limit results to this number")
    parser.add_argument("--year", type=int, default=0,
                        help="Year when you think it was "
                        "release. It will automatically add +5 and -5 years "
                        "to the number.")
    parser.add_argument("--rent", action="store_true",
                        help="Show also renting options")
    parser.add_argument("--verbose", action="store_true",
                        help="Verbose output")

    args = parser.parse_args()

    VERBOSE = args.verbose

    if args.query:
        do_query(args.query, config=Config(args.imdb, args.lang,
                 args.country, args.limit, args.year, args.rent))
        sys.exit()

    try:
        while True:
            in_query = input("Enter a search query: ")

            if in_query.lower() == "exit":
                break
            do_query(in_query, config=Config(args.imdb, args.lang,
                 args.country, args.limit, args.year, args.rent))
    except KeyboardInterrupt:
        r_print("Exiting...")
        sys.exit()
