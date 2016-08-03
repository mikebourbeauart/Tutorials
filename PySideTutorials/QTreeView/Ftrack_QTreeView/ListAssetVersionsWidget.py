from PySide import QtCore, QtGui
from ListAssetVersions import Ui_ListAssetVersions
import ftrack


class ListAssetVersionsWidget(QtGui.QWidget):
    clickedAssetVersionSignal = QtCore.Signal(str, name='clickedAssetVersionSignal')

    def __init__(self, parent, task=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_ListAssetVersions()
        self.ui.setupUi(self)
        self.ui.ListAssetVersionsViewModel = QtGui.QStandardItemModel()
        self.ui.ListAssetVersionsSelectionModel = QtGui.QItemSelectionModel(self.ui.ListAssetVersionsViewModel)

        self.ui.ListAssetVersionsView.setModel(self.ui.ListAssetVersionsViewModel)
        self.ui.ListAssetVersionsView.setSelectionModel(self.ui.ListAssetVersionsSelectionModel)

    @QtCore.Slot(str)
    def updateView(self, ftrackId):
        task = ftrack.Asset(ftrackId)
        versions = task.getVersions()
        versions = sorted(versions, key=lambda a: a.getVersion(), reverse=True)

        self.ui.ListAssetVersionsViewModel.clear()
        for i in range(len(versions)):
            versionRowString = ''
            versionRowString += 'v' + str(versions[i].getVersion())
            versionRowString += ' - '
            versionRowString += str(versions[i].getDate().strftime('%Y-%m-%d'))
            item = QtGui.QStandardItem(versionRowString)
            item.id = versions[i].getId()
            self.ui.ListAssetVersionsViewModel.appendRow(item)
            if i == 0:
                lastVersionIndex = self.ui.ListAssetVersionsViewModel.indexFromItem(item)

        self.ui.ListAssetVersionsSelectionModel.select(lastVersionIndex, QtGui.QItemSelectionModel.Select)
        self.emitAssetVersionId(lastVersionIndex)

    @QtCore.Slot(QtCore.QModelIndex)
    def emitAssetVersionId(self, modelindex):
        clickedItem = self.ui.ListAssetVersionsViewModel.itemFromIndex(modelindex)
        self.clickedAssetVersionSignal.emit(clickedItem.id)

    def clear(self):
        self.ui.ListAssetVersionsViewModel.clear()
