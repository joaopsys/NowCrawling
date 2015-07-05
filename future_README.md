NowCrawling is a crawler developed in Python 3 that will help you find files and all sorts of content all across the internet.

It uses Google Search as a starting crawl point and depending on the arguments you provide, it can crawl through a good part of the internet looking for the content you requested.

-First Steps:

Although you can easily check all the application arguments by using the -h option, we highly encourage you to keep reading.

In order to start a simple crawl, you must first decide what are you crawling for: Files or Content ('things' you want to find in a web page, for example e-mails, social security numbers or even credit cards).

--File Crawling:

nowcrawling -f

If you decided to crawl for files, you must use the -f argument.

---File Crawling Examples:

When it comes to file crawling, there are a bunch of arguments you can specify to limit your crawling results. We might as well give you some examples, since we realize it's not that intuitive.

---- Downloading an episode of a TV series

Let's imagine you want to find the first episode of the first season of Game of Thrones. Pretty specific right? Let's go through the parameters you would need to crawl for this:

nowcrawling -f -k "game of thrones" -t "s01e01" -e "mkv mp4 avi" -s

-k "game of thrones" -> This is the main search term that will be used. NowCrawling will insert this term into Google Search and start crawling from there.

-t "s01e01" -> This is a string representing what you want to find in the file name. Usually seasons and episodes are always identified in the episode file name.

-e "mkv mp4 avi" -> If you're crawling for video files, it's a good idea to specify the extensions you want!

-s -> S stands for Smart Search. By using advanced google search terms, NowCrawling will highly reduce the time it takes to find your file. We recommend you to remove this parameter if you're crawling for multiple files, as it will probably also reduce your crawling results. Since we only want one file in this case, it's perfectly fine to use it. WARNING: DO NOT OVERUSE THIS ARGUMENT - Google will ban you temporarily if you do.

That's it! NowCrawling will start hunting for ALL the first episodes of the first season of Game of Thrones it finds, and we mean ALL of them because surely there are thousands of replicas around the internet. We might want to limit even more our crawling results...

nowcrawling -f -k "game of thrones" -t "s01e01" -e "mkv mp4 avi" -s -a -l 100000000-

We added two arguments to our original query:

-a -> This will ask the user before downloading any file. It is recommended, unless you absolutely know what you're doing. Without this, NowCrawling will download everything it finds without asking.

-l 100000000- -> This defines the size limit of the files you're looking for. Since we're looking for good quality episodes, we should only care for files above 100Mb of size (approximately 100000000 bytes). You can also specify a size interval for example: 100000000-900000000 if you only want files between 100 and 900Mb.

---- Downloading a song

Downloading a song is really similar to the previous example. Let's consider Iron Maiden's Blood Brothers.

nowcrawling -f -k "iron maiden" -t "blood brothers" -e "mp3 flac ogg m4a" -s -a

-k "iron maiden" -> Once again, this is basically the 'core' term of your search. You can be more specific for example by specifying the album of the song. In this case it would be something like -k "iron maiden brave new world" since Blood Brothers belongs to the Brave New World album. Doing this can be really efficient and highly improve the crawling time.

-t "blood brothers" -> Usually, song names are present in the name of the file, so that's what we're looking for. This is not a required parameter and as such, if you decide not to use it, you will be downloading all Iron Maiden audio files that NowCrawling finds.

-e "mp3 flac ogg m4a" -> The file extensions you want. We're looking for four audio formats in this case.

-a -> Explained in the previous example. Queries the user before downloading any file.

---- Downloading lots of wallpapers

Sometimes we just want to fill a folder with a bunch of themed wallpapers. In this case, we want 'Space' themed wallpapers.

nowcrawling -f -k "space wallpapers" -t "1920" -e "jpg jpeg png" -d space -l 100000-

-k "space wallpapers" -> At this point, I'm sure you understand what is this for :)

-t "1920" -> This is not required AT ALL. However, to be sure we only get FullHD wallpapers, we want 1920 to be in the file name (1920x1080, 1920x1200), etc. This however, will miss all the wallpapers with random file names (for example 10wkvnbu4nh8302.png) that can be valuable as well! Don't include this for maximum results.

-e "jpg jpeg png" -> Image file extensions. Pretty standard.

-d space -> Specifies the directory where the images will be 'dumped'. If it doesn't exist, it will be created.

-l 100000- -> Once again, this is not required. We just want to make sure that we don't get garbage (for example 1kb images), so we limit file sizes to be greater than 100Kb. This can also miss valuable wallpapers! Don't include this for maximum results.

---- Using regular expressions in the file names

This is an example for advanced users who want to go deep into NowCrawling's functionalities. We allow the user to specify a regular expression for file names. 

Let's take the game of thrones example above and imagine we want NowCrawling to catch not only files with 's01e01' in their name, but also 'e01s01'. Instead of making two different crawls for this, we can simply specify a regular expression instead of the -t flag:

nowcrawling -f -k "game of thrones" -r "(s01e01|e01s01)" -e "mkv mp4 avi" -s -a -l 100000000-

-r "(s01e01|e01s01)" -> The regular expression you want the file name to match. In this case we force the file name to contain EITHER s01e01 OR e01s01.

-- Content Crawling:

nowcrawling -c

If you decided to crawl for content, you must use the -c argument.

--- Content Crawling Examples:

---- Fetching all gmail addresses we can find

Let's imagine you want to find a bunch of GMail e-mails:

nowcrawling -c -k "gmail leak" -m "[a-zA-Z0-9]*?@gmail.com" -o output.txt

-k "gmail leak" -> As we've seen before, this is the main search term of the crawler.

-m "[a-zA-Z0-9]*?@gmail.com" -> The matching regex of the content you want. In this case, this regex represents a Gmail e-mail address.

-o output.txt -> The output file of our results. In the end it will contain all the e-mail addresses it could find.

You can find many more useful options by using the -h argument (for example -z for recursion depth, which will greatly expand your crawling range)
