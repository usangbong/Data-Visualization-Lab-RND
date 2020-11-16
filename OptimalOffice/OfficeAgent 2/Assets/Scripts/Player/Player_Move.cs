using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;

public class Player_Move : MonoBehaviour
{
    public Transform resetTransform;

    private int idx;
    private bool moveFinish;

    private List<string> moveObjectList;
    private List<Transform> moveList;

    public bool isMoveFinish() { return moveFinish; }
    public void resetMove() { moveFinish = false; }

    private void Awake()
    {
        idx = 0;
        moveFinish = false;

        moveObjectList = new List<string>();
        moveList = new List<Transform>();
    }

    private void Start()
    {
        string data = getFileData("./Assets/Resources/trace.txt");
        AddObjectToTraceData(data);
        resetPos();
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
        char convertCharacter = '\n';
        string[] convertData = data.Split(convertCharacter);

        for (var i = 0; i < convertData.Length; i++)
        {
            moveObjectList.Add(convertData[i].Trim());
        }

        for (var i = 0; i < moveObjectList.Count; i++)
        {
            GameObject obj = GameObject.Find(moveObjectList[i]);
            moveList.Add(obj.transform);
        }
    }

    void resetPos()
    {
        transform.position = resetTransform.position;
    }

    private void Update()
    {
        moveToObject();
    }

    void moveToObject()
    {
        transform.position = Vector3.MoveTowards(transform.position, moveList[idx].position, 10.0f * Time.deltaTime);

        if(transform.position == moveList[idx].position)
        {
            idx++;
        }

        if(idx > moveList.Count - 1)
        {
            idx = 0;
            moveFinish = true;
            resetPos();
        }
    }
}
