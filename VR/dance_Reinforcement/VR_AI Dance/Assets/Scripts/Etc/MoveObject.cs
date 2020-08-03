using System.Collections;
using System.Collections.Generic;
using System.IO;
using UnityEngine;
using MLAgents;

public class MoveObject : Agent
{
    public Transform pivot;

    float averageVelocity = 0f, velocity;
    float timeStep = 0.02f, distance;
    float averageRadius = 0, radius;
    int countVelocity = 0, countRadius = 0;

    List<Vector3> posList = new List<Vector3>(), rotList = new List<Vector3>();

    Vector3 lastPosition, currentPosition;
    Vector3 originPos, originRot;

    int idx;
    bool reverse = false;

    void Awake()
    {
        string path = "./Assets/Resources/Collocate.txt";
        string data = LoadData(path);
        ConvertData(data);

        idx = 1;

        transform.position = posList[0] + pivot.position;
        transform.rotation = Quaternion.Euler(rotList[0]);

        lastPosition = transform.position;

        originPos = transform.position;
        originRot = transform.rotation.eulerAngles;
    }

    public Vector3 getOriginPos()
    {
        return originPos;
    }

    public Vector3 getPos()
    {
        return transform.position;
    }

    public float getRadius()
    {
        return radius;
    }

    public float getAverageRadius()
    {
        return averageRadius;
    }

    public float getVelocity()
    {
        return velocity;
    }

    public float getAverageVelocity()
    {
        return averageVelocity;
    }

    public float getYpos()
    {
        return transform.position.y;
    }

    public override void CollectObservations()
    {
        AddVectorObs(idx);
    }

    public override void AgentAction(float[] vectorAction)
    {
        transform.position = posList[idx] + pivot.position;
        transform.rotation = Quaternion.Euler(rotList[idx]);

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

        currentPosition = transform.position;

        distance = Vector3.Distance(lastPosition, currentPosition);
        velocity = distance / timeStep;

        velocity = Mathf.Round(velocity * 1000) * 0.001f;

        if(velocity <= 100f)
        {
            averageVelocity = averageVelocity + (velocity - averageVelocity) / ++countVelocity;

            averageVelocity = Mathf.Round(averageVelocity * 1000) * 0.001f;
        }

        radius = Vector3.Distance(originPos, transform.position);

        if(radius <= 50f)
        {
            averageRadius = averageRadius + (radius - averageRadius) / ++countRadius;
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
