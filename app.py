from flask import Flask, render_template, redirect, request
from backend import updated_news_api, debrief
import os
from dotenv import load_dotenv

app = Flask(__name__)

@app.route("/app", methods=["POST"])
def build_app():

	main_url = request.get_json()
	title = "Trump executive order to South Africa"
	refined_query = updated_news_api.extract_keywords(title)
	updated_news_api.refined_query(title)
	news_api_key = os.getenv("NEWS_API_KEY")
	articles = updated_news_api.get_news(news_api_key, refined_query)
	
	updated_news_api.display_news(articles)

	summary = "CNN has highlighted prior safety concerns, reporting that in the three years leading up to the crash, pilots had reported near-misses with helicopters at Reagan National Airport. (cnn.com) Reuters provided detailed information on the investigation's progress, including the identification of the soldiers involved and preliminary data suggesting that the helicopter may have been flying above its designated altitude at the time of the collision. (reuters.com) CBS News has focused on the technical aspects of the investigation, reporting that both the plane's black boxes have been recovered and are being analyzed to determine the cause of the crash. (cbs.com)"
	sources = [{"name": "CNN", "image_url": "URL", "article_url": "URL", "date":"2/7/2025", "factuality":"High", "bias":"Center Left", "credibility":"High"}, {"name": "CNN", "image_url": "URL", "article_url": "URL", "date":"2/7/2025", "factuality":"High", "bias":"Center Left", "credibility":"High"}]
	summary_sources = [{"name": "CNN", "image_url": "URL", "article_url": "URL", "date":"2/7/2025", "factuality":"High", "bias":"Center Left", "credibility":"High"}]
	main_source = {"name": "CNN", "image_url": "URL", "article_url": "URL", "date":"2/7/2025", "factuality":"High", "bias":"Center Left", "credibility":"High"}
	media_diet = {}

	return render_template("./testingbase.html", summary=summary, summary_sources=summary_sources, sources=sources, main_source=main_source, media_diet=media_diet)

@app.route("/")
def home():

	summary = "CNN has highlighted prior safety concerns, reporting that in the three years leading up to the crash, pilots had reported near-misses with helicopters at Reagan National Airport. (cnn.com) Reuters provided detailed information on the investigation's progress, including the identification of the soldiers involved and preliminary data suggesting that the helicopter may have been flying above its designated altitude at the time of the collision. (reuters.com) CBS News has focused on the technical aspects of the investigation, reporting that both the plane's black boxes have been recovered and are being analyzed to determine the cause of the crash. (cbs.com)"
	sources = [{"name": "CNN", "image_url": "URL", "article_url": "URL", "date":"2/7/2025", "factuality":"High", "bias":"Center Left", "credibility":"High"}, {"name": "CNN", "image_url": "URL", "article_url": "URL", "date":"2/7/2025", "factuality":"High", "bias":"Center Left", "credibility":"High"}]
	summary_sources = [{"name": "CNN", "image_url": "URL", "article_url": "URL", "date":"2/7/2025", "factuality":"High", "bias":"Center Left", "credibility":"High"}]
	main_source = {"name": "CNN", "image_url": "URL", "article_url": "URL", "date":"2/7/2025", "factuality":"High", "bias":"Center Left", "credibility":"High"}
	media_diet = {}
	
	return render_template("./testingbase.html", summary=summary, summary_sources=summary_sources, sources=sources, main_source=main_source, media_diet=media_diet)