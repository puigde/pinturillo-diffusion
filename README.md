# Pinturillo Diffusion

[Our website](http://pinturillo-diffusion.tech/)

## Running

Development
```
cd app
python -m venv venv
. venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Production
```
docker-compose up --build -d
```
