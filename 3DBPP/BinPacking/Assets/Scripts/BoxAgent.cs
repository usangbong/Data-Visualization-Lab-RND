using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Unity.MLAgents;
using Unity.MLAgents.Sensors;

public class BoxAgent : Agent
{
    private BoxMap map;
    private Data data;
    private List<Box> boxList;
    private Box LargeBox;

    private int sumOfVolume;

    public static int OVER_THE_BOX = 0;
    public static int CANT_INSTALL_BOX = 1;
    public static int NO_SPACE = 2;
    public static int CAN_INSTALL_BOX = 3;

    public override void Initialize()
    {
        data = GameObject.Find("Manager").GetComponent<Data>();

        data.getFileData("./Assets/Resources/data.txt");
        data.ConvertData();

        map = GameObject.Find("Manager").GetComponent<BoxMap>();

        boxList = data.getBoxList();

        LargeBox = new Box(20, 20, 20, 0);

        sumOfVolume = 0;
    }

    public override void OnEpisodeBegin()
    {
        sumOfVolume = 0;

        map.Clear();
    }

    public override void CollectObservations(VectorSensor sensor)
    {
        int[,,] boxMap = map.getBoxMap();

        for (int i = 0; i < 20; i++)
            for (int j = 0; j < 20; j++)
                for (int k = 0; k < 20; k++)
                    sensor.AddObservation(boxMap[i, j, k]);

        for(int i=0;i<boxList.Count;i++)
        {
            sensor.AddObservation(boxList[i].getWidth());
            sensor.AddObservation(boxList[i].getDepth());
            sensor.AddObservation(boxList[i].getHeight());
        }

        sensor.AddObservation(sumOfVolume);
        sensor.AddObservation(LargeBox.getVolume());
        sensor.AddObservation((float)sumOfVolume / LargeBox.getVolume());
    }

    public override void OnActionReceived(float[] vectorAction)
    {
        int x = System.Convert.ToInt32(vectorAction[0]);
        int y = System.Convert.ToInt32(vectorAction[1]);
        int z = System.Convert.ToInt32(vectorAction[2]);
        int selectBox = System.Convert.ToInt32(vectorAction[3]);

        Box box = boxList[selectBox];
        
        if(map.canBoxInstall(box, x, z, y) == OVER_THE_BOX) {
            map.fillMap(box, x, z, y);
            sumOfVolume += box.getVolume();

            if ((float)sumOfVolume / LargeBox.getVolume() > 0.9)
            {
                SetReward((float)sumOfVolume / LargeBox.getVolume());
                EndEpisode();
            }
        }

        else if()
        {
            
            
        }

        else
        {
            SetReward(-1f);
            EndEpisode()
        }
    }
}
