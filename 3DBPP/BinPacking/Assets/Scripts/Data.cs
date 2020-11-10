using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;

public class Data : MonoBehaviour
{
    private string data;
    private List<Box> boxList;

    public string getData() { return data; }
    public List<Box> getBoxList() { return boxList; }

    public void setData(string _data) { data = _data; }
    public void setBoxList(List<Box> _boxList) { boxList = _boxList; }

    public void getFileData(string filePath)
    {
        FileStream file = new FileStream(filePath, FileMode.Open, FileAccess.Read);
        StreamReader reader = new StreamReader(file);

        data = reader.ReadToEnd();

        reader.Close();
        file.Close();
    }

    public void ConvertData()
    {
        char split = '\n';
        boxList = new List<Box>();

        string[] splitEnterData = data.Split(split);

        split = ',';
        for(int i=0;i<splitEnterData.Length;i++)
        {
            string[] splitCommaData = splitEnterData[i].Split(split);

            int width = System.Convert.ToInt32(splitCommaData[0]);
            int depth = System.Convert.ToInt32(splitCommaData[0]);
            int height = System.Convert.ToInt32(splitCommaData[0]);
            float weight = System.Convert.ToSingle(splitCommaData[3]);

            Box box = new Box(width, depth, height, weight);

            boxList.Add(box);
        }
    }
}
