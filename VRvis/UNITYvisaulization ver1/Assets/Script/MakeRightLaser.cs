using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;
using ViveSR.anipal.Eye;

public class MakeRightLaser : MonoBehaviour
{
    public GameObject laserPrefab, EyeRayObj;

    SRanipal_GazeRaySample_v2 rayTest;
    public Transform rightEye;
    Vector3 start, last;
    GameObject laser;

    List<string> moveDataList = new List<string>();

    bool isSave = true, starts = false, firstLine = true;

    void Start()
    {
        firstLine = true;
        rayTest = EyeRayObj.GetComponent<SRanipal_GazeRaySample_v2>();
        laser = Instantiate(laserPrefab);
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
                UpdateLaser();
                Invoke("addPos", 0.02f); //함수 실행 시간 delay
                isSave = false;
            }
        }
    }

    void UpdateLaser()
    {
        start = rightEye.transform.position;
        last = rayTest.Rlast;

        laser.transform.position = Vector3.Lerp(start, last, 0.5f);
        laser.transform.LookAt(last);
        laser.transform.localScale = new Vector3(laser.transform.localScale.x,
            laser.transform.localScale.y, Vector3.Distance(start, last));
    }

    void OnApplicationQuit()
    {
        string path = "./Assets/Resources/Test/" + "laserRightEye" + System.DateTime.Now.ToString("yyyy-MM-dd-HH-mm-ss") + " testPos.txt";

        SavePosition(path, moveDataList);

        Debug.Log("Save Right Finish");

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
        if (firstLine == true)
        {
            pos += "sX" + "," + "sY" + "," + "sZ" + "," + "Type" + "," + "lX" + "," + "lY" + "," + "lZ" + "," + "Type" + "\n";
            firstLine = false;
        }
        pos += PositionToString(start, last);
        moveDataList.Add(pos);
    }

    string PositionToString(Vector3 start, Vector3 last)
    {
        string pos = "";
        pos += getPaddingString(start.x, 12) + "," + getPaddingString(start.y, 12) + "," + getPaddingString(start.z, 12) + "," + "Start" + ",";
        pos += getPaddingString(last.x, 12) + "," + getPaddingString(last.y, 12) + "," + getPaddingString(last.z, 12) + "," + "Last";
        return pos;
    }

    string getPaddingString(float num, int padding)
    {
        return string.Format("{000:0.0000000} ", num).PadLeft(padding);
    }
}

