import re


def parse_to_checkbox(text):
    result = None
    if isinstance(text, list):
        result = []
        for i in text:
            i = re.sub("<ul>", """<ul class="tox-checklist">""", i)
            result.append(i)
    elif isinstance(text, str):
        result = re.sub("<ul>", """<ul class="tox-checklist">""", text)

    return result


if __name__ == "__main__":
    text = "<ul>\r\n<li>eqwe</li>\r\n<li>dsdasdasd</li>\r\n<li>sdasd</li>\r\n<li>dsadasd</li>\r\n<li>&nbsp;</li>\r\n</ul>"
    text2 = [
        "<ul>\r\n<li>eqwe</li>\r\n<li>dsdasdasd</li>\r\n<li>sdasd</li>\r\n<li>dsadasd</li>\r\n</ul>\r\n<p>&nbsp;</p>\r\n<ul>\r\n<li>dasd</li>\r\n</ul>"
    ]

    print(parse_to_checkbox(text))
    print(parse_to_checkbox(text2))
