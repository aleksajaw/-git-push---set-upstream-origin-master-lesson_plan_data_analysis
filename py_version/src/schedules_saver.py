from constants import scheduleExcelPath, excelEngineName, scheduleExcelJSONPath, scheduleDfsJSONPath, scheduleJSONPath
from utils import convertToObjOfDfs, convertObjOfDfsToJSON, createDraftSheetIfNecessary, convertCurrExcelToDfsJSON, writingObjOfDfsToExcel, delDraftIfNecessary, compareAndUpdateFile
#, colLetterToNr
import json
from openpyxl import load_workbook
from openpyxl.styles import Alignment
from openpyxl.utils import column_index_from_string
from pandas import ExcelWriter

classesDataJSON = ''
classesDataDfs = None
classesDataDfsJSON = ''


def loadClassesDataVariables(classesData):
    
    global classesDataJSON, classesDataDfs, classesDataDfsJSON

    classesDataJSON = json.dumps(classesData, indent=4)
    classesDataDfs = convertToObjOfDfs(classesData)
    classesDataDfsJSON = convertObjOfDfsToJSON(classesDataDfs)


def createOrEditExcelFile():
    
    global classesDataJSON, classesDataDfs, classesDataDfsJSON

    createDraftSheetIfNecessary()

    try:

        with ExcelWriter(scheduleExcelPath, mode='a', if_sheet_exists='replace', engine=excelEngineName) as writer:

            workbook = writer.book
            currExcelAsJSON = convertCurrExcelToDfsJSON()

            try:
                if not (currExcelAsJSON == classesDataDfsJSON):
                    writingObjOfDfsToExcel(writer, classesDataDfs)
                    currExcelAsJSON = classesDataDfsJSON

                else:
                    print('Nothing to be updated in Excel file.')

                delDraftIfNecessary(workbook)

                compareAndUpdateFile(scheduleExcelJSONPath, currExcelAsJSON)
                compareAndUpdateFile(scheduleDfsJSONPath, classesDataDfsJSON)
                compareAndUpdateFile(scheduleJSONPath, classesDataJSON)

            except Exception as e: 
                print(f"Error writing data to the Excel file: {e}")


        wb = load_workbook(scheduleExcelPath)
        rowsCounter = 0

        for ws in wb.worksheets:
            rowsCounter+=1
            rowsLines = {}
            colsLength = {}

            for col in ws.columns:
                colLetter = col[0].column_letter
                colIndex = column_index_from_string(colLetter)
                
                # init content length for specific column in worksheet
                colsLength[colIndex] = 1

                for cell in col:

                    if cell.row not in rowsLines:
                        rowsLines[cell.row] = 1

                    maxRowLines = rowsLines[cell.row]
                    maxColLength = colsLength[cell.column]
                    
                    try:
                        if isinstance(cell.value, str) and '\n' in cell.value:
                          linesCount = cell.value.count('\n') + 1
                          rowsLines[cell.row] = max(maxRowLines, linesCount)
                          temp = cell.value.split('\n')
                          for t in temp:
                              colsLength[cell.column] = max(maxColLength, len(str(t)))
                        else:
                          colsLength[cell.column] = max(maxColLength, len(str(cell.value)))

                        cell.alignment = Alignment(wrap_text=True, horizontal='center', vertical='center') 
                    except:
                        pass

                ws.column_dimensions[colLetter].width = colsLength[column_index_from_string(colLetter)] + 1

        wb.save(scheduleExcelPath)
        

    except Exception as e:
        print(f"Error reading the Excel file: {e}")