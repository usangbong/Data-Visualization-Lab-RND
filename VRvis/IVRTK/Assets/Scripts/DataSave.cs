using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;
using EmotivUnityPlugin;
using Zenject;
using UnityEngine.SceneManagement;
using dirox.emotiv.controller;
using System;

public class DataSave : MonoBehaviour
{
    private string SceneName;
    private char keyCode;

    private bool headerInput;
    private List<string> dataList = new List<string>();

    float _timerDataUpdate = 0;
    const float TIME_UPDATE_DATA = 1f;

    string headConvertData;
    string dataConvertData;

    bool dataIn;

    private void Awake()
    {
        headerInput = false;

        keyCode = '3';

        DontDestroyOnLoad(this.gameObject);
    }

    private void Update()
    {
        SceneName = SceneManager.GetActiveScene().name;

        if(Input.GetKeyDown(KeyCode.Alpha0))
        {
            keyCode = '0';
        }

        else if(Input.GetKeyDown(KeyCode.Alpha1))
        {
            keyCode = '1';
        }

        else if (Input.GetKeyDown(KeyCode.Alpha2))
        {
            keyCode = '2';
        }

        else if (Input.GetKeyDown(KeyCode.Alpha3))
        {
            keyCode = '3';
        }

        if (Input.GetKeyDown(KeyCode.RightArrow) || Input.GetKeyDown(KeyCode.LeftArrow))
        {
            keyCode = '3';
        }

        dataIn = false;
        headConvertData = dataConvertData = "";

        _timerDataUpdate += Time.deltaTime;
        if (_timerDataUpdate < TIME_UPDATE_DATA)
            return;

        _timerDataUpdate -= TIME_UPDATE_DATA;
        

        if (DataStreamManager.Instance.GetNumberEEGSamples() > 0)
        {
            string eegHeaderStr = "";
            string eegDataStr = "";
            foreach (var ele in DataStreamManager.Instance.GetEEGChannels())
            {
                string chanStr = ChannelStringList.ChannelToString(ele);
                double[] data = DataStreamManager.Instance.GetEEGData(ele);
                eegHeaderStr += chanStr + ", ";
                if (data != null && data.Length > 0)
                    eegDataStr += data[0].ToString() + ", ";
                else
                    eegDataStr += "null, "; // for null value
            }

            dataIn = true;
            Debug.Log(eegHeaderStr);

            if (!headerInput)
            {
                headConvertData += eegHeaderStr + ",";
            }

            else
            {
                dataConvertData += eegDataStr + ",";
            }            
        }

        if (DataStreamManager.Instance.GetNumberMotionSamples() > 0)
        {
            string motHeaderStr = "Motion Header: ";
            string motDataStr = "Motion Data: ";
            foreach (var ele in DataStreamManager.Instance.GetMotionChannels())
            {
                string chanStr = ChannelStringList.ChannelToString(ele);
                double[] data = DataStreamManager.Instance.GetMotionData(ele);
                motHeaderStr += chanStr + ", ";
                if (data != null && data.Length > 0)
                    motDataStr += data[0].ToString() + ", ";
                else
                    motDataStr += "null, "; // for null value
            }

            dataIn = true;

            if (!headerInput)
            {
                headConvertData += motHeaderStr + ",";
            }

            else
            {
                dataConvertData += motDataStr + ",";
            }
        }

        if (DataStreamManager.Instance.GetNumberPMSamples() > 0)
        {
            string pmHeaderStr = "Performance metrics Header: ";
            string pmDataStr = "Performance metrics Data: ";
            bool hasPMUpdate = true;
            foreach (var ele in DataStreamManager.Instance.GetPMLists())
            {
                string chanStr = ele;
                double data = DataStreamManager.Instance.GetPMData(ele);
                if (chanStr == "TIMESTAMP" && (data == -1))
                {
                    // has no new update of performance metric data
                    hasPMUpdate = false;
                    break;
                }
                pmHeaderStr += chanStr + ", ";
                pmDataStr += data.ToString() + ", ";
            }
            dataIn = true;

            if (hasPMUpdate)
            {
                if (!headerInput)
                {
                    headConvertData += pmHeaderStr + ",";
                }

                else
                {
                    dataConvertData += pmDataStr + ",";
                }
            }
        }

        if (dataIn)
        {
            if (!headerInput)
            {
                headConvertData += keyCode + "," + SceneName;
                Debug.Log("Head: " + headConvertData);
                dataList.Add(headConvertData);
                headerInput = true;
            }

            else
            {
                dataConvertData += keyCode + "," + SceneName;
                Debug.Log("Data: " + dataConvertData);
                dataList.Add(dataConvertData);
            }
        }
    }

    private void OnApplicationQuit()
    {
        string filePath = "E:/eegData/";
        string date = DateTime.Now.ToString("yyyy_MM_dd_HH_mm_ss");

        filePath += date + ".csv";

        FileStream file = new FileStream(filePath, FileMode.Create, FileAccess.Write);
        StreamWriter writer = new StreamWriter(file, System.Text.Encoding.Unicode);

        for (int i = 0; i < dataList.Count; i++)
            writer.WriteLine(dataList[i]);

        writer.Close();
        file.Close();
    }
}
