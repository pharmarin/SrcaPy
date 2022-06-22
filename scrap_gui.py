import pyforms
from pyforms import BaseWidget
from pyforms.controls import ControlButton, ControlCheckBoxList, ControlCombo, ControlText, ControlTextArea
from scra import getLink, queryResults


class ScrapperGUI(BaseWidget):

    def __init__(self) -> None:
        super().__init__()
        self.title = "Scrapper"

        self.formset = [("name", "media"), "searchButton",
                        "resultList", "scrapButton", " "]
        self.name = ControlText('')
        self.media = ControlCombo('')
        self.searchButton = ControlButton('Rechercher')
        self.resultList = ControlCheckBoxList('Résultats : ')
        self.scrapButton = ControlButton('Scrapper les liens')
        self.resultLinks = ControlTextArea('', geometry=(100, 100, 150, 150))

        self.media.add_item('Films', 'films')
        self.media.add_item('Séries', 'series')
        self.media.add_item('Mangas', 'mangas')
        self.media.add_item('Musique', 'musiques')

        self.searchButton.value = self.searchMedia
        self.scrapButton.value = self.scrapMedia
        self.resultList.hide()
        self.scrapButton.hide()
        self.resultLinks.title = "Résultat"
        self.resultLinks.hide()

    def searchMedia(self):
        self._results = queryResults(self.name.value, self.media.value)
        self.resultList.value = self._results.keys()
        self.resultList.show()
        self.scrapButton.show()

    def scrapMedia(self):
        selectedIndex = self.resultList.selected_row_index
        selectedLink = list(self._results.values())[selectedIndex]
        scrappedLinks = getLink(selectedLink)
        print(scrappedLinks)
        for link in scrappedLinks:
            self.resultLinks += link
        self.resultLinks.show()


if __name__ == '__main__':
    pyforms.start_app(ScrapperGUI, geometry=(100, 100, 600, 600))
