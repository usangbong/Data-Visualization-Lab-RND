using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;
using Unity.MLAgents;
using Unity.MLAgents.Sensors;

public class TableAgent : Agent
{
    public Transform obj;
    public GameObject Cell;
    public Transform window;

    private float[] xList;
    private float[] zList;

    int[] cntList = new int[24];

    float time;

    string result = "";

    public override void Initialize()
    {
        xList = new float[] { 10, 6, 2, -2, -6, -10 };
        zList = new float[] { -5.65f, -1.9f, 1.85f, 5.6f };

        time = 0f;

        initCntList();
    }

    void initCntList()
    {
        for (int i = 0; i < 24; i++)
            cntList[i] = 0;
    }

    public override void OnEpisodeBegin()
    {
        int selectXpos = Random.Range(0, 6);
        int selectZpos = Random.Range(0, 4);
        initCntList();

        obj.position = new Vector3(xList[selectXpos], 0, zList[selectZpos]);
    }

    public override void CollectObservations(VectorSensor sensor)
    {
        sensor.AddObservation(window.position);

        sensor.AddObservation(obj.position);
        sensor.AddObservation(Vector3.Distance(obj.position, window.position));
    }

    public override void CollectDiscreteActionMasks(DiscreteActionMasker actionMasker)
    {
        if (obj.position.x >= 10)
        {
            actionMasker.SetMask(0, new int[1] { 1 });
        }

        else if (obj.position.x <= -10)
        {
            actionMasker.SetMask(0, new int[1] { 2 });
        }

        if(obj.position.z >= 5.6f)
        {
            actionMasker.SetMask(0, new int[1] { 3 });
        }

        else if(obj.position.z <= -5.6f)
        {
            actionMasker.SetMask(0, new int[1] { 4 });
        }
    }

    int cnt = 0;
    public override void OnActionReceived(float[] vectorAction)
    {
        int action = System.Convert.ToInt32(vectorAction[0]);

        switch(action)
        {
            case 0:
                break;
            case 1:
                obj.position = new Vector3(obj.position.x + 4, 0, obj.position.z);
                break;
            case 2:
                obj.position = new Vector3(obj.position.x - 4, 0, obj.position.z);
                break;
            case 3:
                obj.position = new Vector3(obj.position.x, 0, obj.position.z + 3.75f);
                break;
            case 4:
                obj.position = new Vector3(obj.position.x, 0, obj.position.z - 3.75f);
                break;
            default:
                break;
        }

        cnt += 1;
        
        for(int i=0;i<24;i++)
        {
            if(Cell.transform.GetChild(i).transform.position == obj.position)
            {
                cntList[i]++;
                break;
            }
        }

        SetReward(-Vector3.Distance(obj.position, window.position));

        if(cnt > 1000)
        {
            string res = "";
            int ccnt = 0;

            float sum = cntList[11];
            Debug.Log("Table: " + sum / 1000 * 100 + "%");

            for(int i=0;i<24;i++)
            {
                res += (i + 1) + ": " + cntList[i] + ", ";
                ccnt += cntList[i];
            }

            res += "total: " + ccnt;
            result += res + "\n";

            EndEpisode();
            cnt = 0;
        }

        time = 0f;
    }

    private void FixedUpdate()
    {
        time += Time.fixedDeltaTime;
        if(time >= 0.01f)
        {
            time = 0f;
            RequestDecision();
        }
    }

    private void OnApplicationQuit()
    {
        FileStream file = new FileStream("Assets/window.txt", FileMode.Create, FileAccess.Write);
        StreamWriter writer = new StreamWriter(file, System.Text.Encoding.Unicode);
        writer.WriteLine(result);
        writer.Close();
        file.Close();
    }
}
