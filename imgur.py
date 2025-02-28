# meta developer @YA_ManuI

import requests
import os
from hikkatl.types import Message
from hikkatl.tl.types import DocumentAttributeVideo
from .. import loader, utils

@loader.tds
class ImgurVideoUploaderMod(loader.Module):
    """Загрузка видео в Imgur по реплаю для получения ссылки банера"""
    strings = {"name": "ImgurVideoUploader"}

    async def client_ready(self, client, db):
        self.client = client
        #по желанию можете вставить свой ид
        self.imgur_client_id = "7d2898754c1a0285ccbf9952f310dd2e" 

    @loader.command()
    async def ivup(self, message: Message):
        """Загрузить видео из реплая в Imgur"""
        reply = await message.get_reply_message()
        if not reply or not reply.media:
            await utils.answer(message, "❌ Нужен реплай на видео!")
            return


        try:
            video = await reply.download_media(bytes)
        except Exception as e:
            await utils.answer(message, f"❌ Ошибка скачивания: {e}")
            return

        if len(video) > 200 * 1024 * 1024:
            await utils.answer(message, "❌ Файл слишком большой (макс. 200MB)!")
            return

        await utils.answer(message, "⏳ Загружаю....")

        try:
            response = requests.post(
                "https://api.imgur.com/3/upload",
                headers={"Authorization": f"Client-ID {self.imgur_client_id}"},
                files={"video": video},
            )
            response.raise_for_status()
            data = response.json()
        
            if data.get("success", False):
                link = data["data"].get("link", "")
                await utils.answer(message, f"✅ Видео загружено!\n🔗 {link}")
            else:
                await utils.answer(message, f"❌ Ошибка загрузки: {data.get('data', {}).get('error', 'Unknown error')}")
    
        except Exception as e:
            await utils.answer(message, f"❌ Ошибка при загрузке: {e}")