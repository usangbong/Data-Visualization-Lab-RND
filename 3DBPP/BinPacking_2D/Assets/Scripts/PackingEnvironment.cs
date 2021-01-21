using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;

using UnityEngine.SceneManagement;
using UnityEngine.UI;
using JetBrains.Annotations;

public class PackingEnvironment : MonoBehaviour
{
    public GameObject middleBoxPrefab;
    public GameObject largeBoxPrefab;

    private MiddleBox middleBox;
    private LargeBox largeBox;
    private BoxMap map;

    //private string data;

    //int episodeCnt = 0;

    private void Awake()
    {
        //agent = GameObject.Find("Agent").GetComponent<BoxAgent>();

        middleBox = new MiddleBox(2, 2, middleBoxPrefab);
        largeBox = new LargeBox(20, 20, largeBoxPrefab);
    }

    private void Start()
    {
        //map = new BoxMap();
    }

    public MiddleBox getMiddleBox() { return middleBox; }
    public LargeBox getLargeBox() { return largeBox; }
    public BoxMap getBoxMap() { return map; }

    public void endEpisode(LargeBox largeBox)
    {
        //dataList.Add(data);

        map.Clear();
    }

    /*private void OnApplicationQuit()
    {
        string fileName = "./Assets/Data/";

        string data = System.DateTime.Now.ToString("yyyy_MM_DD_HH_mm_ss");

        fileName += data + "data.txt";

        FileStream file = new FileStream(fileName, FileMode.Create, FileAccess.Write);
        StreamWriter writer = new StreamWriter(file, System.Text.Encoding.Unicode);

        for (int i = 0; i < dataList.Count; i++)
            writer.WriteLine(dataList[i]);

        writer.Close();
        file.Close();
    }*/
}