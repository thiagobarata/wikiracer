import subprocess
from urllib.parse import unquote
import utils

"""
The Command I want to imitate

curl -s https://en.wikipedia.org/wiki/Linux \
| htmlq --attribute href a \
| grep '^/wiki/' \
| grep -Ev '^/wiki/(Special:|Help:|Talk:|Portal:|File:|Wikipedia:|Category:)'


"""


def get_links_to_other_pages(link_snippet):

    url = utils.to_url(link_snippet)

    # curl -s <url>
    curl_output = subprocess.Popen(
        ['curl', '-s', url],
        stdout=subprocess.PIPE,
        text=True
    )

    # htmlq --attribute href a
    all_links = subprocess.Popen(
        ['htmlq', '--attribute', 'href', 'a'],
        stdin=curl_output.stdout,
        stdout=subprocess.PIPE,
        text=True
    )

    # grep '^/wiki/'
    wiki_links = subprocess.Popen(
        ['grep', '^/wiki/'],
        stdin=all_links.stdout,
        stdout=subprocess.PIPE,
        text=True
    )

    # grep -Ev '^/wiki/(Special:|Help:|Talk:|Portal:|File:|Wikipedia:|Category:)'
    wiki_links_to_other_pages = subprocess.Popen(
        ['grep', '-Ev', '^/wiki/(Special:|Help:|Talk:|Portal:|File:|Wikipedia:|Category:|Template:|Template_Talk:)'],
        stdin=wiki_links.stdout,
        stdout=subprocess.PIPE,
        text=True
    )

    # Get final output
    output, _ = wiki_links_to_other_pages.communicate()

    links = output.strip().split('\n') if output else []
    decoded_links = [unquote(link) for link in links] # This part is for links encoded partially in hexadecimal characters e.g Victor Félix Bernadou with that special é
    
    # Sometimes we get duplicate links, so we need to remove them

    no_duplicates_decoded_links = utils.remove_duplicates(decoded_links)

    # Removing the wiki prefix
    cleaned_list = [link[6:] for link in no_duplicates_decoded_links ]

    return cleaned_list

if __name__ =="__main__":
    links = get_links_to_other_pages("Denis_Matiola")
    print(links)



