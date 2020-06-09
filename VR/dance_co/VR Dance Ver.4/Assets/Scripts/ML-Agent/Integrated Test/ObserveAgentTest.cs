using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using MLAgents;
using System.IO;

public class ObserveAgentTest : Agent
{
    public Transform pivot, target;

    IntegratedCorWrong cw;

    Vector3 originPos, originRot;
    Vector3 lastPosition, currentPosition;

    List<Vector3> posList = new List<Vector3>(), rotList = new List<Vector3>();

    float averageRadius = 0, averageVelocity = 0;
    float radius, velocity;
    float distance, timeStep = 0.02f;

    int idx;
    int hSel, vSel, rSel;
    int countRadius = 0, countVelocity = 0;

    bool reverse = false;

    void Awake()
    {
        cw = GameObject.Find("CorWrong").GetComponent<IntegratedCorWrong>();

        StartCoroutine(timeChecker());

        string path = "./Assets/Resources/Test/integratedPos.txt";
        string data = LoadData(path);
        ConvertData(data);

        idx = 1;

        target.position = posList[0] + pivot.position;
        target.rotation = Quaternion.Euler(rotList[0]);

        originPos = target.position;
        originRot = target.rotation.eulerAngles;

        lastPosition = target.position;
    }

    public override void AgentReset()
    {
        
    }

    public override void CollectObservations()
    {
        AddVectorObs(hSel);
        AddVectorObs(vSel);
        AddVectorObs(rSel);
        AddVectorObs(target.position.y);
        AddVectorObs(velocity);
        AddVectorObs(radius);
        AddVectorObs(averageVelocity);
        AddVectorObs(originPos);
        AddVectorObs(target.position);
        AddVectorObs(averageRadius);

        //14 Observe
    }

    public override void AgentAction(float[] vectorAction)
    {
        hSel = Mathf.FloorToInt(vectorAction[0]);
        vSel = Mathf.FloorToInt(vectorAction[1]);
        rSel = Mathf.FloorToInt(vectorAction[2]);

        target.position = posList[idx] + pivot.position;
        target.rotation = Quaternion.Euler(rotList[idx]);

        if (!reverse) idx++;
        else idx--;

        if(idx == 0)
        {
            reverse = false;
            idx++;
        }

        else if(idx == posList.Count)
        {
            reverse = true;
            idx--;
        }

        currentPosition = target.position;

        distance = Vector3.Distance(lastPosition, currentPosition);
        radius = Vector3.Distance(originPos, target.position);

        velocity = distance / timeStep;

        averageVelocity = averageVelocity + (velocity - averageVelocity) / ++countVelocity;
        averageRadius = averageRadius + (radius - averageRadius) / ++countRadius;

        if(hSel == 0)
        {
            if (target.position.y >= 1.65f)
            {
                cw.hCorrect++;
                AddReward(1f);
            }

            else
            {
                cw.hWrong++;
                AddReward(-1f);
            }
        }

        else if(hSel == 1)
        {
            if(target.position.y >= 1.65f)
            {
                cw.hWrong++;
                AddReward(-1f);
            }

            else
            {
                cw.hCorrect++;
                AddReward(1f);
            }
        }

        if(vSel == 0)
        {
            if(velocity >= averageVelocity)
            {
                cw.vCorrect++;
                AddReward(1f);
            }

            else
            {
                cw.vWrong++;
                AddReward(-1f);
            }
        }

        else if(vSel == 1)
        {
            if(velocity >= averageVelocity)
            {
                cw.vWrong++;
                AddReward(-1f);
            }

            else
            {
                cw.vCorrect++;
                AddReward(1f);
            }
        }

        if(rSel == 0)
        {
            if(radius >= averageRadius)
            {
                cw.rCorrect++;
                AddReward(1f);
            }

            else
            {
                cw.rWrong++;
                AddReward(-1f);
            }
        }

        else if(rSel == 1)
        {
            if(radius >= averageRadius)
            {
                cw.rWrong++;
                AddReward(-1f);
            }

            else
            {
                cw.rCorrect++;
                AddReward(1f);
            }
        }

        lastPosition = currentPosition;
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
        for(var i=0;i<splitDataToEnter.Length - 1;i++)
        {
            splitDataToComma = splitDataToEnter[i].Split(sp2);

            pos = new Vector3(System.Convert.ToSingle(splitDataToComma[0]), System.Convert.ToSingle(splitDataToComma[1]), System.Convert.ToSingle(splitDataToComma[2]));
            rot = new Vector3(System.Convert.ToSingle(splitDataToComma[3]), System.Convert.ToSingle(splitDataToComma[4]), System.Convert.ToSingle(splitDataToComma[5]));

            posList.Add(pos);
            rotList.Add(rot);
        }
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
}
