"""
A handful of self-contained demo tasks against real, stable public sites
(no login/captcha) so the agent can be recorded end-to-end.
"""

TASKS = {
    "wiki_research": {
        "start_url": "https://www.wikipedia.org",
        "instruction": (
            "Search Wikipedia for 'Alan Turing', open his article, and extract "
            "the year he was born and the year he died. Finish with both years "
            "in your result."
        ),
    },
    "form_fill": {
        "start_url": "https://www.selenium.dev/selenium/web/web-form.html",
        "instruction": (
            "Fill out the web form: put 'Ada Lovelace' in the text input, "
            "'A test message from an autonomous browser agent' in the textarea, "
            "select the second option in the dropdown, check the checkbox, "
            "then click the Submit button. Finish once the page shows the "
            "'Form submitted' confirmation."
        ),
    },
    "book_search_compare": {
        "start_url": "https://books.toscrape.com",
        "instruction": (
            "Find a book in the 'Travel' category and a book in the 'Mystery' "
            "category. Extract both titles and prices. Finish by reporting "
            "which of the two is cheaper."
        ),
    },
    "quotes_extract": {
        "start_url": "https://quotes.toscrape.com",
        "instruction": (
            "Find a quote tagged 'inspirational' on the site, extract the quote "
            "text and its author, and finish by reporting both."
        ),
    },
}
