# Obtain these keys from the Telstra Developer Portal
CONSUMER_KEY="ZDuzM5gKWl9IM8G4e0VMH2bKorRIU33t"
CONSUMER_SECRET="AUbyh8CJy8gASog1"

curl -X POST \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "client_id=$CONSUMER_KEY&client_secret=$CONSUMER_SECRET&grant_type=client_credentials&scope=SMS" \
"https://api.telstra.com/v1/oauth/token"
