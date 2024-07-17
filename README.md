## Running The App

pip install -r requirements.txt

```bash
python main.py
```

## Viewing The App

Build the image using 

docker build -t eduhub .

Run this after creating the image

docker run -d -p 5000:5000 eduhub

go to the container and view