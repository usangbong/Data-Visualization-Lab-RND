using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;
using Valve.VR;

public class TempPosSave : MonoBehaviour
{
    public SteamVR_Input_Sources handType;
    public SteamVR_Action_Boolean grapGripAction, triggerAction;
    public GameObject obj;

    public string pathName;

    List<string> moveDataList = new List<string>();

    bool isSave = true, starts = false;

    void Start()
    {
        moveDataList.Clear();
    }
    
    void Update()
    {
        if(triggerAction.GetStateDown(handType) && !starts)
        {
            starts = true;
            Debug.Log("START");
        }

        if (starts)
        {
            if (isSave)
            {
                Invoke("addPos", 0.02f);
                isSave = false;
            }

            if (grapGripAction.GetStateDown(handType))
            {
                string path = "./Assets/Resources/Test/" + pathName + ".txt";

                SavePosition(path, moveDataList);

                UnityEditor.AssetDatabase.Refresh();
                UnityEditor.EditorApplication.isPlaying = false;
            }
        }
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
