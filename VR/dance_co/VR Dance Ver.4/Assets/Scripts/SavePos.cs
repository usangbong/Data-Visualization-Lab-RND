using System.Collections;
using System.Collections.Generic;
using System.IO;

using UnityEngine;
using UnityEngine.UI;
using Valve.VR;

public class SavePos : MonoBehaviour
{
    const bool Last = false;
    const bool All = true;

    public GameObject Head, LeftHand, RightHand;
    public GameObject Hip, LeftFoot, RightFoot;
    public GameObject Canvas, Text;

    public bool isBack, isInitialize;

    List<string> moveDataList = new List<string>();

    int fileNum;    

    bool isButton, isSave;

    void Start()
    {
        isSave = true;
        moveDataList.Clear();
        Canvas.SetActive(false);

        string fileCntString = LoadData();
        fileCntString = fileCntString.Replace("\n", "");

        fileNum = System.Convert.ToInt32(fileCntString);

        if (isBack)
        {
            Canvas.SetActive(true);
            Text.GetComponent<Text>().text = "가장 최근의 파일을 지우겠습니까?";
        }

        if (isInitialize)
        {
            Canvas.SetActive(true);
            Text.GetComponent<Text>().text = "모든 파일을 지우고 초기화하겠습니까?";
        }

        string[] titleList = new string[] { "Head", "Left Hand", "Right Hand", "Hip", "Left Foot", "Right Foot" };
        int[] tabCount = new int[] { 21, 20, 20, 22, 20 };

        string title = "";
        for (var i = 0; i < 6; i++)
        {
            title += titleList[i];
            if (i == 5) break;

            for (var j = 0; j < tabCount[i]; j++)
                title += "\t";
        }

        moveDataList.Add(title);
    }

    void Update()
    {
        if (!isBack && !isInitialize)
        {
            if (isSave)
            {
                Invoke("addPos", 0.02f);
                isSave = false;
            }
        }

        else if (isBack && isInitialize) Text.GetComponent<Text>().text = "ERROR";

        else
        {
            if (isButton)
            {
                if (isBack)
                {
                    deleteFile(Last);
                    saveFileCount();
                }

                if (isInitialize)
                {
                    deleteFile(All);
                    saveFileCount();
                }

                UnityEditor.AssetDatabase.Refresh();
                UnityEditor.EditorApplication.isPlaying = false;
            }
        }
    }

    private void OnApplicationQuit()
    {
        if (!isInitialize && !isBack)
        {
            string filePath = "./Assets/Data/Player/player";

            filePath += fileNum;
            filePath += ".txt";

            SavePosition(filePath);

            fileNum++;
            saveFileCount();

            UnityEditor.AssetDatabase.Refresh();
        }
    }

    public void setButton(bool active)
    {
        isButton = active;
    }

    void SavePosition(string filePath)
    {
        FileStream file = new FileStream(filePath, FileMode.Create, FileAccess.Write);
        StreamWriter writer = new StreamWriter(file, System.Text.Encoding.Unicode);

        for (var i = 0; i < moveDataList.Count; i++)
            writer.WriteLine(moveDataList[i]);

        writer.Close();
        file.Close();
    }

    void saveFileCount()
    {
        FileStream file = new FileStream("./Assets/Resources/fileCnt.txt", FileMode.Create, FileAccess.Write);
        StreamWriter writer = new StreamWriter(file, System.Text.Encoding.Unicode);

        writer.WriteLine(fileNum);

        writer.Close();
        file.Close();
    }

    string LoadData()
    {
        string data;

        FileStream file = new FileStream("./Assets/Resources/fileCnt.txt", FileMode.Open, FileAccess.Read);
        StreamReader reader = new StreamReader(file);

        data = reader.ReadToEnd();

        reader.Close();
        file.Close();

        return data;
    }

    void deleteFile(bool isAll)
    {
        if (isAll)
        {
            for (int i = 0; i < fileNum; i++)
            {
                string filePath = "./Assets/Data/Player/player" + i + ".txt";
                File.Delete(filePath);
            }

            fileNum = 0;
        }

        else
        {
            string filePath = "./Assets/Data/Player/player" + (fileNum - 1) + ".txt";
            File.Delete(filePath);

            fileNum--;
        }
    }

    void addPos()
    {
        string pos = "";
        pos += PositionToString(Head) + ",\t" + PositionToString(LeftHand) + ",\t" +
            PositionToString(RightHand) + ",\t" + PositionToString(Hip) + ",\t" +
            PositionToString(LeftFoot) + ",\t" + PositionToString(RightFoot);

        moveDataList.Add(pos);

        isSave = true;
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
