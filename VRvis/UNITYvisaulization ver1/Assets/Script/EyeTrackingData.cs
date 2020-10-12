using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;

public class EyeTrackingData : MonoBehaviour
{
    public GameObject obj;

    List<string> moveDataList = new List<string>();

    bool isSave = true, starts = false;

    void Start()
    {
        moveDataList.Clear();
    }

    void Update()
    {
        if (!starts)
        {
            starts = true;
        }

        if (starts)
        {
            if (isSave)
            {
                Debug.Log("Start Save " + obj.name + " position");
                Invoke("addPos", 0.02f); //함수 실행 시간 delay
                isSave = false;
            }
        }
    }

    void OnApplicationQuit()
    {
        string path = "./Assets/Resources/Test/" + obj.name + System.DateTime.Now.ToString("yyyy-MM-dd-HH-mm-ss") + " testPos2.txt";

        SavePosition(path, moveDataList);

        Debug.Log("Save Finish");

        UnityEditor.AssetDatabase.Refresh();
        UnityEditor.EditorApplication.isPlaying = false;
    }

    void SavePosition(string filePath, List<string> list)
    {
        FileStream file = new FileStream(filePath, FileMode.Create, FileAccess.Write);
        StreamWriter writer = new StreamWriter(file, System.Text.Encoding.Unicode);

        for (var i = 0; i < list.Count; i++)
            writer.WriteLine(list[i]);

        writer.Close();
        file.Close();
    }

    void addPos()
    {
        PlayerAddPos();

        isSave = true;
    }

    void PlayerAddPos()
    {
        string pos = "";
        pos += PositionToString(obj);
        moveDataList.Add(pos);
    }

    string PositionToString(GameObject obj)
    {
        string pos = "";
        pos += "(" + getPaddingString(obj.transform.position.x, 12) + ", " + getPaddingString(obj.transform.position.y, 12) + ", " + getPaddingString(obj.transform.position.z, 12) + ", " +
            getPaddingString(obj.transform.rotation.eulerAngles.x, 12) + ", " + getPaddingString(obj.transform.rotation.eulerAngles.y, 12) + ", " + getPaddingString(obj.transform.rotation.eulerAngles.z, 12) + ")";
        return pos;
    }

    string getPaddingString(float num, int padding)
    {
        return string.Format("{000:0.0000000} ", num).PadLeft(padding);
    }
}