#!/usr/bin/env python3
##
## Copyright (C) 2015 João Ricardo Lourenço <jorl17.8@gmail.com>, João Soares <joaosoares11@hotmail.com>
##
## Github: https://github.com/Jorl17, https://github.com/xJota/
##
## Project main repository: https://github.com/xJota/NowCrawling
##
## This file is part of NowCrawling.
##
## NowCrawling is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 2 of the License, or
## (at your option) any later version.
##
## NowCrawling is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with NowCrawling.  If not, see <http://www.gnu.org/licenses/>.
##

## Order is alphabetical. Jota is the king of regexes!
__author__ = "João Ricardo Lourenço, João Soares"
__copyright__ = "Copyright 2015, João Ricardo Lourenço, João Soares"
__credits__ = ["João Ricardo Lourenço", "João Soares"]
__license__ = "GPLv2"
__email__ = ["jorl17.8@gmail.com", "joaosoares11@hotmail.com"]
__version__ = "0.9.0"

import contextlib
import os
import time
import sys
from urllib.error import ContentTooShortError, HTTPError, URLError
import urllib.request
import urllib.parse
from optparse import OptionParser, OptionGroup
import re
from timeit import default_timer as timer

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
# GLOBALS
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

# Google's search URL, used for crawling
GOOGLE_SEARCH_URL = "http://google.com/search?%s"

# Regex used to find search results
GOOGLE_SEARCH_REGEX = 'a href="[^\/]*\/\/(?!webcache).*?"'

# Regex used to find recursable URLs
RECURSION_SEARCH_REGEX = """(href="[^<>]*?")|(href=.?'[^<>]*?')"""

# A smart search is made by appending the following string to the search query
SMART_FILE_SEARCH = " intitle:index of "

# Results we ask google to give us. Might give us more. If they give us less, then there are no more results.
GOOGLE_NUM_RESULTS = 100

# The user agent we report to pages, and to google
GOOGLE_USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'

# Headers to report to pages
GLOBAL_HEADERS = {'User-Agent': GOOGLE_USER_AGENT }

# Max data size for an URL
MAX_DATA_SIZE = 25*(2**20)

# Pre-compiled regex for recursable URLs
RECURSION_COMPILED_REGEX = re.compile(RECURSION_SEARCH_REGEX, re.IGNORECASE)

##    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
## GOOGLE_SEARCH_REGEX = 'href="\/url\?q=[^\/]*\/\/(?!webcache).*?&amp'

# REGEX used to identify files. There are several placeholders which need to be replace()-ed. tagholder, typeholder,
# and holdertag.
FILE_REGEX = '((?:href|src)=[^<>]*tagholder[^<>]*\.(?:typeholder))|((?:ftp|http|https):\/\/[^<>\n\t ]*holdertag[^<>\n\t ]*\.(?:typeholder))'

YES = ['yes', 'y', 'ye']

# The default request timeout, in seconds
DEFAULT_URL_TIMEOUT = 7

# Maximum file size, in bytes, allowed. This is used when no upper bound/limit is given.
MAX_FILE_SIZE = 2**50

ALL_VISITED_URLS=[]

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

    def log ( self, message, is_bold=False, color='', log_time=True, indentation_level=0):
        prefix = ''
        suffix = ''

        if log_time:
            prefix += '[{:s}] {:s}'.format(self.get_timestamp(), '...'*indentation_level)

        if os.name.lower() == 'posix':
            if is_bold:
                prefix += self.shell_mod['BOLD']
            prefix += self.shell_mod[color.upper()]

            suffix = self.shell_mod['RESET']

        message = prefix + message + suffix
        try:
            print ( message )
        except:
            print ("Windows can't display this message.")
        sys.stdout.flush()


    def error(self, err, log_time=True, indentation_level=0):
        self.log(err, True, 'RED', log_time, indentation_level)

    def fatal_error(self, err, log_time=True, indentation_level=0):
        self.error(err, log_time, indentation_level)
        exit()

#------------------------------------------------------------------------------
# A function decorator to assign static values to functions, such as those
# found in the C-language. Example:
# @static_vars(a1=1, a2=2)
# def test():
#  ... now you can use test.a1 and test.a2 freely, and their value is kept
# between function invocations
#------------------------------------------------------------------------------
def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorate

#------------------------------------------------------------------------------
# Return a regex as a printable string. FIXME: it's currently a very raw
# prototype.
#------------------------------------------------------------------------------
def regex_as_string(url):
    return url.replace('\t', '\\t').replace('\n', '\\n')

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
# A function to convert from a human-readable size to any number of bytes.
#------------------------------------------------------------------------------
def humanReadableSizeToBytes(filesize):
    filesize = filesize.upper()
    units = [ ('EZ',2**70), ('EB', 2**60), ('PB', 2**50), ('TB', 2**40), ('GB', 2**30), ('MB', 2**20), ('KB', 2**10), ('B', 1) ]
    for unit,value in units:
        if filesize.endswith(unit):
            number = filesize[:-len(unit)].strip()
            if number.isdigit():
                return round(float(number)*value)
    return (int(filesize) if filesize.isdigit() else None)

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
def download_progress_bar(progress, speedPerSec = None, prefix='Progress'):
    progress = max(min(progress, 1), 0)
    if speedPerSec:
        speed_text = '{:s}/s '.format(humanReadableSize(speedPerSec))
    else:
        speed_text = '---B/s'
    MAX_CARDINALS = getTerminalWidth()-len('{:s}: [] 100% '.format(prefix)) - len(speed_text)
    num_cardinals = round(progress*MAX_CARDINALS)
    num_whites = MAX_CARDINALS - num_cardinals
    sys.stdout.write('\r{0}: [{1}{2}] {3}% {4}'.format(prefix, '#'*num_cardinals,' '*num_whites, round(progress*100), speed_text))
    sys.stdout.flush()


#------------------------------------------------------------------------------
# Wrapper function to perform an action only if verbosity is enabled
#------------------------------------------------------------------------------
def doVerbose(f, verbose=False):
    if verbose:
        f()


#------------------------------------------------------------------------------
# Modified urllib.request.urlretrieve which supports sending custom headers.
# It is a modified version of the same function grabbed from some python source
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
# Given a list in the form of (regex, compiled_regex) pairs, check if
# there is any match in str and return that match or False in case there wasn't
#------------------------------------------------------------------------------
def match_regex_list(s, regex_list):
    if regex_list:
        for regex,p in regex_list:
            if p.match(s):
                return regex
    return False

#------------------------------------------------------------------------------
# Given a blacklist in the form of (regex, compiled_regex) pairs, check if
# there is any match in a URL's domain and return that match or False in case
# there wasn't
#------------------------------------------------------------------------------
def is_blacklisted(url, blacklist):
    host = urllib.parse.urlsplit(url).netloc
    return match_regex_list(host, blacklist)

#------------------------------------------------------------------------------
# Given a whitelist in the form of (regex, compiled_regex) pairs, check if
# there is any match in a URL's domain and return that match or False in case
# there wasn't
#------------------------------------------------------------------------------
def is_whitelisted(url, whitelist):
    if not whitelist:
        return True
    host = urllib.parse.urlsplit(url).netloc
    return match_regex_list(host, whitelist)

#------------------------------------------------------------------------------
# Read a full webpage from a URL and return it as a string. Catch CTRL+C events
# producing a fatal error if needed. In case there is a timeout or the data
# is not available, print a message and return None
#------------------------------------------------------------------------------
def read_data_from_url(url, timeout, headers, verbose, indentation_level=0, max_data_size=MAX_DATA_SIZE, blacklist=None, whitelist=None):

    blacklist_regex = is_blacklisted(url, blacklist)
    if blacklist_regex:
        doVerbose(lambda: Logger().log("URL {:s} skipped because it's blacklisted ({:s})".format(url, regex_as_string(blacklist_regex)), False, 'YELLOW',indentation_level=indentation_level), verbose)
        return None

    if not is_whitelisted(url, whitelist):
        doVerbose(lambda: Logger().log("URL {:s} skipped because it's not whitelisted".format(url), False, 'YELLOW', indentation_level=indentation_level), verbose)
        return None

    def isValid(responseInfo):
        if 'text' in str(responseInfo.get_all("Content-Type")[0]):
            try:
                datasize = int(responseInfo.get_all("Content-Length")[0])
                return datasize <= max_data_size
            except TypeError:
                return True
        else:
            return False

    try:
        request = urllib.request.Request(url, None, headers)
        response = urllib.request.urlopen(request,timeout=timeout)
        if isValid(response.info()):
            return str(response.read())
        else:
            doVerbose(lambda: Logger().log('URL {:s} does not look like a web page'.format(url), True, 'RED', indentation_level=indentation_level),verbose)
    except KeyboardInterrupt:
        Logger().fatal_error('Interrupted. Exiting...', indentation_level=indentation_level)
    except HTTPError as e:
        doVerbose(lambda: Logger().log('URL {:s} not available or timed out ({:d})'.format(url, e.code), True, 'RED', indentation_level=indentation_level),verbose)
    except URLError as e:
        if 'win' in os.name.lower():
            doVerbose(lambda: Logger().log('URL {:s} not available or timed out (URL Error)'.format(url),True, 'RED', indentation_level=indentation_level), verbose)
        else:
            doVerbose(lambda: Logger().log('URL {:s} not available or timed out (URL Error: {:s})'.format(url, str(e.reason)),True, 'RED', indentation_level=indentation_level), verbose)
    except Exception as e:
        if 'win' in os.name.lower():
            doVerbose(lambda: Logger().log('URL {:s} not available or timed out'.format(url),True, 'RED', indentation_level=indentation_level), verbose)
        else:
            doVerbose(lambda: Logger().log('URL {:s} not available or timed out ({:s})'.format(url, str(e)),True, 'RED', indentation_level=indentation_level), verbose)
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
    data = read_data_from_url(url, None, GLOBAL_HEADERS, True)
    if not data:
        Logger().fatal_error('Cannot crawl google (perhaps a temporary ban?). Quitting.')

    p = re.compile(GOOGLE_SEARCH_REGEX, re.IGNORECASE)

    ##return list(set(x.replace('href="/url?q=', '').replace('HREF="/url?q=', '').replace('"', '').replace('&amp', '') for x in p.findall(data)))
    return list(set(x.replace('a href=', '').replace('a HREF=', '').replace('"', '').replace('A HREF=', '') for x in p.findall(data)))

#------------------------------------------------------------------------------
# Regex parsing and building
#------------------------------------------------------------------------------

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
    regex_str = userRegex
    if getfiles:
        if not tags and not userRegex:
            regex_str = FILE_REGEX.replace('tagholder', '').replace('typeholder', getTypesRe(types)).replace('holdertag','')
        elif tags:
            regex_str = FILE_REGEX.replace('tagholder', getTagsRe(tags, 1)).replace('typeholder', getTypesRe(types)).replace('holdertag',getTagsRe(tags, 2))
        else:
            regex_str = FILE_REGEX.replace('tagholder', userRegex).replace('typeholder', getTypesRe(types)).replace('holdertag', userRegex)

    return re.compile(regex_str,re.IGNORECASE),regex_str

#------------------------------------------------------------------------------
# Webpage crawling
#------------------------------------------------------------------------------

def findRecursableURLS(text,crawlurl):
    prettyurls = [''.join(x) for x in RECURSION_COMPILED_REGEX.findall(text)]
    prettyurls = list(set(x.replace('href=', '').replace('HREF=', '').replace('"', '').replace('\'','').replace('\\','') for x in prettyurls))
    prettyurls = [urllib.parse.urljoin(crawlurl,url) for url in prettyurls]
    return prettyurls

def recursiveCrawlURLForMatches(crawlurl, getfiles, compiled_regex, verbose, timeout, blacklist, whitelist, currentDepth=0, maxDepth=2, visitedUrls=[], prepend=''):
    # Stop if we have exceeded maxDepth
    if currentDepth > maxDepth:
        return []

    if maxDepth != 0:
        doVerbose(lambda: Logger().log('{:s}Recursively crawling into {:s} (depth {:d}, max depth {:d}).'.format(prepend,crawlurl, currentDepth+1, maxDepth+1), indentation_level=currentDepth),verbose)
    else:
        doVerbose(lambda: Logger().log('{:s}Crawling into {:s}'.format(prepend,crawlurl), indentation_level=currentDepth), verbose)

    visitedUrls += [crawlurl]

    data = read_data_from_url(crawlurl, timeout, GLOBAL_HEADERS, verbose, currentDepth, blacklist=blacklist, whitelist=whitelist)
    if not data:
        #doVerbose(lambda: Logger().log('{:s}Could not access {:s}.'.format(prepend,crawlurl), indentation_level=currentDepth), verbose)
        return []

    if currentDepth < maxDepth:
        urls = [url for url in findRecursableURLS(data,crawlurl) if url not in visitedUrls]
    else:
        if maxDepth != 0:
            doVerbose(lambda: Logger().log('{:s}Max depth reached, not listing URLs and not recursing.'.format(prepend), indentation_level=currentDepth), verbose)

    matches = crawlURLForMatches(crawlurl, getfiles, compiled_regex, verbose, timeout, blacklist, whitelist, currentDepth+1, data)

    if currentDepth < maxDepth:
        if not urls:
            doVerbose(lambda: Logger().log('{:s}No URLs found in {:s}: '.format(prepend,crawlurl), indentation_level=currentDepth), verbose)

        else:
            doVerbose(lambda: Logger().log('{:s}Recursable non-visited URLs found in {:s}: '.format(prepend,crawlurl) + ', '.join(urls), indentation_level=currentDepth), verbose)
            for url_number,url in enumerate(urls):
                recurse_prepend = prepend[:-2] + ', {:d}/{:d}] '.format(url_number+1, len(urls))
                matches += recursiveCrawlURLForMatches(url, getfiles, compiled_regex, verbose, timeout, blacklist, whitelist, currentDepth+1, maxDepth, visitedUrls, recurse_prepend)
    return matches

# This is Jota's crazy magic trick
def crawlURLForMatches(crawlurl, getfiles, compiled_regex, verbose, timeout, blacklist, whitelist, indentationLevel, data=None):
    doVerbose(lambda: Logger().log('Looking for matches in {:s} ...'.format(crawlurl), indentation_level=indentationLevel), verbose)
    if not data:
        data = read_data_from_url(crawlurl, timeout, GLOBAL_HEADERS, verbose, indentationLevel, blacklist=blacklist, whitelist=whitelist)
    if not data:
        return []

    doVerbose(lambda: Logger().log('Page downloaded. Checking...', indentation_level=indentationLevel), verbose)

    tuples = compiled_regex.findall(data)
    if not tuples:
        doVerbose(lambda: Logger().log('Done looking for matches in {:s}... Found no matches.'.format(crawlurl), indentation_level=indentationLevel), verbose)
        return []

    if getfiles:
        tuples = [j[i] for j in tuples for i in range(len(j)) if '.' in j[i]]
        for i,x in enumerate(tuples):
            if x.lower().startswith('href='):
                tuples[i] = x[5:]
            elif x.lower().startswith('src='):
                tuples[i] = x[4:]
            tuples[i] = tuples[i].replace('"', '').replace('\'', '').replace('\\', '')

        # Resolve all URLs (might be relative, absolute, prepended with //, and others. urlib.parse.urljoin deals with
        # this for us)
        prettyurls = [urllib.parse.urljoin(crawlurl,url) for url in tuples]
    else:
        ## RETURN EVERYTHING IF TUPLES
        if isinstance(tuples[0],tuple):
            prettyurls = list(j[i] for j in tuples for i in range(len(j)))
        else:
            prettyurls = list(x for x in tuples)

    matches = list(set(prettyurls))
    doVerbose(lambda: Logger().log('Done looking for matches in {:s}...Found {:d} matches.'.format(crawlurl, len(matches)), indentation_level=indentationLevel), verbose)
    return [[i,crawlurl] for i in matches]

#------------------------------------------------------------------------------
# File downloading
#------------------------------------------------------------------------------

def downloadFile(file, directory, filename):
    DOWNLOAD_FILE_WINDOW_SIZE = 5
    DOWNLOAD_FILE_SAMPLING_SECONDS = 0.5

    @static_vars(last_time=timer(), speeds=[], accumulator=0)
    def reporthook(blocknum, bs, size):
        now = timer()
        if (size < 0):
            download_progress_bar(1)
        else:
            reporthook.accumulator += bs
            diff = now - reporthook.last_time
            if diff >= DOWNLOAD_FILE_SAMPLING_SECONDS:
                downloadFile.last_time = now
                speed = reporthook.accumulator / diff
                downloadFile.accumulator = 0
                if len(reporthook.speeds) == DOWNLOAD_FILE_WINDOW_SIZE:
                    reporthook.speeds = reporthook.speeds[1:] + [speed]
                else:
                    reporthook.speeds += [speed]

            if reporthook.speeds:
                download_progress_bar(min(size,blocknum*bs/size), sum(reporthook.speeds)/len(reporthook.speeds) )
            else:
                download_progress_bar(min(size, blocknum * bs / size))

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
        print()
        Logger().log('Download of file {:s} interrupted. Continuing...'.format(file),color='YELLOW')
        return False
    return True

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
    for file,sourceurl in downloadurls:

        # Check if we've reached the maximum number of files
        if maxfiles and downloaded >= maxfiles:
            doVerbose(lambda: Logger().log('All files have been downloaded. Exiting...', True, 'GREEN'), verbose)
            exit()

        doVerbose(lambda: Logger().log('Checking '+file), verbose)
        filename = urllib.parse.unquote(file.split('/')[-1])
        try:
            filesize = get_filesize(file, timeout, GLOBAL_HEADERS)

            # Check filesize
            if check_filesize_bounds(filesize, filename, minsize, maxsize, limit, verbose):
                # Check with user
                if ask:
                    Logger().log('Download file {:s} of size {:s} from {:s} [real source: {:s}]? [y/n]: '.format(filename, humanReadableSize(filesize) if filesize>=0 else 'Unknown', file, sourceurl),color='DARKCYAN')
                    choice = input().lower()
                    if choice not in YES:
                        continue

                # Get the file
                Logger().log('Downloading file {:s} of size {:s}'.format(filename, humanReadableSize(filesize) if filesize>=0 else 'Unknown'),color='GREEN')
                if downloadFile(file, directory, filename):
                    Logger().log('Done downloading file {:s}'.format(filename),color='GREEN')
                downloaded += 1
        except KeyboardInterrupt:
            Logger().fatal_error('Interrupted. Exiting...')
        except HTTPError as e:
            Logger().log('File {:s} from {:s} not available ({:d})'.format(file, searchurl, e.code), True, 'RED')
        except URLError as e:
            if 'win' in os.name.lower():
                doVerbose(lambda: Logger().log('File {:s} from {:s} not available (URL Error)'.format(file, searchurl), True, 'RED'), verbose);
            else:
                doVerbose(lambda: Logger().log('File {:s} from {:s} not available (URL Error: {:s})'.format(file, searchurl, str(e.reason)), True, 'RED'), verbose);
        except Exception as e:
            if 'win' in os.name.lower():
                doVerbose(lambda: Logger().log('File {:s} from {:s} not available'.format(file, searchurl), True, 'RED'), verbose);
            else:
                doVerbose(lambda: Logger().log('File {:s} from {:s} not available ({:s})'.format(file, searchurl, str(e)), True, 'RED'), verbose);

    return downloaded

#------------------------------------------------------------------------------
# Main Crawler code
#------------------------------------------------------------------------------

def getMinMaxSizeFromLimit(limit):
    if limit:
        minsize, maxsize = limit.split('-')
        if not minsize:
            minsize = '0'
        if not maxsize:
            maxsize = str(MAX_FILE_SIZE)

        maxsize = humanReadableSizeToBytes(maxsize)
        minsize = humanReadableSizeToBytes(minsize)

        if maxsize==None or minsize==None:
            return None
        if maxsize < minsize:
            Logger().log("You are dumb, but it's fine, I will swap limits", color='YELLOW')
            return maxsize, minsize
        return minsize, maxsize
    else:
        return 0, MAX_FILE_SIZE

def build_regex_list_from_file(file_path):
    with open(file_path) as f:
        lines = [line.strip() for line in f.readlines() if not line.strip().startswith('#')]
        return [ (regex, re.compile('^'+regex+'$', re.IGNORECASE)) for regex in lines]

# When in content mode, use this to log all the matches. Possibly logging to an output file.
def logKeywordMatches(matches, contentFile):
    for match in matches:
        Logger().log(match, color='GREEN')
        if contentFile:
            with open(contentFile, 'a') as f:
                f.write(match + "\n")

# Fetch URLs to crawl from Google or directly from the user supplied list
def fetch_urls(url_list, keywords, start, smart, url_list_supplied, verbose):
    if url_list_supplied:
        doVerbose(lambda: Logger().log('Using URL list:'), verbose)
        for url in url_list:
            doVerbose(lambda: Logger().log('\t{:s}'.format(url)), verbose)
    else:
        doVerbose(lambda: Logger().log('Fetching {:d} results from Google.'.format(GOOGLE_NUM_RESULTS)), verbose)
        url_list = crawlGoogle(GOOGLE_NUM_RESULTS, start, keywords, smart)
        doVerbose(lambda: Logger().log('Fetched {:d} results.'.format(len(url_list))), verbose)

    return url_list

def crawl(getfiles, keywords, extensions, smart, tags, regex, ask, limit, maxfiles, directory, contentFile, verbose, timeout, recursion_depth, blacklist_file, whitelist_file, url_list):
    downloaded = 0
    start = 0
    minsize, maxsize = limit if limit else 0, MAX_FILE_SIZE
    compiled_regex,regex_str = build_regex(getfiles, tags, regex, extensions)
    blacklist = build_regex_list_from_file(blacklist_file) if blacklist_file else []
    whitelist = build_regex_list_from_file(whitelist_file) if whitelist_file else []
    url_list_supplied = (url_list != None)

    doVerbose(lambda: Logger().log('Search regex: ->\'{:s}\'<-.'.format(regex_as_string(regex_str))), verbose)
    try:
        while True:
            # Fetch results from google or use user-supplied url list
            url_list = fetch_urls(url_list, keywords, start, smart, url_list_supplied, verbose)

            # Find matches in results. if getfiles, then these are urls
            for url_number,searchurl in enumerate(url_list):
                matches = recursiveCrawlURLForMatches(searchurl, getfiles, compiled_regex, verbose, timeout, blacklist, whitelist, maxDepth=recursion_depth ,visitedUrls=ALL_VISITED_URLS, prepend='[{:d}/{:d}] '.format(url_number+1, len(url_list)))
                urllib.request.urlcleanup()
                if not matches:
                    doVerbose(lambda: Logger().log('No results in '+searchurl), verbose)
                else:
                    # Got results
                    matchnames = [match for match,url in matches]
                    if getfiles:
                        doVerbose(lambda: Logger().log('Files: \t' + '\n\t'.join(matchnames)), verbose)
                        downloaded += downloadFiles(downloaded, matches, ask, searchurl, maxfiles, limit,minsize, maxsize, directory,verbose,timeout)
                    else:
                        doVerbose(lambda: Logger().log('Results: \t' + '\n\t'.join(matchnames)), verbose)
                        logKeywordMatches(matchnames, contentFile)

            # Stop if:
            # a) We were given a URL list and so, we're done
            # b) We were searching Google, but they gave us less results than we asked for, thus we've reached the end
            if url_list_supplied or len(url_list) < GOOGLE_NUM_RESULTS:
                Logger().log('No more results. Exiting.', True, 'GREEN')
                break

            start+=len(url_list)
    except KeyboardInterrupt:
        Logger().fatal_error('Interrupted. Exiting...')

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
# Input parsing
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

def get_url_list(file_path):
    with open(file_path) as f:
        return [url.strip() for url in f.readlines() if not url.startswith('#')]


def parse_input():
    parser = OptionParser(description='NowCrawling version {:s} by {:s}.'.format(__version__, ' & '.join(__credits__)))
    parser.add_option('-f', '--files', help='Crawl for files', action="store_true", dest="getfiles")
    parser.add_option('-c', '--content', help='Crawl for content (words, strings, pages, regexes)', action="store_false", dest="getfiles")
    parser.add_option('-k', '--keywords', help='(Required) A quoted list of words separated by spaces which will be the search terms of the crawler', dest='keywords', type='string')
    parser.add_option('-i', '--ignore-after', help='Time (in seconds) for an URL to be considered down (Default: 7)', dest='timeout', type='int', default=DEFAULT_URL_TIMEOUT)
    parser.add_option('-z', '--recursion-depth', help='Recursion depth (starts at 1, which means no recursion). Default: 1', dest='recursion_depth', type='int', default=1)
    parser.add_option('-v', '--verbose', help='Display all error/warning/info messages', action="store_true", dest="verbose",default=False)
    parser.add_option('-b', '--blacklist', help="Provide a BLACKLIST file for DOMAINS. One regex per line (use '#' for comments). e.g., to match all .com domains: '.*\.com'.", type="string", dest="blacklist_file",default=None)
    parser.add_option('-w', '--whitelist', help="Provide a WHITELIST file for DOMAINS. One regex per line (use '#' for comments). e.g., to match all .com domains: '.*\.com'.", type="string", dest="whitelist_file", default=None)
    parser.add_option('-u', '--url-list', help='Provide a list of URLs to use for crawling, instead of performing a google search. The list can be supplied in two ways: 1) a simple comma-separated list of URLs which begins with the keyword "list:" (e.g. -u "list:http://a.com,http://b.com") or 2) the path to a file which contains one URL per line, prefixed by the keyword "file:" (e.g. -u "file:a_file.txt"). In this file, use \'#\' for comments.',type="string", dest="url_list", default=None)

    filesgroup = OptionGroup(parser, "Files (-f) Crawler Arguments")
    filesgroup.add_option('-a', '--ask', help='Ask before downloading', action="store_true", dest="ask", default=False)
    filesgroup.add_option('-l', '--limit', help='File size limit in bytes separated by a hyphen (example: 500-1200 for files between 500 and 1200 bytes, -500 for files smaller than 500 bytes, 500- for files larger than 500 bytes. You can use human-readable suffixes such as MB, KB, GB, etc. E.g.: 50MB- means files larger than 50 MB) (Default: None)', dest="limit", type='string', default=None)
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
    if options.getfiles and not options.keywords and not options.url_list:
        parser.error('You must either specify keywords (-k) or a URL list (-u) when crawling for files.')
    if not options.getfiles and not options.keywords:
        parser.error('You must specify keywords when crawling for content.')
    if options.getfiles and options.tags and options.regex:
        parser.error("You can't pick both file name search options: -t or -r/-m")
    if options.getfiles and options.limit:
        if '-' not in options.limit:
            parser.error('Limits must be separated by a hyphen.')
        options.limit = getMinMaxSizeFromLimit(options.limit)
        if not options.limit:
            parser.error('Invalid limits supplied.')
    if not options.getfiles and not options.regex:
        parser.error('You must specify a matching regex (-m/-r) when crawling for content.')
    if not options.getfiles and (options.ask or options.limit or options.maxfiles or options.smart):
        parser.error('Options -a, -l, -n, -s and -t can only be used when crawling for files.')
    if options.getfiles and options.contentFile:
        parser.error('Options -o can only be used when crawling for content.')
    if options.recursion_depth < 1:
        parser.error('Recursion depth must be greater than 0')
    if options.blacklist_file and options.whitelist_file:
        parser.error('Cannot use blacklist and whitelist at the same time. Use either blacklist (-b), whitelist (-w) or none (default).')
    if options.url_list and (options.keywords or options.smart):
        parser.error("Cannot use URL list (-u) with keyword (-k) and/or smart search (-s). What's the point of supplying keywords for a google search if we're not searching google?")

    if options.url_list:
        if options.url_list.lower().startswith('list:'):
            options.url_list = [url.strip() for url in options.url_list[5:].split(',')]
        elif options.url_list.lower().startswith('file:'):
            options.url_list = get_url_list(options.url_list[5:].strip())
        else:
            parser.error('A URL list (-u) must be prefixed with the "list:" or the "file:" keyword to indicate a comma-separated list of URLs or a file with one URL per line.')
    # Adjust the offset (we expect it to start at 0)
    options.recursion_depth -= 1

    return options.getfiles, options.keywords, options.extensions, options.smart, options.tags, options.regex, options.ask, options.limit, options.maxfiles, options.directory, options.contentFile, options.verbose, options.timeout, options.recursion_depth, options.blacklist_file, options.whitelist_file, options.url_list

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

