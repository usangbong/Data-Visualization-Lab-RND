using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;
using System.Text;

public class pieChartDataRead : MonoBehaviour
{
    [Tooltip("Text asset containing the data")]
    public TextAsset data;
    // Start is called before the first frame update
    
    List<Dictionary<string, object>> data_Dialog = CSVreader.Read(data);
    
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}



/// <summary>
/// CSV Reader
/// * Resources/CSV/[path] csv파일 저장
/// * OnLoadCSV(path) Method csv파일 로드
/// * OnLoadTextAsset(data) 로드된 csv TextAsset데이터 파싱
/// </summary>
public class CSVReader : MonoBehaviour
{
    /// <summary>
    /// Parse CSV to TextAsset
    /// </summary>
    /// <param name="path"> CSV file path </param>
    public void OnLoadCSV(string path)
    {
        string file_path = "CSV/";
        file_path = string.Concat(file_path, path);
        TextAsset ta = Resources.Load(file_path, typeof(TextAsset)) as TextAsset;

        OnLoadTextAsset(ta.text);

        Resources.UnloadAsset(ta);
        ta = null;
    }

    /// <summary>
    ///  CSV Data Load
    /// </summary>
    /// <param name="data"></param>
    public void OnLoadTextAsset(string data)
    {
        string[] str_lines = data.Split('\n');
        for (int i = 0; i < str_lines.Length - 1; ++i)
        {
            string[] d = str_lines[i].Split(',');
            for (int j = 0; j < d.Length; j++)
            {
                Debug.Log("data row: " + (i + 1) + "==> data: " + d[j]);
            }
        }
    }
}
