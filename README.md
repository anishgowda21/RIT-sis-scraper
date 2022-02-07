
# RIT SIS scraper

An api built using fastapi to get student info from [RIT](http://parents.msrit.edu) website

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) [![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Fanishgowda21%2FRIT-sis-scraper&count_bg=%23C428CF&title_bg=%23555555&icon=visualstudiocode.svg&icon_color=%23E7E7E7&title=hits&edge_flat=false)](https://hits.seeyoufarm.com) [![Open Source Love svg1](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/)

## Run Locally

Clone the project

```bash
  git clone https://github.com/anishgowda21/RIT-sis-scraper
```

Go to the project directory

```bash
  cd RIT-sis-scraper
```

Install dependencies

```bash
  pip3 install -r requirements.txt
```

Start the server

```bash
  uvicorn main:app --reload
```

- Go to `http://127.0.0.1:8000/doc` (The port number may be diffrent check it in your terminal)
## Deployment

### If you wish to deploy this project in heroku just click the button below 
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/anishgowda21/RIT-sis-scraper/tree/master)


## API Reference

#### Get sis data

```http
  GET /sis/?usn={usn}&dob={dob}
```
### Note if you are a first year please add parameter `firstyear=true`
```http
  GET /sis/?usn={usn}&dob={dob}&firstyear=true
```
| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `usn` | `string` | **Required**. your usn  |
| `dob` | `string` | **Required**. your dob in yyyy-mm-dd form  |
| `firstyear` | `bool` | **optional**. If you are a first year add this|

## Example api call from local machine

### `http://127.0.0.1:8000/sis/?usn=1ms19cd540&dob=2001-07-21`

## For a first year student

### `http://127.0.0.1:8000/sis/?usn=1ms19cd540&dob=2001-07-21&firstyear=true`
## 
## Contributing

Any suggestions for this project is welcome
- Just fork the repo make your changes and send a PR

### If you like this [project](https://github.com/anishgowda21/RIT-sis-scraper) show some :heart: and give this repo a :star:
## Thank You