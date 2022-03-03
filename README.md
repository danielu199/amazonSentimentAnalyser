# amazonSentimentAnalyzer

amazonSentimentAnalyzer is a repository for getting a quick overview over many Amazon reviews for a product. It scrapes up to 1000 most relevant reviews (depending on how many there are), identifies relevant categories, and analyses a general sentiment for those categories. Finally, it presents its findings in a simple bar graph.

## Usage

Create a virtual environment

```bash
python3 -m venv /path/to/repository
```

Change the current directory and activate the environment

```bash
cd /path/to/repository
source bin/activate
```
Then you install all required packages with the requirements.txt

```bash
pip install -r requirements.txt
```
Finally start the scrip 'start.py'

```bash
python start.py
``` 

Now you can start, just find any product from amazon.com and insert the product ID. You can find it in the url of the product. It always comes after /dp/. It could look something like: 

https://www.amazon.com/dp/**B07PY34G7Y**/

Have fun playing with different products. All are possible.

This repository is for educational purposes only.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)