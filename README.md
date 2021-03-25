# ETtoday Spider

This is a simple project for crawling news data from ETtoday, a Chinese news website.

## Requirement

* python 3.X
* beautifulsoup4
* requests
* tqdm

## Data Format

```=json
{
    "tag": "..",
    "date": "2021/03/24",
    "title": "..",
    "content": ["..", "..", ".."]
}
...
```

## Usage

```
python ettoday.py --start="YYYY/MM/DD" --end="YYYY/MM/DD"
```