# usage: sethook telegram_bot_token <url_to_send_updates_to>
# https://api.telegram.org/bot{my_bot_token}/setWebhook?url={url_to_send_updates_to}
# echo description from response json

if [ -z "$1" ]; then
    echo "Usage:"
    echo "npx sethook telegram_bot_token <url_to_send_updates_to>"
    exit 1
fi

curl -s https://api.telegram.org/bot$1/setWebhook?url=$2 | jq -r '.description'
