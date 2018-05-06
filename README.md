# EmailEraserUOL

#### UOL email webapp has a limit of 100 email deletion for each action.
#### This constraint makes manually deleting a full inbox infeasible, so I wrote this script to automate this process.

# Running it:
1. Have Python 2.7x, pip and (optionally) virtualenv installed on your machine. 
1. Clone this repository
1. Run 'pip install -r requirements'
1. Log into your UOL account and copy _webmail_session_id cookie value and paste it into COOKIE_STR environment variable inside .env file. (You can do that with EditThisCookie Chrome extension or analyzing the request in your browser)
1. Run 'python eraseEmail.py'
1. Wait a little bit, because this scripts uses blocking requests.
