using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using Unity.MLAgents;
using Unity.MLAgents.Sensors;
using Unity.MLAgents.Policies;

public class BoxAgent : Agent
{
    public GameObject middleBoxPrefab;
    public GameObject largeBoxPrefab;
    public GameObject mapObj;

    private List<MiddleBox> boxList;

    private MiddleBox middleBox;
    private LargeBox largeBox;
    private BoxMap map;

    private float time;
    private int x, z;

    int episodeCnt = 0;

    public const int CAN_INSTALL = 0;
    public const int OVER_THE_BOX = 1;
    public const int NO_SPACE = 2;
    public const int CANT_INSTALL_BOX = 3;

    int boxCnt;

    public override void Initialize()
    {
        boxList = new List<MiddleBox>();

        for(int i=0;i<100;i++)
        {
            middleBox = new MiddleBox(2, 2, middleBoxPrefab);
            boxList.Add(middleBox);
        }

        largeBox = new LargeBox(20, 20, largeBoxPrefab);

        largeBox.MakeLargebox();

        map = new BoxMap(mapObj, Color.white, Color.red);

        time = 0f;
    }

    public override void OnEpisodeBegin()
    {
        boxCnt = 0;

        map.Clear();
        largeBox.Clear();
    }

    public override void CollectObservations(VectorSensor sensor)
    {
        for (int i = 0; i < 20; i++)
            for (int j = 0; j < 20; j++)
                sensor.AddObservation(map.getBoxMap()[i, j]);        

        sensor.AddObservation(middleBox.getLength());
        sensor.AddObservation(middleBox.getWidth());

        sensor.AddObservation(largeBox.getLength());
        sensor.AddObservation(largeBox.getWidth());

        sensor.AddObservation(largeBox.getBoxCount());

        sensor.AddObservation(middleBox.getArea());
        sensor.AddObservation(largeBox.getArea());
        sensor.AddObservation(largeBox.getFillingRate());
    }

    public override void OnActionReceived(float[] vectorAction)
    {
        x = intToFloat(vectorAction[0]);
        z = intToFloat(vectorAction[1]);

        middleBox = boxList[boxCnt];

        int state = map.canBoxInstall(middleBox, x, z);

        switch (state)
        {
            case CAN_INSTALL:
                installBox(middleBox, x, z);
                break;
            case OVER_THE_BOX:
                Retry();
                break;
            case NO_SPACE:
                endThisEpisode();
                break;
            case CANT_INSTALL_BOX:
                Retry();
                break;
            default:
                break;
        }
    }

    private int intToFloat(float n)
    {
        return System.Convert.ToInt32(n);
    }

    private void installBox(MiddleBox box, int x, int z)
    {
        map.fillMap(box, x, z);
        box.setObjectPoint(new Vector3(x, 0, z));
        box.makeMiddleBoxObject();

        largeBox.addBox(box);

        boxCnt++;

        AddReward(0.01f);
    }

    private void Retry()
    {
        AddReward(-0.005f);
    }

    private void endThisEpisode()
    {
        AddReward(largeBox.getBoxCount() * largeBox.getFillingRate());

        Debug.Log("Episode " + episodeCnt + "\nCnt: " + largeBox.getBoxCount() + " Rate: " + largeBox.getFillingRate());

        episodeCnt++;
        EndEpisode();
    }

    bool stop = false;
    private void FixedUpdate()
    {
        time += Time.fixedDeltaTime;

        if(Input.GetKeyDown(KeyCode.Space))
        {
            stop = !stop;
        }

        if (stop) return;

        if (time > 0.01f)
        {
            RequestDecision();
            time = 0;
        }
    }
}
