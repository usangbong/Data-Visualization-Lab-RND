using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;
using System;
using Valve.VR;

public class TrakerPos_Script :  MonoBehaviour
{
    public SteamVR_Input_Sources handType;
    public SteamVR_Action_Boolean grapGribAction;
    public GameObject TL, TR, TH, TLF, TRF, Head;
    List<string> positionDataList = new List<string>();
    
    void Start()
    {
        positionDataList.Clear();
    }

    void Update()
    {
        DecodeTransformData();
        if(grapGribAction.GetStateDown(handType))
        {
            string name = "Traker-" + DateTime.Now.ToString("yyyy-MM-dd-HH-mm-ss");
            SaveData("Assets/Data/Traker/" + name + ".cvs");
        }
    }

    void DecodeTransformData()
    {
        string transformData;

        transformData = TL.transform.position.x + "," + TL.transform.position.y + "," + TL.transform.position.z + "," +
            TL.transform.rotation.eulerAngles.x + "," + TL.transform.rotation.eulerAngles.y + "," + TL.transform.rotation.eulerAngles.z + "," +
            TR.transform.position.x + "," + TR.transform.position.y + "," + TR.transform.position.z + "," +
            TR.transform.rotation.eulerAngles.x + "," + TR.transform.rotation.eulerAngles.y + "," + TR.transform.rotation.eulerAngles.z + "," +
            TH.transform.position.x + "," + TH.transform.position.y + "," + TH.transform.position.z + "," +
            TH.transform.rotation.eulerAngles.x + "," + TH.transform.rotation.eulerAngles.y + "," + TH.transform.rotation.eulerAngles.z + "," +
            TLF.transform.position.x + "," + TLF.transform.position.y + "," + TLF.transform.position.z + "," +
            TLF.transform.rotation.eulerAngles.x + "," + TLF.transform.rotation.eulerAngles.y + "," + TLF.transform.rotation.eulerAngles.z + "," +
            TRF.transform.position.x + "," + TRF.transform.position.y + "," + TRF.transform.position.z + "," +
            TRF.transform.rotation.eulerAngles.x + "," + TRF.transform.rotation.eulerAngles.y + "," + TRF.transform.rotation.eulerAngles.z + "," +
            Head.transform.position.x + "," + Head.transform.position.y + "," + Head.transform.position.z + "," +
            Head.transform.rotation.eulerAngles.x + "," + Head.transform.rotation.eulerAngles.y + "," + Head.transform.rotation.eulerAngles.z;

        positionDataList.Add(transformData);

    }

    void SaveData(string filePath)
    {
        FileStream file = new FileStream(filePath, FileMode.Create, FileAccess.Write);
        StreamWriter writer = new StreamWriter(file, System.Text.Encoding.Unicode);

         for (int i = 0; i < positionDataList.Count; i++)
         {
             writer.WriteLine(positionDataList[i]);
         }
        writer.Close();
        file.Close();
    }

    void OnApplicationQuit()
    {
        string name = "Traker-" + DateTime.Now.ToString("yyyy-MM-dd-HH-mm-ss");
        SaveData("Assets/Data/Traker/" + name + ".cvs");
    }
}
