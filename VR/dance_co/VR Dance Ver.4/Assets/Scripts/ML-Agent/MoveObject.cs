using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;
using MLAgents;

public class MoveObject : Agent
{
    public Transform target, pivot;

    List<Vector3> posList = new List<Vector3>(), rotList = new List<Vector3>();

    VelocityCollocateTest vc;
    RadiusCollocateTest rc;

    int idx;
    bool reverse = false;

    void Start()
    {
        vc = GameObject.Find("Velocity Agent").GetComponent<VelocityCollocateTest>();
        rc = GameObject.Find("Radius Agent").GetComponent<RadiusCollocateTest>();

        string path = "./Assets/Resources/Test/Collocate.txt";
        string data = LoadData(path);
        ConvertData(data);

        idx = 1;

        target.position = posList[0] + pivot.position;
        target.rotation = Quaternion.Euler(rotList[0]);

        vc.setLastPosition(target.position);
        rc.setOrigin(target);
    }

    public override void CollectObservations()
    {
        AddVectorObs(idx);
    }

    public override void AgentAction(float[] vectorAction)
    {
        target.position = posList[idx] + pivot.position;
        target.rotation = Quaternion.Euler(rotList[idx]);

        if (!reverse) idx++;
        else idx--;

        if (idx == 0)
        {
            reverse = false;
            idx++;
        }

        else if (idx == posList.Count)
        {
            reverse = true;
            idx--;
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

    void ConvertData(string data)
    {
        data = data.Replace("(", "").Replace(")", "").Replace(" ", "");

        Vector3 pos, rot;

        string[] splitDataToEnter, splitDataToComma;
        char sp = '\n', sp2 = ',';

        splitDataToEnter = data.Split(sp);
        for (var i = 0; i < splitDataToEnter.Length - 1; i++)
        {
            splitDataToComma = splitDataToEnter[i].Split(sp2);

            pos = new Vector3(System.Convert.ToSingle(splitDataToComma[0]), System.Convert.ToSingle(splitDataToComma[1]), System.Convert.ToSingle(splitDataToComma[2]));
            rot = new Vector3(System.Convert.ToSingle(splitDataToComma[3]), System.Convert.ToSingle(splitDataToComma[4]), System.Convert.ToSingle(splitDataToComma[5]));

            posList.Add(pos);
            rotList.Add(rot);
        }
    }
}
