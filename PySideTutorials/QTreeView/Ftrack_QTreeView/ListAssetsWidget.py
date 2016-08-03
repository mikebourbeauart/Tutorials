from PySide import QtCore, QtGui
from ListAssets import Ui_ListAssets
import ftrack


class ListAssetsWidget(QtGui.QWidget):
    clickedAssetSignal = QtCore.Signal(str, name='clickedAssetSignal')
    clickedAssetTypeSignal = QtCore.Signal(str, name='clickedAssetTypeSignal')

    def __init__(self, parent, task=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_ListAssets()
        self.ui.setupUi(self)
        self.currentAssetType = None
        self.ui.ListAssetsViewModel = QtGui.QStandardItemModel()

        self.ui.ListAssetsSortModel = QtGui.QSortFilterProxyModel()

        self.ui.ListAssetsSortModel.setDynamicSortFilter(True)
        self.ui.ListAssetsSortModel.setFilterKeyColumn(1)
        self.ui.ListAssetsSortModel.setSourceModel(self.ui.ListAssetsViewModel)

        self.ui.ListAssetsView.setModel(self.ui.ListAssetsSortModel)

        self.ui.ListAssetsComboBoxModel = QtGui.QStandardItemModel()

        assetTypes = ftrack.getAssetTypes()
        assetTypes = sorted(assetTypes, key=lambda a: a.getName().lower())

        assetTypeItem = QtGui.QStandardItem('Show All')
        self.ui.ListAssetsComboBoxModel.appendRow(assetTypeItem)

        for assetType in assetTypes:
            assetTypeItem = QtGui.QStandardItem(assetType.getName())
            assetTypeItem.type = assetType.getShort()
            self.ui.ListAssetsComboBoxModel.appendRow(assetTypeItem)

        self.ui.ListAssetsComboBox.setModel(self.ui.ListAssetsComboBoxModel)

    @QtCore.Slot(str)
    def updateView(self, ftrackId):
        try:
            task = ftrack.Task(ftrackId)
            assets = task.getAssets()
            assets = sorted(assets, key=lambda a: a.getName().lower())
            self.ui.ListAssetsViewModel.clear()

            for i in range(len(assets)):
                item = QtGui.QStandardItem(assets[i].getName())
                item.id = assets[i].getId()
                itemType = QtGui.QStandardItem(assets[i].getType().getShort())

                self.ui.ListAssetsViewModel.setItem(i, 0, item)
                self.ui.ListAssetsViewModel.setItem(i, 1, itemType)

        except:
            pass

    @QtCore.Slot(QtCore.QModelIndex)
    def emitAssetId(self, modelindex):
        clickedItem = self.ui.ListAssetsViewModel.itemFromIndex(self.ui.ListAssetsSortModel.mapToSource(modelindex))
        self.clickedAssetSignal.emit(clickedItem.id)

    @QtCore.Slot(int)
    def emitAssetType(self, comboIndex):
        comboItem = self.ui.ListAssetsComboBoxModel.item(comboIndex)
        self.clickedAssetTypeSignal.emit(comboItem.type)
        self.currentAssetType = comboItem.type

    @QtCore.Slot(int)
    def setFilter(self, comboBoxIndex):
        if comboBoxIndex:
            comboItem = self.ui.ListAssetsComboBoxModel.item(comboBoxIndex)
            self.ui.ListAssetsSortModel.setFilterFixedString(comboItem.type)
        else:
            self.ui.ListAssetsSortModel.setFilterFixedString('')

    def getAssetType(self):
        return self.currentAssetType
