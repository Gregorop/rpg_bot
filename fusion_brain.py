import asyncio
import os, requests, json, base64

from dotenv import load_dotenv
load_dotenv()

fusion_url = 'https://api-key.fusionbrain.ai/'
fusion_api_key = os.getenv('fusion_api_key')
fusion_secret_key = os.getenv('fusion_secret_key')

class Req:
    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
                            'X-Key': f'Key {api_key}',
                            'X-Secret': f'Secret {secret_key}',
                            }
        self.model = self.get_model()

    def get_model(self):
        response = requests.get(self.URL + 'key/api/v1/models', headers=self.AUTH_HEADERS)
        data = response.json()
        return data[0]['id']

    def generate(self, prompt, images=1, width=1024, height=1024):
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {
                "query": f"{prompt}"
            }
        }

        data = {
                'model_id': (None, self.model),
                'params': (None, json.dumps(params), 'application/json')
            }
        
        response = requests.post(self.URL + 'key/api/v1/text2image/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        #если сервис не доступен, то uuid нету
        return data['uuid']

    async def check_generation(self, request_id, attempts=10, delay=15):
        while attempts > 0:
            response = requests.get(
                                f'{self.URL}key/api/v1/text2image/status/{request_id}',
                                headers=self.AUTH_HEADERS)
            
            data = response.json()
            #print(data)
            if data['status'] == 'DONE': return data
            
            attempts -= 1
            await asyncio.sleep(delay)

    def save_pic(self,base64_string,to_filename):
        """
        Декодирование в файл из base64.
        :param name: Имя файла для декодирования
        """
        img = base64.b64decode(base64_string)
        with open(to_filename, 'wb') as file:
            file.write(img)

    def load_pic_to_base64(self,filename='static/404fusion_stub.png'):
        """
        Кодирование изображения в base64, для заглушки цензуры.

        :param filename: Имя файла изображения.
        :return: Строка base64
        """
        with open(filename, 'rb') as file:
            img_data = file.read()
            base64_string = base64.b64encode(img_data)
            return base64_string

    async def generate_for_bot(self,promt):
        m = self.get_model()
        uuid = self.generate(promt,m)
        data = await self.check_generation(uuid)
        if data['censored']: 
            img = self.load_pic_to_base64('static/horny.jpg')
        elif 'images' in data and len(data['images']) > 0:
            img = data['images'][0] #генерируется base64 строка
        else:
            img = self.load_pic_to_base64()
 
        return img #base64 строка

api = Req(fusion_url,fusion_api_key,fusion_secret_key)

async def test():

    #img = api.load_pic_to_base64()
    #api.save_pic(img,'test.png')

    image = await api.generate_for_bot('чтото ужасно неприличное!')
    api.save_pic(image,'test.png')


if __name__ == "__main__":
    asyncio.run(test())