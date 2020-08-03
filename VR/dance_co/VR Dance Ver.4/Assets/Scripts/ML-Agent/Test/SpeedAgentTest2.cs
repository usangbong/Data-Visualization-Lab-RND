using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using MLAgents;
using System.IO;

public class SpeedAgentTest2 : Agent
{
    public Transform pivot, target;

    Vector3 lastPosition, currentPosition;

    CorWrong cw;

    float averageVelocity = 0, velocity;
    float timeStep = 0.02f, distance;
    int countVelocity = 0, select, idx;

    List<Vector3> posList = new List<Vector3>();
    List<Vector3> rotList = new List<Vector3>();

    string[] splitDataToEnter, splitDataToComma;
    char sp = '\n', sp2 = ',';

    bool reverse = false;

    void Awake()
    {
        cw = GameObject.Find("CorWrong").GetComponent<CorWrong>();

        StartCoroutine(timeChecker());

        string path = "./Assets/Resources/Test/testPos.txt";

        string data = LoadData(path);
        ConvertData(data);

        idx = 1;

        target.position = posList[0] + pivot.position;
        target.rotation = Quaternion.Euler(rotList[0]);

        lastPosition = target.position;
    }

    public override void AgentReset()
    {

    }

    public override void CollectObservations()
    {
        AddVectorObs(velocity);
        AddVectorObs(averageVelocity);
        AddVectorObs(select);
    }

    public override void AgentAction(float[] vectorAction)
    {
        select = Mathf.FloorToInt(vectorAction[0]);

        target.position = posList[idx] + pivot.position;
        target.rotation = Quaternion.Euler(rotList[idx]);

        if (!reverse) idx++;
        else idx--;

        if (idx == 0)
        {
            reverse = false;
            idx += 1;
        }

        else if (idx == posList.Count)
        {
            reverse = true;
            idx--;
        }

        currentPosition = target.position;

        distance = Vector3.Distance(lastPosition, currentPosition);
        velocity = distance / timeStep;
        averageVelocity = averageVelocity + (velocity - averageVelocity) / ++countVelocity;

        if (select == 0)
        {
            if (velocity >= averageVelocity)
            {
                AddReward(1f);
                cw.correct += 1;
            }

            else
            {
                AddReward(-1f);
                cw.wrong += 1;
            }
        }

        else if (select == 1)
        {
            if (velocity >= averageVelocity)
            {
                AddReward(-1f);
                cw.wrong += 1;
            }

            else
            {
                AddReward(1f);
                cw.correct += 1;
            }
        }

        lastPosition = currentPosition;
    }

    IEnumerator timeChecker()
    {
        while (true)
        {
            yield return new WaitForSeconds(100f);

            cw.change = true;
            Done();
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
