# sethook - Set Telegram Webhook for the bot via npx

Now you don't need to remember the syntax to set the webhook for your Telegram bot. Just use `npx` to set the webhook for your bot.

## Usage

### Set the webhook

```bash
npx sethook <token> <url>

# Example
npx sethook 123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11 https://example.com/bot
```

### Delete the webhook

```bash
npx sethook <token>

# Example
npx sethook 123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
```

## Arguments

- `token` - The Telegram Bot API token
- `url` - The URL to set the webhook to


## Description

This package is a simple CLI tool to set the Telegram Webhook for a bot. It uses the Telegram Bot API to set the webhook to the provided URL. If the URL is not provided, it will delete the webhook.

## See also

- [Netlify Telegram Webhook Template](https://github.com/vvmspace/netlify-telegram-webhook-template) - A template to create a Telegram bot webhook using Netlify Functions
