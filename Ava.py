from telethon import functions, types
from .. import loader, utils
import io, os
from PIL import Image
def register(cb): cb(AvaMod())
class AvaMod(loader.Module):
    """Встановлення/видаленнч аватарок через команди"""
    strings = {'name': 'Ava'}
    def __init__(self): self.name = self.strings['name']
    async def client_ready(self, client, db): pass
    async def avacmd(self, message):
        'Встановити аватаркуку <reply to image>'
        reply = await message.get_reply_message()
        try: reply.media
        except: return await message.edit("ALO нема медіа/>?")
        await message.edit("Качаємо фото")
        await message.edit("Ставимо аву")
        up = await make_square(reply)
        await message.client(
            functions.photos.UploadProfilePhotoRequest(
                fallback=True,
                file=await message.client.upload_file(photo=file),
                )
            )
        await message.edit("Ава встаноалена")
    async def delavacmd(self, message):
        'Видалити активну аватарку'
        ava = await message.client.get_profile_photos('me', limit=1)
        if len(ava) > 0:
            await message.edit("Видаляємо аватарку...")
            await message.client(functions.photos.DeletePhotosRequest(ava))
            await message.edit("Перша аватарка видадена")
        else:
            await message.edit("Гей, шкірчний чоловіче!Здається в тебе нема аватарок.")
    async def delavascmd(self, message):
        'Видалити усі аватарки'
        ava = await message.client.get_profile_photos('me')
        if len(ava) > 0:
            await message.edit("Видаляємо аватарки...")
            await message.client(functions.photos.DeletePhotosRequest(await message.client.get_profile_photos('me')))
            await message.edit("Аватарки видалені.")
        else:
            await message.edit("Гей,шкірчний чоловіче! Здається в тебе нема аватарок")
async def make_square(msg):
    '''not checking input'''
    image = Image.open(io.BytesIO(await msg.download_media(bytes)))
    width, height = image.size
    # Calculate the upper left and lower right coordinates for the cropped image
    left = (width - min(width, height)) // 2
    upper = (height - min(width, height)) // 2
    right = left + min(width, height)
    lower = upper + min(width, height)
    image = image.crop((left, upper, right, lower)).convert("RGB")
    output_bytes = io.BytesIO()
    image.save(output_bytes, format='JPEG', quality=100)
    output_bytes.seek(0)
    return output_bytes
