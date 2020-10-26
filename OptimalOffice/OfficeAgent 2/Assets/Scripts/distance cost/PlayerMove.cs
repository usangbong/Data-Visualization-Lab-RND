using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;

public class PlayerMove : MonoBehaviour
{
    [HideInInspector]
    public bool isMoveFinish = false;
    [HideInInspector]
    public int finIdx = 0;
    int idx = 0;

    List<string> moveObjectList = new List<string>();
    List<Transform> moveList = new List<Transform>();

    private void Awake()
    {
        string data = getFileData("./Assets/Resources/trace.txt");

        AddObjectToTraceData(data);

        resetPos();
    }

    private void Update()
    {
        moveToObject();
    }

    void moveToObject()
    {
        transform.position = Vector3.MoveTowards(transform.position, moveList[idx].position, 10.0f * Time.deltaTime);

        if (transform.position == moveList[idx].position)
        {
            idx++;
        }

        if (idx > moveList.Count - 1)
        {
            idx = 0;
            isMoveFinish = true;
            resetPos();
        }
    }

    public void resetPos()
    {
        transform.position = new Vector3(9.3f, 1.6f, -7.2f);
    }

    string getFileData(string filePath)
    {
        FileStream file = new FileStream(filePath, FileMode.Open, FileAccess.Read);
        StreamReader reader = new StreamReader(file);

        string data = reader.ReadToEnd();

        reader.Close();
        file.Close();

        return data;
    }

    void AddObjectToTraceData(string data)
    {
        char convert = '\n';
        string[] convertData = data.Split(convert);

        for(int i=0;i<convertData.Length;i++)
        {
            moveObjectList.Add(convertData[i].Trim());
        }

        for (int i = 0; i < moveObjectList.Count; i++)
        {
            GameObject obj = GameObject.Find(moveObjectList[i]);
            moveList.Add(obj.transform);
        }

        Debug.Log(getDistanceToTrace());
    }

    float getDistanceToTrace()
    {
        float distanceSum = 0;

        for(int i=0;i<moveList.Count - 1; i++)
        {
            Transform obj1 = moveList[i];
            Transform obj2 = moveList[i + 1];

            float distance = Vector3.Distance(obj1.position, obj2.position);
            distanceSum += distance;
        }

        return distanceSum;
    }
}
