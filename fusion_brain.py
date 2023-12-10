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

    def get_model(self):
        response = requests.get(self.URL + 'key/api/v1/models', headers=self.AUTH_HEADERS)
        data = response.json()
        return data[0]['id']

    def generate(self, prompt, model, images=1, width=1024, height=1024):
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
                'model_id': (None, model),
                'params': (None, json.dumps(params), 'application/json')
            }
        
        response = requests.post(self.URL + 'key/api/v1/text2image/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        #если сервис не доступен, то uuid нету
        return data['uuid']

    async def check_generation(self, request_id, attempts=10, delay=10):
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/text2image/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            if data['status'] == 'DONE':
                return data['images'][0]

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

    async def generate_from_bot(self,promt):
        m = self.get_model()
        uuid = self.generate(promt,m)
        image = await self.check_generation(uuid)
        img = base64.b64decode(image)
        return img #base64 строка

api = Req(fusion_url,fusion_api_key,fusion_secret_key)

async def test():
    m = api.get_model()
    uuid = api.generate('рпг перс',m)
    image = await api.check_generation(uuid)
    api.save_pic(image,'test.png','/')

if __name__ == "__main__":
    asyncio.run(test())