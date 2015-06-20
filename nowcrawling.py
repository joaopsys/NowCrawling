#!/usr/bin/env python3
import contextlib
import os
import time
import sys
from urllib.error import ContentTooShortError
import urllib.request
import urllib.parse
from optparse import OptionParser, OptionGroup
import re

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
# GLOBALS
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

# Google's search URL, used for crawling
GOOGLE_SEARCH_URL = "http://google.com/search?%s"

# Regex used to find search results
GOOGLE_SEARCH_REGEX = 'a href="[^\/]*\/\/(?!webcache).*?"'

# A smart search is made by appending the following string to the search query
SMART_FILE_SEARCH = " intitle:index of "

# Results we ask google to give us. Might give us more. If they give us less, then there are no more results.
GOOGLE_NUM_RESULTS = 100

# The user agent we report to pages, and to google
GOOGLE_USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'

# Headers to report to pages
GLOBAL_HEADERS = {'User-Agent': GOOGLE_USER_AGENT }

##    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
## GOOGLE_SEARCH_REGEX = 'href="\/url\?q=[^\/]*\/\/(?!webcache).*?&amp'

# REGEX used to identify files. There are several placeholders which need to be replace()-ed. tagholder, typeholder,
# and holdertag.
FILE_REGEX = '(href=[^<>]*tagholder[^<>]*\.(?:typeholder))|((?:ftp|http|https):\/\/[^<>\n\t ]*holdertag[^<>\n\t ]*\.(?:typeholder))'

YES = ['yes', 'y', 'ye']

# The default request timeout, in seconds
DEFAULT_URL_TIMEOUT = 7

# Maximum file size, in bytes, allowed. This is used when no upper bound/limit is given.
MAX_FILE_SIZE = 2**50

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
# UTILITY STUFF
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
# Logger class, used to log messages. A special method can be used to
# shutdown the application with an error message.
#------------------------------------------------------------------------------
class Logger:

    shell_mod = {
        '':'',
       'PURPLE' : '\033[95m',
       'CYAN' : '\033[96m',
       'DARKCYAN' : '\033[36m',
       'BLUE' : '\033[94m',
       'GREEN' : '\033[92m',
       'YELLOW' : '\033[93m',
       'RED' : '\033[91m',
       'BOLD' : '\033[1m',
       'UNDERLINE' : '\033[4m',
       'RESET' : '\033[0m'
    }

    def get_timestamp(self):
        return time.strftime('%Y/%m/%d %H:%M:%S')

    def log ( self, message, is_bold=False, color='', log_time=True):
        prefix = ''
        suffix = ''

        if log_time:
            prefix += '[{:s}] '.format(self.get_timestamp())

        if os.name == 'posix':
            if is_bold:
                prefix += self.shell_mod['BOLD']
            prefix += self.shell_mod[color.upper()]

            suffix = self.shell_mod['RESET']

        message = prefix + message + suffix
        print ( message )
        sys.stdout.flush()


    def error(self, err):
        self.log(err, True, 'RED')

    def fatal_error(self, err):
        self.error(err)
        exit()

#------------------------------------------------------------------------------
# Set of functions used for a progress bar
#------------------------------------------------------------------------------

# Adapted from the console package. Yep, it's ugly
def getTerminalWidth():
    import os
    if 'windows' in os.name.lower():
        return 80
    env = os.environ
    def ioctl_GWINSZ(fd):
        try:
            import fcntl, termios, struct, os
            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ,
        '1234'))
        except:
            return
        return cr
    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        cr = (env.get('LINES', 25), env.get('COLUMNS', 80))
    return int(cr[1])

# Invoke continuously. When finished, remember to emit a newline.
def progress_bar(progress, prefix='Progress'):
    progress = max(min(progress, 1), 0)
    MAX_CARDINALS = getTerminalWidth()-len('{:s}: [] 100%'.format(prefix))
    num_cardinals = round(progress*MAX_CARDINALS)
    num_whites = MAX_CARDINALS - num_cardinals
    sys.stdout.write('\r{0}: [{1}{2}] {3}%'.format(prefix, '#'*num_cardinals,' '*num_whites, round(progress*100)))
    sys.stdout.flush()

#------------------------------------------------------------------------------
# Set of functions used for printing human readable sizes (converting them from
# bytes to KB/MB/GB/etc).
#------------------------------------------------------------------------------

# Adapted from  http://stackoverflow.com/questions/1094841/reusable-library-to-get-human-readable-version-of-file-size
def sizeof_fmt(num, suffix='B'):
    for unit in ['','K','M','G','T','P','E','Z']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Y', suffix)

def humanReadableSize(filesize):
    return sizeof_fmt(filesize)


#------------------------------------------------------------------------------
# Wrapper function to perform an action only if verbosity is enabled
#------------------------------------------------------------------------------
def doVerbose(f, verbose=False):
    if verbose:
        f()


#------------------------------------------------------------------------------
# Modified urllib.request.urlretrieve which supports sending custom headers.
# It is a modified version of the same function grabbed from some python soruce
# code (sadly, Pycharm fucked up so I don't know what). Several things we didn't
# need were removed
#------------------------------------------------------------------------------
def url_retrieve_with_headers(url, filename=None, headers=None, reporthook=None):
    url_type, path = urllib.parse.splittype(url)
    opener = urllib.request.build_opener()
    if headers:
        opener.addheaders = list(headers.items())
    with contextlib.closing(opener.open(url)) as fp:
        headers = fp.info()

        # Just return the local path and the "headers" for file://
        # URLs. No sense in performing a copy unless requested.
        if url_type == "file" and not filename:
            return os.path.normpath(path), headers

        tfp = open(filename, 'wb')

        with tfp:
            result = filename, headers
            bs = 1024*8
            size = -1
            read = 0
            blocknum = 0
            if "content-length" in headers:
                size = int(headers["Content-Length"])

            if reporthook:
                reporthook(blocknum, bs, size)

            while True:
                block = fp.read(bs)
                if not block:
                    break
                read += len(block)
                tfp.write(block)
                blocknum += 1
                if reporthook:
                    reporthook(blocknum, bs, size)

    if size >= 0 and read < size:
        raise ContentTooShortError(
            "retrieval incomplete: got only %i out of %i bytes"
            % (read, size), result)

    return result

#------------------------------------------------------------------------------
# Read a full webpage from a URL and return it as a string. Catch CTRL+C events
# producing a fatal error if needed. In case there is a timeout or the data
# is not available, print a message and return None
#------------------------------------------------------------------------------
def read_data_from_url(url, timeout, headers, verbose):
    request = urllib.request.Request(url, None, headers)
    try:
        response = urllib.request.urlopen(request,timeout=timeout)
        return str(response.read())
    except KeyboardInterrupt:
        Logger().fatal_error('Interrupted. Exiting...')
        return None
    except:
        doVerbose(lambda: Logger().log('URL '+url+' not available or timed out', True, 'RED'), verbose)
        return None

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
# Main application code
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# Crawl google with the given query, looking for a number of results at a given
# start.
#------------------------------------------------------------------------------
def crawlGoogle(numres, start, query, doSmartSearch):
    query = urllib.parse.urlencode({'num': numres, 'q': (query+SMART_FILE_SEARCH if doSmartSearch and SMART_FILE_SEARCH not in query else query), "start": start})
    url = GOOGLE_SEARCH_URL % query
    request = urllib.request.Request(url, None, GLOBAL_HEADERS)
    response = urllib.request.urlopen(request)
    data = str(response.read())
    p = re.compile(GOOGLE_SEARCH_REGEX, re.IGNORECASE)

    ##return list(set(x.replace('href="/url?q=', '').replace('HREF="/url?q=', '').replace('"', '').replace('&amp', '') for x in p.findall(data)))
    return list(set(x.replace('a href=', '').replace('a HREF=', '').replace('"', '').replace('A HREF=', '') for x in p.findall(data)))

def getTagsRe(tags, flag):
    tagslist = tags.split()
    if flag == 1:
        tagsre = "[^<>]*".join(tagslist)
    else:
        tagsre = "[^<>\n\t ]*".join(tagslist)
    ##print(tagsre)
    return tagsre

def getTypesRe(types):
    return types.replace(' ', '|')

def build_regex(getfiles, tags, userRegex, types):
    if getfiles:
        if not tags and not userRegex:
            return FILE_REGEX.replace('tagholder', '').replace('typeholder', getTypesRe(types)).replace('holdertag','')
        elif tags:
            return FILE_REGEX.replace('tagholder', getTagsRe(tags, 1)).replace('typeholder', getTypesRe(types)).replace('holdertag',getTagsRe(tags, 2))
        else:
            return FILE_REGEX.replace('tagholder', userRegex).replace('typeholder', getTypesRe(types)).replace('holdertag', userRegex)
    else:
        return userRegex

# This is Jota's crazy magic trick
def crawlURLs(crawlurl, tags, userRegex, types, getfiles, verbose, timeout):
    data = read_data_from_url(crawlurl, timeout, GLOBAL_HEADERS, verbose)
    if not data:
        return []

    doVerbose(lambda: Logger().log('Page downloaded. Checking...'), verbose)

    regex = build_regex(getfiles, tags, userRegex, types)
    p = re.compile(regex, re.IGNORECASE)

    tuples = p.findall(data)
    if not tuples:
        return []

    if getfiles:
        tuples = [j[i] for j in tuples for i in range(len(j)) if '.' in j[i]]
        prettyurls = list(x.replace('href=', '').replace('HREF=', '').replace('"', '').replace('\'', '').replace('\\', '') for x in tuples)
        prettyurls = list(crawlurl+x if "://" not in x else x for x in prettyurls)
    else:
        ## RETURN EVERYTHING IF TUPLES
        if isinstance(tuples[0],tuple):
            prettyurls = list(j[i] for j in tuples for i in range(len(j)))
        else:
            prettyurls = list(x for x in tuples)

    return list(set(prettyurls))

def getMinMaxSizeFromLimit(limit):
    if limit:
        minsize, maxsize = limit.split('-')
        if not minsize:
            minsize = '0'
        if not maxsize:
            maxsize = str(MAX_FILE_SIZE)

        if maxsize and minsize and int(maxsize) < int(minsize):
            Logger().log("You are dumb, but it's fine, I will swap limits", color='RED')
            return int(maxsize), int(minsize)
        return int(minsize), int(maxsize)
    else:
        return 0, MAX_FILE_SIZE

def downloadFile(file, directory, filename):
    def reporthook(blocknum, bs, size):
        if (size < 0):
            progress_bar(1)
        else:
            progress_bar(min(size,blocknum*bs/size))

    # Ensure directory exists
    try:
        os.mkdir(directory)
    except:
        pass

    # Download the file and continuously update the progress
    try:
        url_retrieve_with_headers(file, os.path.join(directory, filename), headers=GLOBAL_HEADERS, reporthook=reporthook)
    except KeyboardInterrupt:
        ## FIXME Leave the half-file there? For now let's not be intrusive
        Logger().log('\nDownload of file {:s} interrupted. Continuing...'.format(file),color='YELLOW')
        return

# Get the filesize of a given URL with the given timeout and headers
def get_filesize(url, timeout, headers):
    request = urllib.request.Request(url, None, headers)
    meta = urllib.request.urlopen(request, timeout=timeout).info()
    try:
        return int(meta.get_all("Content-Length")[0])
    except TypeError:
        # No content-length. Weird but possible
        return -1

# Check that the filesize is within bounds and inform the user if it is not. Return if it is within bounds or not
def check_filesize_bounds(filesize, filename, minsize, maxsize, limit, verbose):
    if limit:
        if filesize < 0:
            doVerbose(lambda: Logger().log('Skipping file {:s} because file size cannot be determined.'.format(filename),color='YELLOW'), verbose)
            return False

        if not (minsize <= filesize <= maxsize):
            doVerbose(
            lambda: Logger().log('Skipping file {:s} because {:s} is off limits.'.format(filename, humanReadableSize(filesize)),color='YELLOW'), verbose)
        return False

    return True

# Download files from downloadurls, respecting conditions, updating file counts and printing info to user
def downloadFiles(downloaded, downloadurls, ask, searchurl, maxfiles, limit,minsize, maxsize, directory, verbose, timeout):
    for file in downloadurls:

        # Check if we've reached the maximum number of files
        if maxfiles and downloaded >= maxfiles:
            doVerbose(lambda: Logger().log('All files have been downloaded. Exiting...', True, 'GREEN'), verbose)
            exit()

        doVerbose(lambda: Logger().log(Logger().log('Checking '+file), verbose))
        filename = urllib.parse.unquote(file.split('/')[-1])
        try:
            filesize = get_filesize(file, timeout, GLOBAL_HEADERS)

            # Check filesize
            if check_filesize_bounds(filesize, filename, minsize, maxsize, limit, verbose):
                # Check with user
                if ask:
                    Logger().log('Download file {:s} of size {:s} from {:s}? [y/n]: '.format(filename, humanReadableSize(filesize) if filesize>=0 else 'Unknown', file),color='DARKCYAN')
                    choice = input().lower()
                    if choice not in YES:
                        continue

                # Get the file
                doVerbose(lambda: Logger().log('Downloading file {:s} of size {:s}'.format(filename, humanReadableSize(filesize) if filesize>=0 else 'Unknown'),color='GREEN'), verbose)
                downloadFile(file, directory, filename)
                doVerbose(lambda: Logger().log('Done downloading file {:s}'.format(filename),color='GREEN'), verbose)
                downloaded += 1
        except KeyboardInterrupt:
            Logger().fatal_error('Interrupted. Exiting...')
        except:
            doVerbose(lambda: Logger().log('File ' + file + ' from ' + searchurl + ' not available', True, 'RED'),
                      verbose)
            #raise

    return downloaded

# When in content mode, use this to log all the matches. Possibly logging to an output file.
def logKeywordMatches(matches, contentFile):
    for match in matches:
        Logger().log(match, color='GREEN')
        if contentFile:
            with open(contentFile, 'a') as f:
                f.write(match + "\n")


def crawl(getfiles, keywords, extensions, smart, tags, regex, ask, limit, maxfiles, directory, contentFile, verbose, timeout):
    downloaded = 0
    start = 0
    minsize, maxsize = getMinMaxSizeFromLimit(limit)
    try:
        while True:
            # Fetch results
            doVerbose(lambda: Logger().log('Fetching {:d} results.'.format(GOOGLE_NUM_RESULTS)), verbose)
            googleurls = crawlGoogle(GOOGLE_NUM_RESULTS, start, keywords, smart)
            ##FIXME: It disgusts me to see all of this here
            ##fixme a good test for content length
            #googleurls=['http://www.vulture.com/2015/06/game-of-thrones-adaptation-debate.html']
            ##fixme a good test for urls regex
            #googleurls=['http://www.amazon.com/Tchaikovsky-Music-Index-Gerald-Abraham/dp/0781296269']
            ##fixme a good test for forbidden
            #googleurls=['http://0audio.com/downloads/Game%20of%20Thrones%20S01%20Ep%2001-10/']
            ##FIXME            http://www.newgrounds.com/games spit out a 500 once
            doVerbose(lambda: Logger().log('Fetched {:d} results.'.format(len(googleurls))),verbose)

            # Find matches in results. if getfiles, then these are urls
            for searchurl in googleurls:
                doVerbose(lambda: Logger().log('Crawling into '+searchurl+' ...'), verbose)
                matches = crawlURLs(searchurl, tags, regex, extensions, getfiles, verbose, timeout)
                doVerbose(lambda: Logger().log('Done crawling {:s}.'.format(searchurl)), verbose)
                urllib.request.urlcleanup()
                if not matches:
                    doVerbose(lambda: Logger().log('No results in '+searchurl), verbose)
                else:
                    doVerbose(lambda: Logger().log('Files: \t' + '\n\t'.join(matches)), verbose)
                    # Got results
                    if getfiles:
                        downloaded += downloadFiles(downloaded, matches, ask, searchurl, maxfiles, limit,minsize, maxsize, directory,verbose,timeout)
                    else:
                        logKeywordMatches(matches, contentFile)

            # If google gave us less results than we asked for, then we've reached the end
            if len(googleurls) < GOOGLE_NUM_RESULTS:
                Logger().log('No more results. Exiting.', True, 'GREEN')
                break

            start+=len(googleurls)
    except KeyboardInterrupt:
        Logger().fatal_error('Interrupted. Exiting...')

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
# Input parsing
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

def parse_input():
    parser = OptionParser()
    parser.add_option('-f', '--files', help='Crawl for files', action="store_true", dest="getfiles")
    parser.add_option('-c', '--content', help='Crawl for content (words, strings, pages, regexes)', action="store_false", dest="getfiles")
    parser.add_option('-k', '--keywords', help='(Required) A quoted list of words separated by spaces which will be the search terms of the crawler', dest='keywords', type='string')
    parser.add_option('-i', '--ignore-after', help='Time (in seconds) for an URL to be considered down (Default: 7)', dest='timeout', type='int', default=DEFAULT_URL_TIMEOUT)
    parser.add_option('-v', '--verbose', help='Display all error/warning/info messages', action="store_true", dest="verbose",default=False)

    filesgroup = OptionGroup(parser, "Files (-f) Crawler Arguments")
    filesgroup.add_option('-a', '--ask', help='Ask before downloading', action="store_true", dest="ask", default=False)
    filesgroup.add_option('-l', '--limit', help='File size limit in bytes separated by a hyphen (example: 500-1200 for files between 500 and 1200 bytes, -500 for files smaller than 500 bytes, 500- for files larger than 500 bytes) (Default: None)', dest="limit", type='string', default=None)
    filesgroup.add_option('-n', '--number', help='Number of files to download until crawler stops (Default: Max)', dest="maxfiles", type='int', default=None)
    filesgroup.add_option('-e', '--extensions', help='A quoted list of file extensions separated by spaces. Default: all', dest='extensions', type='string', default='[a-zA-Z0-9]+')
    filesgroup.add_option('-s', '--smart', help='Smart file search, will highly reduce the crawling time but might not crawl all the results. Basically the same as appending \'intitle:index of\' to your keywords.', action="store_true", dest="smart", default=False)
    filesgroup.add_option('-d', '--directory', help='Directory to download files to. Will be created if it does not exist. Default is current directory', type="string", dest="directory", default='.')

    filenamegroup = OptionGroup(parser, "File Names Options", "You can only pick one."" If none are picked, EVERY file matching the specified extension will be downloaded")
    filenamegroup.add_option('-t', '--tags', help='A quoted list of words separated by spaces that must be present in the file name that you\'re crawling for', dest='tags', type='string')
    filenamegroup.add_option('-r', '--regex', help='Instead of tags you can just specify a regex for the file name you\'re looking for', dest='regex', type='string')
    ##TODO FIXME -R STILL NEEDS TESTING!
    ##TODO FIXME MAIS UM ARGUMENTO COM UM SITE ESPECIFICO PARA NAO TER DE IR AO GOOGLE
    parser.add_option_group(filesgroup)
    parser.add_option_group(filenamegroup)

    contentgroup = OptionGroup(parser, "Content (-c) Crawler Arguments")
    contentgroup.add_option('-m', '--match', help='(Required) A regex that will match the content you are crawling for', dest='regex', type='string')
    contentgroup.add_option('-o', '--output-file', help='Output file to store content matches', dest='contentFile', type='string')

    parser.add_option_group(contentgroup)

    (options, args) = parser.parse_args()

    if options.getfiles is None:
        parser.error('You must specify the crawler type: -f for files or -c for content')
    if options.getfiles and not options.keywords:
        parser.error('You must specify keywords (-k) when crawling for files.')
    if not options.getfiles and not options.keywords:
        parser.error('You must specify keywords when crawling for content.')
    if options.getfiles and options.tags and options.regex:
        parser.error("You can't pick both file name search options: -t or -r/-m")
    if options.getfiles and options.limit and '-' not in options.limit:
        parser.error('Limits must be separated by a hyphen.')
    if not options.getfiles and not options.regex:
        parser.error('You must specify a matching regex (-m/-r) when crawling for content.')
    if not options.getfiles and (options.ask or options.limit or options.maxfiles or options.smart):
        parser.error('Options -a, -l, -n, -s and -t can only be used when crawling for files.')
    if options.getfiles and options.contentFile:
        parser.error('Options -o can only be used when crawling for content.')

    return options.getfiles, options.keywords, options.extensions, options.smart, options.tags, options.regex, options.ask, options.limit, options.maxfiles, options.directory, options.contentFile, options.verbose, options.timeout

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
# Main
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

def main():
    try:
        #crawl(True, "pink floyd", "mp3", True, None, None, False, None, None, '.', None, True)
        crawl(*parse_input())
    except KeyboardInterrupt:
        Logger().fatal_error('Interrupted. Exiting...')

if __name__ == '__main__':
    main()

