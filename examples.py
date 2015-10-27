# create an object
 curl -X POST \
  -H "X-Parse-Application-Id: APP_ID" \
  -H "X-Parse-REST-API-Key: MASTER_KEY" \
  -H "Content-Type: application/json" \
  -d '{"headline": "Article Headline","id": 1,"page_url": "<www.article.com>"}' \
  https://api.parse.com/1/classes/Article


# create a trigger hook
curl -X POST \
  -H "X-Parse-Application-Id: APP_ID" \
  -H "X-Parse-Master-Key: MASTER_KEY" \
  -H "Content-Type: application/json" \
  -d '{"className": "Article", "triggerName": "beforeSave", "url": "https://api.example.com/Article/beforeSave"}' \
https://api.parse.com/1/hooks/triggers