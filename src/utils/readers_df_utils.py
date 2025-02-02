from error_utils import handleErrorMsg, getTraceback
from src.constants.paths_constants import scheduleClassesExcelPath
from src.constants.conversion_constants import excelEngineName, JSONIndentValue
from src.constants.schedule_structures_constants import excelMargin, timeIndexNames, dayAndAttrNames, dfColWeekDayNamesTuples5el, dfColWeekDayNamesTuples4el
from pandas import read_excel, MultiIndex, DataFrame
import json



def readExcelFileAsObjOfDfs(excelFilePath=scheduleClassesExcelPath):
    from files_utils import doesFileExist
    dataToConvert = {}
    msgText = ''

    if doesFileExist(excelFilePath):
        try:
            excelData = read_excel( io=excelFilePath, sheet_name=None, engine=excelEngineName, keep_default_na=False,
                                    header=[excelMargin['row'], excelMargin['row']+1], index_col=[excelMargin['col'], excelMargin['col']+1])

            for sheetName, df in excelData.items():
                unnamedColIndices = [col   for i, col in enumerate(df.columns)   if 'Unnamed' in str(col[0])]

                if len(unnamedColIndices):
                    excelData[sheetName] = df.drop(unnamedColIndices, axis=1)

            dataToConvert = excelData
        except Exception as e:
            msgText = handleErrorMsg('\nError converting existing schedule Excel file to JSON.', getTraceback(e))

        if msgText: print(msgText)


    return dataToConvert



# JSON WITH OBJECT OF DATA FRAMES
#    =>   OBJECT OF DATA FRAMES
def readDfsJSONAsObjOfDfs(JSONFilePath = ''):
    msgText=''
    objOfDfs = {}

    try:
        with open(JSONFilePath, 'r') as file:
            objOfDfsTemp = json.load(file)
            
            
        for dfName, dfData in objOfDfsTemp.items():
          dfData = json.loads(dfData)
          dfData['index'] = MultiIndex.from_tuples(dfData['index'], names=timeIndexNames)

          try:
              dfData['columns'] = MultiIndex.from_tuples(dfColWeekDayNamesTuples5el, names=dayAndAttrNames)
              objOfDfs[dfName] = DataFrame(data=dfData['data'], index=dfData['index'], columns=dfData['columns'])

          except:
              dfData['columns'] = MultiIndex.from_tuples(dfColWeekDayNamesTuples4el, names=dayAndAttrNames)
              objOfDfs[dfName] = DataFrame(data=dfData['data'], index=dfData['index'], columns=dfData['columns'])


    except Exception as e:
        msgText = handleErrorMsg('Error while reading JSON file with Data Frames as object with Data Frames.', getTraceback(e))
    
    if msgText: print(msgText)

    return objOfDfs



# EXCEL CONTENT
#    =>   OBJECT OF DATA FRAMES
#       =>   JSON
def readExcelAsDfsJSON(excelFilePath=scheduleClassesExcelPath):
    from files_utils import doesFileExist
    dataToConvert = {}
    msgText = ''

    if doesFileExist(excelFilePath):
        try:
            excelData = read_excel( io=excelFilePath, sheet_name=None, engine=excelEngineName, keep_default_na=False,
                                    header=[excelMargin['row'], excelMargin['row']+1], index_col=[excelMargin['col'], excelMargin['col']+1])

            for sheetName, df in excelData.items():
                unnamedColIndices = [col   for i, col in enumerate(df.columns)   if 'Unnamed' in str(col[0])]
                if len(unnamedColIndices):
                    df = df.drop(unnamedColIndices, axis=1)

                dataToConvert[sheetName] = df.to_json(orient='split')

        except Exception as e:
            msgText = handleErrorMsg('\nError converting existing schedule Excel file to JSON.', getTraceback(e))

        if msgText: print(msgText)


    return json.dumps(dataToConvert, indent=JSONIndentValue)