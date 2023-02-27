"""
Export entities to an HTML view of your document
"""

import json
import re

import requests
from documentcloud.addon import AddOn


class EntityExport(AddOn):
    def main(self):

        document = next(self.get_documents())

        text = document.get_full_text()

        resp = self.client.get(f"documents/{document.id}/entities/?expand=entity")
        occurrences = []
        for entity in resp.json()["results"]:
            for occurrence in entity["occurrences"]:
                occurrences.append(
                    (
                        occurrence["offset"],
                        len(occurrence["content"]),
                        entity["entity"]["wikipedia_url"],
                    )
                )
        occurrences.sort()

        builder = []
        current = 0
        for offset, length, url in occurrences:
            builder.append(text[current:offset])
            builder.append(f'<a href="{url}">')
            builder.append(text[offset : offset + length])
            builder.append(f"</a>")
            current = offset + length

        builder.append(text[current:])
        text = "".join(builder)

        with open("template.html") as template, open(
            f"{document.title}.html", "w+"
        ) as file:
            output_text = template.read().replace("{{ text }}", text)
            file.write(output_text)

            self.upload_file(file)


if __name__ == "__main__":
    EntityExport().main()
