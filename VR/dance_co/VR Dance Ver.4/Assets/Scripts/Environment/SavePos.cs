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

    public bool isBack, isInitialize, nonSave;

    List<string> moveDataList = new List<string>();
    List<string> objMoveDataList = new List<string>();

    int fileNum;    

    bool isButton, isSave;

    void Start()
    {
        if (!nonSave)
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

            string[] objTitlelist = new string[] { "Flat", "Heart", "Ring", "VObj", "Puzzle", "Cone", "Wave" };
            int objTabCount = 21;

            title = "";
            for (var i = 0; i < 7; i++)
            {
                title += objTitlelist[i];
                if (i == 6) break;

                for (var j = 0; j < objTabCount; j++)
                    title += "\t";
            }

            objMoveDataList.Add(title);
        }
    }

    void Update()
    {
        if (!nonSave)
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
    }

    private void OnApplicationQuit()
    {
        if (!nonSave)
        {
            if (!isInitialize && !isBack)
            {
                string filePath = "./Assets/Data/Player/player";

                filePath += fileNum;
                filePath += ".txt";

                SavePosition(filePath, moveDataList);

                filePath = "./Assets/Data/Object/object";
                filePath += fileNum;
                filePath += ".txt";

                SavePosition(filePath, objMoveDataList);

                fileNum++;
                saveFileCount();

                UnityEditor.AssetDatabase.Refresh();
            }
        }
    }

    public void setButton(bool active)
    {
        isButton = active;
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

                filePath = "./Assets/Data/Object/object" + i + ".txt";
                File.Delete(filePath);
            }

            fileNum = 0;
        }

        else
        {
            string filePath = "./Assets/Data/Player/player" + (fileNum - 1) + ".txt";
            File.Delete(filePath);

            filePath = "./Assets/Data/Object/object" + (fileNum - 1) + ".txt";
            File.Delete(filePath);

            fileNum--;
        }
    }

    void addPos()
    {
        PlayerAddPos();
        ObjectAddPos();

        isSave = true;
    }

    void PlayerAddPos()
    {
        string pos = "";
        pos += PositionToString(Head) + ",\t" + PositionToString(LeftHand) + ",\t" +
            PositionToString(RightHand) + ",\t" + PositionToString(Hip) + ",\t" +
            PositionToString(LeftFoot) + ",\t" + PositionToString(RightFoot);

        moveDataList.Add(pos);
    }

    void ObjectAddPos()
    {
        string pos = "";

        GameObject parent = GameObject.Find("ObjectList").gameObject;

        for(var i=0;i<parent.transform.childCount;i++)
        {
            pos += PositionToString(parent.transform.GetChild(i).gameObject);
            if (i == parent.transform.childCount - 1) break;
            pos += "\t";
        }

        objMoveDataList.Add(pos);
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
