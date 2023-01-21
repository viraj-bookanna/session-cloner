import base64,logging,os,sys,time,telethon,asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.functions.auth import AcceptLoginTokenRequest
from dotenv import load_dotenv

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
load_dotenv(override=True)

API_ID = os.getenv('TG_API_ID')
API_HASH = os.getenv('TG_API_HASH')

async def clone():
    while 1:
        client = TelegramClient(StringSession(input('SESSION_STRING: ')), API_ID, API_HASH)
        await client.connect()
        is_valid = await client.is_user_authorized()
        if not is_valid:
            print('session invalid')
            client.disconnect()
        else:
            break
    try:
        clone = TelegramClient(StringSession(), API_ID, API_HASH)
        await clone.connect()
        qr_login = await clone.qr_login()
        token = base64.urlsafe_b64decode(qr_login.url.split('token=')[1]+'==')
        result = await client(AcceptLoginTokenRequest(token=token))
        try:
            await qr_login.wait()
        except telethon.errors.SessionPasswordNeededError:
            await client.sign_in(password=input('Password: '))
        print('\n', '='*20, 'CLONED SESSION SUCCESSFULLY','='*20, '\n{}\n'.format(clone.session.save()) ,'='*50, '\n')
    except Exception as e:
        print(repr(e))
    await client.disconnect()
    await clone.disconnect()
asyncio.run(clone())