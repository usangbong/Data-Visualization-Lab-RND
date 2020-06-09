using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;

public class PlayerMoveTest : MonoBehaviour
{
    public GameObject VRPlayer;
    public int playerCount;

    List<List<Vector3>> posList, rotList;

    string[] splitDataToEnter, splitDataToComma;

    string path, data;

    char sp = '\n', sp2 = ',';

    void Start()
    {
        path = "./Assets/Data/Player/player" + playerCount + ".txt";

        data = LoadData(path);

        data = ManufactureData(data);

        Initialize2DList();

        getPosRot();

        GameObject parent = GameObject.Find("VR Player");
        for (var i = 0; i < 6; i++)
        {
            //Object Move
            StartCoroutine(moveObject(parent.transform.GetChild(i).gameObject, i));
        }
    }

    void Initialize2DList()
    {
        posList = new List<List<Vector3>>();
        for (var i = 0; i < 6; i++)
        {
            posList.Add(new List<Vector3>());
        }

        rotList = new List<List<Vector3>>();
        for (var i = 0; i < 6; i++)
        {
            rotList.Add(new List<Vector3>());
        }
    }

    string LoadData(string path)
    {
        FileStream file = new FileStream(path, FileMode.Open, FileAccess.Read);
        StreamReader reader = new StreamReader(file);

        string data = reader.ReadToEnd();

        reader.Close();
        file.Close();

        return data;
    }

    string ManufactureData(string Data)
    {
        string data = Data;

        data = data.Replace(" ", "").Replace("(", "").Replace(")", "").Replace("\r", "").Replace("\r\n", "");

        for(var i=0;i<VRPlayer.transform.childCount;i++)
        {
            data = data.Replace(VRPlayer.transform.GetChild(i).name, "");
        }

        return data;
    }

    void getPosRot()
    {
        Vector3 pos, rot;

        splitDataToEnter = data.Split(sp);
        
        for(var i=1;i<splitDataToEnter.Length-1;i++)
        {
            splitDataToComma = splitDataToEnter[i].Split(sp2);

            for(var j=0;j<splitDataToComma.Length;j+=6)
            {
                pos = new Vector3(System.Convert.ToSingle(splitDataToComma[j]), System.Convert.ToSingle(splitDataToComma[j + 1]), System.Convert.ToSingle(splitDataToComma[j + 2]));
                rot = new Vector3(System.Convert.ToSingle(splitDataToComma[j + 3]), System.Convert.ToSingle(splitDataToComma[j + 4]), System.Convert.ToSingle(splitDataToComma[j + 5]));
                posList[j / 6].Add(pos);
                rotList[j / 6].Add(rot);
            }
        }
    }

    IEnumerator moveObject(GameObject obj, int idx)
    {
        //init Object Position and Rotation
        obj.transform.position = posList[idx][0];
        obj.transform.rotation = Quaternion.Euler(rotList[idx][0]);

        var i = 0;

        while (true)
        {
            obj.transform.position = posList[idx][i];
            obj.transform.rotation = Quaternion.Euler(rotList[idx][i]);
           
            i++;

            if (i == posList[idx].Count)
            {
                obj.transform.position = posList[idx][0];
                obj.transform.rotation = Quaternion.Euler(rotList[idx][0]);
                i = 0;
            }

            yield return new WaitForSeconds(0.02f);
        }
    }
}
