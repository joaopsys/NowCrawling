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
* `-t`,`--tags`: The tags argument is used to mandate the existance of certain terms in the files that **NowCrawling** will download. By doing `-t s01e01` we are forcing this file to have this specific keyword somewhere in its name (or, rather, in the URL that directly leads to it). The idea is to use a generic term to search and then limit the desired files with the tags. You can supply any number of tags, separated by spaces. Order is important! Although we intend to change this behavior, the order of tags in the `-t`argument dictates the order in which they must appear in the file. Also note that this option mandates that ALL its arguments be included in the file.
* `-e`, `--extensions`: This argument is used to specify the different extensions (enclosed in commas and separated by spaces) you want to allow in your file. Since we are looking for video, we supply it with *"mkv mp4 avi"* to search for mkv, mp4 and avi files.
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

# TO BE CONTINUED
