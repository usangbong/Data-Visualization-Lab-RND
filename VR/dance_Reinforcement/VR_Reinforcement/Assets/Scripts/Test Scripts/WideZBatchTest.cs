using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Unity.MLAgents;
using Unity.MLAgents.Sensors;

public class WideZBatchTest : Agent
{ 
    public Transform target, obj, heightBatch;
    public Transform InitialTransform;

    public float speed = 0.1f;

    HeightSpeedBatchTest hTest;

    public override void Initialize()
    {
        hTest = heightBatch.GetComponent<HeightSpeedBatchTest>();
    }

    public override void CollectObservations(VectorSensor sensor)
    {
        sensor.AddObservation(target.position.z);
        sensor.AddObservation(obj.position.z);
    }

    public override void OnActionReceived(float[] vectorAction)
    {
        int zWide = Mathf.FloorToInt(vectorAction[0]);
        int moveForward = Mathf.FloorToInt(vectorAction[1]);

        if (moveForward == 1) obj.Translate(Vector3.forward * speed * Time.deltaTime);
        else obj.Translate(Vector3.back * speed * Time.deltaTime);

        if (obj.position.z > 1.2f || obj.position.z < -1.2f)
        {
            AddReward(-1f);
            hTest.EndEpisode();
        }

        else
        {
            CheckUpDown(zWide);
        }
    }

    void CheckUpDown(int isWideZ)
    {
        if (target.position.z >= 0.5f || target.position.z <= -0.5f)
        {
            if (obj.position.z >= 0.5f || obj.position.z <= -0.5f)
            {
                if (isWideZ == 1) AddReward(0.005f);
                else AddReward(-0.005f);
            }

            else if (obj.position.z > -0.5f && obj.position.z < 0.5f)
            {
                AddReward(-0.005f);
            }
        }

        else if (target.position.z > -0.5f && target.position.z < 0.5f)
        {
            if (obj.position.z > -0.5f && obj.position.z < 0.5f)
            {
                if (isWideZ == 1) AddReward(-0.005f);
                else AddReward(0.005f);
            }

            else if (obj.position.z >= 0.5f || obj.position.z <= -0.5f)
            {
                AddReward(-0.005f);
            }
        }
    }
}
