import sys
import maya.OpenMayaUI as omui
from PySide2 import QtWidgets, QtGui, QtCore
import maya.cmds as cmds
from shiboken2 import wrapInstance

def maya_main_window():
    """Return the maya main window widget"""
    main_window = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window), QtWidgets.QWidget)

class HSToolUI(QtWidgets.QDialog):

    def __init__(self, parent=None):
        """Constructor"""

        super(HSToolUI, self).__init__(parent=maya_main_window())
        self.setWindowTitle("Hard Surface Modeling Tool")
        self.resize(500, 200)
        self.setWindowFlags(self.windowFlags() ^
                            QtCore.Qt.WindowContextHelpButtonHint)
        self.create_widgets()
        self.create_layout()
        self.create_connections()
        self.num_bc = 0
        self.num_s = 0
        self.num_r = 0
        self.num_bu = 0
        self.num_b = 0
        self.total_dist = {
            'X': 0,
            'Y': 0,
            'Z': 0
        }

    def create_widgets(self):
        self.cube_btn = QtWidgets.QPushButton()
        self.cube_btn.setIcon(QtGui.QIcon("C:/Users/King/Documents/toolsdev_assignment03/src/bevcube.jpg"))
        self.cube_btn.setIconSize(QtCore.QSize(64, 64))
        self.cube_lbl = QtWidgets.QLabel("Beveled Cube")

        self.screw_btn = QtWidgets.QPushButton()
        self.screw_btn.setIcon(QtGui.QIcon("C:/Users/King/Documents/toolsdev_assignment03/src/screw.jpg"))
        self.screw_btn.setIconSize(QtCore.QSize(64, 64))
        self.screw_lbl = QtWidgets.QLabel("Screw Thread")

        self.ridge_btn = QtWidgets.QPushButton()
        self.ridge_btn.setIcon(QtGui.QIcon("C:/Users/King/Documents/toolsdev_assignment03/src/ridge.jpg"))
        self.ridge_btn.setIconSize(QtCore.QSize(64, 64))
        self.ridge_lbl = QtWidgets.QLabel("Ridges")

        self.button_btn = QtWidgets.QPushButton()
        self.button_btn.setIcon(QtGui.QIcon("C:/Users/King/Documents/toolsdev_assignment03/src/button.jpg"))
        self.button_btn.setIconSize(QtCore.QSize(64, 64))
        self.button_lbl = QtWidgets.QLabel("Button")

        self.brick_btn = QtWidgets.QPushButton()
        self.brick_btn.setIcon(QtGui.QIcon("C:/Users/King/Documents/toolsdev_assignment03/src/brick.jpg"))
        self.brick_btn.setIconSize(QtCore.QSize(64, 64))
        self.brick_lbl = QtWidgets.QLabel("Brick")

        self.selected_lbl = QtWidgets.QLabel("Selected")
        self.selected_le = QtWidgets.QLineEdit()

        self.axis_lbl = QtWidgets.QLabel("Axis Direction")
        self.axis_cmb = QtWidgets.QComboBox()
        self.axis_cmb.addItems(['X', 'Y', 'Z'])

        self.copies_lbl = QtWidgets.QLabel("Copies")
        self.copies_spinbox = QtWidgets.QSpinBox()
        self.copies_spinbox.setValue(1)

        self.dist_lbl = QtWidgets.QLabel("Distance * 0.1 units")
        self.dist_spinbox = QtWidgets.QSpinBox()
        self.dist_spinbox.setValue(10)
        self.dist_spinbox.setMaximum(1000)

        self.create_btn = QtWidgets.QPushButton("Create")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")

    def create_layout(self):
        self.gridlay = QtWidgets.QGridLayout()
        self.gridlay.addWidget(self.cube_btn, 0, 0)
        self.gridlay.addWidget(self.screw_btn, 0, 1)
        self.gridlay.addWidget(self.ridge_btn, 0, 2)
        self.gridlay.addWidget(self.button_btn, 0, 3)
        self.gridlay.addWidget(self.brick_btn, 0, 4)
        self.gridlay.addWidget(self.cube_lbl, 1, 0)
        self.gridlay.addWidget(self.screw_lbl, 1, 1)
        self.gridlay.addWidget(self.ridge_lbl, 1, 2)
        self.gridlay.addWidget(self.button_lbl, 1, 3)
        self.gridlay.addWidget(self.brick_lbl, 1, 4)

        self.selected_lay = QtWidgets.QHBoxLayout()
        self.selected_lay.addWidget(self.selected_lbl)
        self.selected_lay.addWidget(self.selected_le)

        self.axis_lay = QtWidgets.QHBoxLayout()
        self.axis_lay.addWidget(self.axis_lbl)
        self.axis_lay.addWidget(self.axis_cmb)

        self.copies_lay = QtWidgets.QHBoxLayout()
        self.copies_lay.addWidget(self.copies_lbl)
        self.copies_lay.addWidget(self.copies_spinbox)

        self.dist_lay = QtWidgets.QHBoxLayout()
        self.dist_lay.addWidget(self.dist_lbl)
        self.dist_lay.addWidget(self.dist_spinbox)

        self.bottom_btn_lay = QtWidgets.QHBoxLayout()
        self.bottom_btn_lay.addWidget(self.create_btn)
        self.bottom_btn_lay.addWidget(self.cancel_btn)

        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.addLayout(self.gridlay)
        self.main_layout.addLayout(self.selected_lay)
        self.main_layout.addLayout(self.axis_lay)
        self.main_layout.addLayout(self.copies_lay)
        self.main_layout.addLayout(self.dist_lay)
        self.main_layout.addStretch()
        self.main_layout.addLayout(self.bottom_btn_lay)
        self.setLayout(self.main_layout)

    def create_connections(self):
        """Connect out widget signals to slots"""
        self.create_btn.clicked.connect(self.create)
        self.cancel_btn.clicked.connect(self.cancel)
        self.cube_btn.clicked.connect(self.cube)
        self.screw_btn.clicked.connect(self.screw)
        self.ridge_btn.clicked.connect(self.ridge)
        self.button_btn.clicked.connect(self.button)
        self.brick_btn.clicked.connect(self.brick)

    def movePoly(self, name):
        dist_val = self.dist_spinbox.value()
        current_axis = self.axis_cmb.currentText()
        isX = current_axis == 'X'
        isY = current_axis == 'Y'
        isZ = current_axis == 'Z'
        self.total_dist[current_axis] += dist_val
        cmds.move(self.total_dist['X'] * isX * .1, self.total_dist['Y'] * isY * .1, self.total_dist['Z'] * isZ * .1,
                  name,
                  absolute=False)

    def createBeveledCube(self):
        name = 'bc' + str(self.num_bc)
        cmds.polyCube(n=name, sx=1, sy=1, sz=1, h=1, w=1, d=1)
        cmds.polyBevel(name + '.e[0]',
                       name + '.e[1]',
                       name + '.e[2]',
                       name + '.e[3]',
                       segments=4,
                       fraction=0.5,
                       offsetAsFraction=1)
        cmds.delete(name + '.e[9]',
                    name + '.e[5]',
                    name + '.e[13]',
                    name + '.e[1]',
                    name + '.e[7]',
                    name + '.e[11]',
                    name + '.e[15]',
                    name + '.e[3]')
        self.num_bc += 1
        return name

    def createBrick(self):
        name = 'b' + str(self.num_b)
        cmds.polyCube(n=name, sx=1, sy=1, sz=1, h=1, w=2, d=1)
        cmds.polyBevel(n=name, segments=2, fraction=.1, offsetAsFraction=1)
        self.num_b += 1
        return name

    def createRidge(self):
        name = 'r' + str(self.num_r)
        cmds.polyCube(n=name, sx=1, sy=1, sz=1, h=1, w=1, d=5)
        cmds.scale(0.65, 1, 1, name + '.vtx[2:5]')
        self.num_r += 1
        return name

    def createButton(self):
        name = 'bu' + str(self.num_bu)
        cmds.polyCylinder(n=name, sx=8, sy=2, sz=3, h=.2)
        cmds.move(0, 0.144676, 0, name + '.e[40:47]', relative=True)
        cmds.move(0, 0.246665, 0, name + '.e[48:55]', relative=True)
        cmds.move(0, 0.290494, 0, name + '.vtx[57]', relative=True)
        self.num_bu += 1
        return name

    def createScrew(self):
        name = 's' + str(self.num_s)
        cmds.polyHelix(n=name, sa=3, h=11.2, c=12, w=2.3, sco=16, r=.25)
        cmds.delete(name + '.f[0]',
                    name + '.f[3]',
                    name + '.f[6]',
                    name + '.f[9]',
                    name + '.f[12]',
                    name + '.f[15]',
                    name + '.f[18]',
                    name + '.f[21]',
                    name + '.f[24]',
                    name + '.f[27]',
                    name + '.f[30]',
                    name + '.f[33]',
                    name + '.f[36]',
                    name + '.f[39]',
                    name + '.f[42]',
                    name + '.f[45]',
                    name + '.f[48]',
                    name + '.f[51]',
                    name + '.f[54]',
                    name + '.f[57]',
                    name + '.f[60]',
                    name + '.f[63]',
                    name + '.f[66]',
                    name + '.f[69]',
                    name + '.f[72]',
                    name + '.f[75]',
                    name + '.f[78]',
                    name + '.f[81]',
                    name + '.f[84]',
                    name + '.f[87]',
                    name + '.f[90]',
                    name + '.f[93]',
                    name + '.f[96]',
                    name + '.f[99]',
                    name + '.f[102]',
                    name + '.f[105]',
                    name + '.f[108]',
                    name + '.f[111]',
                    name + '.f[114]',
                    name + '.f[117]',
                    name + '.f[120]',
                    name + '.f[123]',
                    name + '.f[126]',
                    name + '.f[129]',
                    name + '.f[132]',
                    name + '.f[135]',
                    name + '.f[138]',
                    name + '.f[141]',
                    name + '.f[144]',
                    name + '.f[147]',
                    name + '.f[150]',
                    name + '.f[153]',
                    name + '.f[156]',
                    name + '.f[159]',
                    name + '.f[162]',
                    name + '.f[165]',
                    name + '.f[168]',
                    name + '.f[171]',
                    name + '.f[174]',
                    name + '.f[177]',
                    name + '.f[180]',
                    name + '.f[183]',
                    name + '.f[186]',
                    name + '.f[189]',
                    name + '.f[192]',
                    name + '.f[195]',
                    name + '.f[198]',
                    name + '.f[201]',
                    name + '.f[204]',
                    name + '.f[207]',
                    name + '.f[210]',
                    name + '.f[213]',
                    name + '.f[216]',
                    name + '.f[219]',
                    name + '.f[222]',
                    name + '.f[225]',
                    name + '.f[228]',
                    name + '.f[231]',
                    name + '.f[234]',
                    name + '.f[237]',
                    name + '.f[240]',
                    name + '.f[243]',
                    name + '.f[246]',
                    name + '.f[249]',
                    name + '.f[252]',
                    name + '.f[255]',
                    name + '.f[258]',
                    name + '.f[261]',
                    name + '.f[264]',
                    name + '.f[267]',
                    name + '.f[270]',
                    name + '.f[273]',
                    name + '.f[276]',
                    name + '.f[279]',
                    name + '.f[282]',
                    name + '.f[285]',
                    name + '.f[288]',
                    name + '.f[291]',
                    name + '.f[294]',
                    name + '.f[297]',
                    name + '.f[300]',
                    name + '.f[303]',
                    name + '.f[306]',
                    name + '.f[309]',
                    name + '.f[312]',
                    name + '.f[315]',
                    name + '.f[318]',
                    name + '.f[321]',
                    name + '.f[324]',
                    name + '.f[327]',
                    name + '.f[330]',
                    name + '.f[333]',
                    name + '.f[336]',
                    name + '.f[339]',
                    name + '.f[342]',
                    name + '.f[345]',
                    name + '.f[348]',
                    name + '.f[351]',
                    name + '.f[354]',
                    name + '.f[357]',
                    name + '.f[360]',
                    name + '.f[363]',
                    name + '.f[366]',
                    name + '.f[369]',
                    name + '.f[372]',
                    name + '.f[375]',
                    name + '.f[378]',
                    name + '.f[381]',
                    name + '.f[384]',
                    name + '.f[387]',
                    name + '.f[390]',
                    name + '.f[393]',
                    name + '.f[396]',
                    name + '.f[399]',
                    name + '.f[402]',
                    name + '.f[405]',
                    name + '.f[408]',
                    name + '.f[411]',
                    name + '.f[414]',
                    name + '.f[417]',
                    name + '.f[420]',
                    name + '.f[423]',
                    name + '.f[426]',
                    name + '.f[429]',
                    name + '.f[432]',
                    name + '.f[435]',
                    name + '.f[438]',
                    name + '.f[441]',
                    name + '.f[444]',
                    name + '.f[447]',
                    name + '.f[450]',
                    name + '.f[453]',
                    name + '.f[456]',
                    name + '.f[459]',
                    name + '.f[462]',
                    name + '.f[465]',
                    name + '.f[468]',
                    name + '.f[471]',
                    name + '.f[474]',
                    name + '.f[477]',
                    name + '.f[480]',
                    name + '.f[483]',
                    name + '.f[486]',
                    name + '.f[489]',
                    name + '.f[492]',
                    name + '.f[495]',
                    name + '.f[498]',
                    name + '.f[501]',
                    name + '.f[504]',
                    name + '.f[507]',
                    name + '.f[510]',
                    name + '.f[513]',
                    name + '.f[516]',
                    name + '.f[519]',
                    name + '.f[522]',
                    name + '.f[525]',
                    name + '.f[528]',
                    name + '.f[531]',
                    name + '.f[534]',
                    name + '.f[537]',
                    name + '.f[540]',
                    name + '.f[543]',
                    name + '.f[546]',
                    name + '.f[549]',
                    name + '.f[552]',
                    name + '.f[555]',
                    name + '.f[558]',
                    name + '.f[561]',
                    name + '.f[564]',
                    name + '.f[567]',
                    name + '.f[570]',
                    name + '.f[573]',
                    name + '.f[576:577]')
        cmds.polyAppend(s=1, tx=1, a=[959, 912])
        cmds.polyAppend(s=1, tx=1, a=[387, 434])
        cmds.polyBridgeEdge(name + '.e[390]', name + '.e[393]', name + '.e[396]', name + '.e[399]', name + '.e[402]',
                            name + '.e[405]', name + '.e[408]', name + '.e[411]', name + '.e[414]', name + '.e[417]',
                            name + '.e[420]', name + '.e[423]', name + '.e[426]', name + '.e[429]', name + '.e[432]',
                            name + '.e[435]', name + '.e[437:438]', name + '.e[440:441]', name + '.e[443:444]',
                            name + '.e[446:447]', name + '.e[449:450]', name + '.e[452:453]', name + '.e[455:456]',
                            name + '.e[458:459]', name + '.e[461:462]', name + '.e[464:465]', name + '.e[467:468]',
                            name + '.e[470:471]', name + '.e[473:474]', name + '.e[476:477]', name + '.e[479:480]',
                            name + '.e[482:483]', name + '.e[485:486]', name + '.e[488:489]', name + '.e[491:492]',
                            name + '.e[494:495]', name + '.e[497:498]', name + '.e[500:501]', name + '.e[503:504]',
                            name + '.e[506:507]', name + '.e[509:510]', name + '.e[512:513]', name + '.e[515:516]',
                            name + '.e[518:519]', name + '.e[521:522]', name + '.e[524:525]', name + '.e[527:528]',
                            name + '.e[530:531]', name + '.e[533:534]', name + '.e[536:537]', name + '.e[539:540]',
                            name + '.e[542:543]', name + '.e[545:546]', name + '.e[548:549]', name + '.e[551:552]',
                            name + '.e[554:555]', name + '.e[557:558]', name + '.e[560:561]', name + '.e[563:564]',
                            name + '.e[566:567]', name + '.e[569:570]', name + '.e[572:573]', name + '.e[575:576]',
                            name + '.e[578:579]', name + '.e[581:582]', name + '.e[584:585]', name + '.e[587:588]',
                            name + '.e[590:591]', name + '.e[593:594]', name + '.e[596:597]', name + '.e[599:600]',
                            name + '.e[602:603]', name + '.e[605:606]', name + '.e[608:609]', name + '.e[611:612]',
                            name + '.e[614:615]', name + '.e[617:618]', name + '.e[620:621]', name + '.e[623:624]',
                            name + '.e[626:627]', name + '.e[629:630]', name + '.e[632:633]', name + '.e[635:636]',
                            name + '.e[638:639]', name + '.e[641:642]', name + '.e[644:645]', name + '.e[647:648]',
                            name + '.e[650:651]', name + '.e[653:654]', name + '.e[656:657]', name + '.e[659:660]',
                            name + '.e[662:663]', name + '.e[665:666]', name + '.e[668:669]', name + '.e[671:672]',
                            name + '.e[674:675]', name + '.e[677:678]', name + '.e[680:681]', name + '.e[683:684]',
                            name + '.e[686:687]', name + '.e[689:690]', name + '.e[692:693]', name + '.e[695:696]',
                            name + '.e[698:699]', name + '.e[701:702]', name + '.e[704:705]', name + '.e[707:708]',
                            name + '.e[710:711]', name + '.e[713:714]', name + '.e[716:717]', name + '.e[719:720]',
                            name + '.e[722:723]', name + '.e[725:726]', name + '.e[728:729]', name + '.e[731:732]',
                            name + '.e[734:735]', name + '.e[737:738]', name + '.e[740:741]', name + '.e[743:744]',
                            name + '.e[746:747]', name + '.e[749:750]', name + '.e[752:753]', name + '.e[755:756]',
                            name + '.e[758:759]', name + '.e[761:762]', name + '.e[764:765]', name + '.e[767:768]',
                            name + '.e[770:771]', name + '.e[773:774]', name + '.e[776:777]', name + '.e[779:780]',
                            name + '.e[782:783]', name + '.e[785:786]', name + '.e[788:789]', name + '.e[791:792]',
                            name + '.e[794:795]', name + '.e[797:798]', name + '.e[800:801]', name + '.e[803:804]',
                            name + '.e[806:807]', name + '.e[809:810]', name + '.e[812:813]', name + '.e[815:816]',
                            name + '.e[818:819]', name + '.e[821:822]', name + '.e[824:825]', name + '.e[827:828]',
                            name + '.e[830:831]', name + '.e[833:834]', name + '.e[836:837]', name + '.e[839:840]',
                            name + '.e[842:843]', name + '.e[845:846]', name + '.e[848:849]', name + '.e[851:852]',
                            name + '.e[854:855]', name + '.e[857:858]', name + '.e[860:861]', name + '.e[863:864]',
                            name + '.e[866:867]', name + '.e[869:870]', name + '.e[872:873]', name + '.e[875:876]',
                            name + '.e[878:879]', name + '.e[881:882]', name + '.e[884:885]', name + '.e[887:888]',
                            name + '.e[890:891]', name + '.e[893:894]', name + '.e[896:897]', name + '.e[899:900]',
                            name + '.e[902:903]', name + '.e[905:906]', name + '.e[908:909]', name + '.e[911]',
                            name + '.e[914]', name + '.e[917]', name + '.e[920]', name + '.e[923]', name + '.e[926]',
                            name + '.e[929]', name + '.e[932]', name + '.e[935]', name + '.e[938]', name + '.e[941]',
                            name + '.e[944]', name + '.e[947]', name + '.e[950]', name + '.e[953]', name + '.e[956]',
                            sma=30, dv=0)
        self.num_s += 1
        return name

    """Connections"""

    @QtCore.Slot()
    def cube(self):
        self.selected_le.setText("Beveled Cube")

    @QtCore.Slot()
    def screw(self):
        self.selected_le.setText("Screw Thread")

    @QtCore.Slot()
    def ridge(self):
        self.selected_le.setText("Ridge")

    @QtCore.Slot()
    def button(self):
        self.selected_le.setText("Button")

    @QtCore.Slot()
    def brick(self):
        self.selected_le.setText("Brick")

    @QtCore.Slot()
    def create(self):
        selected = self.selected_le.displayText()
        copies = self.copies_spinbox.value()
        for i in range(copies):
            if selected == "Beveled Cube":
                self.movePoly(self.createBeveledCube())

            if selected == "Screw Thread":
                self.movePoly(self.createScrew())

            if selected == "Ridge":
                self.movePoly(self.createRidge())

            if selected == "Button":
                self.movePoly(self.createButton())

            if selected == "Brick":
                self.movePoly(self.createBrick())

    @QtCore.Slot()
    def cancel(self):
        self.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = GridLayout()
    window.show()
    sys.exit(app.exe_())
