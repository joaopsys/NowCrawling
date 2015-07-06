# NowCrawling
**NowCrawling** intially started as a **Google crawler**, automating file and pattern searches. It has since become a more **general crawler capable of easily finding patterns and files in user supplied URLs**. It is written in Python 3 and is compatible with the latest PyPy release for maximum performance. It also works in every major platform out there (Windows and *nix).

**So what's it really all about?** Lots of things! Want to search for a generic wallpaper and download all the images you can find? Want to google for all emails from a given domain? Want to automatically download all listed files in a certain webserver? **NowCrawling** helps you do this, with loads of options.

[Below](#example-usage) is a sequence of example use cases with a detailed explanation. For a more detailed FAQ, see [here](#faq).

Table of Contents
=================
  
  * **[Example Usage](#example-usage)**
    * **[File Crawling Mode examples](#file-crawling-mode-examples)**
      * [Downloading an episode of a TV series](#downloading-an-episode-of-a-tv-series)
      * [Downloading a song](#downloading-a-song)
      * [Downloading lots of HD wallpapers to a specific folder](#downloading-lots-of-hd-wallpapers-to-a-specific-folder)
      * [Downloading files off of your own URLs](#downloading-files-off-of-your-own-urls)
      * [Using your own regexes](#using-your-own-regexes)
    * **[Content Crawling Mode examples](#content-crawling-mode-examples)**
      * [Finding leaked gmail addresses](#finding-leaked-gmail-addresses)
      * [Finding leaked gmail addresses <em>and</em> passwords](#finding-leaked-gmail-addresses-and-passwords)
      * [Finding credit card numbers on the web](#finding-credit-card-numbers-on-the-web
    * **[Advanced Crawling](#advanced-crawling)**
      * [Going deeper: crawling linked pages too (e.g. folders in fileservers)](#going-deeper-crawling-linked-pages-too-eg-folders-in-fileservers
      * [Verbosity](#verbosity)
      * [Whitelists and Blacklists](#whitelists-and-blacklists)
      * [Finding leaked emails and passwords with better regexes](#finding-leaked-emails-and-passwords-with-better-regexes
  * **[FAQ](#faq)**
    * [How does NowCrawling really work?](#how-does-nowcrawling-really-work)
    * [Is this illegal?](#is-this-illegal)
    * [How does NowCrawling deal with javascript?](#how-does-nowcrawling-deal-with-javascript)
    * [I have some websites for which I need to be logged in to access. Can I use NowCrawling with them?](#i-have-some-websites-for-which-i-need-to-be-logged-in-to-access-c-i-use-nowcrawling-with-them)
    * [The source-code is huge! If NowCrawling is this simple, why is that so?](#the-source-code-is-huge-if-nowcrawling-is-this-simple-why-is-that-so)
    * [Do you support other search engines (i.e. can <code>-k</code> be used with other engines)?](#do-you-support-other-search-engines-ie-can--k-be-used-with-other-engines)
    * [Why is the <em>recursion depth</em> set to 1 by default?](#why-is-the-recursion-depth-set-to-1-by-default)
    * [What user-agent does NowCrawling report to its websites? Can I change it?](#what-user-agent-does-nowcrawling-report-to-its-websites-can-i-change-it)
    * [What operating systems does it run on? Is compatibility the same in all of them?](#what-operating-systems-does-it-run-on-is-compatibility-the-same-in-all-of-them)
    * [Is there a Python 2 port?](#is-there-a-python-2-port)
    * [Can I change the default connection timeout? What's the default?](#can-i-change-the-default-connection-timeout-whats-the-default)
    * [Can I limit the downloaded files by number or by size?](#can-i-limit-the-downloaded-files-by-number-or-by-size)
    * [How does smart search work?](#how-does-smart-search-work)
    * [I'm searching for images. Can NowCrawling automatically detect images in webpages and download them if their name matches my criteria?](#im-searching-for-images-canowcrawling-automatically-detect-images-in-webpages-and-download-them-if-their-name-matches-my-criteria)
    * [I've seen my downloads randomly stop for no reason. Why's that?](#ive-seen-my-downloads-randomly-stop-for-no-reason-whys-that)
    * [What protocols does NowCrawling support?](#what-protocols-does-nowcrawling-support)
    * [Why should I use NowCrawling?](#why-should-i-use-nowcrawling)
    * [Is PyPy3 signifficantly faster than Python3 with NowCrawling?](#is-pypy3-signifficantly-faster-than-python3-with-nowcrawling)
    * [If you're just crawling webpages, can't it happen that you find a huge page and get stuck downloading it?](#if-youre-just-crawling-webpages-cant-it-happen-that-yofind-a-huge-page-and-get-stuck-downloading-it)
    * [Can I be banned from Google if I overuse NowCrawling?](#can-i-be-banned-from-google-if-i-overuse-nowcrawling)
    * [When I run NowCrawling with the same arguments at two different times, results are different! Why is that?](#when-i-run-nowcrawling-with-the-same-arguments-at-twdifferent-times-results-are-different-why-is-that)
    * [I'm running Windows and NowCrawling told me "Windows can't display this message"](#im-running-windows-and-nowcrawling-told-me-windows-cant-display-this-message)
    * [Why does NowCrawling sometimes visit weird looking URLs and get an obvious 404?](#why-does-nowcrawling-sometimes-visit-weird-looking-urls-and-get-an-obvious-404)
    * [Is it possible to provide a list of match regexes and use different output directories/files for each of them?](#is-it-possible-to-provide-a-list-of-match-regexes-anuse-different-output-directoriesfiles-for-each-of-them)
    * [When I'm downloading a file, the whole crawling process stops. Could downloading be done in the background, or in parallel?](#when-im-downloading-a-file-the-wholcrawling-process-stops-could-downloading-be-done-in-the-background-or-in-parallel)

(TOC created with [gh-md-toc](https://github.com/ekalinin/github-markdown-toc))

## Example Usage
Here are some examples of how **NowCrawling** can be used.

### File Crawling Mode examples
Below is a series of examples of **NowCrawling** in *File Crawling Mode*, designed to find and download files. An alternative mode is the *Content Crawling Mode*, for which examples can be found [below](#content-crawling-mode-examples).
#### Downloading an episode of a TV series
If you're looking to download an episode of a TV series (e.g. Game of Thrones), you can now do it by running a one-liner in your command line with **NowCrawling**.

Below is the example of downloading (only in theory!) the first episode of the Game of Thrones TV series.

##### Command

    nowcrawling -f -k "game of thrones" -t "s01e01" -e "mkv mp4 avi" -s -a -l 100MB-

##### Explanation

The following options are used **(note that nearly all of these are fully case insensitive, as well as their arguments)**:
* `-f`, `--files`: This tells **NowCrawling** that you want to use it in *File Crawling Mode*, whereby it will download files. An alternative mode, which we cover later, is the *Content Crawling Mode* (`-c`, `--content`).
* `-k`, `--keywords`: This option automatically tells **NowCrawling** that you want it to Google for some keywords and use the results as the basis for your search. Alternatively, you could ask it to directly crawl a list of URLs you found beforehand (this can be done with the `-u`, `--url-list`option). In this example, you google for *"game of thrones"*. You can supply anything you want as the keyword argument and it will be used as part of the query sent to Google (e.g., you could also google for "Game Of Thrones Season X, Episode Y", although we do this in a more efficient way with the `-t` option; another example is that you could use Google specific keywords, such as '+','-', quotes, 'insite:', etc.)
* `-t`,`--tags`: The tags argument is used to mandate the existance of certain terms in the file names that **NowCrawling** will download. By doing `-t s01e01` we are forcing this file to have this specific keyword somewhere in its name (or, rather, in the URL that directly leads to it). The idea is to use a generic term to search and then limit the desired files with the tags. You can supply any number of tags, separated by spaces. Order is important! Although we intend to change this behavior, the order of tags in the `-t`argument dictates the order in which they must appear in the file. Also note that this option mandates that ALL its arguments must be included in the file name.
* `-e`, `--extensions`: This argument is used to specify the different extensions (enclosed in quotes and separated by spaces) you want to allow in your file. Since we are looking for video, we supply it with *"mkv mp4 avi"* to search for mkv, mp4 and avi files.
* `-s`, `--smart`: This instructs **NowCrawling** to perform a *smart* Google search. **NowCrawling** will then use advanced Google search terms, highly reducing the time it takes to find your file. **Usage of this parameter should be taken with care:** it highly limits your results (and, hence, is not the best idea if you are looking for a broad search with multiple files), and it often leads to **temporary (~30 minute) bans from certain parts of Google** (e.g. you may still query google but cannot use more advanced queries, such as those involving "intitle" and "inurl" expressions). Since we only want one file in this case, it's perfectly fine to use it. However, if we got no results with it, the best idea would be to try the search again without `-s`.
* `-a`, `--ask`: By default, **NowCrawling** downloads every file it finds without asking for permission. This flag forces **NowCrawling** to ask before downloading a file, making it an interactive application and ideal for simple, specific searches such as this one.
* `-l`, `--limit`: By using this option, **NowCrawling** will only look for files that satisfy a given filesize range. The format is `minsize-maxsize`, where sizes can be given in readable form (e.g. 50MB) and, if no unit is supplied, bytes are assumed. It may also be the case that you only want to supply upper or lower bounds, in which case you can ignore minsize or maxsize. In our example, we look only for files bigger than *100MB*, by doing `-l 100MB-`. The idea is that we instantly ignore bad or misleading links. Do note that **if file size cannot be determined and you provided size limits, NowCrawling uses a pessimistic approach and does not download it**.

#### Downloading a song
Downloading a song is really similar to the previous example. Let's consider Iron Maiden's Blood Brothers.
##### Command

    nowcrawling -f -k "iron maiden" -t "blood brothers" -e "mp3 flac ogg m4a" -s -a

##### Explanation
The following options are used **(note that nearly all of these are fully case insensitive, as well as their arguments)**:
* `-f`, `--files`: Explained in the [previous example](#downloading-an-episode-of-a-tv-series). Tells **NowCrawling** that you want to use it in *File Crawling Mode*.
* `-k`, `--keywords`: Explained in the [previous example](#downloading-an-episode-of-a-tv-series). This is the base query of the search, as if you were to directly type it in Google. You can be more specifical, e.g., by specifying the album of the song. In this case, it could be something such as `-k iron maiden brave new world`, since the Blood Brothers song belongs to the Brave New World album. **The proper choice of keywords/query can greatly reduce crawling time.**
* `-t`,`--tags`: Explained in the [previous example](#downloading-an-episode-of-a-tv-series). Usually, song titles are present in the file names, so by supplying `-t "blood brothers"` we force the existance of two keywords, in that order, in the file (i.e. *blood* and *brothers*). This means that NowCrawling will download files such as "blood brothers.mp3", "blood and lots of brothers.mp3" and "\_blood_brothers_.mp3". Since `-t` is an optional parameter, you might opt by not using it, in which case you will download any file that is found during this search (most likely iron maiden songs, but not restricted to them).
* `-e`,`--extensions`: Explained in the [previous example](#downloading-an-episode-of-a-tv-series). We are looking for mp3, flac, ogg and m4a files, meaning other extensions will not be matched.
* `-s`,`--smart`: Explained in the [previous example](#downloading-an-episode-of-a-tv-series). Since we are looking for a specific file, a *smart* search is appropriate.
* `-a`,`--ask`: Explained in the [previous example](#downloading-an-episode-of-a-tv-series). Ask before downloading.

#### Downloading lots of HD wallpapers to a specific folder
**NowCrawling** is great for filling a folder with a bunch of themed wallpapers. Suppose that you want to find *space themed wallpapers*.
##### Command

    nowcrawling -f -k "space wallpapers" -t "1920" -e "jpg jpeg png" -d space -l 100KB-
    
##### Explanation
The following options are used **(note that nearly all of these are fully case insensitive, as well as their arguments)**:
* `-f`, `--files`: Explained in the [previous example](#downloading-an-episode-of-a-tv-series). Tells **NowCrawling** that you want to use it in *File Crawling Mode*.
* `-k`, `--keywords`: Explained in the [previous example](#downloading-an-episode-of-a-tv-series). This is the base query of the search, as if you were to directly type it in Google. We want any kind of space-related wallpaper!
* `-t`,`--tags`: Explained in the [previous example](#downloading-an-episode-of-a-tv-series). As previously, it's good to remember that this flag is optional. Since we are looking mainly for HD wallpapers, we can force part of the filename to be *"1920"*, with the idea of including files whose name contains high definition resolutions (e.g. 1920x1080, 1920x1200, etc). However, by using `-t` in this way we instantly lose all files with random names (e.g. *10wkvnbu4nh8302.png*). On the other hand, if we further wanted to refine our search, we could do `-t "1920 1080"`to guaruantee that both sizes appeared in the file name. **Proper usage of `-t` is, therefore, critical to your crawling results!** If you want more backgrounds, at the risk of quality (and bandwidth), remove `-t` altogether!
* `-e`,`--extensions`: Explained in the [previous example](#downloading-an-episode-of-a-tv-series). We are looking for image file extensions such as *jpg*, *jpeg* and *png*. Note how we automatically exclude *gif* and other formats.
* `-d`, `--directory`: Specifies a target folder where the files will be downloaded to. If it does not exist, it will be created (however, note that chains of folders will not be created, i.e., in /test/folder/, if `test` does not exist, then `folder` will not be created and downloads will fail). This optional flag is particularly useful for large batch file downloads.
* `-l`,`--limit`: Explained in the [previous example](#downloading-an-episode-of-a-tv-series). In order to automatically dismiss erroneous results (1 KB images and other such false positives), we force images to be of at least *100KB*.

#### Downloading files off of your own URLs
Suppose you've already found a webpage with interesting content that you'd like to download. Maybe it's a page full of images (**NowCrawling** can inspect HTML "*img src=*" tags and download images), or maybe it's a website full of songs you found on the web, such as [http://www.mmnt.net/db/0/0/195.137.185.2/Music/Iron%20Maiden](http://www.mmnt.net/db/0/0/195.137.185.2/Music/Iron%20Maiden). **NowCrawling** will make it easy for you to download these files (although you should *really* look into the legality of that).
##### Command

     nowcrawling -f -u "list:http://www.cyn.net/music/Iron%20Maiden%20-%20Brave%20New%20World/" -e mp3 -d "Iron Maiden"
    
##### Explanation
The following options are used **(note that nearly all of these are fully case insensitive, as well as their arguments)**:
* `-f`, `--files`: Explained in the [previous example](#downloading-an-episode-of-a-tv-series). Tells **NowCrawling** that you want to use it in *File Crawling Mode*.
* `-u`, `--url-list`: This option (which cannot be used with `-k` and `-s`) tells **NowCrawling** to directly use a list of URLs instead of querying Google. This list can be supplied in two different ways:
    * Inline, as part of the argument. It should be a **comma-separated list** prefixed by the "list:" keyword. In this example, we do `-u list:http://www.cyn.net/music/Iron%20Maiden%20-%20Brave%20New%20World/` to use this mode.
    * In a file, supplied as the argument. This file should have all URLs, one per line (with '#' being used for comments). To pass the file to the application, prefix its path by "file:", much like you did with "list:" for the list of URLs.
* `-e`,`--extensions`: Explained in the [previous example](#downloading-an-episode-of-a-tv-series). We are looking for *mp3* files.
* `-d`, `--directory`: Explained in the [previous example](#downloading-lots-of-hd-wallpapers-to-a-specific-folder). Specifies a directory where we want to save all downloaded files.

#### Using your own regexes
If you're finally getting to grips with **NowCrawling**'s basic commands, such as `-t`, you might consider doing some more advanced crawling by directly building a regex for **NowCrawling** to use.

Take the TV series episode example seen [previously](#downloading-an-episode-of-a-tv-series) and imagine that instead of simply matching *"s01e01"* in the file name, you wanted to *also* match *"e01s01"*. You could run two different NowCrawling instances with different `-t` arguments, or you could replace the `-t` functionality with your own regex to match file names.


##### Command

    nowcrawling -f -k "game of thrones" -r "(s01e01|e01s01)" -e "mkv mp4 avi" -s -a -l 100MB-
    
##### Explanation
Since this is an advanced topic, most of these won't be explained. See the [other examples](#file-crawling-mode-examples) for a detailed explanation of them:
* `-f`, `-k`, `-e`, `-s`, `-a` and , `-l`: These are the same as in the [original example](#downloading-an-episode-of-a-tv-series).
* `-r`,`--regex`: This option can be used instead of `-t` to provide a regex which should match part of the filename, but not all of it. By using the "(s01e01|e01s01)" regex, we are forcing the filenames to contain either "s01e01" or "e01s01" (case insensitive) in the filename. This regex parameter allows for flexible filtering of results, improving upon the `-t` option.

### Content Crawling Mode examples
Below is a series of examples of **NowCrawling** in *Content Crawling Mode*, designed to find patterns on the web (e.g. leaked emails, credit card numbers, funky and weirdly named images, etc). An alternative mode is the *File Crawling Mode*, for which examples can be found [above](#file-crawling-mode-examples).
#### Finding leaked gmail addresses
Content mode is great for finding things on the web. Thinking of building a new spambot targeted at those pesky gmail users? (just kidding, we know you're not *that* pesky) **NowCrawling** can help you! In this example, we do a very simple search for leaked gmail addresses and store them in a file for later inspection.

##### Command

    nowcrawling -c -k "gmail leak" -m "[a-zA-Z0-9]*?@gmail.com" -o leaked_emails.txt

##### Explanation

The following options are used **(note that nearly all of these are fully case insensitive, as well as their arguments)**:
* `-c`, `--content`: This tells **NowCrawling** that you want to use it in *Content Crawling Mode*, whereby it will look for content matches and print them to the screen and, optionally, save them to a file. An alternative mode, which we covered [previously](#file-crawling-mode-examples), is the *File Crawling Mode* (`-f`, `--file-crawling`).
* `-k`, `--keywords`: This argument works as it did in *File Crawling Mode* (see [the previous example](#downloading-an-episode-of-a-tv-series)). In this particular case, we do a generic search for a "gmail leak".
* `-m`, `--match`: This option is somewhat similar to the `-r` option in *File Crawling Mode*. It is the obligatory regex you want to use to match patterns. Anything that matches the regex supplied with `-m` will be printed to the console and optionally saved to a file (if such a file has been supplied with `-o`). In our example, we supply a **ridiculously oversimplified email-match regex** to find leaked gmail emails. This is simple, but has moderately good results and should be enough to get you started.
* `-o`, `--output-file`: This optional parameter can be used to pass a file where **NowCrawling** will write the results, besides the standard output. We use it to redirect all our matches to `leaked_emails.txt`, which we could later use in other ways.

#### Finding leaked gmail addresses *and* passwords
The previous example shows how you can find an email address dump, but with a bit more of creativity, there are more "interesting" things that you can find. The following example modifies the previous with a very, very, very primitive regex that is, however, enough to find some leaked emails and passwords.

##### Command

    nowcrawling -c -k "gmail leak dump passwords" -m "[a-zA-Z0-9]*?@gmail\.com:[a-zA-Z0-9]* -o usernames_and_passwords.txt

##### Explanation

The following options are used **(note that nearly all of these are fully case insensitive, as well as their arguments)**:
* `-c`, `--content`: This tells **NowCrawling** that you want to use it in *Content Crawling Mode*, whereby it will look for content matches and print them to the screen and, optionally, save them to a file. An alternative mode, which we covered [previously](#file-crawling-mode-examples), is the *File Crawling Mode* (`-f`, `--file-crawling`).
* `-k`, `--keywords`: Explained in the [previous example](#finding-leaked-gmail-addresses). Use for querying Google. In this particular case, we do a generic search for "gmail leak dump passwords". Of course you can refine the search with Google specific keywords to make the results better. Also note that **you can use the _smart search_ (`-s`) functionality in _Content Crawling Mode_** too!
* `-m`, `--match`: Explained in the [previous example](#finding-leaked-gmail-addresses). This time, we modify our regex to include a grossly oversimplified password (with only alphanumeric characters) after a ":" and the email. This gives (perhaps surprisingly) good results!
* `-o`, `--output-file`: Explained in the [previous example](#finding-leaked-gmail-addresses). Stores all found leaked emails and passwords in the desired output file.

#### Finding credit card numbers on the web
Suppose you want to find credit card numbers that are out on the web, for whatever reason you see fit. With **NowCrawling**'s *Content Crawling Mode*, this is trivial, provided your regex skills are up to the task.

##### Command

    nowcrawling -c -k "credit cards leak" -m "[0-9]{4}[- ][0-9]{4}[- ][0-9]{4}[- ][0-9]{4}" -o creditcards.txt

##### Explanation

The following options are used **(note that nearly all of these are fully case insensitive, as well as their arguments)**:
* `-c`, `--content`: This tells **NowCrawling** that you want to use it in *Content Crawling Mode*, whereby it will look for content matches and print them to the screen and, optionally, save them to a file. An alternative mode, which we covered [previously](#file-crawling-mode-examples), is the *File Crawling Mode* (`-f`, `--file-crawling`).
* `-k`, `--keywords`: Explained in the [previous example](#finding-leaked-gmail-addresses). Use for querying Google. In this particular case, we do a generic search for a "credit cards leak".
* `-m`, `--match`: Explained in the [previous example](#finding-leaked-gmail-addresses). We use this option to pass our content matching regex. In this particular case, we're looking for four chunks of four digits divided by a space or a hyphen. As with all regexes, this can be greatly improved, for example by specifying the first digits of the card, since they decide the credit card corporation (e.g. 5 for MasterCard and 4 for Visa). **The beauty of NowCrawling's *Content Crawling Mode* is precisely that it all depends on the user's ability to produce great regular expressions!**
* `-o`, `--output-file`: Explained in the [previous example](#finding-leaked-gmail-addresses). Stores all found credit card numbers in the desired output file.

### Advanced Crawling
Below is a series of more advanced examples where additional, more complex functionality of *NowCrawling* is used.

#### Going deeper: crawling linked pages too (e.g. folders in fileservers)
Sometimes, when crawling for files, your search will return a page which does not have the files yet, but which links to a page which does. This is commonly seen in FTP server pages, such as [http://www.mmnt.net/db/0/0/195.137.185.2/Music/Iron%20Maiden](http://www.mmnt.net/db/0/0/195.137.185.2/Music/Iron%20Maiden). In these cases, it would be useful to allow **NowCrawling** to visit these pages too. Well, you can!

**NowCrawling** has the concept of *recursion depth*, which defines how far away from the base URLs (typically found from Google results with `-k`) you want to go looking for results. By default, this *recursion depth* is fixed at 1, meaning you cannot visit pages linked by your search results. In the example of the FTP server page shown above, the directories containing the actual files will not be visited when you pass that URL to the `-u` option. You can override this behavior and tell **NowCrawling** to go deeper, as we show. **Note that you are guaranteed that for each URL found in your Google search (or manually supplied with `-u`), NowCrawling won't visit duplicate links.**

##### Command

    nowcrawling -f -u "list:http://www.mmnt.net/db/0/0/195.137.185.2/Music/Iron%20Maiden" -e "mp3" -d "Iron Maiden" -z 2

##### Explanation

You should already be familiar with the `-f`, `-u`, `-e`, and `-d`options. If you are not, go read their examples [above](#file-crawling-mode-examples).

`-z`,`--recursion--depth`: This option changes the *recursion depth* of **NowCrawling**. With `-z 2`, we are telling it to visit pages inside the supplied URL itself. If we did `-z 3`, we would allow for even "deeper" searches. **This option is very powerful, and can be used in both *File Content Mode* and *Content Crawling Mode*, but you should be wary of its implications!** The number of visited pages grows **exponentially** with the recursion depth. Consider this, if you visit 10 pages and each of them has 50 links (most of them have over 100 links), you'll be crawling 500 pages instead of 10!


#### Verbosity
**NowCrawling** tries to be quite silent when it runs, so as not to spam the standard output. It displays very little information: the current file download progress and the matched content. However, you might be interested in getting more information about what it's doing. For this, you can use `-v`,`--verbose` to enable **high verbosity**. With this flag, **NowCrawling** will print out loads of useful output, showing the recursion depth, all the URLs being expected, their errors, the progress in the current recursion tree branch, and others. If you like to get the maximum Logging information, it might be a good idea to run **NowCrawling** with `-v` and redirect the relevant output to a file with `-d` (for *File Crawling Mode*) and `-o` (for *Content Crawling Mode*).

#### Whitelists and Blacklists
You'll quickly notice that while **NowCrawling** is fast (particularly with PyPy), it can't do wonders. Websites such as Youtube or Google Plus have complex HTML and take longer to process. Yet, most times you won't even want to include these pages in your search. It makes sense, then, to be able to **blacklist certain domains** -- which **NowCrawling** supports.

Similarly, you may be interested in only accessing a restricted set of domains To this end, you can use **whitelists**! Blacklists and whitelists are particularly valuable when you are crawling at higher [recursion levels](#going-deeper-crawling-linked-pages-too-eg-folders-in-fileservers), such as `-z 2`and `-z 3`, because they help you filter out lots of unwanted pages.

Both whitelists and blacklists use **_domain files_**. These files contain one domain regex per line (with the possibility of using '#') for comments. For instance, you can match all .com domains with `.*\.com`; you can also match youtube with `.*youtube.*\.com`. If you have good regex skills, you'll find writing *domain files* to be a piece of cake.

To tell **NowCrawling** to use a **whitelist** use `-w`,`--whitelist`, e.g.:

    nowcrawling -f -k "Song of Ice and Fire" -e "mp3" -s -w whitelist.list

where `whitelist.list` is just a *domain file* with a couple of regexes for the domains you want to visit. 

The same can be done for **blacklists** with `-b`,`--blacklist`, e.g.:

    nowcrawling -f -k "Song of Ice and Fire" -e "mp3" -s -b blacklist.list

where `blacklist.list` is also a *domain file*

Note that you can't use both `-b`and `-w` and the same time, for obvious reasons.


#### Finding leaked emails and passwords with better regexes
In [another example](#finding-leaked-gmail-addresses-and-passwords), we showed how simple it was to use equally simple regexes to find leaked emails and passwords (we looked at the specific case of gmail). As a final example, take the following more advanced **NowPlaying** command line, with more advanced regexes to find most kinds of email and password leaks.

##### Example Command 1

    nowcrawling -c -k "email leak dump passwords" -m "[a-zA-Z0-9][a-zA-Z0-9\._]*?@[a-zA-Z0-9]+?\.[a-zA-Z][a-zA-Z]?[a-zA-Z]?:[a-zA-Z0-9\._*\!\@\#\$\%\€\&\=\-\+]+" -o leaked_emails_and_passwords.txt
    
The above command gives impressive results, but we could try to leverage the power of Google to do something more sophisticated. Many leaks come from websites such as [pastebin.com](http://pastebin.com), so why not try to go through Pastebin, using [whitelists](#whitelists-and-blacklists)? Furthermore, sometimes leaks happen in "close pasties", so we can also try to crawl these neighbouring pasties, which might appear as links in the original pasties. Thus, we can use [higher recursion depth levels](#going-deeper-crawling-linked-pages-too-eg-folders-in-fileservers), combined with whitelists to achieve faster results, at the cost of some leaked emails and passwords:

##### Example Command 2
    nowcrawling -c -k "email leak dump passwords" -m "[a-zA-Z0-9][a-zA-Z0-9\._]*?@[a-zA-Z0-9]+?\.[a-zA-Z][a-zA-Z]?[a-zA-Z]?:[a-zA-Z0-9\._*\!\@\#\$\%\€\&\=\-\+]+" -o leaked_emails_and_passwords.txt -z 2 -w whitelist.list
    
where whitelist.list contains:

    .*pastebin.*

## FAQ
### How does NowCrawling really work?
At its core, **NowCrawling** is really basic stuff. Picture yourself googling for something and then visiting all the results that google gives you. In each result, you carefully look for any URLs that may be in the page (e.g. also in *src=* tags) for interesting content. You may be looking for images, files, leaked emails or something else entirely! As you do this, you download the interesting files you see and proceed to the next search results. **NowCrawling** is doing exactly the same, except in automated exception.

Internally, its only dependency is Python 3, and everything else is built using the standard library and regular expressions. The project did indeed start as a "glorified automated google search crawler", but it has since grown into a much larger crawler, capable of much more than simple Google crawling.
### Is this illegal?
No tool such as this one is illegal by itself in most countries. This does not mean that you can't do illegal things with it. Use common sense -- you can use **NowCrawling** to do many, many things, ranging from finding backgrounds for your next desktop, to downloading pirated content off the web.
### How does NowCrawling deal with javascript?
At the moment, it doesn't. NowCrawling only downloads the static HTML file and parses it, much like *wget* would do. Maybe in the future, if it seems necessary, the engine can be reworked to include dynamic page modifications, namely in the form of Javascript
### I have some websites for which I need to be logged in to access. Can I use NowCrawling with them?
The short answer is that, no, you can't. Maybe you can get away with acessing them with your browser and then saving a local cached copy of it on your computer and pointing **NowCrawling** to it with `-u "list:file://cached_page.htm"`, but it might not always work.

Perhaps in the future we can implement an interactive mode where you input your username and password and it gets saved in the cookies of the current session.

### The source-code is huge! If NowCrawling is this simple, why is that so?
**NowCrawling** itself isn't simple. Its idea, and the process it tries to automate, is. There are many different things that **NowCrawling** must deal with, including whitelists, blacklists, progress bars, dealing with time-outs, disconnects, encoding errors, crawling google, crawling webpages, checking their sizes, downloading files, creating directories, dynamically generating regexes, and more. This has to be done as fast as possible to ensure performance. We also provide an extensive Logging support throughout the code, which can be tuned with the `-v, --verbose` option.

### Do you support other search engines (i.e. can `-k` be used with other engines)?

Not at the moment, but this shouldn't be too hard. We tried hard to make the code modular and loosely coupled precisely to implement this kind of functionality in the future. Note that nothing is to stop you from implementing these features yourself and sending us a pull request!

### Why is the *recursion depth* set to 1 by default?

*[Recursion Depth](#going-deeper-crawling-linked-pages-too-eg-folders-in-fileservers)* is very powerful, but can quickly lead to very long waiting times. Try it yourself! Run any search with a recursion depth of 2 and pass in the verbosity flag (`-v`) to see just how many pages are being crawled, most of them without any need for such. This is an expert flag to be used in rare situations where you really know what you're doing.

### What user-agent does NowCrawling report to its websites? Can I change it?

You can't currently change it, but that would be trivial to change. The reason we haven't done it is that we haven't had any real problems with it. **NowCrawling** currently presents itself as

    Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36

### What operating systems does it run on? Is compatibility the same in all of them?

It runs in every major operating system. Windows and *nix. However, colors are currently only supported in *nix. Some websites with funky characters in the names will also trigger encoding errors in Windows (it's the fault of Microsoft's badly designed console) which won't happen in *nix. We've tried to minimize the impact of these errors to the maximum (worst case scenario: you miss some content, but the application doesn't crash)

### Is there a Python 2 port?
No. It shouldn't be terribly difficult to port it to Python 2, but we don't currently see a reason to do so.

### Can I change the default connection timeout? What's the default?

Yes! The default timeout is 7 seconds, but you can change this with the `-i`,`--ignore-after` flag.

### Can I limit the downloaded files by number or by size?

You can limit the number of downloaded files by their count with the `-n`, `--number` flag. (e.g. to download at most 100 files, do `-n 100`.

You can also limit each file's individual size with the `-l`,`--limit` flag which we explain in [this example](#downloading-an-episode-of-a-tv-series). In short, the format is `minSize-maxSize`, with these sizes in human-readable form (e.g., 5MB), and the possibility of only supplying one of these arguments. Do read the [example](#downloading-an-episode-of-a-tv-series) explanation to really understand it.

### How does smart search work?
The *smart search* (`-s`) option tries to speed Google searches when you're looking for files. It essentially tries to look for public-access repositories and FTP servers, where files are easily listed. This is done by appending the string " intitle:index of " to your query. This obviously leads to faster results because you quickly get to files. However, if your search terms are not right, it might limit your rate of success in finding what you want.

### I'm searching for images. Can NowCrawling automatically detect images in webpages and download them if their name matches my criteria?
Yes! Besides looking for any reference of a URL in webpages, NowCrawling takes particular care with *src* attributes in HTML (notably in *script* and *img* tags), manually inspecting them for potentially crawlable URLs.

### I've seen my downloads randomly stop for no reason. Why's that?
If you're not using high verbosity output (`-v`, `--verbosity`), **NowCrawling** will show the least amount of information possible. In general, it will try to only show you the name and progress of the current file being transfered (or, in *Content Crawling Mode*, the matched content). If there's an error (such as a disconnect or other kind of error), the transfer will stop abruptly, as it would with any other application. The key difference is that we don't show errors without `-v`. This is due to the fact that the output would quickly get spammed with many "false errors", coming from "fake 404s" and other similar errors. We might consider changing part of this in future releases.

### What protocols does NowCrawling support?
Anything that Python 3 supports is automatically supported by NowCrawling. That includes HTTP, HTTPS, FTP, FILE, etc..

### Why should I use NowCrawling?
This project started because we wanted to make our lives easier. There are many tasks that we can now automate, such as finding backgrounds or finding documents on the web and downloading them *en masse*. We've got a couple of [examples](#example-usage) of how **NowCrawling** can really be a helpful tool.

Hopefully, it will also be useful for you. Use it to find news, to google yourself, to crawl that page with millions of images you really wanted to download, to find interesting stuff over at Pastebin and similar sites (though if you're looking for an automated Pastebin crawler, one of us has also developed a [Pastebin Crawler](https://github.com/Jorl17/Pastebin-Crawler) which might be of interest).

### Is PyPy3 signifficantly faster than Python3 with NowCrawling?
We haven't run any benchmarks yet, but the difference is noticeable, particularly in complex pages. We really recommend you use PyPy3 if you can.

### If you're just crawling webpages, can't it happen that you find a huge page and get stuck downloading it?

We don't visit a page if its bare HTML  is over 20MB (i.e. only the HTML, not the images, scripts, etc). This prevents the situation described, as we encountered it on several occasions, in particular where *mkv* files reported themselves as *text/plain* files.

If the file size can't be determined *a priori*, though, we download the page until the end, regardless of its size. We plan to change this in the future.

### Can I be banned from Google if I overuse NowCrawling?

You can't be *permanently* banned, but you will on rare occasions be temporarily banned for about 30 minutes. This happens when google detects abnormal traffic from your IP, in particular when using *smart search* (`-s`) . Note that these temporary bans also only apply to certain parts of Google. In particular, you can still do regular searches in your browser, insofar as you don't use Google specific keywords such as "intitle" and "inurl" (f you are temporarily banned and use them, Google will give you an HTTP 503).

We plan to introduce a "back-off time" in the future for when we detect that Google is temporarily blocking you. This way, **NowCrawling** won't stop and print an error message but, rather, will keep trying with appropriate time intervals, allowing you to leave it running on your machine without worrying about it.

### When I run NowCrawling with the same arguments at two different times, results are different! Why is that?

You only see this behavior when you use `-k` (rather than `-u`). This is a consequence of the way Google works. When we ask it for results, it may present them randomly, thus changing their order. In the long run, both executions will lead to the same results, even if in a different order.

There are a couple of things that we could do to minimize this difference. These include sorting the search results a priori and buffering them in batches of 100 before expecting them. There hasn't been great need for this, so it's not implemented at the moment.

### I'm running Windows and NowCrawling told me "Windows can't display this message"

This is a problem with Windows' command line application. It has very limited support for UTF-8 and might cause some errors if we try to print characters out of its default codepage. We catch these exceptions and do our best to ignore them, but there is really nothing we can do (nor can Python). We have some workaround ideas, but since currently this only affects printing and not actual functionality, we won't yet try them around. Also see [this FAQ question](#what-operating-systems-does-it-run-on-is-compatibility-the-same-in-all-of-them).

### Why does NowCrawling sometimes visit weird looking URLs and get an obvious 404?

**NowCrawling** was designed to find URLs anywhere in a webpage. This falls under the assumption that, for instance, in a forum, not all links will be part of an *a href=* tag/attribute pair. To achieve this, we use a couple of fairly advanced regexes that try to find any possible URL in a webpage. If you've read [RFC 1738](https://www.ietf.org/rfc/rfc1738.txt) for URLs, you'll know that they can be pretty esoteric. In addition to that, many URLs with such esoteric look do exist on the web, containing unescaped spaces, dozens of funky arguments and other things. We try to catch all of these and prefer to catch a couple of expressions that aren't URLs rather than failing to catch all possible URLs. The "wrong" URLs are easily discarded with a 404 when we try to access them.

### Is it possible to provide a list of match regexes and use different output directories/files for each of them?

Not at the moment. You probably ask this if you're familiar with [Pastebin Crawler](https://github.com/Jorl17/Pastebin-Crawler)'s mode of operation. We intend to eventually add support for this.

### When I'm downloading a file, the whole crawling process stops. Could downloading be done in the background, or in parallel?

This is not implemented, but we plan to do so. Note that parallel downloads won't really give you a big boost. The only real advantage is that if two different threads handle downloading and page parsing in parallel, you might get a boost, as more pages can be parses while the download is happening. For this reason, we'll probably initially just implement a download queue. This also raises problems with the standard output and verbosity (if two threads try to print at the same time, and, in particular, if one of them is a progress bar, what will happen?). Additionally, with higher recursion depth levels we already do something to try and minimize this issue: we don't download files until we've finished visiting the whole recursion branch (e.g. even if you do `-z 100`, and get 3 Google search results, there will only be three periods during which downloads will be allowed: after the first page (and its web tree) has been visited, after the second and after the third).

Hang on and it might come in a future release :)


