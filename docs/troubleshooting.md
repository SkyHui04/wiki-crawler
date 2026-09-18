# Troubleshooting

## CORS Errors from Cached Responses
1. The Ultimate Chrome Network Flush (The Only Way to Clear Internal HSTS/CORS State)
Chrome retains socket pools and preflight caches deep within its internal net-internals system. Standard clearing does not touch these.
2. Open a new tab and go to: [chrome://net-internals/#sockets](chrome://net-internals/#sockets)
3. Click the Flush socket pools button.
4. Next, go to: [chrome://net-internals/#dns](chrome://net-internals/#dns)
5. Click Clear host cache.
6. Close your frontend/backend tabs completely and reopen them.
