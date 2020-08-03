using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;

public class ObjectMove : MonoBehaviour
{
    const int objCnt = 7;

    public bool pingpong;

    GameObject parent;

    List<List<Vector3>> posList, rotList;

    string[] splitDataToEnter, splitDataToComma;

    string basePath, path;
    char sp = '\n', sp2 = ',';

    void Start()
    {
        //Make 2D List
        Initialize2DList();
        basePath = "./Assets/Resources/";

        parent = GameObject.Find("ObjectList").gameObject;

        for(var i=0;i<objCnt;i++)
        {
            //get Path
            path = basePath + parent.transform.GetChild(i).gameObject.name + ".txt";

            getPosRot(path, i);
        }
        
        for(var i=0;i<objCnt;i++)
        {
            //Object Move
            StartCoroutine(moveObject(parent.transform.GetChild(i).gameObject, i));
        }
    }

    void Initialize2DList()
    {
        //Make 2D List for Position
        posList = new List<List<Vector3>>();
        for (var i = 0; i < objCnt; i++)
        {
            posList.Add(new List<Vector3>());
        }

        //Make 2D List for Rotation
        rotList = new List<List<Vector3>>();
        for (var i = 0; i < objCnt; i++)
        {
            rotList.Add(new List<Vector3>());
        }
    }

    void getPosRot(string path, int idx)
    {
        string Data = getData(path);

        Data = Data.Replace("(", "").Replace(")", "").Replace(" ", "");

        Vector3 pos, rot;

        //Split to \n
        splitDataToEnter = Data.Split(sp);
        for(var i=0;i<splitDataToEnter.Length-1;i++)
        {
            //Split to ,
            splitDataToComma = splitDataToEnter[i].Split(sp2);

            //get Position and Rotation
            pos = new Vector3(System.Convert.ToSingle(splitDataToComma[0]), System.Convert.ToSingle(splitDataToComma[1]), System.Convert.ToSingle(splitDataToComma[2]));
            rot = new Vector3(System.Convert.ToSingle(splitDataToComma[3]), System.Convert.ToSingle(splitDataToComma[4]), System.Convert.ToSingle(splitDataToComma[5]));

            //Add to List
            posList[idx].Add(pos);
            rotList[idx].Add(rot);
        }
    }

    string getData(string path)
    {
        FileStream file = new FileStream(path, FileMode.Open, FileAccess.Read);
        StreamReader reader = new StreamReader(file);

        string Data = reader.ReadToEnd();

        reader.Close();
        file.Close();

        return Data;
    }

    IEnumerator moveObject(GameObject obj, int idx)
    {
        //init Object Position and Rotation
        obj.transform.position = posList[idx][0];
        obj.transform.rotation = Quaternion.Euler(rotList[idx][0]);

        var i = 0;
        bool pp = false;

        while(true)
        {
            obj.transform.position = posList[idx][i];
            obj.transform.rotation = Quaternion.Euler(rotList[idx][i]);

            if (!pp)
            {
                i++;
            }

            else
            {
                i--;
            }

            if (pingpong)
            {
                if(i==0)
                {
                    i++;
                    pp = false;
                }

                else if(i == posList[idx].Count)
                {
                    i--;
                    pp = true;
                }
            }

            else
            {
                //init Object Position and Rotation
                if (i == posList[idx].Count)
                {
                    obj.transform.position = posList[idx][0];
                    obj.transform.rotation = Quaternion.Euler(rotList[idx][0]);
                    i = 0;
                }
            }

            yield return new WaitForSeconds(0.02f);
        }
    }
}
