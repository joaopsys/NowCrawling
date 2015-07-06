# NowCrawling
**NowCrawling** intially started as a **Google crawler**, automating file and pattern searches. It has since become a more **general crawler capable of easily finding patterns and files in user supplied URLs**. It is written in Python 3 and is compatible with the latest PyPy release for maximum performance. It also works in every major platform out there (Windows and *nix).

**So what's it really all about?** Lots of things! Want to search for a generic wallpaper and download all the images you can find? Want to google for all emails from a given domain? Want to automatically download all listed files in a certain webserver? **NowCrawling** helps you do this, with loads of options.

[Below](FIXME) is a sequence of example use cases with a detailed explanation. For a more detailed FAQ, see [here](FIXME).

(FIXME: Aqui meter a TOC)

## Example Usage
Here are some examples of how **NowCrawling** can be used.

### File Crawling Mode examples
Below is a series of examples of **NowCrawling** in *File Crawling Mode*, designed to find and download files. An alternative mode is the *Content Crawling Mode*, for which examples can be found [below](FIXME).
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
* `-f`, `--files`: Explained in the [previous example](FIXME). Tells **NowCrawling** that you want to use it in *File Crawling Mode*.
* `-k`, `--keywords`: Explained in the [previous example](FIXME). This is the base query of the search, as if you were to directly type it in Google. You can be more specifical, e.g., by specifying the album of the song. In this case, it could be something such as `-k iron maiden brave new world`, since the Blood Brothers song belongs to the Brave New World album. **The proper choice of keywords/query can greatly reduce crawling time.**
* `-t`,`--tags`: Explained in the [previous example](FIXME). Usually, song titles are present in the file names, so by supplying `-t "blood brothers"` we force the existance of two keywords, in that order, in the file (i.e. *blood* and *brothers*). This means that NowCrawling will download files such as "blood brothers.mp3", "blood and lots of brothers.mp3" and "\_blood_brothers_.mp3". Since `-t` is an optional parameter, you might opt by not using it, in which case you will download any file that is found during this search (most likely iron maiden songs, but not restricted to them).
* `-e`,`--extensions`: Explained in the [previous example](FIXME). We are looking for mp3, flac, ogg and m4a files, meaning other extensions will not be matched.
* `-s`,`--smart`: Explained in the [previous example](FIXME). Since we are looking for a specific file, a *smart* search is appropriate.
* `-a`,`--ask`: Explained in the [previous example](FIXME). Ask before downloading.

#### Downloading lots of HD wallpapers to a specific folder
**NowCrawling** is great for filling a folder with a bunch of themed wallpapers. Suppose that you want to find *space themed wallpapers*.
##### Command

    nowcrawling -f -k "space wallpapers" -t "1920" -e "jpg jpeg png" -d space -l 100KB-
    
##### Explanation
The following options are used **(note that nearly all of these are fully case insensitive, as well as their arguments)**:
* `-f`, `--files`: Explained in the [previous example](FIXME). Tells **NowCrawling** that you want to use it in *File Crawling Mode*.
* `-k`, `--keywords`: Explained in the [previous example](FIXME). This is the base query of the search, as if you were to directly type it in Google. We want any kind of space-related wallpaper!
* `-t`,`--tags`: Explained in the [previous example](FIXME). As previously, it's good to remember that this flag is optional. Since we are looking mainly for HD wallpapers, we can force part of the filename to be *"1920"*, with the idea of including files whose name contains high definition resolutions (e.g. 1920x1080, 1920x1200, etc). However, by using `-t` in this way we instantly lose all files with random names (e.g. *10wkvnbu4nh8302.png*). On the other hand, if we further wanted to refine our search, we could do `-t "1920 1080"`to guaruantee that both sizes appeared in the file name. **Proper usage of `-t` is, therefore, critical to your crawling results! **If you want more backgrounds, at the risk of quality (and bandwidth), remove `-t` altogether!
* `-e`,`--extensions`: Explained in the [previous example](FIXME). We are looking for image file extensions such as *jpg*, *jpeg* and *png*. Note how we automatically exclude *gif* and other formats.
* `-d`, `--directory`: Specifies a target folder where the files will be downloaded to. If it does not exist, it will be created (however, note that chains of folders will not be created, i.e., in /test/folder/, if `test` does not exist, then `folder` will not be created and downloads will fail). This optional flag is particularly useful for large batch file downloads.
* `-l`,`--limit`: Explained in the [previous example](FIXME). In order to automatically dismiss erroneous results (1 KB images and other such false positives), we force images to be of at least *100KB*.

#### Downloading files off of your own URLs
Suppose you've already found a webpage with interesting content that you'd like to download. Maybe it's a page full of images (**NowCrawling** can inspect HTML "*img src=*" tags and download images), or maybe it's a website full of songs you found on the web, such as [http://www.mmnt.net/db/0/0/195.137.185.2/Music/Iron%20Maiden](http://www.mmnt.net/db/0/0/195.137.185.2/Music/Iron%20Maiden). **NowCrawling** will make it easy for you to download these files (although you should *really* look into the legality of that).
##### Command

     nowcrawling -f -u "list:http://www.cyn.net/music/Iron%20Maiden%20-%20Brave%20New%20World/" -e mp3 -d "Iron Maiden"
    
##### Explanation
The following options are used **(note that nearly all of these are fully case insensitive, as well as their arguments)**:
* `-f`, `--files`: Explained in the [previous example](FIXME). Tells **NowCrawling** that you want to use it in *File Crawling Mode*.
* `-u`, `--url-list`: This option (which cannot be used with `-k` and `-s`) tells **NowCrawling** to directly use a list of URLs instead of querying Google. This list can be supplied in two different ways:
    * Inline, as part of the argument. It should be a **comma-separated list** prefixed by the "list:" keyword. In this example, we do `-u list:http://www.cyn.net/music/Iron%20Maiden%20-%20Brave%20New%20World/` to use this mode.
    * In a file, supplied as the argument. This file should have all URLs, one per line (with '#' being used for comments). To pass the file to the application, prefix its path by "file:", much like you did with "list:" for the list of URLs.
* `-e`,`--extensions`: Explained in the [previous example](FIXME). We are looking for *mp3* files.
* `-d`, `--directory`: Explained in the [previous example](FIXME). Specifies a directory where we want to save all downloaded files.

#### Using your own regexes
If you're finally getting to grips with **NowCrawling**'s basic commands, such as `-t`, you might consider doing some more advanced crawling by directly building a regex for **NowCrawling** to use.

Take the example seen [previously](FIXME) and imagine that instead of simply matching *"s01e01"* in the file name, you wanted to *also* match *"e01s01". You could run two different NowCrawling instances with different `-t` arguments, or you could replace the `-t` functionality with your own regex to match file names.


##### Command

    nowcrawling -f -k "game of thrones" -r "(s01e01|e01s01)" -e "mkv mp4 avi" -s -a -l 100MB-
    
##### Explanation
Since this is an advanced topic, most of these won't be explained. See the [other examples](FIXME) for a detailed explanation of them:
* `-f`, `-k`, `-e`, `-s`, `-a` and , `-l`: These are the same as in the [original example](FIXME).
* `-r`,`--regex`: This option can be used instead of `-t` to provide a regex which should match part of the filename, but not all of it. By using the "(s01e01|e01s01)" regex, we are forcing the filenames to contain either "s01e01" or "e01s01" (case insensitive) in the filename. This regex parameter allows for flexible filtering of results, improving upon the `-t` option.

### Content Crawling Mode examples
Below is a series of examples of **NowCrawling** in *Content Crawling Mode*, designed to find patterns on the web (e.g. leaked emails, credit card numbers, funky and weirdly named images, etc). An alternative mode is the *File Crawling Mode*, for which examples can be found [above](FIXME).
#### Finding leaked gmail addresses
Content mode is great for finding things on the web. Thinking of building a new spambot targeted at those pesky gmail users? (just kidding, we know you're not *that* pesky) **NowCrawling** can help you! In this example, we do a very simple search for leaked gmail addresses and store them in a file for later inspection.

##### Command

    nowcrawling -c -k "gmail leak" -m "[a-zA-Z0-9]*?@gmail.com" -o leaked_emails.txt

##### Explanation

The following options are used **(note that nearly all of these are fully case insensitive, as well as their arguments)**:
* `-c`, `--content`: This tells **NowCrawling** that you want to use it in *Content Crawling Mode*, whereby it will look for content matches and print them to the screen and, optionally, save them to a file. An alternative mode, which we covered [previously](FIXME), is the *File Crawling Mode* (`-f`, `--file-crawling`).
* `-k`, `--keywords`: This argument works as it did in *File Crawling Mode* (see [the previous example](FIXME)). In this particular case, we do a generic search for a "gmail leak".
* `-m`, `--match`: This option is somewhat similar to the `-r` option in *File Crawling Mode*. It is the obligatory regex you want to use to match patterns. Anything that matches the regex supplied with `-m` will be printed to the console and optionally saved to a file (if such a file has been supplied with `-o`). In our example, we supply a **ridiculously oversimplified email-match regex** to find leaked gmail emails. This is simple, but has moderately good results and should be enough to get you started.
* `-o`, `--output-file`: This optional parameter can be used to pass a file where **NowCrawling** will write the results, besides the standard output. We use it to redirect all our matches to `leaked_emails.txt`, which we could later use in other ways.

#### Finding leaked gmail addresses *and* passwords
The previous example shows how you can find an email address dump, but with a bit more of creativity, there are more "interesting" things that you can find. The following example modifies the previous with a very, very, very primitive regex that is, however, enough to find some leaked emails and passwords.

##### Command

    nowcrawling -c -k "gmail leak dump passwords" -m "[a-zA-Z0-9]*?@gmail\.com:[a-zA-Z0-9]* -o usernames_and_passwords.txt

##### Explanation

The following options are used **(note that nearly all of these are fully case insensitive, as well as their arguments)**:
* `-c`, `--content`: This tells **NowCrawling** that you want to use it in *Content Crawling Mode*, whereby it will look for content matches and print them to the screen and, optionally, save them to a file. An alternative mode, which we covered [previously](FIXME), is the *File Crawling Mode* (`-f`, `--file-crawling`).
* `-k`, `--keywords`: Explained in the [previous example](FIXME). Use for querying Google. In this particular case, we do a generic search for "gmail leak dump passwords". Of course you can refine the search with Google specific keywords to make the results better. Also note that **you can use the *smart search* (`-s`) functionality in *Content Crawling Mode*** too!
* `-m`, `--match`: Explained in the [previous example](FIXME). This time, we modify our regex to include a grossly oversimplified password (with only alphanumeric characters) after a ":" and the email. This gives (perhaps surprisingly) good results!
* `-o`, `--output-file`: Explained in the [previous example](FIXME). Stores all found leaked emails and passwords in the desired output file.

#### Finding credit card numbers on the web
Suppose you want to find credit card numbers that are out on the web, for whatever reason you see fit. With ** NowCrawling**'s *Content Crawling Mode*, this is trivial, provided your regex skills are up to the task.

##### Command

    nowcrawling -c -k "credit cards leak" -m "[0-9]{4}[- ][0-9]{4}[- ][0-9]{4}[- ][0-9]{4}" -o creditcards.txt

##### Explanation

The following options are used **(note that nearly all of these are fully case insensitive, as well as their arguments)**:
* `-c`, `--content`: This tells **NowCrawling** that you want to use it in *Content Crawling Mode*, whereby it will look for content matches and print them to the screen and, optionally, save them to a file. An alternative mode, which we covered [previously](FIXME), is the *File Crawling Mode* (`-f`, `--file-crawling`).
* `-k`, `--keywords`: Explained in the [previous example](FIXME). Use for querying Google. In this particular case, we do a generic search for a "credit cards leak".
* `-m`, `--match`: Explained in the [previous example](FIXME). We use this option to pass our content matching regex. In this particular case, we're looking for four chunks of four digits divided by a space or a hyphen. As with all regexes, this can be greatly improved, for example by specifying the first digits of the card, since they decide the credit card corporation (e.g. 5 for MasterCard and 4 for Visa). **The beauty of NowCrawling's *Content Crawling Mode* is precisely that it all depends on the user's ability to produce great regular expressions!**
* `-o`, `--output-file`: Explained in the [previous example](FIXME). Stores all found credit card numbers in the desired output file.
### Advanced Crawling
Below is a series of more advanced examples where additional, more complex functionality of *NowCrawling* is used.

#### Going deeper: crawling linked pages too (e.g. folders in fileservers)
Sometimes, when crawling for files, your search will return a page which does not have the files yet, but which links to a page which does. This is commonly seen in FTP server pages, such as [http://www.mmnt.net/db/0/0/195.137.185.2/Music/Iron%20Maiden](http://www.mmnt.net/db/0/0/195.137.185.2/Music/Iron%20Maiden). In these cases, it would be useful to allow **NowCrawling** to visit these pages too. Well, you can!

**NowCrawling** has the concept of *recursion depth*, which defines how far away from the base URLs (typically found from Google results with `-k`) you want to go looking for results. By default, this *recursion depth* is fixed at 1, meaning you cannot visit pages linked by your search results. In the example of the FTP server page shown above, the directories containing the actual files will not be visited when you pass that URL to the `-u` option. You can override this behavior and tell **NowCrawling** to go deeper, as we show. **Note that you are guaranteed that for each URL found in your Google search (or manually supplied with `-u`), **NowCrawling** won't visit duplicate links.**

##### Command

    nowcrawling -f -u "list:http://www.mmnt.net/db/0/0/195.137.185.2/Music/Iron%20Maiden" -e "mp3" -d "Iron Maiden" -z 2

##### Explanation

You should already be familiar with the `-f`, `-u`, `-e`, and `-d`options. If you are not, go read their examples [above](FIXME).

`-z`,`--recursion--depth`: This option changes the *recursion depth* of **NowCrawling**. With `-z 2`, we are telling it to visit pages inside the supplied URL itself. If we did `-z 3`, we would allow for even "deeper" searches. **This option is very powerful, and can be used in both *File Content Mode* and *Content Crawling Mode*, but you should be wary of its implications!** The number of visited pages grows **exponentially** with the recursion depth. Consider this, if you visit 10 pages and each of them has 50 links (most of them have over 100 links), you'll be crawling 500 pages instead of 10!

#### Whitelists and Blacklists
You'll quickly notice that while **NowCrawling** is fast (particularly with PyPy), it can't do wonders. Websites such as Youtube or Google Plus have complex HTML and take longer to process. Yet, most times you won't even want to include these pages in your search. It makes sense, then, to be able to **blacklist certain domains** -- which **NowCrawling** supports.

Similarly, you may be interested in only accessing a restricted set of domains To this end, you can use **whitelists**! Blacklists and whitelists are particularly valuable when you are crawling at higher [recursion levels](FIXME), such as `-z 2`and `-z 3`, because they help you filter out lots of unwanted pages.

Both whitelists and blacklists use ***domain files***. These files contain one domain regex per line (with the possibility of using '#') for comments. For instance, you can match all .com domains with `.*\.com`; you can also match youtube with `.*youtube.*\.com`. If you have good regex skills, you'll find writing *domain files* to be a piece of cake.

To tell **NowCrawling** to use a **whitelist** use `-w`,`--whitelist`, e.g.:

    nowcrawling -f -k "Song of Ice and Fire" -e "mp3" -s -w whitelist.list

where `whitelist.list` is just a *domain file* with a couple of regexes for the domains you want to visit. 

The same can be done for **blacklists** with `-b`,`--blacklist`, e.g.:

    nowcrawling -f -k "Song of Ice and Fire" -e "mp3" -s -b blacklist.list

where `blacklist.list` is also a *domain file*

Note that you can't use both `-b`and `-w` and the same time, for obvious reasons.


#### Finding leaked emails and passwords with better regexes
In [another example](FIXME), we showed how simple it was to use equally simple regexes to find leaked emails and passwords (we looked at the specific case of gmail). As a final example, take the following more advanced **NowPlaying** command line, with more advanced regexes to find most kinds of email and password leaks.

##### Example Command 1

    nowcrawling -c -k "email leak dump passwords" -m "[a-zA-Z0-9][a-zA-Z0-9\._]*?@[a-zA-Z0-9]+?\.[a-zA-Z][a-zA-Z]?[a-zA-Z]?:[a-zA-Z0-9\._*\!\@\#\$\%\€\&\=\-\+]+" -o leaked_emails_and_passwords.txt
    
The above command gives impressive results, but we could try to leverage the power of Google to do something more sophisticated. Many leaks come from websites such as [pastebin.com](http://pastebin.com), so why not try to go through Pastebin, using [whitelists](FIXME)? Furthermore, sometimes leaks happen in "close pasties", so we can also try to crawl these neighbouring pasties, which might appear as links in the original pasties. Thus, we can use [higher recursion depth levels](FIXME), combined with whitelists to achieve faster results, at the cost of some leaked emails and passwords:

##### Example Command 2
    nowcrawling -c -k "email leak dump passwords" -m "[a-zA-Z0-9][a-zA-Z0-9\._]*?@[a-zA-Z0-9]+?\.[a-zA-Z][a-zA-Z]?[a-zA-Z]?:[a-zA-Z0-9\._*\!\@\#\$\%\€\&\=\-\+]+" -o leaked_emails_and_passwords.txt -z 2 -w whitelist.list
    
where whitelist.list contains:

    .*pastebin.*

## FAQ
### How does NowCrawling really work?
At its core, **NowCrawling** is really basic stuff. Picture yourself googling for something and then visiting all the results that google gives you. In each result, you carefully look for any URLs that may be in the page (e.g. also in *src=* tags) for interesting content. You may be looking for images, files, leaked emails or something else entirely! As you do this
# TO BE CONTINUED

