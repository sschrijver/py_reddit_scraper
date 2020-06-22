# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import Dict, List, Optional

# Pip
from jsoncodable import JSONCodable

# Local
from .comment import Comment
from .video import Video
from .image import Image
from .post_type import PostType

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ------------------------------------------------------------- class: Post -------------------------------------------------------------- #

class Post(JSONCodable):

    # ------------------------------------------------------------- Init ------------------------------------------------------------- #

    def __init__(
        self,
        post_json: Dict,
        comments_json: Optional[List[Dict]] = None
    ):
        self.sub            = post_json['subreddit']
        self.title          = post_json['title']
        self.content        = post_json['selftext']
        self.nsfw           = post_json['over_18']
        self.pinned         = post_json['pinned']
        self.id             = post_json['id']
        self.score          = post_json['score']
        self.upvote_ratio   = post_json['upvote_ratio']
        self.flair_text     = post_json['link_flair_text']
        self.url            = post_json['url'].strip('/')
        self.ts             = int(post_json['created_utc'])
        self.author         = post_json['author']
        self.distinguished  = post_json['distinguished']

        self.post_dict      = post_json
        self.comments_dict  = comments_json

        self.type = PostType.Text if len(self.content) > 0 else PostType.Text
        self.video = None
        self.image = None

        if post_json['is_video']:
            video = Video(post_json)

            if video.video_url is not None:
                self.video = video
                self.type = PostType.Video
        else:
            image = Image(post_json['preview'])

            if image.url is not None:
                self.image = image
                self.type = PostType.Image

        self.comments = []

        if comments_json is None:
            return

        for comment_json in comments_json:
            try:
                self.comments.append(Comment(comment_json['data']))
            except Exception as e:
                print('comment_e', e)

                pass
    
    def __get_video(post: Dict) -> (Optional[str], Optional[str]):
        try:
            video = post['media']['reddit_video']
            
            return video['fallback_url'], video['duration']
        except:
            try:
                video = post['preview']['reddit_video_preview']

                return video['fallback_url'], video['duration']
            except:
                return None, None

        
        post['vid_url'] = post['vid_url'].replace('?source=fallback', '')
    video_url = post['vid_url']
    audio_url = video_url.rsplit('/', 1)[0] + '/audio'


# ---------------------------------------------------------------------------------------------------------------------------------------- #