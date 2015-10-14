# * Recipient number should be in the format of "04xxxxxxxx" where x is a digit
# * Authorization header value should be in the format of "Bearer xxx" where xxx is access token returned 
#   from a previous GET https://api.telstra.com/v1/oauth/token request.
RECIPIENT_NUMBER="0478543891"
TOKEN="3AMIAG7p04LOtQ0pfLomEkdtD2IE"
CONTENT='HELLO'
 
curl -H "Content-Type: application/json" \
-H "Authorization: Bearer $TOKEN" \
-d "{\"to\":\"$RECIPIENT_NUMBER\", \"body\":\"$CONTENT\"}" \
"https://api.telstra.com/v1/sms/messages"
