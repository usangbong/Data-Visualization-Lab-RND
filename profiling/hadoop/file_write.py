from hdfs import InsecureClient

client = InsecureClient('http://localhost:50070')
client.write('upload/testdata.csv', data = 'testdata.csv', encoding = 'utf-8')