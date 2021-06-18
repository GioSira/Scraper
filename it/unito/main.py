import sys
from optparse import OptionParser

from it.unito import *
from it.unito.scraper.Scraper import Scraper


def main():
    scraper = Scraper(options.facet, options.threads, options.restart)
    scraper.extract_items()


if __name__ == '__main__':
    argv = sys.argv[1:]
    parser = OptionParser()

    parser.add_option('-f', '--facet', help='facet file path', action="store", type="string", dest="facet",
                      default="/Users/giovanni/PycharmProjects/Scraper/data/prova")
    parser.add_option('-t', '--threads', help='number of threads', action="store", type="int", dest="threads",
                      default=3)
    parser.add_option('-r', '--restart', help='restart scraping, i.e. it deletes the urls log', action='store',
                      dest='restart', default=False)

    (options, args) = parser.parse_args()

    main()
