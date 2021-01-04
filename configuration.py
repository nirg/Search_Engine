class ConfigClass:
    def __init__(self):
        self.corpusPath = r'C:\Users\adirm\Downloads\data\benchmark_data_train.snappy.parquet'
        self.savedFileMainFolder = '\saved_data'
        self.saveFilesWithStem = self.savedFileMainFolder + "/WithStem"
        self.saveFilesWithoutStem = self.savedFileMainFolder + "/WithoutStem"
        self.toStem = False

        print('Project was created successfully..')

    def get__corpusPath(self):
        return self.corpusPath
