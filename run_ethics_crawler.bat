@echo off
echo AI and Robotics Ethics Wikipedia Crawler
echo.
echo This will crawl Wikipedia for ethics-related articles to enhance the knowledge base.
echo.
pause

cd scripts
python crawl_ethics_wiki.py

echo.
echo Crawling complete! Check the data/wikipedia folder for new articles.
pause