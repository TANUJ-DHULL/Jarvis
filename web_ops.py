import webbrowser
import wikipedia

def search_wikipedia(query):
    try:
        query = query.replace("wikipedia", "")
        results = wikipedia.summary(query, sentences=2)
        return results
    except Exception as e:
        return f"Could not find information on {query}."

def open_youtube():
    webbrowser.open_new_tab("https://youtube.com")

def open_google():
    webbrowser.open_new_tab("https://google.com")

def search_google(query):
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open_new_tab(url)

def open_facebook():
    webbrowser.open_new_tab("https://facebook.com")

def open_instagram():
    webbrowser.open_new_tab("https://instagram.com")

def open_whatsapp():
    try:
        from system_ops import open_application
        if not open_application("whatsapp"):
            webbrowser.open_new_tab("https://web.whatsapp.com")
    except:
        webbrowser.open_new_tab("https://web.whatsapp.com")

def open_twitter():
    webbrowser.open_new_tab("https://twitter.com")

def open_discord():
    webbrowser.open_new_tab("https://discord.com/app")

def open_telegram():
    webbrowser.open_new_tab("https://web.telegram.org")

def play_on_youtube(query):
    import urllib.request
    import urllib.parse
    import re
    try:
        query_string = urllib.parse.urlencode({"search_query": query})
        html_content = urllib.request.urlopen("https://www.youtube.com/results?" + query_string)
        search_results = re.findall(r'watch\?v=(\S{11})', html_content.read().decode())
        if search_results:
            video_url = "https://www.youtube.com/watch?v=" + search_results[0]
            webbrowser.open_new_tab(video_url)
            return True
        return False
    except:
        return False
