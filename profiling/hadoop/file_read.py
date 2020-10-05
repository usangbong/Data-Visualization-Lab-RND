from hdfs import InsecureClient

client = InsecureClient('http://localhost:50070')
with client.read('upload/testdata.csv') as file_data:
    input_data = pd.read_csv(file_data)