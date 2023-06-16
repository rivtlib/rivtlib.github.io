#
import logging
import warnings
import fnmatch
import os
import sys
import textwrap
from io import StringIO
from pathlib import Path

import html2text as htm
import matplotlib.pyplot as plt
import pandas as pd
import sympy as sp
import numpy.linalg as la
import numpy as np
from sympy.abc import _clash2
from sympy.core.alphabets import greeks
from sympy.parsing.latex import parse_latex
from tabulate import tabulate
from rivt import parse
from rivt.units import *
from commands import Commands


class CmdRST(Commands):

    def __init__(self, paramL, incrD, folderD,  localD):
        """_summary_

        :param paramL: _description_
        :type paramL: _type_
        :param incrD: _description_
        :type incrD: _type_
        :param folderD: _description_
        :type folderD: _type_
        :param localD: _description_
        :type localD: _type_
        :return: _description_
        :rtype: _type_
        """

        self.localD = localD
        self.folderD = folderD
        self.incrD = incrD
        self.widthII = incrD["widthI"] - 1
        self.paramL = paramL
        self.errlogP = folderD["errlogP"]

        modnameS = __name__.split(".")[1]
        # print(f"{modnameS=}")
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)-8s  " + modnameS +
            "   %(levelname)-8s %(message)s",
            datefmt="%m-%d %H:%M",
            filename=self.errlogP,
            filemode="w",
        )
        warnings.filterwarnings("ignore")

        folderS = paramL[1]
        fileS = paramL[2]
        cmdS = paramL[0]
        if len(folderS) == 3:
            pathP = folderD["pubP"]
            for fS in os.listdir(pathP):
                if fnmatch.fnmatch(fS[0:4], fileS):
                    self.privP = Path(fS)  # private folder
        elif len(folderS) == 5:
            pathP = folderD["prvP"]
            for fS in os.listdir(pathP):
                if fnmatch.fnmatch(fS[0:6], fileS):
                    self.pubP = Path(fS)  # private folder

        self.cmd_parse(cmdS)

    def cmd_parse(self, cmdS):
        """_summary_
        """
        self.cmdS = cmdS
        return eval("self." + cmdS+"()")

    def append(self):
        """append pdf files
        """
        pass

    def github(self):
        """_summary_
        """
        pass

    def project(self):
        """insert project information from csv, xlsx or syk

            :return lineS: md table
            :rtype: str
        """

        alignD = {"s": "", "d": "decimal",
                  "c": "center", "r": "right", "l": "left"}

        tableS = ""
        plenI = 4
        if len(self.paramL) != plenI:
            logging.info(
                f"{self.cmdS} not evaluated: {plenI} parameters required")
            return

        if self.paramL[0].strip() == "resource":
            folderP = Path(self.folderD["resourceP"])
        else:
            folderP = Path(self.folderD["resourceP"])
        fileP = Path(self.paramL[1].strip())
        pathP = Path(folderP / fileP)                    # file path
        maxwI = int(self.paramL[2].split(",")[0])        # max column width
        alignS = alignD[self.paramL[2].split(",")[1].strip()]
        colS = self.paramL[3].strip()                    # rows read
        extS = (pathP.suffix).strip()
        if extS == ".csv":                               # read csv file
            with open(pathP, "r") as csvfile:
                readL = list(csv.reader(csvfile))
        elif extS == ".xlsx":                            # read xls file
            pDF1 = pd.read_excel(pathP, header=None)
            readL = pDF1.values.tolist()
        else:
            logging.info(
                f"{self.cmdS} not evaluated: {extS} file not processed")
            return

        incl_colL = list(range(len(readL[1])))
        if colS == "[:]":
            colL = [] * len(incl_colL)
        else:
            incl_colL = eval(colS)
            colL = eval(colS)
        for row in readL[1:]:                           # select columns
            colL.append([row[i] for i in incl_colL])
        wcontentL = []
        for rowL in colL:                               # wrap columns
            wrowL = []
            for iS in rowL:
                templist = textwrap.wrap(str(iS), int(maxwI))
                templist = [i.replace("""\\n""", """\n""") for i in templist]
                wrowL.append("""\n""".join(templist))
            wcontentL.append(wrowL)
        sys.stdout.flush()
        old_stdout = sys.stdout
        output = StringIO()
        output.write(
            tabulate(
                wcontentL,
                tablefmt="rst",
                headers="firstrow",
                numalign="decimal",
                stralign=alignS,
            )
        )
        tableS = output.getvalue() + "\n\n"
        sys.stdout = old_stdout

        return tableS

    def image(self):
        """insert image from file

        Args:
            il (list): image parameters
        """
        rstS = ""
        iL = self.paramL
        if len(iL[1].split(",")) == 1:
            scale1S = iL[2]
            file1S = iL[1].strip()
            if iL[0].strip() == "resource":
                img1S = str(Path(self.folderD["resourceP"], file1S))
            else:
                img1S = str(Path(self.folderD["resourceP"], file1S))
            img1S = img1S.replace("\\", "/")
            rstS = ("\n.. image:: "
                    + img1S + "\n"
                    + "   :scale: "
                    + scale1S + "%" + "\n"
                    + "   :align: center"
                    + "\n\n"
                    )
        elif len(iL[1].split(",")) == 2:
            iL = self.paramL
            scale1S = iL[2]
            scale2S = iL[4]
            file1S = iL[1].strip()
            file2S = iL[3].strip()
            if iL[0].strip() == "resource":
                img1S = str(Path(self.folderD["resourceP"], file1S))
                img2S = str(Path(self.folderD["resourceP"], file2S))
            else:
                img1S = str(Path(self.folderD["resourceP"], file1S))
                img2S = str(Path(self.folderD["resourceP"], file2S))
            img1S = img1S.replace("\\", "/")
            img2S = img2S.replace("\\", "/")
            rstS = ("|L| . |R|"
                    + "\n\n"
                    + ".. |L| image:: "
                    + img1S + "\n"
                    + "   :width: "
                    + scale1S + "%"
                    + "\n\n"
                    + ".. |R| image:: "
                    + img2S + "\n"
                    + "   :width: "
                    + scale2S + "%"
                    + "\n\n"
                    )
        return rstS

    def table(self):
        """insert table from csv or xlsx file

        Args:
            ipl (list): parameter list
        """
        alignD = {"s": "", "d": "decimal",
                  "c": "center", "r": "right", "l": "left"}

        tableS = ""
        plenI = 4
        if len(self.paramL) != plenI:
            logging.info(
                f"{self.cmdS} command not evaluated: {plenI} parameters required")
            return
        if self.paramL[0] == "data":
            folderP = Path(self.folderD["dataP"])
        else:
            folderP = Path(self.folderD["dataP"])
        fileP = Path(self.paramL[1].strip())
        pathP = Path(folderP / fileP)                    # file path
        maxwI = int(self.paramL[2].split(",")[0])        # max column width
        alignS = alignD[self.paramL[2].split(",")[1].strip()]
        align2S = self.paramL[2].split(",")[1].strip()
        colS = self.paramL[3].strip()                    # rows read
        extS = (pathP.suffix).strip()                    # file suffix
        if extS == ".csv":                               # read csv file
            with open(pathP, "r") as csvfile:
                readL = list(csv.reader(csvfile))
        elif extS == ".xlsx":                            # read xls file
            pdfO = pd.read_excel(pathP, header=None)
            readL = pdfO.values.tolist()
        else:
            logging.info(
                f"{self.cmdS} command not evaluated: {extS} files not processed")
            return
        sys.stdout.flush()
        old_stdout = sys.stdout

        output = StringIO()
        output.write(tabulate(readL, tablefmt="rst", maxcolwidths=maxwI,
                              headers="firstrow", numalign="decimal"))
        rstS = output.getvalue()
        sys.stdout = old_stdout

        # restS = ".. raw:: latex" + "\n\n"       # align cells
        # # for i in rstS.split("\n"):
        # #     counter = i.count("&")
        # #     if counter > 0:
        # #         cS = "{|" + (align2S + "|") * (counter + 1) + "}"
        # #         cS = "{" + align2S * (counter + 1) + "}"
        # #         continue
        # restS += "  \\vspace{.15in}" + "\n"
        # inrstS = ""
        # for i in rstS.split("\n"):
        #     inrstS += "  " + i + "\n\n"
        # restS = restS + inrstS
        # restS += "  \\vspace{.15in}\n"

        restS = "\n" + rstS + "\n\n"
        return restS

    def text(self):
        """insert text from file

        || text | folder | file | type | shade

        """
        plenI = 3
        if len(self.paramL) != plenI:
            logging.info(
                f"{self.cmdS} command not evaluated:  \
                                    {plenI} parameters required")
            return
        if self.paramL[0] == "data":
            folderP = Path(self.folderD["dataP"])
        else:
            folderP = Path(self.folderD["dataP"])
        fileP = Path(self.paramL[1].strip())
        pathP = Path(folderP / fileP)
        txttypeS = self.paramL[2].strip()
        extS = pathP.suffix
        with open(pathP, "r", encoding="md-8") as f1:
            txtfileS = f1.read()
        with open(pathP, "r", encoding="md-8") as f2:
            txtfileL = f2.readlines()
        j = ""
        if extS == ".txt":
            # print(f"{txttypeS=}")
            if txttypeS == "plain":
                for iS in txtfileL:
                    j += "   " + iS
                return "\n\n::\n\n" + j + "\n\n"
            elif txttypeS == "code":
                pass
            elif txttypeS == "tags":
                xtagC = parse.RivtParseTag(
                    self.folderD, self.incrD,  self.localD)
                xrstS, self.incrD, self.folderD, self.localD = xtagC.rst_parse(
                    txtfileL)
                return xrstS
        elif extS == ".html":
            txtS = ".. raw:: html" + "\n\n"
            for iS in txtfileL:
                j += "   " + iS
            return txtS + j + "\n\n"
        elif extS == ".tex":
            if txttypeS == "plain":
                txtS = ".. raw:: latex" + "\n\n"
                for iS in txtfileL:
                    j += "   " + iS
                return txtS + j + "\n\n"
            if txttypeS == "math":
                txtS = ".. math:: " + "\n\n"
                for iS in txtfileL:
                    j += "   " + iS
                return txtS + j + "\n\n"
