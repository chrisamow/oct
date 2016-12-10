




questions / assumptions (since noone to answer them)
	- [ ] rest an fyi not a requirement?  will be easier to make refactorable to rest
	- [ ] word cloud top100 - 
		assume frequent words like 'the' eliminated to make useful
	- [ ] case sensitivity an issue


problems
	wasted time on single quote problem
	first wordcloud had dependency
	getting wordcloud to work



investigate:
	- [ ] any libraries disallowed on app engine - need to check this early
		- yes, using: werkzeug, 
		- yes, useful? pycrypto, pil
	- [ ] tornado security
		http://www.tornadoweb.org/en/stable/guide/security.html
	- [ ] haven't used tornado before
		- interesting, matplotlib has a tornado engine built-in
		- appengine support - need to install but ok
			https://cloud.google.com/appengine/docs/python/tools/using-libraries-python-27
		- http://matplotlib.org/examples/user_interfaces/embedding_webagg.html
		- simple plot
			https://windelbouwman.wordpress.com/2013/07/02/matplotlib-and-tornado/
	- [ ] word cloud - find some leverage - security an issue, must be local
		https://github.com/amueller/word_cloud
		- EMBEDDED C not going to work - disappointing! looked cool
		- [ ] render and upload and image?
		- trying to keep it simple (not using mpld3, etc.)
		- http://matplotlib.org/faq/howto_faq.html#clickable-images-for-html
		https://github.com/atizo/PyTagCloud
		- depends on pygame, not allowed :(
	- [ ] assym enc strategy
	- [ ] appengine storage - anything different about cloudsql?
	- [x] verify appengine environment set up from experiments
	- [ ] bother with sqlalchemy?
	- [ ] font size setting with templates
	- [ ] leverage for html wordcloud



strategy:
- [ ] unit test wordcloud functionality
- [ ] enc proof of concept but don't imp until the end after testing
	https://pythonhosted.org/python-gnupg/
	can generate public key externally and use that programatically
	- [ ] need to check the full round trip and decrypt
- [ ] problem breakdown - each can probably be in a sep module
	- web
		auth
		wordcloud display
		admin summary
	- wordcloud in:url  out:image, histogram
		retrieve
		count
		generate image
	- wordcount
		all db
		enc



checklist at the end:
	- [ ] https appspot.com
	- [ ] security review for each part of the project

	- pyflakes it

