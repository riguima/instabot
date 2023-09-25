from pathlib import Path

from instagrapi import Client
from instagrapi.types import StoryLink, StoryMention
from instagrapi.exceptions import UserNotFound


class Browser:
    def post_story(
        self,
        client: Client,
        media_path: str,
        mentions: list[str] = [],
        links: list[str] = [],
    ) -> None:
        if Path(media_path).name.split('.')[1] in ['jpg', 'jpeg', 'png']:
            function = client.photo_upload_to_story
        else:
            function = client.video_upload_to_story
        story_mentions = []
        for mention in mentions:
            try:
                user = client.user_info_by_username(mention)
                story_mentions.append(
                    StoryMention(
                        user=user,
                        x=0.1,
                        y=0.1,
                        width=0.1,
                        height=0.1,
                    )
                )
            except UserNotFound:
                continue
        function(
            str(Path(media_path).absolute()),
            mentions=story_mentions,
            links=[StoryLink(webUri=link, x=0.5, y=0.75) for link in links],
        )
