from feedgen.feed import FeedGenerator

fg = FeedGenerator()
fg.load_extension("podcast")

fg.title("My Podcast")
fg.link(href="https://mypodcast.com", rel="alternate")
fg.description("A great podcast!")
fg.language("en")

episode = fg.add_entry()
episode.id("episode-id")
episode.title("Episode 1")
episode.description("Description")
episode.enclosure("https://mypodcast.com/audio/ep1.mp3", 12345678, "audio/mpeg")

fg.rss_file("podcast.xml")
