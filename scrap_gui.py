import pyforms
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlButton, ControlCheckBoxList, ControlCombo, ControlText, ControlTextArea
import pyperclip
from scra import formatWish, getLink, search


class ScrapperGUI(BaseWidget):

    def __init__(self) -> None:
        super().__init__()
        self.title = "Scrapper"

        self.formset = [("name", "media"), "searchButton",
                        "resultList", "scrapButton", ("sitePicker", "resultButton"), " "]
        self.name = ControlText('')
        self.media = ControlCombo('')
        self.searchButton = ControlButton('Rechercher')
        self.resultList = ControlCheckBoxList('Résultats : ')
        self.scrapButton = ControlButton('Scrapper les liens')
        self.sitePicker = ControlCombo('Choisir un site de téléchargement :')
        self.resultButton = ControlButton('Copier')
        self.resultLinks = ControlTextArea('', geometry=(100, 100, 150, 150))

        self.media.add_item('Films', 'films')
        self.media.add_item('Séries', 'series')
        self.media.add_item('Mangas', 'mangas')
        self.media.add_item('Musique', 'musiques')

        self.searchButton.value = self.searchMedia
        self.scrapButton.value = self.scrapMedia
        self.resultButton.value = self.copyLinks

        self.resultList.hide()
        self.scrapButton.hide()
        self.sitePicker.hide()
        self.resultButton.hide()

    def searchMedia(self):
        self._results = {}
        self._results.update(search(
            formatWish(self.name.value), self.media.value))
        self.resultList.value = self._results.keys()
        self.resultList.show()
        self.scrapButton.show()

    def scrapMedia(self):
        selectedIndex = self.resultList.selected_row_index
        selectedLink = list(self._results.values())[selectedIndex]
        self._scrappedLinks = getLink(selectedLink)

        self.sitePicker.add_item("Tous")
        for site in self._scrappedLinks.keys():
            self.sitePicker.add_item(site)

        self.sitePicker.show()
        self.resultButton.show()

    def copyLinks(self):
        if self.sitePicker.value == "Tous":
            allLinks = []
            for site in self._scrappedLinks.values():
                allLinks += site
            pyperclip.copy("\n".join(allLinks))
        else:
            pyperclip.copy(
                "\n".join(self._scrappedLinks[self.sitePicker.value]))


if __name__ == '__main__':
    pyforms.start_app(ScrapperGUI, geometry=(100, 100, 600, 600))
