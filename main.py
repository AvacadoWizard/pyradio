import vlc
import time

# Create a VLC instance
instance = vlc.Instance()

# Create a media player
player = instance.media_player_new()

# Create a media object from a URL
media = instance.media_new("https://das-edge11-live365-dal03.cdnstream.com/a88248")

# Set the media to the player
player.set_media(media)

# Play the media
player.play()


while True:
    print("oka")
    media.parse()
    print("Metadata:")
    print(f"  Title: {media.get_meta(vlc.Meta.Title)}")
    print(f"  Artist: {media.get_meta(vlc.Meta.Artist)}")
    print(f"  Album: {media.get_meta(vlc.Meta.Album)}")
    print(f"  Genre: {media.get_meta(vlc.Meta.Genre)}")
    time.sleep(1)
    print("hj")